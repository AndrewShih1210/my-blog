"""Restore source-aligned course pages without generating a different stack."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def build(en):
    suffix = '_en' if en else ''
    for stem in ['quickstart', 'process']:
        name = f'{stem}{suffix}.html'
        source = ROOT / 'scripts/linebot-course-site-templates' / name
        (ROOT / 'linebot-course-site' / name).write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
if __name__ == '__main__':
    build(False)
    build(True)
