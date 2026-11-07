"""Source-bounded workshop planning content, shared by both invitation pages."""

def section(en=False):
    def t(zh, english):
        return english if en else zh
    suffix = '_en' if en else ''
    paths = [
        ('教師研習與AI融入教學', 'AI for educators',
         '適合教師與教學支援人員。從一個教學目標出發，練習產生教材初稿、設計活動，再檢查內容正確性與評量是否對齊。',
         'For teachers and teaching-support teams. Start with a learning objective, draft materials and activities, then review accuracy and assessment alignment.',
         '可討論的練習成果：一份活動設計與人工查核清單。', 'Possible practice output: an activity plan and a human-review checklist.',
         '2026-04-16育達科技大學演講；感謝狀可於下方紀錄查閱。', 'Related experience: the April 16, 2026 talk at Yu Da University; the certificate is linked below.',
         f'../ai-course-site/index{suffix}.html', '查看AI教材', 'Explore AI teaching materials'),
        ('行政文書與研究工作流', 'Administrative and research workflows',
         '適合行政人員、研究生與研究支援人員。練習說明需求、提供參考資料、整理文件與分析步驟；研究引用仍須回到原始文獻核對。',
         'For administrators, graduate students and research-support teams. Practice specifying requests, supplying references and organizing document or analysis steps. Verify research citations against original publications.',
         '可討論的練習成果：一份可重用的任務流程與來源核對表。', 'Possible practice output: a reusable task workflow and source-checking sheet.',
         '2026-06-02臺中教育大學Gemini整合演講；下方提供活動圖片與影片。', 'Related experience: the June 2, 2026 Gemini workshop at NTCU; an event image and video are linked below.',
         f'../author-works/index{suffix}.html', '查看研究成果', 'Explore research outputs'),
        ('LINE Bot與服務自動化', 'LINE Bot and service automation',
         '適合已有試算表操作經驗、希望理解服務流程的人員。依原課程學習LINE、GAS與Google Sheets的資料流，再評估金鑰保護、配額及人工接手。',
         'For participants familiar with spreadsheets who want to understand service workflows. Follow the original LINE, GAS and Google Sheets course, then assess secret handling, quotas and human handoff.',
         '可討論的練習成果：流程圖、訊息測試紀錄與部署前檢查表；不保證單次研習完成正式上線。', 'Possible practice output: a workflow diagram, message-test log and deployment checklist. A single workshop does not guarantee production readiness.',
         '相關經歷：2026-06-30苗栗旅宿服務課程；另提供公開LINE Bot教材與代表成果。', 'Related experience: the June 30, 2026 Miaoli hospitality course, with public LINE Bot materials and a separate showcase.',
         f'../linebot-course-site/index{suffix}.html', '查看LINE Bot教材', 'Explore LINE Bot materials'),
        ('AI入門與內容規劃', 'AI fundamentals and content planning',
         '適合企劃、文案及初次使用AI的團隊。從日常工作問題整理需求與參考資料，練習產出內容架構，再由人確認事實、語氣與使用限制。',
         'For planning, writing and AI-beginner teams. Turn everyday tasks into clear requests and reference material, draft a content outline, and review facts, tone and usage constraints.',
         '可討論的練習成果：一份任務說明、內容大綱與修訂紀錄。', 'Possible practice output: a task brief, content outline and revision log.',
         '相關經歷：2026-10-28就享知公開活動；2026-10-30內容策略分享另有作者文章。', 'Related experience: the October 28, 2026 DigiKnow event and the October 30 content-strategy session documented in an author article.',
         'https://www.digiknow.com.tw/activity/aabc6430061b4', '閱讀主辦方活動介紹', 'Read the host event introduction'),
    ]
    cards = ''.join(f'<article><h3>{t(a,b)}</h3><p>{t(c,d)}</p><p>{t(e,f)}</p><p class="small">{t(g,h)}</p><p><a href="{url}">{t(zh,eng)}</a></p></article>' for a,b,c,d,e,f,g,h,url,zh,eng in paths)
    return f'''<section aria-labelledby="learning-paths"><div class="section-heading"><h2 id="learning-paths">{t('如何選擇適合團隊的AI研習？','Which AI workshop fits your team?')}</h2></div>
<p>{t('在臺中（台中）規劃教師研習、行政培訓或AI實作活動，可先從參與者要完成的任務選題，再討論先備能力與設備。以下是依既有授課經歷與公開教材整理的規劃方向，不是固定班期或已驗證的成效承諾。','For an AI workshop in Taichung, start with the tasks participants need to complete, then discuss prior knowledge and equipment. These planning options draw on existing teaching experience and public materials; they are not scheduled courses or claims of measured effectiveness.')}</p>
<div class="topics">{cards}</div></section>
<section aria-labelledby="prepare"><div class="section-heading"><h2 id="prepare">{t('先看示範，再決定研習內容','Review an example before planning a workshop')}</h2></div>
<ol><li>{t('先選一項真實任務，例如教材設計、文件整理或訊息回覆，避免只列想學的工具名稱。','Choose one real task, such as lesson design, document preparation or message handling, rather than only naming tools.')}</li>
<li>{t('閱讀對應教材或觀看下方演講紀錄，確認團隊需要概念導入、操作示範，還是帶著做的工作坊。','Review the linked materials or recordings below and decide whether your team needs an introduction, demonstration or hands-on workshop.')}</li>
<li>{t('來信提供參與對象、日期、人數、設備與預期成果，再共同確認內容及可配合形式。英文網頁供資訊查閱，授課語言須另行確認。','Email the audience, dates, attendance, equipment and intended output so scope and format can be agreed. This English page provides information; the delivery language must be confirmed separately.')}</li></ol>
<p class="small">{t('內容更新：','Content updated: ')}<time datetime="2026-11-07">2026-11-07</time></p></section>'''
