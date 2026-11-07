"""Add an optional Threads preview to the course and its source templates."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for folder in ['linebot-course-site', 'scripts/linebot-course-site-templates']:
    for en in [False, True]:
        path = ROOT / folder / ('index_en.html' if en else 'index.html')
        text = path.read_text(encoding='utf-8')
        if 'data-threads-preview' in text:
            continue
        def t(zh, eng): return eng if en else zh
        section = f'''<section class="wrap" id="community-sharing" data-threads-preview>
<article class="panel"><p class="section-label">Community</p><h2>{t('教材分享與社群討論','Teaching resources and community discussion')}</h2>
<p>{t('我在Threads分享這套LINE Bot、Google Apps Script與Google Sheets教材，介紹Google雲端環境中的訊息處理與自動化應用。可先依教材完成基本流程，再依需求評估延伸功能、權限與配額限制。','I shared these LINE Bot, Google Apps Script and Google Sheets materials on Threads, introducing messaging and automation in the Google cloud environment. Start with the basic course workflow, then assess extensions, permissions and quotas for your needs.')}</p>
<p class="muted">{t('這是作者本人的公開分享，非第三方推薦或教學成效證明。','This is an author-written public post, not a third-party endorsement or evidence of learning effectiveness.')}</p>
<div class="cta-row"><a class="button primary" href="quickstart{'_en' if en else ''}.html">{t('開始閱讀教材','Start the tutorial')}</a><a class="button" href="https://www.threads.com/@andrewshih1210/post/DfYGB0Tk_IO">{t('到Threads查看原文與討論','Read the original post and discussion (Chinese)')}</a><button type="button" class="button">{t('載入Threads貼文預覽','Load Threads preview')}</button></div>
<p class="muted">{t('點擊載入後才會連線到Threads，並受該平台的隱私政策約束。若預覽受瀏覽器或平台限制，仍可使用上方原文連結。','Loading connects to Threads and is subject to its privacy policy. If the browser or platform blocks the preview, the original-post link remains available.')}</p>
<p role="status" aria-live="polite"></p><div data-embed-host style="max-width:100%;overflow:auto"></div>
</article></section>
'''
        text = text.replace('</main>', section + '</main>', 1)
        text = text.replace('</body>', '<script defer src="threads-preview.js"></script>\n</body>')
        path.write_text(text, encoding='utf-8')
