from playwright.sync_api import sync_playwright
from pathlib import Path
import os
import sys
os.chdir(Path(__file__).resolve().parents[1])
base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:4173/design-review/'
if not base.endswith('/'):
 base+='/'
errors=[]
with sync_playwright() as p:
 browser=p.chromium.launch()
 for name in ['journal','fieldguide','record']:
  page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
  page.on('pageerror', lambda e:errors.append(str(e)))
  for path in ['index.html','road-to-seed-round.html','history.html']:
   response=page.goto(base+name+'/'+path,wait_until='domcontentloaded')
   assert response.status==200
   page.evaluate('document.fonts.ready')
   assert page.locator('h1').count()==1
   assert page.locator('main').count()==1
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), name+path+' desktop overflow'
   if path=='index.html':
    assert page.locator('h1').inner_text().find('\\n')==-1
    page.screenshot(path=f'design-review/assets/{name}-desktop.png',full_page=True)
   if path=='road-to-seed-round.html':
    assert 'Every new feature was its own mini mvp' in page.locator('.prose').inner_text()
    page.screenshot(path=f'design-review/assets/{name}-reading.png',full_page=False)
   if path=='history.html':
    assert page.locator('.history-event').count()==13
   page.set_viewport_size({'width':390,'height':844})
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), name+path+' mobile overflow'
   if path=='index.html':page.screenshot(path=f'design-review/assets/{name}-mobile.png',full_page=True)
   page.set_viewport_size({'width':1440,'height':1000})
  if name=='fieldguide':
   page.goto(base+name+'/index.html')
   page.get_by_role('button',name='Product',exact=True).click()
   assert page.locator('[data-topics]:visible').count()==2
   assert page.locator('[data-filter-count]').inner_text()=='2 published entries'
   page.get_by_role('button',name='Systems',exact=True).click()
   assert page.locator('[data-topics]:visible').count()==6
   page.get_by_role('button',name='Everything',exact=True).click()
   assert page.locator('[data-topics]:visible').count()==8
  page.close()
 page=browser.new_page(java_script_enabled=False,viewport={'width':390,'height':844})
 page.goto(base+'fieldguide/index.html')
 assert page.locator('[data-topics]:visible').count()==8
 assert len(page.locator('main a[href$=".html"]').all())>=8
 page.goto(base+'agents/index.html',wait_until='domcontentloaded')
 page.evaluate('document.fonts.ready')
 page.set_viewport_size({'width':1440,'height':1050})
 page.screenshot(path='design-review/assets/agent-desktop.png',full_page=True)
 page.set_viewport_size({'width':390,'height':844})
 page.screenshot(path='design-review/assets/agent-mobile.png',full_page=True)
 page.goto(base,wait_until='domcontentloaded')
 page.evaluate('document.fonts.ready')
 page.set_viewport_size({'width':1440,'height':1050})
 page.screenshot(path='design-review/assets/comparison.png',full_page=True)
 browser.close()
assert not errors, errors
print('PASS: desktop/mobile home, reading, and history views for all 3 directions; content, filters, no-JS browsing, no horizontal overflow, no JS errors.')
