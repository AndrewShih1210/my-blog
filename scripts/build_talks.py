"""Build the two static invitation pages. Run with Python 3; no dependencies."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'talks'
BASE = 'https://andrewshih1210.github.io/my-blog/'
PLAYLIST = 'https://www.youtube.com/playlist?list=PL1BHO-AUVmwkRRU_LQlyGZXSHLCbKGA1q'
TEACHER = 'https://dct.ntcu.edu.tw/teacher/13'
# Titles and summaries are editorial topic descriptions, not outcome claims.
CASES = [
    ('2026-10-30', '鼎新數智MM會客室', 'Digiwin MM interview', 'AI內容策略', 'AI content strategy', '從AI內容規劃切入，討論內容策略與工作應用。', 'A discussion of AI content planning, strategy and workplace applications.', 'ALKqlyIntrI', 'https://www.digiknow.com.tw/knowledge/3103e77e7c774', '第一手來源：就享知平台上的作者演講文章（2026-11-02發布），另有作者履歷及影片紀錄；非獨立主辦方推薦或背書。', 'Primary source: the author’s lecture article on DigiKnow (published 2026-11-02), alongside the author’s CV and video record; not an independent host recommendation or endorsement.'),
    ('2026-10-28', '就享知', 'DigiKnow', '白話說AI，學習AI不焦慮', 'Understanding AI without the anxiety', '以日常工作為起點，介紹AI基本概念與提示需求的表達。', 'An introduction to AI concepts and expressing requests through everyday work tasks.', 'Mbg3CCZSvjc', 'https://www.digiknow.com.tw/activity/aabc6430061b4', '主辦方公開活動介紹：載明日期與受邀講者。', 'Independent host introduction: identifies the date and invited speaker.'),
    ('2026-06-30', '苗栗縣政府文化觀光局', 'Miaoli County Culture and Tourism Bureau', '旅宿生成式AI與顧客服務自動化應用', 'Generative AI and hospitality service automation', '聚焦旅宿情境中的生成式AI與顧客服務流程。', 'Generative AI and customer-service workflows in hospitality settings.', 'ctx8Pf-WaW4', '../certificates-site/items/item-089.jfif', '主辦單位活動海報（作者網站保存）。', 'Organizer poster, preserved on the author’s website.'),
    ('2026-06-02', '國立臺中教育大學', 'National Taichung University of Education', 'Gemini整合：文書行政、資料分析與學術研究', 'Gemini for administration, data analysis and research', '討論Gemini在文書處理、資料分析及研究工作中的應用。', 'Gemini applications in document work, data analysis and academic research.', 'HAh40P1S5q0', '../certificates-site/items/item-087.png', '作者保存之演講活動圖片。', 'Lecture event image preserved by the author.'),
    ('2026-06-01', '國立中央大學／國立臺中教育大學', 'National Central University / National Taichung University of Education', 'Codex與Gemma：打造筆電AI代理人', 'Codex and Gemma: a laptop AI agent', '以Codex與Gemma本地模型為主題，介紹筆電AI代理人與研究文獻工作。', 'An introduction to laptop AI agents and literature workflows using Codex and local Gemma models.', 'S6a8jfsJxXg', '../certificates-site/items/item-086.png', '圖片標示臺中教育大學；兩校資訊依作者履歷及本人確認，非圖片單獨佐證。', 'The image names NTCU. The two-university attribution is based on the author’s CV and confirmation, not the image alone.'),
    ('2026-04-16', '育達科技大學', 'Yu Da University of Science and Technology', '讓AI成為神隊友：教學現場的應用與創新', 'AI as a teaching teammate: classroom applications', '以教學現場為脈絡，介紹AI輔助教學的應用與創新方向。', 'AI-assisted teaching applications and innovation in classroom contexts.', 'x3QVjyZzlCg', '../certificates-site/items/item-078.jpg', '演講感謝狀（作者網站保存）；非成效評量。', 'Lecture appreciation certificate preserved by the author; not an evaluation of outcomes.'),
]


def build(en=False):
    def t(zh, english):
        return english if en else zh
    file = 'index_en.html' if en else 'index.html'
    title = t('台中AI講師施育廷｜企業內訓與教師研習', 'Yu-Ting Shih | AI Training for Organizations and Educators')
    description = t('施育廷Yu-Ting Shih（Andrew Shih）的演講與研習邀約頁：企業內訓、公部門行政與教師研習，附演講影片與來源說明。', 'Invite Yu-Ting Shih (Andrew Shih) for corporate AI training, public-sector workshops and teacher development. Explore lecture videos and clearly labeled sources.')
    nav = [('index', '首頁', 'Home'), ('sitemap', '網站導覽', 'Sitemap'), ('ai-course-site/index', 'AI教材', 'AI Resources'), ('linebot-course-site/index', 'LINE Bot教材', 'LINE Bot'), ('author-works/index', '研究成果', 'Research')]
    links = ''.join(f'<a href="../{path}{"_en" if en else ""}.html">{t(zh, english)}</a>' for path, zh, english in nav)
    links += f'<a href="{ "index.html" if en else "index_en.html"}" lang="{ "zh-Hant" if en else "en"}" hreflang="{ "zh-Hant" if en else "en"}">{ "繁體中文" if en else "English"}</a>'
    cards = []
    for date, hostzh, hosten, zh, eng, summaryzh, summaryen, video, source, notezh, noteen in CASES:
        heading = t(zh, eng)
        video_label = t('觀看YouTube影片', 'Watch on YouTube')
        video_note = ''
        if video == 'Mbg3CCZSvjc':
            video_label = t('觀看相關精華', 'Watch related highlights')
            video_note = t('作者頻道：白話看AI：從提示詞、Skill到Gemini工作實作［10分鐘精華］。2026-10-30上傳；為相關精華，未確認為10月28日完整錄影。', 'Author channel: AI in plain language, from prompts and Skills to Gemini workflows (10-minute highlights). Uploaded 2026-10-30; related highlights, not a verified full recording of the October 28 event.')
        elif video == 'ALKqlyIntrI':
            video_note = t('作者頻道：就享知｜10/30 MM會客室｜AI內容策略企業與創作者如何持續做出值得被搜尋的內容？2026-11-02上傳；活動日期為2026-10-30。', 'Author channel: DigiKnow | 10/30 MM interview | AI content strategy for businesses and creators. Uploaded 2026-11-02; the event date is 2026-10-30.')
        cards.append(f'''<article class="case">
<a class="thumbnail" href="https://www.youtube.com/watch?v={video}" aria-label="{escape(video_label + ': ' + heading)}"><img src="https://i.ytimg.com/vi/{video}/hqdefault.jpg" width="480" height="360" loading="lazy" decoding="async" alt=""><span>{video_label} ↗</span></a>
<div class="case-copy"><p class="date"><time datetime="{date}">{date}</time> · {escape(t(hostzh, hosten))}</p><h3>{escape(heading)}</h3><p>{escape(t(summaryzh, summaryen))}</p>{f'<p class="small">{escape(video_note)}</p>' if video_note else ''}<p class="source">{escape(t(notezh, noteen))} <a href="{escape(source)}">{t('查閱來源', 'View source')}</a></p></div></article>''')
    topics = [
        ('企業內訓', 'Corporate training', 'AI入門、內容規劃、文件與工作流程；從團隊實際任務討論適合的練習。', 'AI fundamentals, content planning, documents and workflows, with exercises discussed around team tasks.'),
        ('公部門與行政', 'Public-sector administration', '文書整理、資料分析與服務情境；討論資料保護及人工查核的必要環節。', 'Document preparation, data analysis and service scenarios, including data protection and human review.'),
        ('教師研習', 'Teacher development', 'AI輔助教學、研究文獻整理與本地代理人；依參與者經驗調整內容。', 'AI-assisted teaching, literature workflows and local agents, adapted to participants’ experience.'),
    ]
    topic_html = ''.join(f'<article><h3>{t(a,b)}</h3><p>{t(c,d)}</p></article>' for a,b,c,d in topics)
    faqs = [
        ('邀約時需要提供哪些資訊？', 'What should an invitation include?', '請提供單位、參與對象、人數概況、想處理的工作或教學問題、預計日期、地點或線上形式，以及設備與帳號限制。', 'Please include your organization, audience, approximate attendance, work or teaching needs, preferred dates, venue or online format, and device or account constraints.'),
        ('內容、時長與費用如何確認？', 'How are scope, duration and fees agreed?', '先以電子郵件討論需求，再確認主題、活動形式、時長、費用與可配合日期；本頁不提供固定報價或檔期承諾。', 'Scope, format, duration, fees and availability are discussed by email. This page does not promise a fixed price, session length or booking slot.'),
        ('需要準備什麼設備與資料？', 'What equipment and materials are needed?', '實作設備、網路、軟體與帳號需求依主題另行確認。請先使用公開或去識別化範例，不要寄送機密文件或可辨識個人的原始資料。', 'Device, network, software and account needs depend on the topic. Start with public or de-identified examples; do not email confidential documents or identifiable raw data.'),
        ('可以錄影或公開教材嗎？', 'May we record or publish materials?', '錄影、教材分享範圍及公開方式，請於活動前協議；既有影片不代表新邀約已取得相同授權。', 'Please agree on recording, material sharing and publication before the event. Existing public videos do not grant equivalent permissions for a new engagement.'),
    ]
    faq_html = ''.join(f'<details class="faq"><summary>{t(a,b)}</summary><p>{t(c,d)}</p></details>' for a,b,c,d in faqs)
    schema = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Person', '@id': BASE + '#person', 'name': '施育廷', 'alternateName': ['Yu-Ting Shih', 'Andrew Shih'], 'url': BASE, 'email': 'mailto:ytshih0121@gmail.com'},
        {'@type': 'WebPage', '@id': BASE + 'talks/' + file + '#webpage', 'url': BASE + 'talks/' + file, 'name': title, 'description': description, 'inLanguage': 'en' if en else 'zh-Hant', 'about': {'@id': BASE + '#person'}}
    ]}
    return f'''<!doctype html>
<html lang="{'en' if en else 'zh-Hant'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{escape(description)}">
<link rel="canonical" href="{BASE}talks/{file}"><link rel="alternate" hreflang="zh-Hant" href="{BASE}talks/index.html"><link rel="alternate" hreflang="en" href="{BASE}talks/index_en.html"><link rel="alternate" hreflang="x-default" href="{BASE}talks/index.html">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{BASE}talks/{file}">
<link rel="stylesheet" href="styles.css"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head>
<body><a class="skip" href="#main">{t('跳至主要內容', 'Skip to content')}</a>
<header><div class="header-inner"><a class="brand" href="../{'index_en.html' if en else 'index.html'}">{t('施育廷', 'Yu-Ting Shih')}<span>Andrew Shih</span></a><nav class="desktop-nav" aria-label="{t('主要導覽', 'Main navigation')}">{links}</nav><details class="mobile-nav"><summary>{t('選單 / 語言', 'Menu / Language')}</summary><nav aria-label="{t('行動版導覽', 'Mobile navigation')}">{links}</nav></details></div></header>
<main id="main"><section class="hero"><div><h1>{t('台中AI講師施育廷<span>企業內訓與教師研習</span>', 'AI training with Yu-Ting Shih<span>For organizations &amp; educators</span>')}</h1><p class="intro">{t('從實際工作與教學問題出發，討論AI可以怎麼用、哪些地方仍需要人的判斷。', 'Start with real work and teaching needs. Explore where AI can help, and where human judgment still matters.')}</p><div class="actions"><a class="button" href="#invite">{t('洽談演講與研習', 'Discuss an invitation')}</a><a class="text-link" href="#cases">{t('瀏覽演講紀錄', 'Explore lecture records')} ↓</a></div></div>
<aside class="profile" aria-label="{t('講者簡介', 'Speaker profile')}"><h2>施育廷<br><span>Yu-Ting Shih（Andrew Shih）</span></h2><p>{t('國立臺中教育大學兼任講師<br>教育資訊與測驗統計研究所博士候選人', 'Adjunct lecturer, National Taichung University of Education<br>Doctoral candidate, Graduate Institute of Educational Information and Measurement, NTCU')}</p><a href="{TEACHER}">{t('校方教師頁面', 'University faculty page')} ↗</a><p class="small">{t('校方頁面佐證兼任教師身分；博士候選人資訊依作者提供。', 'The faculty page supports the adjunct appointment; doctoral candidacy is author-provided.')}</p></aside></section>
<section aria-labelledby="topics"><div class="section-heading"><h2 id="topics">{t('可以討論的研習方向', 'Workshop directions')}</h2><p>{t('依對象與需求規劃，不以工具清單取代學習目標。', 'Plan around participants and learning needs, not just a list of tools.')}</p></div><div class="topics">{topic_html}</div></section>
<section aria-labelledby="cases"><div class="section-heading"><h2 id="cases">{t('精選演講與研習紀錄', 'Selected talks & workshops')}</h2><a href="{PLAYLIST}">{t('作者影片清單', 'Author’s video playlist')} ↗</a></div><p class="evidence">{t('以下區分主辦方公開介紹、作者演講紀錄及作者保存的活動圖片／感謝狀。列出單位名稱不表示推薦、合作背書或成效保證；影片為演講相關紀錄，不列入單純參與活動或研究計畫。', 'Sources distinguish independent host introductions, author lecture records, and preserved event images or appreciation certificates. Organization names do not imply recommendation, endorsement or guaranteed outcomes. These are lecture-related records, not attendance-only activities or research projects.')}</p><div class="cases">{''.join(cards)}</div></section>
<section class="invitation" aria-labelledby="invite"><div><h2 id="invite">{t('邀請施育廷', 'Invite Yu-Ting Shih')}</h2><p>{t('企業內訓、公部門行政應用、教師研習，歡迎先來信說明需求。', 'For corporate training, public administration or teacher workshops, start by emailing your needs.')}</p><a class="button" href="mailto:ytshih0121@gmail.com">ytshih0121@gmail.com</a></div><div><h3>{t('邀約前常見問題', 'Practical questions')}</h3>{faq_html}</div></section></main>
<footer><p>{t('施育廷Yu-Ting Shih（Andrew Shih）｜演講與研習邀約', 'Yu-Ting Shih (Andrew Shih) | Talks & workshop invitations')}</p><p>{t('摘要為依主題撰寫的簡介，非逐字稿或學習成效證據。', 'Summaries describe topics; they are not transcripts or evidence of learning outcomes.')}</p></footer></body></html>
'''


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for english in (False, True):
        target = OUT / ('index_en.html' if english else 'index.html')
        target.write_text(build(english), encoding='utf-8')
        print(target)
