"""Check bilingual tutorial links and UTF-8 before publication (no credentials)."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
errors = []
pages = list((ROOT / 'linebot-course-site').glob('*.html'))
pages += [ROOT / 'index.html', ROOT / 'index_en.html']
for path in pages:
    text = path.read_text(encoding='utf-8-sig')
    assert '\ufffd' not in text, path
    soup = BeautifulSoup(text, 'html.parser')
    ids = [n['id'] for n in soup.select('[id]')]
    if len(ids) != len(set(ids)):
        errors.append(f'{path.name}: duplicate IDs')
    for tag in soup.select('script[type="application/ld+json"]'):
        json.loads(tag.string or tag.get_text())
    for tag in soup.select('[href], img[src], script[src]'):
        ref = tag.get('href', tag.get('src', ''))
        u = urlsplit(ref)
        if u.scheme or u.netloc:
            continue
        target = path.parent / unquote(u.path) if u.path else path
        if target.is_dir():
            target /= 'index.html'
        if not target.is_file():
            errors.append(f'{path.name}: missing {ref}')
        elif u.fragment and target.suffix == '.html':
            other = BeautifulSoup(target.read_text(encoding='utf-8-sig'), 'html.parser')
            if not other.find(id=unquote(u.fragment)):
                errors.append(f'{path.name}: missing anchor {ref}')
    print('Checked', path.relative_to(ROOT))
for name in ['quickstart.html', 'quickstart_en.html']:
    path = ROOT / 'linebot-course-site' / name
    if not path.exists():
        errors.append(f'Missing tutorial: {name}')
print(json.dumps(errors, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
