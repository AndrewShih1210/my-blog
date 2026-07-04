from __future__ import annotations

from pathlib import Path
from textwrap import dedent


ROOT = Path(r"C:\Users\sweet\OneDrive\Desktop\pd\REFERENCES_GITHUB\linebot-course-site")
BASE_URL = "https://andrewshih1210.github.io/my-blog/linebot-course-site/"


NAV = {
    "zh": [
        ("index.html", "首頁"),
        ("teaching-plan.html", "教學地圖"),
        ("setup.html", "建置流程"),
        ("apps-script.html", "GAS 與 Sheet"),
        ("workflows.html", "功能工作流"),
        ("advanced.html", "進階延伸"),
        ("resources.html", "資源彙整"),
        ("../index.html", "學術首頁"),
        ("../sitemap.html", "網站導覽"),
        ("index_en.html", "EN"),
    ],
    "en": [
        ("index_en.html", "Home"),
        ("teaching-plan_en.html", "Course Map"),
        ("setup_en.html", "Setup"),
        ("apps-script_en.html", "GAS and Sheets"),
        ("workflows_en.html", "Workflows"),
        ("advanced_en.html", "Advanced"),
        ("resources_en.html", "Resources"),
        ("../index_en.html", "Academic Home"),
        ("../sitemap_en.html", "Sitemap"),
        ("index.html", "中文"),
    ],
}


def meta_block(title: str, description: str, canonical: str, zh_href: str, en_href: str, lang: str, body_class: str = "") -> str:
    og_title = title.replace('"', "&quot;")
    desc = description.replace('"', "&quot;")
    body_attr = f' class="{body_class}"' if body_class else ""
    return dedent(
        f"""\
        <!doctype html>
        <html lang="{lang}">
        <head>
          <meta charset="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <meta name="description" content="{desc}" />
          <meta name="author" content="施育廷" />
          <meta name="robots" content="index,follow,max-image-preview:large" />
          <link rel="canonical" href="{canonical}" />
          <link rel="alternate" hreflang="zh-Hant" href="{zh_href}" />
          <link rel="alternate" hreflang="en" href="{en_href}" />
          <meta property="og:type" content="website" />
          <meta property="og:title" content="{og_title}" />
          <meta property="og:description" content="{desc}" />
          <meta property="og:url" content="{canonical}" />
          <meta property="og:image" content="{BASE_URL}assets/figures/line-cloud-manager-map.png" />
          <meta name="twitter:card" content="summary_large_image" />
          <title>{title}</title>
          <link rel="stylesheet" href="styles.css" />
        </head>
        <body{body_attr}>
        """
    )


def render_nav(lang: str) -> str:
    brand = "LINE Bot x GAS 教學網站" if lang == "zh" else "LINE Bot x GAS Teaching Site"
    links = "\n".join([f'        <a href="{href}">{label}</a>' for href, label in NAV[lang]])
    return dedent(
        f"""\
          <header class="site-header">
            <div class="wrap topbar">
              <a class="brand" href="{'index.html' if lang == 'zh' else 'index_en.html'}">{brand}</a>
              <nav class="nav">
        {links}
              </nav>
            </div>
          </header>
        """
    )


def footer(lang: str) -> str:
    text = (
        "本教材由施育廷整理製作，內容整合 LINE Bot、Google Apps Script、Google Sheets 與生成式 AI 教學素材，並以可公開瀏覽的教學網站形式呈現。"
        if lang == "zh"
        else "This site was curated by Yu-Ting Shih and consolidates teaching materials on LINE Bot, Google Apps Script, Google Sheets, and generative AI into a public-facing instructional website."
    )
    home_label = "學術首頁" if lang == "zh" else "Academic Home"
    cert_label = "證照與證明" if lang == "zh" else "Credentials"
    sitemap_label = "網站導覽" if lang == "zh" else "Sitemap"
    home_href = "../index.html" if lang == "zh" else "../index_en.html"
    cert_href = "../certificates-site/index.html" if lang == "zh" else "../certificates-site/index_en.html"
    sitemap_href = "../sitemap.html" if lang == "zh" else "../sitemap_en.html"
    return dedent(
        f"""\
          <footer class="site-footer">
            <div class="wrap footer-grid">
              <article class="panel">
                <p class="section-label">Author</p>
                <h3>施育廷 / Yu-Ting Shih</h3>
                <p class="muted">{text}</p>
              </article>
              <article class="panel">
                <p class="section-label">Links</p>
                <div class="cta-row">
                  <a class="button primary" href="{home_href}">{home_label}</a>
                  <a class="button" href="{cert_href}">{cert_label}</a>
                  <a class="button" href="{sitemap_href}">{sitemap_label}</a>
                </div>
              </article>
            </div>
          </footer>
        </body>
        </html>
        """
    )


def wrap_page(lang: str, title: str, description: str, filename: str, alt_filename: str, content: str, body_class: str = "") -> str:
    canonical = BASE_URL + filename
    zh_filename = filename if lang == "zh" else alt_filename
    en_filename = filename if lang == "en" else alt_filename
    return meta_block(title, description, canonical, BASE_URL + zh_filename, BASE_URL + en_filename, "zh-Hant" if lang == "zh" else "en", body_class) + render_nav(lang) + content + footer(lang)


