"""Apply shared static navigation without serializing or rewriting page content.

Run after page generators. Requires beautifulsoup4 for reading existing links.
Excludes verification files, source templates and the interactive animation editor.
"""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html import escape
import os, re, subprocess
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
def apply(path, source=None):
    text = source if source is not None else path.read_text(encoding='utf-8-sig')
    if '<body' not in text: return False
    en = bool(re.search(r'<html[^>]+lang=["\']en', text))
    soup = BeautifulSoup(text, 'html.parser')
    old = soup.body.find(['header','nav'], recursive=False)
    if old and 'unified-header' in old.get('class', []):
        candidates = old.select('.unified-local:not(.unified-resources) .unified-local-panel a')
    else:
        candidates = old.select('a') if old else []
    suffix = '_en' if en else ''
    targets = [('index'+suffix+'.html', 'Home' if en else '首頁'),
        ('talks/index'+suffix+'.html','Talks' if en else '演講邀約'),
        ('author-works/index'+suffix+'.html','Research' if en else '研究成果'),
        ('ai-course-site/index'+suffix+'.html','AI Courses' if en else 'AI教材'),
        ('linebot-course-site/index'+suffix+'.html','LINE Bot'),
        ('certificates-site/index'+suffix+'.html','Credentials' if en else '證照紀錄'),
        ('sitemap'+suffix+'.html','Sitemap' if en else '網站導覽')]
    rel = lambda p: os.path.relpath(ROOT / p, path.parent).replace('\\','/')
    def link(href,label,current=False):
        return f'<a class="unified-link" href="{escape(href,quote=True)}"'+(' aria-current="page"' if current else '')+f'>{escape(label)}</a>'
    global_links = ''.join(link(rel(p),label,ROOT/p==path) for p,label in targets)
    groups = [
        ('Tools & licenses' if en else '工具與授權', [
            ('veo-crator/index.html', 'Animation Studio' if en else '動態圖室線上版'),
            ('veo-crator/local-version/index.html', 'Local version' if en else '動態圖室本機完整版'),
            ('veo-crator/license.html', 'Noncommercial license' if en else '動態圖室非商業授權'),
            ('veo-crator/third-party.html', 'Third-party licenses' if en else '第三方授權'),
            ('copyright.html', 'Website copyright' if en else '網站內容著作權')]),
        ('Multi-agent learning' if en else '多代理人AI協作教材', [
            ('opencodex-teaching-site/index.html', 'Chinese tutorial' if en else '中文教學網站'),
            ('opencodex-teaching-site/index_en.html', 'English tutorial'),
            ('opencodex-teaching-site/index.html#diagrams', 'Workflow diagrams' if en else '視覺化流程圖'),
            ('opencodex-teaching-site/mermaid-exports/index.html', 'SVG exports' if en else '中英文SVG圖片匯出')]),
        ('OpenCodex model routing' if en else 'OpenCodex模型代理教學', [
            ('opencodex/index.html', 'Chinese guide' if en else '繁體中文完整教學'),
            ('opencodex/index_en.html', 'English guide'),
            ('opencodex/index.html#dashboard', 'Dashboard screenshots' if en else '本機Dashboard實際截圖'),
            ('opencodex/index.html#sources', 'Sources and evidence' if en else '來源與證據')])]
    resource_links = ''.join('<strong class="unified-mobile-label">'+label+'</strong>'+''.join(link(rel(p.split('#')[0])+('#'+p.split('#')[1] if '#' in p else ''),title) for p,title in items) for label,items in groups)
    resource_label = 'Resources' if en else '工具與進階教材'
    resources = f'<details class="unified-local unified-resources"><summary>{resource_label}</summary><nav class="unified-local-panel" aria-label="{resource_label}">{resource_links}</nav></details>'
    peer = path.with_name(path.name.replace('_en.html','.html') if en else path.stem+'_en.html')
    if peer.exists(): global_links += link(peer.name,'繁體中文' if en else 'English')
    excluded = {(ROOT/p).resolve() for p,_ in targets}
    excluded.add(peer.resolve())
    local,seen = [],set()
    for a in candidates:
        href=a.get('href',''); parsed=urlsplit(href)
        if not href or href in seen: continue
        if not parsed.scheme and not parsed.fragment and (path.parent/unquote(parsed.path)).resolve() in excluded: continue
        local.append(link(href,a.get_text(' ',strip=True))); seen.add(href)
    local_links=''.join(local)
    label='Page / course links' if en else '本頁／教材導覽'
    extra=f'<details class="unified-local"><summary>{label}</summary><nav class="unified-local-panel" aria-label="{label}">{local_links}</nav></details>' if local else ''
    mobile_extra=f'<strong class="unified-mobile-label">{label}</strong>{local_links}' if local else ''
    navlabel='Site navigation' if en else '全站導覽'
    header=f'''<header class="unified-header"><div class="unified-inner">
<a class="unified-brand" href="{rel('index'+suffix+'.html')}">{'Yu-Ting Shih' if en else '施育廷'}<span>Andrew Shih</span></a>
<nav class="unified-desktop" aria-label="{navlabel}">{global_links}{resources}{extra}</nav>
<details class="unified-mobile"><summary>{'Menu / Language' if en else '選單／語言'}</summary><nav class="unified-mobile-panel" aria-label="{navlabel}">{global_links}{resource_links}{mobile_extra}</nav></details>
</div></header>'''
    if old:
        text=re.sub(r'<'+old.name+r'\b[^>]*>.*?</'+old.name+'>',lambda _:header,text,count=1,flags=re.S|re.I)
    else:
        text=re.sub(r'(<body\b[^>]*>)',lambda m:m[1]+'\n'+header,text,count=1,flags=re.I)
    def body(m):
        tag=m[0]
        if re.search(r'class=',tag):
            return re.sub(r'class=(["\'])(.*?)\1',lambda x:'class='+x[1]+x[2]+('' if 'site-unified' in x[2].split() else ' site-unified')+x[1],tag)
        return tag[:-1]+' class="site-unified">'
    text=re.sub(r'<body\b[^>]*>',body,text,count=1)
    if 'assets/site-shell.css' not in text:
        text=text.replace('</head>',f'<link rel="stylesheet" href="{rel("assets/site-shell.css")}">\n<script defer src="{rel("assets/site-shell.js")}"></script>\n</head>')
    path.write_text(text,encoding='utf-8',newline='\n')
    return True

if __name__=='__main__':
    count=0
    tracked = subprocess.check_output(['git','ls-files','-z','*.html'],cwd=ROOT).decode('utf-8').split('\0')
    for path in sorted(ROOT / name for name in tracked if name):
        parts=path.relative_to(ROOT).parts
        if parts[0] in ('.git','scripts') or 'local-version' in parts: continue
        if path.name.startswith('google') or parts==('veo-crator','index.html'): continue
        count+=apply(path)
    print(f'Unified {count} content pages; interactive editor and verification files preserved.')
