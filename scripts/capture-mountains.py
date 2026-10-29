from pathlib import Path
import os
from playwright.sync_api import sync_playwright

os.chdir(Path(__file__).resolve().parents[1])
base='http://127.0.0.1:4173/design-review/'
names=['ridge','contour','horizon']
errors=[]
def settle(page):
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
def scroll(page,y):
    page.evaluate('(y)=>scrollTo(0,y)',y);settle(page)
def visible_motion(page):
    start=float(page.locator('body').get_attribute('data-mountain-start'))
    length=float(page.locator('body').get_attribute('data-mountain-range'))
    assert 48<=length<=96
    states=[]
    for p in [.2,.8]:
        scroll(page,start+length*p)
        box=page.locator('.paired-scene').bounding_box()
        masthead=page.locator('.site-head').bounding_box()
        assert box['y']>=masthead['y']+masthead['height'], 'Main motion hidden behind masthead'
        assert box['y']+box['height']<=page.viewport_size['height'], 'Main motion below viewport'
        states.append(page.locator('.paired-scene svg').inner_html())
    assert states[0]!=states[1]

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(base+'quiet-incline/index.html',wait_until='domcontentloaded')
    selected={s:page.locator(s).inner_text() for s in ['.intro>div:first-child','.columns>section','.side']}
    for name in names:
        page.goto(base+f'mountain-{name}/index.html',wait_until='domcontentloaded')
        page.evaluate('document.fonts.ready');settle(page)
        for selector,text in selected.items(): assert page.locator(selector).inner_text()==text
        assert page.locator('.portrait-photo').get_attribute('src')=='../../img/kakto.jpg'
        assert page.locator('.portrait-photo').evaluate('(e)=>e.complete && e.naturalWidth>0')
        assert page.locator('.agent-panel,.mobile-agent-link').count()==0
        assert page.locator('.nav').get_by_role('link',name='Agent version',exact=True).count()==1
        assert page.locator('.paired-scene').bounding_box()['height']<=56.1
        scroll(page,0)
        initial=page.locator('.paired-scene svg').inner_html()
        header_initial=page.locator('.paired-header').inner_html()
        page.locator('.paired-scene').screenshot(path=f'design-review/assets/mountain-{name}-mark.png')
        page.screenshot(path=f'design-review/assets/mountain-{name}-desktop.png',full_page=True)
        visible_motion(page)
        page.screenshot(path=f'design-review/assets/mountain-{name}-early-scroll.png')
        scroll(page,0)
        assert page.locator('.paired-scene svg').inner_html()==initial
        page.evaluate('scrollTo(0,document.documentElement.scrollHeight)');settle(page)
        page.wait_for_function("getComputedStyle(document.querySelector('.paired-header')).opacity==='1'")
        assert page.locator('.paired-header').inner_html()!=header_initial
        idle=page.locator('.paired-header').inner_html()
        page.wait_for_timeout(120)
        assert page.locator('.paired-header').inner_html()==idle
        page.locator('.paired-header').screenshot(path=f'design-review/assets/mountain-{name}-header.png')
        for width,height in [(320,568),(390,844),(768,900)]:
            page.set_viewport_size({'width':width,'height':height});scroll(page,0)
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
            assert page.locator('.paired-scene').bounding_box()['height']<=56.1
            visible_motion(page)
            page.evaluate('scrollTo(0,document.documentElement.scrollHeight)');settle(page)
            box=page.locator('.paired-header').bounding_box();nav=page.locator('.nav').bounding_box()
            assert box['y']+box['height']<=nav['y']
        page.set_viewport_size({'width':390,'height':844});scroll(page,0)
        page.screenshot(path=f'design-review/assets/mountain-{name}-mobile.png',full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        reduced=browser.new_page(reduced_motion='reduce')
        reduced.goto(base+f'mountain-{name}/index.html',wait_until='domcontentloaded');reduced.evaluate('document.fonts.ready');settle(reduced)
        before=reduced.locator('.paired-scene svg').inner_html();scroll(reduced,500)
        assert reduced.locator('.paired-scene svg').inner_html()==before
        assert reduced.locator('.paired-header:visible').count()==0
        reduced.close()
    nojs=browser.new_page(java_script_enabled=False)
    nojs.goto(base+'mountain-ridge/index.html',wait_until='domcontentloaded')
    assert nojs.locator('.portrait-photo').is_visible()
    assert nojs.locator('.post').count()==8
    page.goto(base+'mountains.html',wait_until='domcontentloaded');page.evaluate('document.fonts.ready')
    page.screenshot(path='design-review/assets/mountains-comparison.png',full_page=True)
    page.locator('details').first.locator('summary').click()
    frame=page.frame_locator('iframe').first
    frame.locator('[data-mountain]').wait_for()
    frame.locator('body').evaluate('()=>scrollTo(0,document.documentElement.scrollHeight)')
    frame.locator('body').evaluate('()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))')
    assert float(frame.locator('body').get_attribute('data-mountain-header-progress'))>.9
    browser.close()
assert not errors,errors
print('PASS: three low mountain marks, selected content/photo preserved, <=56px height, actual on-screen early motion at desktop/phone/tablet widths, reversal, idle, header spacing, reduced motion, no-JS, live preview, screenshots.')
