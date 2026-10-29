from pathlib import Path
import os
from playwright.sync_api import sync_playwright

os.chdir(Path(__file__).resolve().parents[1])
base = 'http://127.0.0.1:4173/design-review/'
names = ['ridge','pass','night','contour','traverse','window']
errors = []
def settle(page):
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
def position(page, fraction):
    page.evaluate('(p) => scrollTo(0, (document.documentElement.scrollHeight - innerHeight) * p)', fraction)
    settle(page)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda error: errors.append(str(error)))
    page.goto(base + 'summit/index.html',wait_until='domcontentloaded')
    intro = page.locator('.intro > div:first-child').inner_text()
    writing = page.locator('.columns > section').inner_text()
    side = page.locator('.side > section:not(.agent-panel)').all_inner_texts()
    for name in names:
        page.goto(base+f'pair-{name}/index.html',wait_until='domcontentloaded')
        page.evaluate('document.fonts.ready')
        settle(page)
        assert page.locator('.intro > div:first-child').inner_text() == intro
        assert page.locator('.columns > section').inner_text() == writing
        assert page.locator('.side > section').all_inner_texts() == side
        assert page.locator('.agent-panel, .mobile-agent-link').count() == 0
        tab = page.locator('.nav').get_by_role('link',name='Agent version',exact=True)
        assert tab.count() == 1
        assert tab.evaluate('(e) => getComputedStyle(e).borderBottomWidth') == '0px'
        assert page.locator('.scene-control, input[type=range]').count() == 0
        position(page,0)
        main_start = page.locator('.paired-scene').inner_html()
        header_start = page.locator('.paired-header').inner_html()
        assert main_start != header_start
        page.locator('.paired-scene').screenshot(path=f'design-review/assets/pair-{name}-main.png')
        page.screenshot(path=f'design-review/assets/pair-{name}-desktop.png')
        page.evaluate('scrollTo(0,65)')
        settle(page)
        assert page.locator('.paired-scene').inner_html() != main_start, (name,'main not animated')
        position(page,.55)
        page.wait_for_function("getComputedStyle(document.querySelector('.paired-header')).opacity === '1'")
        header_middle = page.locator('.paired-header').inner_html()
        assert header_middle != header_start, (name,'header not animated')
        page.locator('.paired-header').screenshot(path=f'design-review/assets/pair-{name}-header.png')
        page.screenshot(path=f'design-review/assets/pair-{name}-reading-state.png')
        position(page,.85)
        assert page.locator('.paired-header').inner_html() != header_middle
        idle = page.locator('.paired-header').inner_html()
        page.wait_for_timeout(120)
        assert page.locator('.paired-header').inner_html() == idle
        position(page,0)
        assert page.locator('.paired-scene').inner_html() == main_start
        assert page.locator('.paired-header').inner_html() == header_start
        page.keyboard.press('PageDown')
        page.wait_for_function('scrollY > 0')
        settle(page)
        assert float(page.locator('body').get_attribute('data-main-progress')) > 0
        for width in [320,390,768]:
            page.set_viewport_size({'width':width,'height':844})
            position(page,.6)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (name,width)
            mini = page.locator('.paired-header').bounding_box()
            nav = page.locator('.nav').bounding_box()
            assert mini['y']+mini['height'] <= nav['y'], (name,width,'header overlaps navigation')
        page.set_viewport_size({'width':390,'height':844})
        position(page,0)
        page.screenshot(path=f'design-review/assets/pair-{name}-mobile.png',full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        page.goto(base+f'pair-{name}/road-to-seed-round.html',wait_until='domcontentloaded')
        assert 'Every new feature was its own mini mvp' in page.locator('.prose').inner_text()
        assert page.locator('.nav').get_by_role('link',name='Agent version',exact=True).count()==1
        reduced=browser.new_page(reduced_motion='reduce')
        reduced.goto(base+f'pair-{name}/index.html',wait_until='domcontentloaded')
        reduced.evaluate('document.fonts.ready');settle(reduced)
        initial=reduced.locator('.paired-scene').inner_html()
        position(reduced,1)
        assert reduced.locator('.paired-scene').inner_html()==initial
        assert reduced.locator('.paired-header:visible').count()==0
        reduced.close()
    nojs=browser.new_page(java_script_enabled=False)
    nojs.goto(base+'pair-ridge/index.html',wait_until='domcontentloaded')
    assert nojs.locator('.post').count()==8
    assert nojs.locator('.paired-scene svg').is_visible()
    assert nojs.locator('.nav').get_by_role('link',name='Agent version',exact=True).is_visible()
    page.goto(base+'pairings.html',wait_until='domcontentloaded')
    page.evaluate('document.fonts.ready')
    page.screenshot(path='design-review/assets/pairings-comparison.png',full_page=True)
    page.locator('details').first.locator('summary').click()
    frame = page.frame_locator('iframe').first
    frame.locator('[data-pair]').wait_for()
    frame.locator('body').evaluate('() => scrollTo(0, document.documentElement.scrollHeight)')
    frame.locator('body').evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
    assert float(frame.locator('body').get_attribute('data-header-progress'))>.9
    browser.close()
assert not errors, errors
print('PASS: six distinct pairings; unchanged core content; quiet agent tab; local/global scroll, reversal, idle, keyboard, mobile header spacing, static article views, reduced motion, no-JS, live preview, screenshots.')