HOME_ZH = dedent(
    """\
      <section class="hero">
        <div class="wrap hero-grid">
          <article class="panel callout">
            <p class="eyebrow">LINE Bot Course</p>
            <h1>LINE Bot、Google Apps Script 與 Google Sheets 完整教學網站</h1>
            <p class="lead">這套教材以施育廷的教學與實作脈絡為基礎，聚焦 LINE 官方帳號、Webhook、Google Apps Script、Google 試算表、Google Drive 與 Gemini 協作工作流，整理成可直接授課、研習或自主學習使用的中英文教材網站。</p>
            <div class="tag-row">
              <span class="tag">LINE Messaging API</span>
              <span class="tag">Google Apps Script</span>
              <span class="tag">Google Sheets</span>
              <span class="tag">Google Drive</span>
              <span class="tag">Gemini</span>
            </div>
            <div class="hero-actions">
              <a class="button primary" href="teaching-plan.html">查看教學地圖</a>
              <a class="button" href="setup.html">開始建置</a>
              <a class="button" href="resources.html">教材資源</a>
            </div>
          </article>
          <aside class="panel hero-visual">
            <img src="assets/figures/line-cloud-manager-map.png" alt="LINE 雲端助理架構圖" />
            <div class="summary-box" style="margin-top:18px;">
              <h3>公開課程與延伸入口</h3>
              <div class="cta-row">
                <a class="button primary" href="https://sites.google.com/view/genai-mcp/index">教材網站來源頁</a>
                <a class="button" href="https://www.youtube.com/playlist?list=PL1BHO-AUVmwnWQg8Y55MRjoiQ8wBUBScJ">YouTube 播放清單</a>
                <a class="button" href="https://moocs.moe.edu.tw/moocs/#/course/detail/10002657">教育部磨課師課程</a>
                <a class="button" href="https://www.youtube.com/@ytshihclassworld">施育廷 YouTube 頻道</a>
              </div>
            </div>
          </aside>
        </div>
      </section>
      <main class="wrap main-stack">
        <section class="section" id="overview">
          <div class="section-head">
            <div>
              <p class="section-label">Overview</p>
              <h2>這套教材教什麼</h2>
            </div>
            <p class="section-text">不是只教按步驟操作，而是把系統建置、資料流、對話理解、檔案管理與 AI 擴充整合成一套可教、可做、可維護的實作課程。</p>
          </div>
          <div class="path-grid">
            <article class="path-card">
              <span>01</span>
              <h3>完成基本建置</h3>
              <p>建立 LINE Channel、Google Sheet、Google Drive 與 Apps Script 的最小可運作架構。</p>
            </article>
            <article class="path-card">
              <span>02</span>
              <h3>理解後端邏輯</h3>
              <p>看懂 Webhook、事件解析、Router、Prompt 與工作表記錄的關係。</p>
            </article>
            <article class="path-card">
              <span>03</span>
              <h3>做出實用工作流</h3>
              <p>讓 Bot 能處理檔案上傳、摘要、問答、報告生成與資訊查詢。</p>
            </article>
            <article class="path-card">
              <span>04</span>
              <h3>延伸成研究或行政系統</h3>
              <p>加入多來源資料整合、背景排程、對話式代理人與專利導向架構思維。</p>
            </article>
          </div>
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <p class="section-label">Roadmap</p>
              <h2>教材原始流程對照</h2>
            </div>
            <p class="section-text">以下章節順序直接對應原始教材文件的 Part.1 主結構，優先維持教材敘事與授課邏輯一致。</p>
          </div>
          <div class="unit-grid">
            <a class="unit-card" href="teaching-plan.html"><strong>1. 總覽</strong><p>先理解這套 LINE 智慧助理能做什麼，以及它對教學與工作流程的價值。</p></a>
            <a class="unit-card" href="apps-script.html"><strong>2. 系統架構</strong><p>對照耳朵、大腦、記憶庫、檔案櫃與中樞神經，理解整體元件關係。</p></a>
            <a class="unit-card" href="setup.html"><strong>3. 首次設定</strong><p>依照教材順序完成 Sheet、Drive、Apps Script、API Key 與 Webhook 部署。</p></a>
            <a class="unit-card" href="apps-script.html#logs"><strong>4. 管理員功能</strong><p>理解管理員工具、圖文選單與維運入口如何放進 Google Sheet。</p></a>
            <a class="unit-card" href="workflows.html"><strong>5. 核心功能詳解</strong><p>對應檔案問答、報告生成、Threads、搜尋與其他實用工具。</p></a>
            <a class="unit-card" href="resources.html"><strong>附錄：API 工具與延伸資源</strong><p>集中查看官方文件、公開課程、播放清單與後續實作清單。</p></a>
          </div>
        </section>

        <section class="section two-col">
          <article class="panel">
            <p class="section-label">Key Figure</p>
            <h2>系統教學不是只有程式碼</h2>
            <p class="section-text">本網站同步保留了教材中的圖像說明，包含 APIKEY 工作表、雲端資料夾、LINE 雲端助理總圖、Webhook 說明頁與操作截圖。這樣的設計能同時支援初學者、授課者與維運者。</p>
            <div class="figure-grid">
              <article class="figure-card panel">
                <img src="assets/figures/apikey-sheet.png" alt="APIKEY 工作表示意圖" />
                <p>用 Google Sheet 管理金鑰、工作表與記錄欄位。</p>
              </article>
              <article class="figure-card panel">
                <img src="assets/figures/drive-folder.png" alt="Google Drive 資料夾示意圖" />
                <p>將 Google Drive 視為檔案庫與報告輸出空間。</p>
              </article>
            </div>
          </article>
          <article class="panel">
            <p class="section-label">Patent-Informed Extension</p>
            <h2>視需求加入專利導向架構</h2>
            <p class="section-text">若課程需要從教材進一步走向研究、專題或產品化，本網站納入 <code>LINEBOT_專利</code> 圖像作為進階補充，協助學習者理解多來源資訊整合、對話路由、資料層與交付輸出的整體關係。</p>
            <img src="assets/figures/patent-system-overview.png" alt="專利系統架構總覽" />
          </article>
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <p class="section-label">Source Basis</p>
              <h2>教材整理依據</h2>
            </div>
            <p class="section-text">內容主要來自教材文件、投影片型 PDF 與專利圖像，而非單純摘要，因此頁面中的章節與案例可以直接作為授課內容。</p>
          </div>
          <div class="roadmap">
            <a href="resources.html#sources">教材https.docx：系統總覽、設定步驟、核心功能、API 工具</a>
            <a href="resources.html#sources">互動機器人專題應用.pdf：課程大綱、Webhook 與 GAS 教學脈絡</a>
            <a href="resources.html#sources">LINEBOT_磨課師.pdf：磨課師導向的簡報素材</a>
            <a href="advanced.html#patent">LINEBOT_專利：系統架構、流程圖與雲端服務對應圖</a>
          </div>
        </section>
      </main>
    """
)


