"""Check the agent page's actual URLs over HTTP, including copied-prompt URLs.

Run against a development preview, or against the public site after deployment:
  python scripts/check-agent-links.py http://127.0.0.1:4175
"""
import json
import re
import sys
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

base = (sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:4175').rstrip('/')
origin = urlparse(base)
local_names = {'localhost', '127.0.0.1', '::1'}
checked = {}


def same_site(url):
    parsed = urlparse(url)
    if origin.hostname in local_names:
        return parsed.hostname in local_names and parsed.port == origin.port
    return parsed.netloc == origin.netloc and parsed.scheme == origin.scheme


with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    response = page.goto(base + '/for-agents/')
    assert response.status == 200
    prompt = page.locator('#agent-prompt').input_value()
    prompt_urls = re.findall(r'https?://[^\s<>]+', prompt)
    assert len(prompt_urls) == 3, prompt_urls
    urls = set(prompt_urls)
    for href in page.locator('a[href]').evaluate_all('(links) => links.map(a => a.href)'):
        if same_site(href):
            urls.add(href)
    downloads = page.locator('.file-list a').evaluate_all('(links) => links.map(a => a.href)')
    assert len(downloads) == 4
    for url in prompt_urls + downloads:
        assert same_site(url), f'Preview link points at another site: {url}'

    def fetch(url):
        assert same_site(url), f'Export link points at another site: {url}'
        if url not in checked:
            result = context.request.get(url)
            assert result.status == 200, (url, result.status)
            text = result.text()
            if urlparse(url).path.endswith(('.md', '.txt')):
                assert text.startswith('# '), (url, 'not a plain-text export')
                assert '<!doctype' not in text.lower(), (url, 'HTML error page')
            checked[url] = text
        return checked[url]

    for url in sorted(urls):
        fetch(url)
    profile_url = next(url for url in prompt_urls if urlparse(url).path.endswith('/profile.json'))
    profile = json.loads(fetch(profile_url))
    assert profile['schema_version'] == 1
    for record in profile['writing']:
        article = fetch(record['url'])
        markdown = fetch(record['markdown_url'])
        assert '<article' in article
        assert markdown.startswith('# ' + record['title'])
    writing_url = next(url for url in downloads if urlparse(url).path.endswith('/writing.md'))
    for url in re.findall(r'\]\((https?://[^)]+)\)', fetch(writing_url)):
        fetch(url)
    profile_md_url = next(url for url in downloads if urlparse(url).path.endswith('/profile.md'))
    assert profile['name'] in fetch(profile_md_url)
    assert profile['name'] in fetch(urljoin(base + '/', 'llms.txt'))
    page.locator('#copy-prompt').click()
    page.wait_for_function("document.querySelector('#copy-status').textContent.length > 0")
    assert page.locator('#agent-prompt').input_value() == prompt
    browser.close()
print(f'PASS: all agent-screen links, three prompt URLs, four downloads, and {len(profile["writing"])} HTML/Markdown article pairs ({len(checked)} unique local URLs).')
