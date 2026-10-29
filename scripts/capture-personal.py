from pathlib import Path
import os
from playwright.sync_api import sync_playwright

os.chdir(Path(__file__).resolve().parents[1])
base = 'http://127.0.0.1:4173/design-review/'
errors = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(base + 'journal/index.html')
    baseline = {selector: page.locator(selector).inner_text() for selector in ['.intro > div:first-child', '.columns > section', '.side']}
    for name in ['cat', 'ride', 'summit', 'notebook']:
        page.goto(base + name + '/index.html', wait_until='domcontentloaded')
        page.evaluate('document.fonts.ready')
        if name in ['cat', 'ride']:
            for selector, text in baseline.items():
                assert page.locator(selector).inner_text() == text, (name, selector, 'changed original copy')
        page.screenshot(path=f'design-review/assets/{name}-desktop.png', full_page=True)
        if name == 'cat':
            page.get_by_role('button', name='Wake the cat', exact=True).click()
            assert page.locator('[data-cat]').get_attribute('data-awake') == 'true'
            assert page.get_by_role('button', name='Let the cat sleep').get_attribute('aria-pressed') == 'true'
            page.get_by_role('button', name='Let the cat sleep').click()
            assert page.locator('[data-cat]').get_attribute('data-awake') == 'false'
        if name in ['ride', 'notebook']:
            slider = page.get_by_role('slider', name='Move the rider along the illustrated route')
            start = page.locator('.rider-marker').get_attribute('transform')
            slider.focus()
            page.keyboard.press('End')
            assert slider.input_value() == '100'
            assert page.locator('.rider-marker').get_attribute('transform') != start
            page.keyboard.press('Home')
            assert slider.input_value() == '0'
            slider.fill('31')
        if name == 'summit':
            for step in range(5):
                page.get_by_role('button', name='Take another step', exact=True).click()
            assert page.locator('[data-summit-status]').inner_text() == 'At the summit'
            page.get_by_role('button', name='Back to the trailhead', exact=True).click()
            assert page.locator('[data-summit]').get_attribute('data-step') == '0'
        page.set_viewport_size({'width': 390, 'height': 844})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), name
        page.screenshot(path=f'design-review/assets/{name}-mobile.png', full_page=True)
        page.set_viewport_size({'width': 1440, 'height': 1000})
        page.goto(base + name + '/road-to-seed-round.html', wait_until='domcontentloaded')
        page.evaluate('document.fonts.ready')
        assert 'Every new feature was its own mini mvp' in page.locator('.prose').inner_text()
        page.screenshot(path=f'design-review/assets/{name}-reading.png', full_page=False)
    page.goto(base + 'personal.html', wait_until='domcontentloaded')
    page.evaluate('document.fonts.ready')
    page.screenshot(path='design-review/assets/personal-comparison.png', full_page=True)
    nojs = browser.new_page(java_script_enabled=False, viewport={'width':390, 'height':844})
    nojs.goto(base + 'cat/index.html')
    assert nojs.locator('.post').count() == 8
    assert nojs.locator('.personal-scene svg').is_visible()
    assert nojs.locator('.agent-nav').is_visible()
    reduced = browser.new_page(reduced_motion='reduce')
    reduced.goto(base + 'cat/index.html')
    reduced.get_by_role('button', name='Wake the cat').click()
    assert reduced.locator('.cat-tail').evaluate('(e) => getComputedStyle(e).animationName') == 'none'
    browser.close()
assert not errors, errors
print('PASS: four personal variants; unchanged copy/sections in cat and ride; cat toggle, keyboard bike slider, complete summit/reset, real article bodies, mobile, no-JS, reduced motion, screenshots.')