HOME_EN = dedent(
    """\
      <section class="hero">
        <div class="wrap hero-grid">
          <article class="panel callout">
            <p class="eyebrow">Bilingual Course Site</p>
            <h1>LINE Bot, Google Apps Script, and Google Sheets Teaching Website</h1>
            <p class="lead">This bilingual site turns Yu-Ting Shih's LINE Bot materials into a complete instructional website. It covers LINE official accounts, Webhooks, Google Apps Script, Google Sheets, Google Drive, and Gemini-enabled workflows for classroom teaching, workshops, and self-paced study.</p>
            <div class="tag-row">
              <span class="tag">LINE Messaging API</span>
              <span class="tag">Google Apps Script</span>
              <span class="tag">Google Sheets</span>
              <span class="tag">Google Drive</span>
              <span class="tag">Gemini</span>
            </div>
            <div class="hero-actions">
              <a class="button primary" href="teaching-plan_en.html">Course Map</a>
              <a class="button" href="setup_en.html">Setup Guide</a>
              <a class="button" href="resources_en.html">Resources</a>
            </div>
          </article>
          <aside class="panel hero-visual">
            <img src="assets/figures/line-cloud-manager-map.png" alt="LINE cloud assistant overview" />
            <div class="summary-box" style="margin-top:18px;">
              <h3>Public course and extension links</h3>
              <div class="cta-row">
                <a class="button primary" href="https://sites.google.com/view/genai-mcp/index">Source course site</a>
                <a class="button" href="https://www.youtube.com/playlist?list=PL1BHO-AUVmwnWQg8Y55MRjoiQ8wBUBScJ">YouTube playlist</a>
                <a class="button" href="https://moocs.moe.edu.tw/moocs/#/course/detail/10002657">MOE MOOC</a>
                <a class="button" href="https://www.youtube.com/@ytshihclassworld">YouTube channel</a>
              </div>
            </div>
          </aside>
        </div>
      </section>
      <main class="wrap main-stack">
        <section class="section">
          <div class="section-head">
            <div>
              <p class="section-label">Overview</p>
              <h2>What this site teaches</h2>
            </div>
            <p class="section-text">The goal is not to teach isolated clicks. The site explains how setup, data flow, conversational routing, file management, and AI extensions work together as a teachable and maintainable system.</p>
          </div>
          <div class="path-grid">
            <article class="path-card"><span>01</span><h3>Build the minimum system</h3><p>Set up a LINE channel, Google Sheet, Google Drive, and Apps Script web app.</p></article>
            <article class="path-card"><span>02</span><h3>Read the backend logic</h3><p>Understand events, routers, prompts, worksheets, and logging instead of treating the bot as a black box.</p></article>
            <article class="path-card"><span>03</span><h3>Create useful workflows</h3><p>Implement file upload, summarization, Q and A, report generation, and information lookup.</p></article>
            <article class="path-card"><span>04</span><h3>Extend toward projects</h3><p>Move from a classroom bot to research, administration, or product-oriented agent workflows.</p></article>
          </div>
        </section>

        <section class="section">
          <div class="section-head">
            <div>
              <p class="section-label">Site Map</p>
              <h2>Flow aligned with the original source document</h2>
            </div>
            <p class="section-text">The page order below follows the original Part 1 structure of the teaching document rather than a newly invented layout.</p>
          </div>
          <div class="unit-grid">
            <a class="unit-card" href="teaching-plan_en.html"><strong>1. Overview</strong><p>Explain what the LINE assistant can do and why the workflow matters.</p></a>
            <a class="unit-card" href="apps-script_en.html"><strong>2. System architecture</strong><p>Map the system to message intake, AI reasoning, memory, storage, and orchestration.</p></a>
            <a class="unit-card" href="setup_en.html"><strong>3. First-time setup</strong><p>Complete Sheet, Drive, Apps Script, API key, and Webhook setup in the original order.</p></a>
            <a class="unit-card" href="apps-script_en.html#logs"><strong>4. Admin functions</strong><p>Review admin tools, rich menu control, and maintenance entry points.</p></a>
            <a class="unit-card" href="workflows_en.html"><strong>5. Core functions</strong><p>Cover file Q and A, report generation, Threads posting, search, and practical commands.</p></a>
            <a class="unit-card" href="resources_en.html"><strong>Appendix: APIs and extension resources</strong><p>Collect official docs, public course links, playlists, and practice tasks.</p></a>
          </div>
        </section>

        <section class="section two-col">
          <article class="panel">
            <p class="section-label">Teaching Assets</p>
            <h2>Visual explanations matter</h2>
            <p class="section-text">This site preserves diagrams and screenshots from the original materials so learners can connect setup steps with actual interfaces and data structures.</p>
            <div class="figure-grid">
              <article class="figure-card panel">
                <img src="assets/figures/apikey-sheet.png" alt="API key worksheet" />
                <p>A worksheet can function as a memory layer, key registry, and workflow tracker.</p>
              </article>
              <article class="figure-card panel">
                <img src="assets/figures/drive-folder.png" alt="Google Drive folder" />
                <p>Google Drive serves as the file vault and output space for generated reports.</p>
              </article>
            </div>
          </article>
          <article class="panel">
            <p class="section-label">Research Extension</p>
            <h2>Patent-oriented diagrams are included when needed</h2>
            <p class="section-text">The site selectively incorporates figures from the <code>LINEBOT_專利</code> folder to show how a classroom bot can evolve into a multi-source conversational system with routing, data layers, and structured outputs.</p>
            <img src="assets/figures/patent-system-overview.png" alt="Patent system overview" />
          </article>
        </section>
      </main>
    """
)


PLAN_ZH = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index.html">首頁</a> / 教學地圖</p>
          <p class="eyebrow">Course Map</p>
          <h1>授課節次、學習任務與評量設計</h1>
          <p class="lead">本頁把教材整理成可授課的節次與任務結構，適合大學課程、教師研習、工作坊或自主學習安排。</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>本頁導覽</h3>
          <a href="#weeks">原始教材主流程</a>
          <a href="#variants">時數變形</a>
          <a href="#assessment">評量方式</a>
          <a href="#deliverables">學習產出</a>
        </aside>
        <article class="article">
          <section class="panel" id="weeks">
            <h2>依原始教材整理的主流程</h2>
            <div class="roadmap">
              <a href="teaching-plan.html">1. 總覽：先定義系統任務範圍，理解上傳、問答、報告、搜尋與個人助理功能。</a>
              <a href="apps-script.html">2. 系統架構：用 LINE Messaging API、Gemini、Sheets、Drive、外部 API 與 Apps Script 來對應系統部件。</a>
              <a href="setup.html">3. 首次設定：依教材步驟完成 Google Sheet、Drive、Apps Script、API Key、Google 服務與 Webhook 設定。</a>
              <a href="apps-script.html#logs">4. 管理員功能：回到工作表管理圖文選單與系統操作入口。</a>
              <a href="workflows.html">5. 核心功能詳解：檔案管理與智慧問答、專業報告生成、Threads 發文、資訊查詢與其他工具。</a>
              <a href="resources.html">附錄：使用的主要 API 工具，並延伸到官方文件、播放清單與磨課師入口。</a>
            </div>
          </section>
          <section class="panel">
            <h2>教材第二部分與第三部分如何接續</h2>
            <p>原始教材在 Part.1 之後，進一步展開「與生成式 AI 的協作開發流程」與「專案功能演進全紀錄」。因此課堂若不是只教使用，而是要教開發與專題，建議在完成上述五個主流程後，再延伸到需求釐清、Prompt 設計、API 串接、除錯迭代與版本演進。</p>
          </section>
          <section class="panel" id="variants">
            <h2>不同時數的教學變形</h2>
            <div class="unit-grid">
              <article class="unit-card"><strong>3 小時工作坊</strong><p>聚焦帳號建立、Webhook 驗證、最小回覆測試與示範型工作流。</p></article>
              <article class="unit-card"><strong>6 小時實作班</strong><p>完成 Sheet、Drive、GAS、LINE 串接，並帶入檔案問答與報告生成。</p></article>
              <article class="unit-card"><strong>一學期課程</strong><p>在基礎建置上加入 Prompt 設計、資料治理、維運日誌與專題成果。</p></article>
              <article class="unit-card"><strong>教師研習</strong><p>強調課堂應用、行政文件流程、學生專題與可移植的授課範本。</p></article>
            </div>
          </section>
          <section class="panel rubric" id="assessment">
            <h2>評量方式</h2>
            <table>
              <thead>
                <tr><th>評量面向</th><th>重點</th></tr>
              </thead>
              <tbody>
                <tr><td>系統建置</td><td>是否能完成 LINE、GAS、Sheets 與 Drive 的基本串接。</td></tr>
                <tr><td>流程理解</td><td>是否能說明事件如何被接收、解析、路由與記錄。</td></tr>
                <tr><td>功能實作</td><td>是否完成至少一個可重現的工作流，例如摘要、問答或自動發文。</td></tr>
                <tr><td>教學表達</td><td>是否能用圖文或口頭方式清楚說明系統架構與操作步驟。</td></tr>
              </tbody>
            </table>
          </section>
          <section class="panel" id="deliverables">
            <h2>建議學習產出</h2>
            <ul class="clean-list">
              <li>一個可成功驗證 Webhook 的 LINE Bot。</li>
              <li>一份包含 APIKEY、日誌、筆記與工作欄位的 Google Sheet。</li>
              <li>至少一個完整流程說明：上傳檔案、摘要、提問、生成報告或貼文。</li>
              <li>一份簡報或網站頁面，能向他人說明系統設計與應用價值。</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


