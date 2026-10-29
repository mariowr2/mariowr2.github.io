from playwright.sync_api import sync_playwright
from pathlib import Path
import json

def contrast(foreground, background):
 def luminance(hex_color):
  values=[int(hex_color[i:i+2],16)/255 for i in (1,3,5)]
  linear=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in values]
  return sum(c*w for c,w in zip(linear,[0.2126,0.7152,0.0722]))
 light,dark=sorted([luminance(foreground),luminance(background)],reverse=True)
 return (light+0.05)/(dark+0.05)
from urllib.parse import urlparse,unquote
from html.parser import HTMLParser
root=Path(__file__).resolve().parents[1]
review=root/'design-review'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  self.refs.extend(v for k,v in attrs if k in ('href','src') and v)
count=0
for f in review.rglob('*.html'):
 parser=Links();parser.feed(f.read_text())
 for ref in parser.refs:
  uri=urlparse(ref)
  if uri.scheme or uri.netloc or not uri.path:continue
  target=(f.parent/unquote(uri.path)).resolve()
  assert target.is_file() or (target/'index.html').is_file(), (f,ref)
 count+=1
profile=json.loads((review/'profile.json').read_text())
assert len(profile['experience'])==13 and len(profile['writing'])==8
assert len(list((review/'text').glob('*.md')))==8
with sync_playwright() as p:
 browser=p.chromium.launch()
 page=browser.new_page()
 page.route('**/*',lambda route:route.continue_() if urlparse(route.request.url).hostname=='127.0.0.1' else route.abort())
 for f in review.rglob('*.html'):
  page.goto('http://127.0.0.1:4173/'+str(f.relative_to(root)),wait_until='domcontentloaded')
  page.evaluate('document.fonts.ready')
  palette=page.evaluate("Object.fromEntries(['paper','ink','muted','accent','wash'].map(k=>[k,getComputedStyle(document.body).getPropertyValue('--'+k).trim()]))")
  for foreground in ['ink','muted','accent']:
   for background in ['paper','wash']:
    assert contrast(palette[foreground],palette[background])>=4.5, (f,foreground,background)
  for width in [320,768,1440]:
   page.set_viewport_size({'width':width,'height':900})
   assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (f,width)
 page.goto('http://127.0.0.1:4173/design-review/journal/index.html')
 page.evaluate('document.fonts.ready')
 assert page.evaluate("document.fonts.check('15px \"Plex Mono\"')")
 assert page.locator('.nav').get_by_role('link',name='For agents').count()==1
 assert page.locator('.agent-panel').get_by_role('link',name='Get the agent briefing').count()==1
 page.keyboard.press('Tab')
 assert page.locator(':focus').inner_text()=='Skip to content'
 page.keyboard.press('Enter')
 assert page.evaluate('location.hash')=='#main'
 page.goto('http://127.0.0.1:4173/design-review/agents/index.html')
 assert 'title or date is not established' in page.locator('#agent-prompt').input_value()
 assert page.locator('.file-list a').count()==4
 page.context.grant_permissions(['clipboard-read','clipboard-write'])
 page.get_by_role('button',name='Copy prompt',exact=True).click()
 page.wait_for_function("document.querySelector('[data-copy-status]').textContent.startsWith('Prompt copied')")
 assert 'Mario Mendez' in page.evaluate('navigator.clipboard.readText()')
 page.evaluate("() => { navigator.clipboard.writeText = () => Promise.reject(new Error('Clipboard unavailable')); }")
 page.get_by_role('button',name='Copy prompt',exact=True).click()
 page.wait_for_function("document.querySelector('[data-copy-status]').textContent.startsWith('Text selected')")
 assert page.locator('#agent-prompt').evaluate('(e) => e.selectionEnd === e.value.length && e.selectionStart === 0')
 browser.close()
print(f'PASS: {count} HTML pages, all local href/src targets, JSON and Markdown exports, 320/768/1440px overflow checks, keyboard skip link, text contrast >=4.5:1, agent navigation, clipboard copy and fallback.')
