from pathlib import Path
import os
from playwright.sync_api import sync_playwright

os.chdir(Path(__file__).resolve().parents[1])
base = 'http://127.0.0.1:4173/design-review/'
errors = []
def settle(page):
    page.evaluate('() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
def position(page, fraction):
    page.evaluate('(p) => scrollTo(0, (document.documentElement.scrollHeight - innerHeight) * p)', fraction)
    settle(page)
def signature(page, mode):
    return page.locator('.hiker-marker' if mode == 'summit' else '.scroll-rail > svg > g').first.get_attribute('transform')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width':1440, 'height':1000}, device_scale_factor=1)
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base + 'summit/index.html', wait_until='domcontentloaded')
    baseline = {selector: page.locator(selector).inner_text() for selector in ['.intro > div:first-child', '.columns > section', '.side']}
    for mode in ['bike','summit','trail']:
        page.goto(base + f'scroll-{mode}/index.html', wait_until='domcontentloaded')
        page.evaluate('document.fonts.ready')
        settle(page)
        for selector, text in baseline.items():
            assert page.locator(selector).inner_text() == text, (mode, selector, 'changed selected content')
        assert page.locator('.scene-control, input[type=range]').count() == 0
        position(page, 0)
        start = signature(page, mode)
        page.screenshot(path=f'design-review/assets/scroll-{mode}-start.png')
        position(page, .5)
        middle = signature(page, mode)
        if mode == 'summit':
            page.wait_for_function("getComputedStyle(document.querySelector('.header-summit')).opacity === '1'")
        assert start != middle, (mode, 'did not respond to scroll')
        page.screenshot(path=f'design-review/assets/scroll-{mode}-middle.png')
        if mode == 'summit':
            assert page.locator('.header-summit').evaluate('(e) => getComputedStyle(e).opacity') == '1'
            assert page.locator('.header-summit .hiker-marker').get_attribute('transform') == middle
        position(page, 1)
        assert signature(page, mode) != middle
        page.screenshot(path=f'design-review/assets/scroll-{mode}-end.png')
        idle = signature(page, mode)
        page.wait_for_timeout(150)
        assert signature(page, mode) == idle, (mode, 'keeps moving while idle')
        position(page, 0)
        assert signature(page, mode) == start, (mode, 'does not reverse')
        page.keyboard.press('PageDown')
        page.wait_for_function('window.scrollY > 0')
        settle(page)
        assert signature(page, mode) != start
        page.set_viewport_size({'width':390,'height':844})
        position(page, .55)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        if mode == 'summit':
            miniature = page.locator('.header-summit').bounding_box()
            nav = page.locator('.nav').bounding_box()
            assert miniature['y'] + miniature['height'] <= nav['y'], 'Miniature covers phone navigation'
        page.screenshot(path=f'design-review/assets/scroll-{mode}-mobile.png')
        page.set_viewport_size({'width':1440,'height':1000})
        page.goto(base + f'scroll-{mode}/road-to-seed-round.html', wait_until='domcontentloaded')
        assert 'Every new feature was its own mini mvp' in page.locator('.prose').inner_text()
        reduced = browser.new_page(reduced_motion='reduce')
        reduced.goto(base + f'scroll-{mode}/index.html', wait_until='domcontentloaded')
        reduced.evaluate('document.fonts.ready')
        settle(reduced)
        initial = reduced.locator('.hiker-marker').first.get_attribute('transform')
        position(reduced, 1)
        assert reduced.locator('.hiker-marker').first.get_attribute('transform') == initial
        assert reduced.locator('.scroll-rail:visible, .header-summit:visible').count() == 0
        reduced.close()
    nojs = browser.new_page(java_script_enabled=False)
    nojs.goto(base + 'scroll-summit/index.html', wait_until='domcontentloaded')
    assert nojs.locator('.post').count() == 8
    assert nojs.locator('.summit-scene svg').is_visible()
    assert nojs.locator('.agent-nav').is_visible()
    page.goto(base + 'motion.html', wait_until='domcontentloaded')
    page.evaluate('document.fonts.ready')
    frame = page.frames[1]
    frame.wait_for_selector('.scroll-rail')
    frame.evaluate('scrollTo(0, document.documentElement.scrollHeight)')
    page.wait_for_timeout(100)
    assert float(frame.locator('body').get_attribute('data-scroll-progress')) > .9
    page.screenshot(path='design-review/assets/scroll-comparison.png', full_page=True)
    browser.close()
assert not errors, errors
print('PASS: three scroll variants, unchanged selected content, movement/reversal/idle, keyboard scrolling, phone navigation, reduced motion, no-JS, static article reading, live iframe, and screenshots.')