PLAN_EN = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index_en.html">Home</a> / Course Map</p>
          <p class="eyebrow">Course Map</p>
          <h1>Delivery sequence, tasks, and assessment design</h1>
          <p class="lead">This page turns the source materials into a teachable sequence suitable for university classes, faculty workshops, and self-paced learning.</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>On this page</h3>
          <a href="#weeks">Source-aligned flow</a>
          <a href="#variants">Pacing variants</a>
          <a href="#assessment">Assessment</a>
          <a href="#deliverables">Deliverables</a>
        </aside>
        <article class="article">
          <section class="panel" id="weeks">
            <h2>Main flow aligned to the original teaching document</h2>
            <div class="roadmap">
              <a href="teaching-plan_en.html">1. Overview: define the task scope and explain uploads, Q and A, reports, search, and assistant functions.</a>
              <a href="apps-script_en.html">2. System architecture: map LINE Messaging API, Gemini, Sheets, Drive, external APIs, and Apps Script to system roles.</a>
              <a href="setup_en.html">3. First-time setup: complete Google Sheet, Drive, Apps Script, API key, Google service, and Webhook configuration in the original sequence.</a>
              <a href="apps-script_en.html#logs">4. Admin functions: return to the spreadsheet and manage rich menus and operational controls.</a>
              <a href="workflows_en.html">5. Core functions: file management, Q and A, report generation, Threads posting, search, and utility tools.</a>
              <a href="resources_en.html">Appendix: primary APIs, official docs, playlists, and MOOC entry points.</a>
            </div>
          </section>
          <section class="panel">
            <h2>How Parts 2 and 3 continue the course</h2>
            <p>After Part 1, the original document moves into collaborative development with generative AI and a version-by-version feature evolution log. For a development-oriented course, those sections should follow the five-part usage flow above.</p>
          </section>
          <section class="panel" id="variants">
            <h2>Delivery variants by available time</h2>
            <div class="unit-grid">
              <article class="unit-card"><strong>3-hour workshop</strong><p>Focus on account setup, Webhook verification, minimum reply testing, and live demos.</p></article>
              <article class="unit-card"><strong>6-hour hands-on class</strong><p>Complete Sheets, Drive, GAS, LINE integration, and one AI-enhanced workflow.</p></article>
              <article class="unit-card"><strong>Semester course</strong><p>Add prompt design, governance, logs, and project-based extension.</p></article>
              <article class="unit-card"><strong>Faculty development</strong><p>Emphasize teaching transfer, administrative use, and reusable instructional templates.</p></article>
            </div>
          </section>
          <section class="panel rubric" id="assessment">
            <h2>Assessment dimensions</h2>
            <table>
              <thead>
                <tr><th>Dimension</th><th>Focus</th></tr>
              </thead>
              <tbody>
                <tr><td>System setup</td><td>Can the learner connect LINE, GAS, Sheets, and Drive successfully?</td></tr>
                <tr><td>Process understanding</td><td>Can the learner explain how events are received, parsed, routed, and logged?</td></tr>
                <tr><td>Workflow implementation</td><td>Can the learner build at least one reproducible workflow such as summarization or posting?</td></tr>
                <tr><td>Instructional explanation</td><td>Can the learner explain the design clearly through slides, docs, or a mini-site?</td></tr>
              </tbody>
            </table>
          </section>
          <section class="panel" id="deliverables">
            <h2>Suggested deliverables</h2>
            <ul class="clean-list">
              <li>A LINE Bot that passes Webhook verification.</li>
              <li>A Google Sheet with API keys, logs, notes, and workflow-related tabs.</li>
              <li>At least one complete workflow description such as upload to summary to report.</li>
              <li>A presentation or site page explaining the system design and use case.</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


SETUP_ZH = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index.html">首頁</a> / 建置流程</p>
          <p class="eyebrow">Setup</p>
          <h1>從零開始完成 LINE Bot 建置</h1>
          <p class="lead">本頁按照教材原始脈絡，整理出一條能實際成功部署的路徑：先準備資料層，再建置程式層，最後完成 LINE Webhook 驗證。</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>步驟導覽</h3>
          <a href="#prereq">先備條件</a>
          <a href="#sheet">Google Sheet</a>
          <a href="#drive">Google Drive</a>
          <a href="#line">LINE Developers</a>
          <a href="#deploy">Apps Script 部署</a>
          <a href="#verify">Webhook 驗證</a>
        </aside>
        <article class="article">
          <section class="panel" id="prereq">
            <h2>先備條件</h2>
            <ul class="clean-list">
              <li>一個可登入 LINE Developers 的 LINE 帳號。</li>
              <li>一個可使用 Google Sheets、Drive 與 Apps Script 的 Google 帳號。</li>
              <li>至少一組 Gemini API Key，若需要發佈到 Threads，還需 Threads 與 Cloudinary 金鑰。</li>
              <li>明確規劃好資料夾與工作表命名，避免後續維護混亂。</li>
            </ul>
          </section>
          <section class="panel figure-card" id="sheet">
            <h2>步驟 1：建立 Google Sheet 作為記憶庫</h2>
            <img src="assets/figures/apikey-sheet.png" alt="APIKEY 工作表畫面" />
            <p>教材將 Google Sheet 視為長期記憶層。至少應建立 <code>APIKEY</code>、日誌、筆記、檔案紀錄與暫存相關分頁。所有金鑰、操作紀錄與部分快取資料都會在這裡管理。</p>
            <ul class="clean-list">
              <li>命名試算表，例如「LINE 智慧助理資料庫」。</li>
              <li>建立 APIKEY 分頁，依既定欄位放入 Gemini、LINE、Threads、Cloudinary 等金鑰。</li>
              <li>建立操作日誌與檔案日誌工作表，支援追蹤使用歷程。</li>
            </ul>
          </section>
          <section class="panel figure-card" id="drive">
            <h2>步驟 2：建立 Google Drive 檔案庫</h2>
            <img src="assets/figures/drive-folder.png" alt="Google Drive 資料夾畫面" />
            <p>Google Drive 負責保存從 LINE 上傳的圖片、影片、文件，以及 AI 生成的 Google 文件、簡報或網頁報告。請先建立專用資料夾並保留資料夾 ID。</p>
          </section>
          <section class="panel" id="line">
            <h2>步驟 3：建立 LINE Channel</h2>
            <p>前往 LINE Developers Console 建立 Messaging API Channel，記錄 <code>Channel secret</code> 與 <code>Channel access token</code>。這兩項是系統接收事件與回傳訊息的入口憑證。</p>
            <ul class="clean-list">
              <li>建立 Provider 與 Channel。</li>
              <li>進入 Messaging API 分頁取得 Access Token。</li>
              <li>確認 Use webhook 後續可以被啟用。</li>
            </ul>
          </section>
          <section class="panel figure-card" id="deploy">
            <h2>步驟 4：部署 Google Apps Script 網頁應用程式</h2>
            <img src="assets/figures/webhook-basics.png" alt="Webhook 原理與 Line Bot 建置頁面" />
            <p>回到試算表後，從「擴充功能 &gt; Apps Script」建立專案，貼入核心程式，填入試算表 ID、資料夾 ID、API Key 讀取位置與模型設定，最後部署為網頁應用程式。</p>
            <ul class="clean-list">
              <li>執行身分選擇「我」。</li>
              <li>存取權限選擇「任何人」。</li>
              <li>完成授權後複製網頁應用程式網址，這就是 Webhook URL 的基礎。</li>
            </ul>
          </section>
          <section class="panel" id="verify">
            <h2>步驟 5：設定與驗證 Webhook</h2>
            <p>把部署得到的網址貼到 LINE Developers 的 Webhook URL 欄位，更新後執行 Verify。若驗證成功，表示 LINE 可以把事件送到你的 Apps Script。接著關閉干擾性的 Auto-reply messages，保留 Bot 主控權。</p>
            <div class="summary-box">
              <h3>最小成功指標</h3>
              <ul class="clean-list">
                <li>Webhook Verify 成功。</li>
                <li>從 LINE 傳訊後，Apps Script 有收到事件。</li>
                <li>試算表中出現至少一筆日誌或測試紀錄。</li>
              </ul>
            </div>
          </section>
        </article>
      </main>
    """
)


SETUP_EN = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index_en.html">Home</a> / Setup</p>
          <p class="eyebrow">Setup</p>
          <h1>Build the LINE Bot from scratch</h1>
          <p class="lead">This page follows the original teaching logic: prepare the data layer first, then the script layer, and finally complete LINE Webhook verification.</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>Steps</h3>
          <a href="#prereq">Prerequisites</a>
          <a href="#sheet">Google Sheet</a>
          <a href="#drive">Google Drive</a>
          <a href="#line">LINE Developers</a>
          <a href="#deploy">Apps Script deployment</a>
          <a href="#verify">Webhook verification</a>
        </aside>
        <article class="article">
          <section class="panel" id="prereq">
            <h2>Prerequisites</h2>
            <ul class="clean-list">
              <li>A LINE account that can access LINE Developers.</li>
              <li>A Google account with access to Sheets, Drive, and Apps Script.</li>
              <li>At least one Gemini API key. Threads and Cloudinary keys are needed if posting workflows are enabled.</li>
              <li>A clean naming plan for folders and worksheets so maintenance stays manageable.</li>
            </ul>
          </section>
          <section class="panel figure-card" id="sheet">
            <h2>Step 1: Build Google Sheet as the memory layer</h2>
            <img src="assets/figures/apikey-sheet.png" alt="API key worksheet" />
            <p>The teaching materials treat Google Sheet as a durable memory layer. At minimum, prepare tabs for <code>APIKEY</code>, logs, notes, uploaded files, and temporary workflow data.</p>
          </section>
          <section class="panel figure-card" id="drive">
            <h2>Step 2: Create the Google Drive storage folder</h2>
            <img src="assets/figures/drive-folder.png" alt="Google Drive folder" />
            <p>Google Drive stores uploaded images, videos, and documents from LINE, as well as generated Docs, Slides, and report files. Keep the folder ID ready for configuration.</p>
          </section>
          <section class="panel" id="line">
            <h2>Step 3: Create the LINE Channel</h2>
            <p>In LINE Developers Console, create a Messaging API Channel and record the <code>Channel secret</code> and <code>Channel access token</code>. These values enable event intake and message delivery.</p>
          </section>
          <section class="panel figure-card" id="deploy">
            <h2>Step 4: Deploy Apps Script as a web app</h2>
            <img src="assets/figures/webhook-basics.png" alt="Webhook basics slide" />
            <p>Open Apps Script from the spreadsheet, paste the core code, bind the spreadsheet ID, folder ID, key locations, and model settings, then deploy the project as a web app.</p>
          </section>
          <section class="panel" id="verify">
            <h2>Step 5: Set and verify the Webhook</h2>
            <p>Paste the deployed web app URL into the LINE Webhook URL field and run Verify. If verification succeeds, LINE can deliver events to Apps Script. Disable built-in auto replies so your bot keeps control.</p>
            <div class="summary-box">
              <h3>Minimum success criteria</h3>
              <ul class="clean-list">
                <li>Webhook verification succeeds.</li>
                <li>An event reaches Apps Script when a message is sent.</li>
                <li>A log or test record appears in the spreadsheet.</li>
              </ul>
            </div>
          </section>
        </article>
      </main>
    """
)


