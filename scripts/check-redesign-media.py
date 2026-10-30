"""Verify optional media using isolated temporary builds and validate public exports."""
from pathlib import Path
from tempfile import TemporaryDirectory
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import shutil,subprocess,json,xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
with TemporaryDirectory(prefix='mario-media-') as tmp:
 source=Path(tmp)/'source'; output=Path(tmp)/'output'
 shutil.copytree(root,source,ignore=shutil.ignore_patterns('.git','_site','.bundle','.jekyll-cache','vendor','design-review'))
 handler=partial(SimpleHTTPRequestHandler,directory=str(output))
 server=ThreadingHTTPServer(('127.0.0.1',0),handler)
 Thread(target=server.serve_forever,daemon=True).start()
 with sync_playwright() as p:
  browser=p.chromium.launch()
  for kind in ['image','none']:
   profile=(root/'_data/profile.yml').read_text().replace('kind: ridgeline','kind: '+kind).replace('  src:\n','  src: /img/bg.jpg\n').replace('  alt:\n','  alt: Mountain landscape\n')
   (source/'_data/profile.yml').write_text(profile)
   subprocess.run(['bundle','exec','jekyll','build','--source',str(source),'--destination',str(output)],check=True,capture_output=True)
   page=browser.new_page(viewport={'width':390,'height':844}); errors=[]
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(f'http://127.0.0.1:{server.server_port}/');page.evaluate('document.fonts.ready')
   assert page.locator('.portrait-photo').is_visible()
   assert page.locator('.chapter,.post').count()==8
   assert page.locator('script[src*="ridgeline"]').count()==0
   assert page.locator('.paired-scene,.paired-header').count()==0
   assert page.locator('.feature-image').count()==(1 if kind=='image' else 0)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   assert not errors,errors
   page.close()
  browser.close()
 server.shutdown()
record=json.loads((root/'_site/profile.json').read_text())
assert len(record['experience'])==13 and len(record['writing'])==8
for entry in record['writing']:
 path=root/'_site'/entry['markdown_url'].split('mariomendez.me/')[1]
 text=path.read_text();assert text.startswith('# '+entry['title']);assert '{{' not in text
for name in ['feed.xml','sitemap.xml']:ET.parse(root/'_site'/name)
json.loads((root/'_site/manifest.json').read_text())
assert not (root/'_site/design-review').exists()
print('PASS: isolated image/none builds retain portrait, writing, navigation and bounded layout; no ridgeline controller; 13 history and 8 Markdown/JSON records; valid XML and manifest; no review artifacts.')
