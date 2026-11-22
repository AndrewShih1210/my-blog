"""Publish broad learning directions only; private curriculum stays outside Git."""
from pathlib import Path
import json
import re
from unify_site_shell import apply

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'teaching-directions'
OUT.mkdir(exist_ok=True)
for en in (False, True):
    def t(zh, english): return english if en else zh
    suffix = '_en' if en else ''
    name = f'index{suffix}.html'
    title = t('教學方向與課程規劃｜施育廷', 'Learning Directions and Course Planning | Yu-Ting Shih')
    description = t('依學習階段與工作任務認識施育廷的AI教學方向：從白話理解、創作與資料整理，到教學研究、GAS與LINE Bot實作。區分既有教材與課程規劃建議。', 'Explore AI learning by educational stage and practical task, from plain-language concepts and creative work to research, GAS and LINE Bot. Existing materials and proposed course directions are clearly distinguished.')
    url = f'https://andrewshih1210.github.io/my-blog/teaching-directions/{name}'
    learners = [
        ('國小','Elementary school','以觀察、描述、故事與查證入門，搭配教師示範與紙本活動。','Begin with observation, description, stories and fact-checking through teacher demonstrations and paper-based activities.'),
        ('國中','Junior high school','從修改範本與小組任務，練習流程設計、測試與說明理由。','Modify templates and work in groups to practice workflow design, testing and explaining decisions.'),
        ('高中','Senior high school','以資料探究與互動專題練習整合，保留來源、測試與修訂紀錄。','Integrate data inquiry and interactive projects, retaining sources, tests and revision records.'),
        ('大學','University','結合學科問題與跨域專題，依資訊或非資訊背景調整實作深度。','Connect disciplinary questions with interdisciplinary projects, adapting technical depth to prior experience.'),
        ('研究生','Graduate study','聚焦文獻、研究工作流與結果查核；方法選擇及學術倫理由研究者負責。','Focus on literature, research workflows and result verification, with researchers responsible for methods and academic integrity.'),
        ('成人','Adult learning','從工作或生活任務開始，依數位經驗、設備與使用目的安排練習。','Start with work or everyday tasks, adjusting practice to digital experience, equipment and purpose.')]
    functions = [
        ('行政流程','Administration','表單、通知、任務追蹤與例行作業，先理解流程再評估自動化。','Forms, notifications, task tracking and routine operations: understand the workflow before automating.'),
        ('文書與資料整理','Documents and data','需求說明、摘要、報告架構與試算表整理，逐項核對來源和內容。','Task briefs, summaries, report outlines and spreadsheets, with checks against source material.'),
        ('多媒體與溝通','Multimedia and communication','圖文、腳本、影音與字幕，從表達目的到素材授權及人工校對。','Visual stories, scripts, video and subtitles, from communication goals to permissions and review.'),
        ('管理與協作','Management and collaboration','任務拆解、流程交接與查核責任，討論AI可以協助及不宜代決的環節。','Task decomposition, workflow handoffs and review responsibilities, including where AI should not make decisions.'),
        ('資訊應用與自動化','Applied computing and automation','網頁工具、Google Apps Script（GAS）、Google Sheets與LINE Bot，逐步理解資料流與限制。','Web tools, Google Apps Script (GAS), Google Sheets and LINE Bot, with attention to data flows and limitations.'),
        ('教學、研究與評量','Teaching, research and assessment','活動設計、學習提示、研究資料與評量規準，重視證據、適切性及人的判斷。','Activities, learning prompts, research data and assessment criteria, emphasizing evidence, suitability and human judgment.')]
    def cards(items):
        return ''.join(f'<article><h3>{t(a,b)}</h3><p>{t(c,d)}</p></article>' for a,b,c,d in items)
    body = f'''<main id="main"><section class="hero"><div><h1>{t('找到適合自己的AI學習方向','Find your AI learning direction')}</h1><p class="intro">{t('先看學習者與任務，再選工具。從白話理解、動手實作到查核修正，讓學習與真實問題連在一起。','Start with the learner and the task, then choose tools. Connect plain-language explanations, hands-on practice and critical review to real problems.')}</p><div class="actions"><a class="button" href="#materials">{t('閱讀既有教材','Explore existing materials')}</a><a href="#planning">{t('討論課程規劃','Discuss course planning')}</a></div></div><aside class="profile"><h2>{t('施育廷','Yu-Ting Shih (Andrew Shih)')}</h2><p>{t('國立臺中教育大學兼任講師、教育資訊與測驗統計研究所博士候選人。','Adjunct lecturer at National Taichung University of Education and doctoral candidate in Educational Information and Measurement.')}</p><p>{t('這裡呈現可討論的教學方向，不是已開班清單。課程需依年齡、先備能力與現場條件規劃。','These are directions for discussion, not a schedule of active courses. Plans depend on age, prior knowledge and local conditions.')}</p></aside></section>
<section id="learners"><h2>{t('依學習階段選擇起點','Choose a starting point by learning stage')}</h2><div class="topics">{cards(learners)}</div></section>
<section id="applications"><h2>{t('依工作與應用需求選題','Choose a practical application')}</h2><p>{t('同一個人可能同時有多種需求；可以先選一項最常遇到的任務，不必一次學會所有功能。','People often have several needs. Start with one recurring task rather than trying to learn every feature.')}</p><div class="topics">{cards(functions)}</div></section>
<section id="approach"><h2>{t('重視理解、實作與查核的學習方式','Learning through understanding, practice and review')}</h2><div class="topics">{cards([
('白話說明，逐步進入','Plain language, gradual progression','先用熟悉情境說明概念，再進入工具與操作；新手友善不代表不需要練習。','Explain concepts through familiar situations before using tools. Beginner-friendly learning still requires practice.'),
('做出作品，也說明過程','Create and explain','保留需求、測試與修訂過程，讓學習者能說明做了什麼、為何修改。','Keep requirements, tests and revisions so learners can explain what they did and why they changed it.'),
('把責任放進實作','Build responsibility into practice','在任務中練習來源查核、個資保護、授權與使用限制，不把AI輸出直接視為正確答案。','Practice source verification, privacy, permissions and usage limits; do not treat AI output as automatically correct.')])}</div></section>
<section id="materials"><h2>{t('可立即閱讀的既有教材','Existing materials to explore now')}</h2><p>{t('以下為已公開的教材與紀錄，不等同每個年齡或職能都有完整課程；教師仍需預覽並選擇適合片段。','These are published materials and records, not complete courses for every age or role. Educators should preview and select suitable content.')}</p><div class="actions"><a class="button" href="../ai-course-site/index{suffix}.html">{t('AI教學與實作教材','AI learning materials')}</a><a class="button" href="../linebot-course-site/index{suffix}.html">{t('LINE Bot與GAS教材','LINE Bot and GAS')}</a><a href="../talks/index{suffix}.html#cases">{t('演講與示範紀錄','Talks and demonstrations')}</a></div></section>
<section class="invitation" id="planning"><div><h2>{t('課程規劃與研習洽談','Course planning and workshops')}</h2><p>{t('從學習階段、工作任務與希望完成的作品開始，共同確認主題、時數、設備及教學形式。','Start with the learning stage, practical task and intended output, then agree on topics, duration, equipment and format.')}</p><a class="button" href="../talks/index{suffix}.html#invite">{t('提供需求，討論課程','Discuss your learning needs')}</a></div><div><h3>{t('規劃方向，不是既有班期','Proposed directions, not scheduled courses')}</h3><p>{t('學段與職能分類是課程設計參考，不表示均已實施或具有成效證據。工具帳號、年齡條件、學校規範與教材授權需於課前確認；英文頁供資訊閱讀，授課語言另行協議。','Stage and role categories guide course design; they do not imply completed delivery or measured effectiveness. Account eligibility, age requirements, school policies and material permissions must be checked before teaching. Delivery language is agreed separately.')}</p></div></section></main>'''
    schema = {'@context':'https://schema.org','@type':'WebPage','url':url,'name':title,'description':description,'inLanguage':'en' if en else 'zh-Hant','about':{'@type':'Person','@id':'https://andrewshih1210.github.io/my-blog/#person','name':'施育廷'},'dateModified':'2026-11-22'}
    html = f'''<!doctype html><html lang="{'en' if en else 'zh-Hant'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{description}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="zh-Hant" href="https://andrewshih1210.github.io/my-blog/teaching-directions/index.html"><link rel="alternate" hreflang="en" href="https://andrewshih1210.github.io/my-blog/teaching-directions/index_en.html"><meta property="og:title" content="{title}"><meta property="og:description" content="{description}"><meta property="og:url" content="{url}"><link rel="stylesheet" href="../talks/styles.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">{t('跳至主要內容','Skip to content')}</a>{body}<footer>{t('施育廷｜教學方向與課程規劃','Yu-Ting Shih | Learning directions and course planning')}</footer></body></html>'''
    (OUT / name).write_text(html, encoding='utf-8')
