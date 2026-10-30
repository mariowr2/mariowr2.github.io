"""Optional production browser checks. Serve _site on port 4175 first.
Run with the external Playwright installation documented in docs/QA.md.
"""
from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

base = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4175'
root = Path(__file__).resolve().parents[1]
routes = json.loads((root / 'docs/production-routes.json').read_text())
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
        for path in sorted('/' + str(path.relative_to(root / '_site')) for path in (root / '_site').rglob('*.html')):
            response = page.goto(base + path, wait_until='domcontentloaded')
            assert response.status == 200, (path, response.status)
            settle(page)
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (path,width,'overflow')
            assert page.locator('main h1').count() == 1, (path, 'missing or duplicate main heading')
            page.evaluate("document.querySelectorAll('img').forEach(img => img.loading = 'eager')")
            page.wait_for_function("Array.from(document.images).every(img => img.complete)")
            assert page.evaluate('Array.from(document.images).every(img => img.naturalWidth > 0)'), (path, 'broken image')
            for link in page.locator('a[href*="github.com/"],a[href*="linkedin.com/"]').all():
                assert link.get_attribute('target') == '_blank', (path, 'social link target')
                assert 'noopener' in link.get_attribute('rel')
                assert '↗' in link.inner_text()
            for element in page.locator('script[type="application/ld+json"]').all():
                json.loads(element.text_content())
        page.goto(base + '/')
        settle(page)
        assert page.locator('.chapter').count() == 3
        assert page.locator('.post').count() == 5
        assert page.locator('.portrait-photo').evaluate('(e)=>e.complete && e.naturalWidth>0')
        if page.locator('.feature-image:visible').count():
            assert page.locator('.feature-image:visible img').evaluate('(e)=>e.complete && e.naturalWidth>0')
        if page.locator('.feature-image:visible').count():
            photo = page.locator('.feature-image:visible').bounding_box()
            side = page.locator('.side').bounding_box()
            assert abs(photo['width'] - side['width']) < 1
            assert abs(photo['x'] - side['x']) < 1
            if width <= 760:
                assert page.locator('.side .feature-image').is_visible()
                writing = page.locator('.columns>section').bounding_box()
                assert photo['y'] >= writing['y'] + writing['height']
        page.keyboard.press('Control+Home')
        page.reload()
        page.keyboard.press('Tab')
        assert page.locator('.skip').evaluate('(e) => e === document.activeElement')
        if width in [390,1440]:
            page.locator('.skip').evaluate('(e) => e.blur()')
            page.screenshot(path=f'/tmp/mario-production-{width}.png',full_page=True)
    nojs = browser.new_page(java_script_enabled=False)
    nojs.goto(base + '/')
    assert nojs.locator('.portrait-photo').is_visible()
    assert nojs.locator('.chapter,.post').count() == 8
    assert nojs.get_by_role('link',name='Agent version',exact=True).count() == 2
    for route, name in [('/experience/', 'experience'), ('/for-agents/', 'agents'), ('/blog/', 'archive'), (posts[0], 'article')]:
        for width in [390, 1440]:
            page.set_viewport_size({'width': width, 'height': 1000})
            page.goto(base + route)
            settle(page)
            page.evaluate("document.querySelectorAll('img').forEach(img => img.loading = 'eager')")
            page.wait_for_function("Array.from(document.images).every(img => img.complete)")
            page.screenshot(path=f'/tmp/mario-production-{name}-{width}.png', full_page=True)
    page.goto(base + '/for-agents/')
    page.locator('#copy-prompt').click()
    page.wait_for_function("document.querySelector('#copy-status').textContent.length > 0")
    browser.close()
assert not errors, errors
print('PASS: production routes, four viewport sizes, structured data, portrait, writing, feature media, no-JS, prompt copy.')
