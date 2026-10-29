from pathlib import Path
import os
import re
import math
from playwright.sync_api import sync_playwright

os.chdir(Path(__file__).resolve().parents[1])
base='http://127.0.0.1:4173/design-review/'
names=['incline','sisyphus','cairn']
errors=[]
def settle(page):
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
def position(page,fraction):
    page.evaluate('(p) => scrollTo(0, (document.documentElement.scrollHeight-innerHeight)*p)',fraction)
    settle(page)
def normalize(text): return ' '.join(text.split())
def cue_point(page,selector):
    value=page.locator(selector).get_attribute('transform')
    return [float(n) for n in re.findall(r'-?\d+(?:\.\d+)?',value)[:2]]

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto(base+'pair-pass/index.html',wait_until='domcontentloaded')
    intro=normalize(page.locator('.intro>div:first-child').inner_text())
    writing=normalize(page.locator('.columns>section').inner_text())
    side=page.locator('.side>section').all_inner_texts()
    for name in names:
        page.goto(base+f'quiet-{name}/index.html',wait_until='domcontentloaded')
        page.evaluate('document.fonts.ready');settle(page)
        assert normalize(page.locator('.intro>div:first-child').inner_text())==intro
        assert normalize(page.locator('.columns>section').inner_text())==writing
        assert page.locator('.side>section').all_inner_texts()==side
        assert page.locator('.portrait-photo').count()==1
        image=page.locator('.portrait-photo')
        assert image.get_attribute('src')=='../../img/kakto.jpg'
        assert image.evaluate('(e) => e.complete && e.naturalWidth > 0')
        assert page.locator('.agent-panel,.mobile-agent-link,input[type=range],.scene-control').count()==0
        assert page.locator('.nav').get_by_role('link',name='Agent version',exact=True).count()==1
        assert not re.search(r'cyclist|wheel|bicycle',page.locator('.paired-scene svg').inner_html(),re.I)
        position(page,0)
        start_main=page.locator('.paired-scene svg').inner_html()
        start_header=page.locator('.paired-header').inner_html()
        if name!='cairn': start=cue_point(page,'.paired-scene [data-quiet-cue]')
        page.screenshot(path=f'design-review/assets/quiet-{name}-desktop.png',full_page=True)
        page.evaluate('scrollTo(0,65)');settle(page)
        assert page.locator('.paired-scene svg').inner_html()!=start_main
        position(page,1)
        page.wait_for_function("getComputedStyle(document.querySelector('.paired-header')).opacity === '1'")
        assert page.locator('.paired-header').inner_html()!=start_header
        if name!='cairn':
            end=cue_point(page,'.paired-scene [data-quiet-cue]')
            assert math.dist(start,end)<=16.01
        page.locator('.paired-header').screenshot(path=f'design-review/assets/quiet-{name}-header.png')
        idle=page.locator('.paired-header').inner_html()
        page.wait_for_timeout(120)
        assert page.locator('.paired-header').inner_html()==idle
        position(page,0)
        assert page.locator('.paired-scene svg').inner_html()==start_main
        assert page.locator('.paired-header').inner_html()==start_header
        for width in [320,390,768]:
            page.set_viewport_size({'width':width,'height':844});position(page,.6)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),(name,width)
            mini=page.locator('.paired-header').bounding_box();nav=page.locator('.nav').bounding_box()
            assert mini['y']+mini['height']<=nav['y'],(name,width,'navigation overlap')
        page.set_viewport_size({'width':390,'height':844});position(page,0)
        page.screenshot(path=f'design-review/assets/quiet-{name}-mobile.png',full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        page.goto(base+f'quiet-{name}/road-to-seed-round.html',wait_until='domcontentloaded')
        assert 'Every new feature was its own mini mvp' in page.locator('.prose').inner_text()
        reduced=browser.new_page(reduced_motion='reduce')
        reduced.goto(base+f'quiet-{name}/index.html',wait_until='domcontentloaded');reduced.evaluate('document.fonts.ready');settle(reduced)
        initial=reduced.locator('.paired-scene svg').inner_html();position(reduced,1)
        assert reduced.locator('.paired-scene svg').inner_html()==initial
        assert reduced.locator('.paired-header:visible').count()==0
        reduced.close()
    nojs=browser.new_page(java_script_enabled=False)
    nojs.goto(base+'quiet-cairn/index.html',wait_until='domcontentloaded')
    assert nojs.locator('.portrait-photo').is_visible()
    assert nojs.locator('.post').count()==8
    page.goto(base+'quiet.html',wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
    page.screenshot(path='design-review/assets/quiet-comparison.png',full_page=True)
    page.locator('details').first.locator('summary').click()
    frame=page.frame_locator('iframe').first
    frame.locator('[data-quiet]').wait_for()
    frame.locator('body').evaluate('() => scrollTo(0, document.documentElement.scrollHeight)')
    frame.locator('body').evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
    assert float(frame.locator('body').get_attribute('data-quiet-header-progress'))>.9
    browser.close()
assert not errors,errors
print('PASS: three quiet variants; original portrait loaded, core copy preserved, no cycling SVG, bounded motion, reversal/idle, phone header spacing, article content, reduced motion, no-JS, live preview, screenshots.')