APPS_ZH = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index.html">首頁</a> / GAS 與 Sheet</p>
          <p class="eyebrow">Google Apps Script</p>
          <h1>看懂後端控制核心與工作表結構</h1>
          <p class="lead">LINE Bot 能穩定運作，不是因為單一 API 很強，而是因為 Apps Script 把事件處理、資料存取、記錄與 AI 呼叫串成了可維護的流程。</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>本頁導覽</h3>
          <a href="#roles">角色分工</a>
          <a href="#route">事件路由</a>
          <a href="#sheets">工作表結構</a>
          <a href="#prompt">Prompt 與意圖分析</a>
          <a href="#logs">日誌與管理</a>
        </aside>
        <article class="article">
          <section class="panel figure-card" id="roles">
            <h2>Apps Script 的角色分工</h2>
            <img src="assets/figures/line-cloud-manager-map.png" alt="LINE 雲端助理三段式架構圖" />
            <p>教材把整個系統視為一個多模組機器人：LINE Messaging API 負責耳朵與嘴巴，Gemini 負責意圖判斷與內容生成，Google Sheets 扮演記憶庫，Drive 是檔案櫃，而 Apps Script 則是中樞神經。</p>
          </section>
          <section class="panel" id="route">
            <h2>事件路由的基本思路</h2>
            <p>當 LINE 傳來事件時，後端通常會經過以下順序：接收事件、判斷訊息型態、讀取使用者狀態、決定要走哪一條功能路線、呼叫對應服務、回寫日誌，最後再回覆訊息或主動推播結果。</p>
            <div class="summary-box">
              <h3>推薦的教學拆解順序</h3>
              <ul class="clean-list">
                <li><code>doPost</code>：接收 Webhook。</li>
                <li>Parser：把文字、圖片、位置等事件整理成可處理資料。</li>
                <li>Router：根據指令與狀態決定功能模組。</li>
                <li>Service：執行 Drive、Sheets、Gemini、Threads 等子任務。</li>
                <li>Logger：把輸入、輸出與例外寫回工作表。</li>
              </ul>
            </div>
          </section>
          <section class="panel" id="sheets">
            <h2>工作表不是附件，而是資料層</h2>
            <p>本教材特別適合把 Google Sheet 當成資料結構教學材料。APIKEY 分頁管理金鑰，檔案日誌分頁保存上傳紀錄，筆記分頁承接短文與備忘，另外還可建立暫存狀態工作表，追蹤使用者目前是否正在進行報告生成、Threads 組圖或其他流程。</p>
            <ul class="clean-list">
              <li>工作表能降低非程式背景學員對資料庫的門檻。</li>
              <li>欄位結構可直接對應系統狀態、權限與操作紀錄。</li>
              <li>也因此更需要教學者強調命名一致與欄位維護紀律。</li>
            </ul>
          </section>
          <section class="panel" id="prompt">
            <h2>Prompt 與意圖分析</h2>
            <p>教材中的一個重點不是「叫 AI 亂生成」，而是讓 AI 扮演具體角色。後端 Prompt 應明確定義：系統是 LINE 助理、有哪些可執行任務、該如何抽取參數、何時要要求補充資訊、何時只能回傳結構化結果而不能自行猜測。</p>
            <p>這種設計能讓學生理解：真正可維運的 AI 系統，關鍵在於規則與邊界，而不是只靠模型能力本身。</p>
          </section>
          <section class="panel" id="logs">
            <h2>日誌、管理員選單與維運</h2>
            <p>教學文件提到可透過 Google Sheet 的管理員選單建立圖文選單、解除選單或管理聊天室功能。這表示系統不只是一次性的範例，而是可被持續維運的服務。對課堂來說，這正好能延伸到「如何讓作品可被他人接手」的工程思維。</p>
          </section>
        </article>
      </main>
    """
)


APPS_EN = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index_en.html">Home</a> / GAS and Sheets</p>
          <p class="eyebrow">Google Apps Script</p>
          <h1>Understand the controller layer and worksheet structure</h1>
          <p class="lead">A stable LINE Bot does not come from one powerful API. It comes from Apps Script orchestrating event handling, storage, logging, and AI calls into a maintainable system.</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>On this page</h3>
          <a href="#roles">System roles</a>
          <a href="#route">Routing</a>
          <a href="#sheets">Worksheets</a>
          <a href="#prompt">Prompts and intent parsing</a>
          <a href="#logs">Logs and administration</a>
        </aside>
        <article class="article">
          <section class="panel figure-card" id="roles">
            <h2>Role of Apps Script</h2>
            <img src="assets/figures/line-cloud-manager-map.png" alt="LINE cloud manager overview" />
            <p>The materials frame the system as a multi-module assistant: LINE handles message intake and delivery, Gemini handles interpretation and generation, Sheets provides memory, Drive stores files, and Apps Script coordinates everything.</p>
          </section>
          <section class="panel" id="route">
            <h2>How routing works</h2>
            <p>When LINE sends an event, the backend typically receives the payload, identifies the event type, reads user state, selects the target workflow, invokes the required services, records the result, and then replies or pushes a follow-up message.</p>
          </section>
          <section class="panel" id="sheets">
            <h2>Worksheets are part of the data architecture</h2>
            <p>Google Sheets is not just an attachment. In this course, it becomes a lightweight data layer: API keys, file logs, notes, state flags, and workflow traces are all structured there.</p>
          </section>
          <section class="panel" id="prompt">
            <h2>Prompts and intent extraction</h2>
            <p>The course emphasizes role-based prompting rather than generic text generation. A useful backend prompt should define tasks, constraints, required parameters, clarification behavior, and when structured output is required.</p>
          </section>
          <section class="panel" id="logs">
            <h2>Logs, admin menus, and maintenance</h2>
            <p>The original materials also discuss admin-side menu control inside Google Sheets. That turns the bot into a maintainable service, which is why this site treats engineering maintenance as part of the learning outcome.</p>
          </section>
        </article>
      </main>
    """
)


