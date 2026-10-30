"""Verify all optional media modes in isolated builds; no source files are changed."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread
import json
import shutil
import subprocess
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
expected_history = json.loads(subprocess.check_output(
    ['ruby', '-ryaml', '-rjson', '-e', 'puts YAML.load_file(ARGV[0]).fetch("events").to_json', str(root / '_config.yml')],
    text=True))
expected_posts = len(list((root / '_posts').glob('*.md')))

with TemporaryDirectory(prefix='mario-media-') as tmp:
    source, output = Path(tmp) / 'source', Path(tmp) / 'output'
    shutil.copytree(root, source, ignore=shutil.ignore_patterns(
        '.git', '_site', '.bundle', '.jekyll-cache', 'vendor', 'docs'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(output)))
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for kind in ['image', 'none']:
                profile = (root / '_data/profile.yml').read_text().split('feature_media:')[0]
                profile += f'feature_media:\n  kind: {kind}\n  src: /img/bg.jpg\n  alt: Mountain landscape\n  width: 1200\n  height: 800\n'
                (source / '_data/profile.yml').write_text(profile)
                subprocess.run(['bundle', 'exec', 'jekyll', 'build', '--source', str(source), '--destination', str(output)],
                               cwd=root, check=True, capture_output=True)
                page = browser.new_page()
                errors = []
                page.on('pageerror', lambda error: errors.append(str(error)))
                for width in [320, 390, 768, 1440]:
                    page.set_viewport_size({'width': width, 'height': 1000})
                    page.goto(f'http://127.0.0.1:{server.server_port}/')
                    page.evaluate('document.fonts.ready')
                    assert page.locator('.portrait-photo').is_visible()
                    assert page.locator('.chapter,.post').count() == expected_posts
                    assert page.locator('.feature-image:visible').count() == (1 if kind == 'image' else 0)
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                assert not errors, errors
                page.close()
            browser.close()
    finally:
        server.shutdown()

record = json.loads((root / '_site/profile.json').read_text())
assert len(record['experience']) == len(expected_history)
assert len(record['writing']) == expected_posts
assert [event['title'] for event in record['experience']] == [event['title'] for event in expected_history]
assert not (root / '_site/docs').exists()
print('PASS: image/none at four widths, portrait and writing retained, history/export parity.')
