"""Optional production browser checks. Serve _site on port 4175 first.
Run with the external Playwright installation documented in design-review/QA.md.
"""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

base = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4175'
routes = json.loads(Path('design-review/production-routes.json').read_text())
posts = [post['url'] for post in routes['posts']]
errors = []

def settle(page):
    page.evaluate('document.fonts.ready')
    page.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))')

def scroll(page, y):
    page.evaluate('(y) => scrollTo(0,y)', y)
    settle(page)

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    # Deterministic layout checks; remote legacy embeds are outside this audit.
    context.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base) else route.abort())
    page = context.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    for width, height in [(320,568),(390,844),(768,900),(1440,1000)]:
        page.set_viewport_size({'width':width,'height':height})
        for path in ['/', '/blog/', '/experience/', '/for-agents/', '/categories/robotics.html', '/tags/robotics.html', '/404.html'] + posts:
            response = page.goto(base + path, wait_until='domcontentloaded')
            assert response.status == 200, (path, response.status)
            settle(page)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (path,width,'overflow')
            for element in page.locator('script[type="application/ld+json"]').all():
                json.loads(element.text_content())
        page.goto(base + '/')
        settle(page)
        assert page.locator('.chapter').count() == 3
        assert page.locator('.post').count() == 5
        assert page.locator('.portrait-photo').evaluate('(e)=>e.complete && e.naturalWidth>0')
        assert page.locator('.paired-scene').bounding_box()['height'] <= 56.1
        start = float(page.locator('body').get_attribute('data-mountain-start'))
        length = float(page.locator('body').get_attribute('data-mountain-range'))
        assert 48 <= length <= 96
        original = page.locator('.paired-scene svg').inner_html()
        states = []
        for progress in [.2,.8]:
            scroll(page,start+length*progress)
            scene = page.locator('.paired-scene').bounding_box()
            head = page.locator('.site-head').bounding_box()
            assert scene['y'] >= head['y']+head['height'], (width,'motion hidden')
            assert scene['y']+scene['height'] <= height, (width,'motion below viewport')
            states.append(page.locator('.paired-scene svg').inner_html())
        assert states[0] != states[1]
        scroll(page,0)
        assert page.locator('.paired-scene svg').inner_html() == original
        scroll(page,10000)
        page.wait_for_function("getComputedStyle(document.querySelector('.paired-header')).opacity === '1'")
        if width <= 900:
            head = page.locator('.paired-header').bounding_box()
            nav = page.locator('.nav').bounding_box()
            assert head['y']+head['height'] <= nav['y']
        scroll(page,0)
        if width in [390,1440]:
            page.screenshot(path=f'/tmp/mario-production-{width}.png',full_page=True)
    reduced = browser.new_page(reduced_motion='reduce')
    reduced.goto(base + '/')
    settle(reduced)
    before = reduced.locator('.paired-scene svg').inner_html()
    scroll(reduced,500)
    assert reduced.locator('.paired-scene svg').inner_html() == before
    assert not reduced.locator('.paired-header').is_visible()
    nojs = browser.new_page(java_script_enabled=False)
    nojs.goto(base + '/')
    assert nojs.locator('.portrait-photo').is_visible()
    assert nojs.locator('.chapter,.post').count() == 8
    assert nojs.get_by_role('link',name='Agent version',exact=True).count() == 2
    page.goto(base + '/for-agents/')
    page.locator('#copy-prompt').click()
    page.wait_for_function("document.querySelector('#copy-status').textContent.length > 0")
    browser.close()
assert not errors, errors
print('PASS: production routes, four viewport sizes, structured data, portrait, writing, visible ridgeline motion, reversal, header spacing, reduced motion, no-JS, prompt copy.')