WORKFLOW_ZH = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index.html">首頁</a> / 功能工作流</p>
          <p class="eyebrow">Workflows</p>
          <h1>把 LINE 對話轉成可用的工作流</h1>
          <p class="lead">教材最有價值的地方，在於它不把 Bot 只當聊天工具，而是把對話視為一個工作入口，進而帶出檔案處理、報告生成、資訊查詢與跨平台發佈。</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>流程導覽</h3>
          <a href="#files">檔案處理</a>
          <a href="#reports">報告生成</a>
          <a href="#threads">Threads 發文</a>
          <a href="#search">搜尋與輔助功能</a>
          <a href="#teaching">教學活動</a>
        </aside>
        <article class="article">
          <section class="panel" id="files">
            <h2>流程 1：檔案上傳、命名、摘要與問答</h2>
            <p>使用者直接把圖片、影片、文件或表格丟進 LINE。系統接收後，把檔案存進 Drive，再由 AI 生成檔名、摘要與分類結果，並把這些資訊寫回 Google Sheet。之後學員可以再對同一份檔案提問，形成「上傳 - 建檔 - 查詢」閉環。</p>
          </section>
          <section class="panel" id="reports">
            <h2>流程 2：一鍵生成文件、簡報或網頁報告</h2>
            <p>當使用者輸入特定指令，例如為某份檔案產生分析報告，系統可進一步詢問輸出格式，接著在背景生成 Google 文件、簡報或網頁型報告。這個流程很適合用來教「任務拆解」與「非同步處理」。</p>
          </section>
          <section class="panel figure-card" id="threads">
            <h2>流程 3：從 LINE 直發 Threads</h2>
            <img src="assets/figures/threads-publish.png" alt="Threads 發文流程截圖" />
            <p>教材中展示了從 LINE 暫存貼文文字、補充多張圖片，再推送到 Threads 的設計。這使課程不只停留在教學 Bot，也能延伸到媒體發佈與行政工作流。</p>
          </section>
          <section class="panel" id="search">
            <h2>流程 4：搜尋、行事曆、Email、筆記與位置服務</h2>
            <p>除了 AI 摘要與問答，系統還可擴充為搜尋助手與個人工作流入口，例如查 Google、查 YouTube、記錄位置、建立行事曆、寄 Email、寫筆記。這一段很適合拿來討論「什麼叫做對話式介面整合多工具」。</p>
          </section>
          <section class="panel" id="teaching">
            <h2>可直接使用的教學活動</h2>
            <ul class="clean-list">
              <li>請學員畫出「一則 LINE 訊息」在系統內部走過哪些元件。</li>
              <li>請學員比較「檔案上傳摘要」與「直接純文字提問」在資料流上的差異。</li>
              <li>請學員設計一個新指令，並說明需要新增哪些工作表欄位與後端模組。</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


WORKFLOW_EN = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index_en.html">Home</a> / Workflows</p>
          <p class="eyebrow">Workflows</p>
          <h1>Turn LINE conversations into usable workflows</h1>
          <p class="lead">The strongest part of the source materials is that the bot is treated as a work entry point rather than a chat toy. Conversations trigger file handling, report generation, information search, and cross-platform posting.</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>Workflow map</h3>
          <a href="#files">File handling</a>
          <a href="#reports">Report generation</a>
          <a href="#threads">Threads publishing</a>
          <a href="#search">Search and utility tools</a>
          <a href="#teaching">Teaching uses</a>
        </aside>
        <article class="article">
          <section class="panel" id="files">
            <h2>Workflow 1: Upload, rename, summarize, and ask questions</h2>
            <p>Users send a file through LINE. The system stores it in Drive, uses AI to generate a filename, summary, and category, writes the metadata into Google Sheets, and then allows follow-up questions against the uploaded file.</p>
          </section>
          <section class="panel" id="reports">
            <h2>Workflow 2: Generate docs, slides, or web reports</h2>
            <p>When a user requests an analysis report, the system can ask for the output format and then create a Google Doc, Slides deck, or web-style report in the background. This is ideal for teaching task decomposition and asynchronous handling.</p>
          </section>
          <section class="panel figure-card" id="threads">
            <h2>Workflow 3: Post to Threads from LINE</h2>
            <img src="assets/figures/threads-publish.png" alt="Threads posting workflow" />
            <p>The materials include a workflow for staging text, appending images, and publishing to Threads. This expands the course beyond chatbots into content operations and digital communication pipelines.</p>
          </section>
          <section class="panel" id="search">
            <h2>Workflow 4: Search, calendar, email, notes, and location tools</h2>
            <p>In addition to AI summaries and Q and A, the system can act as a search assistant and personal workflow hub: Google search, YouTube lookup, location capture, calendar creation, email drafting, and note-taking.</p>
          </section>
          <section class="panel" id="teaching">
            <h2>Classroom activity ideas</h2>
            <ul class="clean-list">
              <li>Ask learners to diagram the internal path of one LINE message.</li>
              <li>Compare file-based Q and A with plain text prompting from a data-flow perspective.</li>
              <li>Design a new command and specify the worksheets and modules it would require.</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


