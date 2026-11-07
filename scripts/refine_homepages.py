"""Targeted bilingual homepage refinement; preserve existing layout and navigation."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = 'https://vocus.cc/article/6ab118b7fd8978000116d596'

for en in (False, True):
    suffix = '_en' if en else ''
    path = ROOT / f'index{suffix}.html'
    html = path.read_text(encoding='utf-8')
    def t(zh, eng):
        return eng if en else zh
    replacements = {
        t('href="#invite">演講與研習邀約', 'href="#invite">Discuss a talk or workshop'):
        t('href="talks/index.html">演講與研習邀約', 'href="talks/index_en.html">Discuss a talk or workshop'),
        t('href="#resources">開始學習 →', 'href="#resources">Explore learning resources →'):
        t('href="#featured">查看代表成果 →', 'href="#featured">Explore featured work →'),
        t('<section class="block"><div class="wrap"><div class="section-head"><h2>從一個問題，開始實作。</h2>', '<section class="block"><div class="wrap"><div class="section-head"><h2>Start with a real question.</h2>'):
        t('<section class="block" id="featured"><div class="wrap"><div class="section-head"><h2>代表成果：從問題到實作</h2>', '<section class="block" id="featured"><div class="wrap"><div class="section-head"><h2>Featured work: from questions to practice</h2>'),
        t('<h3>讓訊息進入工作流程</h3><p>追蹤訊息如何接收、處理與記錄，從基本回覆開始練習，再逐步串接AI。</p><a href="linebot-course-site/index.html">閱讀教材或紀錄 ↗</a>', '<h3>From a message to a workflow</h3><p>Trace how messages are received, processed and recorded. Start with a basic reply before connecting AI.</p><a href="linebot-course-site/index_en.html">Explore the resource ↗</a>'):
        t('<h3>LINE Bot雲端管理與AI工作流</h3><p>查看操作影片、原課程教材與I918530專利證書。專利資訊與功能展示分開說明，並列出使用限制。</p><a href="linebot-course-site/showcase.html">觀看成果與專利證書 ↗</a>', '<h3>LINE Bot cloud management and AI workflows</h3><p>Explore demonstrations, original course materials and the I918530 patent certificate. Patent information and demonstrated features are distinguished, with usage limitations.</p><a href="linebot-course-site/showcase_en.html">View the showcase and patent certificate ↗</a>'),
        t('<h2>公開授課與交流紀錄</h2>', '<h2>Teaching & public conversations</h2>'):
        t('<h2>公開介紹與授課紀錄</h2>', '<h2>Public introductions and teaching records</h2>'),
        t('<p>代表專利 I918530；專利資訊與研究成果分開標示。</p><a href="author-works/index.html">查看專利與來源 ↗</a>', '<p>Patent I918530, presented separately from research outcomes.</p><a href="author-works/index_en.html">View patent and sources ↗</a>'):
        t('<p>發明專利I918530；可查閱證書、官方來源與相關實作影片。</p><a href="linebot-course-site/showcase.html">查看專利證書與實作 ↗</a>', '<p>Invention patent I918530, with its certificate, official source and related demonstrations.</p><a href="linebot-course-site/showcase_en.html">View the certificate and demonstrations ↗</a>'),
        t('<small>請提供單位、參與對象、主題需求與預計日期。</small>', '<small>Please include your organization, audience, topic and proposed dates.</small>'):
        t('<small>請提供單位、參與對象、主題需求與預計日期。</small><p><a href="talks/index.html#learning-paths">先看研習方向與準備事項 →</a></p>', '<small>Please include your organization, audience, topic and proposed dates.</small><p><a href="talks/index_en.html#learning-paths">Review workshop options and preparation →</a></p>'),
    }
    for old, new in replacements.items():
        if old in html:
            html = html.replace(old, new)
        else:
            assert new in html, old
    if 'id="teaching-approach"' not in html:
        section = f'''<section class="block" id="teaching-approach"><div class="wrap research"><div><h2>{t('讓初學者理解，<br>也讓結果能被檢查。','Make learning approachable.<br>Keep results open to review.')}</h2><p>{t('從文組背景走進科技與教育，我在意的不只是做出工具，而是讓學習者理解每一步為什麼這樣做。先釐清問題與資料，再練習操作、除錯與查核。','Coming from a humanities background into technology and education, I focus on helping learners understand why each step matters. We clarify the problem and data before practicing, debugging and reviewing results.')}</p><a class="text-link" href="{ARTICLE}">{t('閱讀我的教學理念與自我介紹（方格子） →','Read my teaching philosophy and introduction on Vocus (Chinese) →')}</a><p class="note">{t('作者自述，非第三方推薦。文章發布於2026-09-21，更新於2026-10-03。','Author-written introduction, not a third-party endorsement. Published September 21, 2026; updated October 3, 2026.')}</p></div><div class="research-list"><article><h3>{t('先把需求說清楚','Clarify the task first')}</h3><p>{t('把教學或工作任務拆成資料、處理步驟與互動方式，再決定是否需要AI。','Separate a teaching or work task into data, processing steps and interaction before deciding whether AI is needed.')}</p></article><article><h3>{t('陪伴操作與除錯','Practice and debug together')}</h3><p>{t('以淺白說明降低入門門檻，保留手動操作、測試與修正的學習過程。','Use plain language to support beginners while retaining hands-on operation, testing and revision.')}</p></article><article><h3>{t('由人負責查核','Keep people responsible for review')}</h3><p>{t('AI產出是待檢查的草稿；來源、學術倫理與使用限制仍須由人判斷。','Treat AI output as a draft to check. People remain responsible for sources, academic ethics and usage limits.')}</p></article></div></div></section>'''
        html = html.replace('<section class="block resource-band"', section + '\n<section class="block resource-band"', 1)
    faculty = f'''<article class="evidence-item"><span>{t('校方師資介紹','Faculty profile')}</span><div><h3>{t('國立臺中教育大學｜兼任教師','National Taichung University of Education | Adjunct faculty')}</h3><p>{t('校方公開師資頁；博士候選人身分依作者提供。','University faculty listing; doctoral candidacy is author-provided.')}</p><a href="https://dct.ntcu.edu.tw/teacher/13">{t('查閱校方介紹 ↗','View the university profile ↗')}</a></div></article>'''
    if 'href="https://dct.ntcu.edu.tw/teacher/13">' not in html:
        html = html.replace('<div class="evidence-list">', '<div class="evidence-list">' + faculty, 1)
    description = t('施育廷Yu-Ting Shih（Andrew Shih），國立臺中教育大學兼任講師、教育資訊與測驗統計研究所博士候選人。提供AI教學、行政研究應用與LINE Bot實作教材，並整理演講邀約、代表成果及公開授課來源。', 'Yu-Ting Shih (Andrew Shih), NTCU adjunct lecturer and doctoral candidate. Explore AI teaching, administrative and research workflows, LINE Bot materials, workshop invitations and documented public talks.')
    html = re.sub(r'(<meta (?:name="(?:description|twitter:description)"|property="og:description") content=")[^"]*', lambda m: m[1] + description, html)
    def schema(match):
        data = json.loads(match[1])
        for node in data.get('@graph', []):
            if node.get('@type') == 'WebPage':
                node['description'] = description
                node['dateModified'] = '2026-11-07'
        return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n  </script>'
    html = re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, html, flags=re.S)
    path.write_text(html, encoding='utf-8')
