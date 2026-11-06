"""Dependency-free static checks: python talks/check.py."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.headings = 0
        self.cases = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag != 'iframe'
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'h1':
            self.headings += 1
        if tag == 'article' and attrs.get('class') == 'case':
            self.cases += 1
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'img':
            assert 'alt' in attrs and 'width' in attrs and 'height' in attrs


for filename in ('index.html', 'index_en.html'):
    text = (ROOT / filename).read_text(encoding='utf-8')
    page = Page()
    page.feed(text)
    assert page.headings == 1 and page.cases == 6
    assert len(page.ids) == len(set(page.ids))
    for href in page.links:
        parsed = urlsplit(href)
        if not parsed.scheme and not parsed.netloc:
            if parsed.path:
                assert (ROOT / parsed.path).is_file(), href
            elif parsed.fragment:
                assert parsed.fragment in page.ids, href
    schema = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)[1])
    assert schema['@graph'][0]['@id'] == 'https://andrewshih1210.github.io/my-blog/#person'
    assert schema['@graph'][1]['@type'] == 'WebPage'
    assert all(f'hreflang="{lang}"' in text for lang in ('zh-Hant', 'en', 'x-default'))
    assert 'VideoObject' not in text and 'autoplay' not in text
    assert '3103e77e7c774' in text and '2026-11-02' in text
    print(f'{filename}: passed links, anchors, six cases, headings, images and schema')
