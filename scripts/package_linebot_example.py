"""Package only reviewed tutorial sources; never collect a real .env file."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'linebot-course-site/examples/reply-bot'
FILES = ('server.mjs', 'Code.gs', 'package.json', 'Dockerfile', '.env.example',
         '.gitignore', '.gcloudignore', 'test.mjs', 'test-gas.mjs', 'README.md')
if __name__ == '__main__':
    with ZipFile(SOURCE.with_suffix('.zip'), 'w', ZIP_DEFLATED) as archive:
        for name in FILES:
            archive.write(SOURCE / name, 'reply-bot/' + name)
    print('Packaged', len(FILES), 'allowlisted files; no runtime credentials.')