ADVANCED_ZH = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index.html">首頁</a> / 進階延伸</p>
          <p class="eyebrow">Advanced</p>
          <h1>處理模型限制、外部文件與專利架構延伸</h1>
          <p class="lead">當專案不再只是課堂練習，而要走向可擴充系統時，真正的重點會轉向上下文管理、外部 API 整合、權限治理與架構抽象化。</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>本頁導覽</h3>
          <a href="#limits">模型限制</a>
          <a href="#docs">文件與網址上下文</a>
          <a href="#patent">專利延伸</a>
          <a href="#governance">治理與安全</a>
        </aside>
        <article class="article">
          <section class="panel figure-card" id="limits">
            <h2>當模型知識不夠時怎麼辦</h2>
            <img src="assets/figures/model-limit-solution.png" alt="超出模型處理範圍的解法" />
            <p>教材明確指出：當服務更新、API 改版或模型沒有見過某個新功能時，不能只靠模型硬猜。更穩定的做法是加入 Google Search grounding、URL context，或直接提供官方說明文件與關鍵欄位位置。</p>
          </section>
          <section class="panel" id="docs">
            <h2>把文件當成 AI 協作前置條件</h2>
            <p>這套教材很適合拿來教一個重要觀念：與生成式 AI 協作時，好的上下文比更長的提示詞更重要。當需要串接 Threads API、Cloudinary 或其他外部服務時，應主動提供官方文件網址、金鑰儲存位置與目標輸出格式，讓 AI 與開發者在同一套規格上工作。</p>
          </section>
          <section class="panel figure-card" id="patent">
            <h2>加入 LINEBOT_專利作為架構補充</h2>
            <div class="figure-grid">
              <article class="figure-card panel">
                <img src="assets/figures/patent-flow-overview.png" alt="專利功能流程圖" />
                <p>功能流程圖適合說明事件驗證、任務路由與結果封裝。</p>
              </article>
              <article class="figure-card panel">
                <img src="assets/figures/patent-cloud-map.png" alt="專利雲端服務對應圖" />
                <p>雲端服務對應圖可協助學習者從工具列表提升到系統架構思維。</p>
              </article>
            </div>
            <p>若課程要延伸到專題、研究或產品化，專利圖像提供了更高層次的整合視角：使用者互動、LINE 平台、後端協調核心、AI 與資料層、交付輸出，外加治理與維運層。</p>
          </section>
          <section class="panel" id="governance">
            <h2>治理與安全提醒</h2>
            <ul class="clean-list">
              <li>金鑰不可直接硬寫在公開程式碼或截圖中。</li>
              <li>記錄與檔案存取應區分測試與正式環境。</li>
              <li>若系統處理學生資料、行政資料或研究資料，需額外討論權限與留存政策。</li>
              <li>AI 生成結果必須保留人工查核與例外追蹤機制。</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


ADVANCED_EN = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index_en.html">Home</a> / Advanced</p>
          <p class="eyebrow">Advanced</p>
          <h1>Model boundaries, external docs, and patent-informed architecture</h1>
          <p class="lead">Once the project moves beyond a classroom demo, the real focus shifts to context management, external API integration, access control, and architecture abstraction.</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>On this page</h3>
          <a href="#limits">Model boundaries</a>
          <a href="#docs">Documentation context</a>
          <a href="#patent">Patent extension</a>
          <a href="#governance">Governance</a>
        </aside>
        <article class="article">
          <section class="panel figure-card" id="limits">
            <h2>What to do when the model lacks the right context</h2>
            <img src="assets/figures/model-limit-solution.png" alt="How to handle model limits" />
            <p>The materials make a strong point: when services change, APIs evolve, or the model has not seen the feature before, the answer is not to guess harder. It is to add grounding, URL context, or the official documentation and exact storage locations.</p>
          </section>
          <section class="panel" id="docs">
            <h2>Documentation as a design input</h2>
            <p>One of the key lessons in this course is that good context matters more than long prompts. When integrating Threads, Cloudinary, or any other external service, the developer should provide the official docs, key storage locations, and expected output shape.</p>
          </section>
          <section class="panel figure-card" id="patent">
            <h2>Using the patent folder as an advanced supplement</h2>
            <div class="figure-grid">
              <article class="figure-card panel">
                <img src="assets/figures/patent-flow-overview.png" alt="Patent workflow overview" />
                <p>The workflow diagram helps explain validation, routing, and response packaging.</p>
              </article>
              <article class="figure-card panel">
                <img src="assets/figures/patent-cloud-map.png" alt="Patent cloud service map" />
                <p>The cloud service view helps learners move from tool lists toward system architecture thinking.</p>
              </article>
            </div>
            <p>The patent-oriented figures show a larger design frame: user interaction, LINE platform, backend orchestration, AI and data layers, outputs, and the governance layer required for real operations.</p>
          </section>
          <section class="panel" id="governance">
            <h2>Governance and security reminders</h2>
            <ul class="clean-list">
              <li>Never hard-code secrets into public code or screenshots.</li>
              <li>Separate testing and production storage whenever possible.</li>
              <li>If the system handles student, administrative, or research data, discuss retention and access policies explicitly.</li>
              <li>AI-generated outputs still require human review and exception tracking.</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


RES_ZH = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index.html">首頁</a> / 資源彙整</p>
          <p class="eyebrow">Resources</p>
          <h1>教材來源、官方文件與延伸練習</h1>
          <p class="lead">本頁整理可公開連用的教材來源、官方工具入口與適合課堂使用的實作清單。</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>本頁導覽</h3>
          <a href="#links">公開課程連結</a>
          <a href="#sources">教材來源</a>
          <a href="#official">官方文件</a>
          <a href="#practice">練習清單</a>
        </aside>
        <article class="article">
          <section class="panel" id="links">
            <h2>公開課程與延伸入口</h2>
            <div class="hero-actions">
              <a class="button primary" href="https://sites.google.com/view/genai-mcp/index">教材網站來源頁</a>
              <a class="button" href="https://www.youtube.com/playlist?list=PL1BHO-AUVmwnWQg8Y55MRjoiQ8wBUBScJ">YouTube 播放清單</a>
              <a class="button" href="https://moocs.moe.edu.tw/moocs/#/course/detail/10002657">教育部磨課師課程</a>
              <a class="button" href="https://www.youtube.com/@ytshihclassworld">施育廷 YouTube 頻道</a>
            </div>
          </section>
          <section class="panel" id="sources">
            <h2>本網站整理依據</h2>
            <ul class="clean-list">
              <li><code>教材https.docx</code>：提供系統總覽、設定流程、核心功能與 API 說明。</li>
              <li><code>互動機器人專題應用.pdf</code>：提供 Webhook、LINE Bot、GAS 與 AI 串接的教學脈絡。</li>
              <li><code>LINEBOT_磨課師.pdf</code>：作為磨課師與課程簡報型素材。</li>
              <li><code>LINE_Gemini_Cloud_Manager.pdf.pdf</code>：補充 LINE 個人雲端助理的圖像架構。</li>
              <li><code>LINEBOT_專利</code>：在需要進階系統觀時，加入專利圖像與架構思路。</li>
            </ul>
          </section>
          <section class="panel" id="official">
            <h2>官方工具與文件</h2>
            <div class="hero-actions">
              <a class="button" href="https://developers.line.biz/">LINE Developers</a>
              <a class="button" href="https://script.google.com/">Google Apps Script</a>
              <a class="button" href="https://workspace.google.com/products/sheets/">Google Sheets</a>
              <a class="button" href="https://aistudio.google.com/">Google AI Studio</a>
              <a class="button" href="https://developers.google.com/apps-script">Apps Script Docs</a>
            </div>
          </section>
          <section class="panel" id="practice">
            <h2>建議練習清單</h2>
            <ul class="clean-list">
              <li>完成一個只回傳固定文字的最小 LINE Bot。</li>
              <li>新增一張工作表，記錄每次對話的事件類型與時間戳。</li>
              <li>讓 Bot 接收一張圖片並把檔名與摘要寫進工作表。</li>
              <li>設計一個可以查詢 YouTube 或 Google 的文字指令。</li>
              <li>嘗試加入一個自訂工作流，並用圖表說明其資料流。</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


