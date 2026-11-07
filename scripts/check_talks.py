"""Validate invitation content, local links and responsive navigation."""
from pathlib import Path
import json
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=True)
    page = browser.new_page()
    page.route('https://**/*', lambda route: route.abort())
    for file in (ROOT / 'talks').glob('index*.html'):
        text = file.read_text(encoding='utf-8')
        assert '\ufffd' not in text and '????' not in text
        soup = BeautifulSoup(text, 'html.parser')
        assert len(soup.select('h1')) == 1
        ids = [n['id'] for n in soup.select('[id]')]
        assert len(ids) == len(set(ids))
        for script in soup.select('script[type="application/ld+json"]'):
            json.loads(script.string)
        for node in soup.select('[href], [src]'):
            url = urlsplit(node.get('href', node.get('src', '')))
            if url.scheme or url.netloc:
                continue
            target = (file.parent / unquote(url.path)).resolve() if url.path else file
            assert target.exists(), target
            if url.fragment and target.suffix == '.html':
                assert BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser').find(id=url.fragment), url
        for width in (390, 1440):
            page.set_viewport_size({'width': width, 'height': 900})
            page.goto(file.as_uri())
            assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 2')
            if width == 390:
                page.locator('.unified-mobile > summary').click()
                page.keyboard.press('Escape')
                assert page.locator('.unified-mobile').get_attribute('open') is None
            page.locator('#learning-paths').scroll_into_view_if_needed()
            page.screenshot(path=str(ROOT.parent / f'talks-{file.stem}-{width}.png'))
            print('PASS', file.name, width)
    browser.close()