# Both language peers must exist before creating navigation.
for path in OUT.glob('*.html'):
    apply(path)
for en in (False, True):
    suffix = '_en' if en else ''
    label = 'Learning directions and course planning' if en else '教學方向與課程規劃'
    for folder in ['', 'talks/', 'ai-course-site/']:
        path = ROOT / folder / f'index{suffix}.html'
        html = path.read_text(encoding='utf-8')
        if 'id="directions-entry"' in html: continue
        href = ('../' if folder else '') + f'teaching-directions/index{suffix}.html'
        intro = 'Choose a starting point by learning stage or practical task. Explore published materials or discuss a tailored plan.' if en else '依學習階段或實際任務選擇起點，先閱讀公開教材，或討論適合的課程與研習安排。'
        box = f'<section id="directions-entry" class="block"><div class="wrap"><article class="panel"><h2>{label}</h2><p>{intro}</p><a class="button" href="{href}">{label} →</a></article></div></section>'
        html = html.replace('</main>',box+'\n</main>',1)
        path.write_text(html,encoding='utf-8')
    template=ROOT/'scripts/linebot-course-site-templates'/f'index{suffix}.html'
    # Only update sitemap entries for these newly published pages.
    sitemap=ROOT/'sitemap.xml'
    xml=sitemap.read_text(encoding='utf-8')
    url=f'https://andrewshih1210.github.io/my-blog/teaching-directions/index{suffix}.html'
    if url not in xml:
        xml=xml.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>2026-11-22</lastmod></url>\n</urlset>')
        sitemap.write_text(xml,encoding='utf-8')