RES_EN = dedent(
    """\
      <section class="page-hero">
        <div class="wrap">
          <p class="breadcrumb"><a href="index_en.html">Home</a> / Resources</p>
          <p class="eyebrow">Resources</p>
          <h1>Source materials, official documentation, and practice tasks</h1>
          <p class="lead">This page gathers the public teaching sources, official tools, and practical exercises that support the course site.</p>
        </div>
      </section>
      <main class="wrap content-grid">
        <aside class="sidebar">
          <h3>On this page</h3>
          <a href="#links">Public course links</a>
          <a href="#sources">Source basis</a>
          <a href="#official">Official docs</a>
          <a href="#practice">Practice checklist</a>
        </aside>
        <article class="article">
          <section class="panel" id="links">
            <h2>Public course and extension links</h2>
            <div class="hero-actions">
              <a class="button primary" href="https://sites.google.com/view/genai-mcp/index">Source course site</a>
              <a class="button" href="https://www.youtube.com/playlist?list=PL1BHO-AUVmwnWQg8Y55MRjoiQ8wBUBScJ">YouTube playlist</a>
              <a class="button" href="https://moocs.moe.edu.tw/moocs/#/course/detail/10002657">MOE MOOC course</a>
              <a class="button" href="https://www.youtube.com/@ytshihclassworld">Yu-Ting Shih YouTube channel</a>
            </div>
          </section>
          <section class="panel" id="sources">
            <h2>Source basis for this site</h2>
            <ul class="clean-list">
              <li><code>教材https.docx</code>: system overview, setup steps, core functions, and API references.</li>
              <li><code>互動機器人專題應用.pdf</code>: instructional path for Webhooks, LINE Bot, GAS, and AI integration.</li>
              <li><code>LINEBOT_磨課師.pdf</code>: MOOC-oriented slide material.</li>
              <li><code>LINE_Gemini_Cloud_Manager.pdf.pdf</code>: visual overview of the LINE-based cloud assistant model.</li>
              <li><code>LINEBOT_專利</code>: architecture diagrams used as advanced system-thinking supplements.</li>
            </ul>
          </section>
          <section class="panel" id="official">
            <h2>Official tools and documentation</h2>
            <div class="hero-actions">
              <a class="button" href="https://developers.line.biz/">LINE Developers</a>
              <a class="button" href="https://script.google.com/">Google Apps Script</a>
              <a class="button" href="https://workspace.google.com/products/sheets/">Google Sheets</a>
              <a class="button" href="https://aistudio.google.com/">Google AI Studio</a>
              <a class="button" href="https://developers.google.com/apps-script">Apps Script Docs</a>
            </div>
          </section>
          <section class="panel" id="practice">
            <h2>Suggested practice checklist</h2>
            <ul class="clean-list">
              <li>Build a minimum LINE Bot that returns a fixed text response.</li>
              <li>Add a worksheet that logs event type and timestamp for every interaction.</li>
              <li>Make the bot accept an image and write its filename and summary to Sheets.</li>
              <li>Design one text command for Google or YouTube search.</li>
              <li>Create a new workflow and document its data flow with a diagram.</li>
            </ul>
          </section>
        </article>
      </main>
    """
)


PAGES = [
    ("index.html", "index_en.html", "zh", "LINE Bot、Google Apps Script 與 Google Sheets 教學網站", "施育廷整理製作的 LINE Bot、Google Apps Script、Google Sheets 與 Gemini 工作流雙語教材網站。", HOME_ZH),
    ("index_en.html", "index.html", "en", "LINE Bot, Google Apps Script, and Google Sheets Teaching Website", "A bilingual teaching site on LINE Bot, Google Apps Script, Google Sheets, and Gemini-enabled workflows curated by Yu-Ting Shih.", HOME_EN),
    ("teaching-plan.html", "teaching-plan_en.html", "zh", "LINE Bot 教學地圖與評量設計", "LINE Bot、Google Apps Script 與 Google Sheets 課程的節次安排、任務設計與評量方式。", PLAN_ZH),
    ("teaching-plan_en.html", "teaching-plan.html", "en", "LINE Bot Course Map and Assessment Design", "Delivery sequence, assignments, and assessment design for the LINE Bot, GAS, and Google Sheets course.", PLAN_EN),
    ("setup.html", "setup_en.html", "zh", "LINE Bot 建置流程：LINE、GAS 與 Google Sheet 設定", "從 Google Sheet、Drive、LINE Developers 到 Apps Script 網頁應用程式的完整設定步驟。", SETUP_ZH),
    ("setup_en.html", "setup.html", "en", "LINE Bot Setup: LINE, GAS, and Google Sheets", "Step-by-step setup for Google Sheets, Drive, LINE Developers, and Apps Script deployment.", SETUP_EN),
    ("apps-script.html", "apps-script_en.html", "zh", "GAS 與 Google Sheets：LINE Bot 後端控制核心", "說明 LINE Bot 的 Apps Script 協調核心、工作表設計、Prompt 與日誌維運。", APPS_ZH),
    ("apps-script_en.html", "apps-script.html", "en", "GAS and Google Sheets: LINE Bot Backend Logic", "Explains the Apps Script controller layer, worksheet design, prompts, and logging logic behind the LINE Bot.", APPS_EN),
    ("workflows.html", "workflows_en.html", "zh", "LINE Bot 功能工作流：檔案、報告、搜尋與 Threads", "整理 LINE Bot 的檔案處理、報告生成、搜尋與 Threads 發文等實用工作流。", WORKFLOW_ZH),
    ("workflows_en.html", "workflows.html", "en", "LINE Bot Workflows: Files, Reports, Search, and Threads", "Practical workflow guide for file handling, reports, search, and Threads posting with a LINE Bot.", WORKFLOW_EN),
    ("advanced.html", "advanced_en.html", "zh", "LINE Bot 進階延伸：模型限制、外部文件與專利架構", "進階整理模型限制處理、文件上下文、外部 API 與專利導向的 LINE Bot 架構思維。", ADVANCED_ZH),
    ("advanced_en.html", "advanced.html", "en", "Advanced LINE Bot Topics: Model Limits, Docs, and Architecture", "Advanced coverage of model boundaries, external documentation, API expansion, and patent-informed architecture.", ADVANCED_EN),
    ("resources.html", "resources_en.html", "zh", "LINE Bot 教材資源彙整", "彙整 LINE Bot、Google Apps Script、Google Sheets 教學網站使用的教材來源、官方文件與實作清單。", RES_ZH),
    ("resources_en.html", "resources.html", "en", "LINE Bot Teaching Resources", "Source materials, official documentation, and practice tasks for the LINE Bot teaching website.", RES_EN),
]


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for filename, alt_filename, lang, title, description, content in PAGES:
        output = ROOT / filename
        output.write_text(
            wrap_page(lang, title, description, filename, alt_filename, content),
            encoding="utf-8",
        )
    print(f"Generated {len(PAGES)} pages in {ROOT}")


if __name__ == "__main__":
    main()
