"""Build a bilingual showcase from the existing course layout and certificate."""
from pathlib import Path
from bs4 import BeautifulSoup
from html import escape
import json, shutil, re
from unify_site_shell import apply

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'linebot-course-site'
PLAYLIST='https://www.youtube.com/playlist?list=PL1BHO-AUVmwkB-mArAOehqNvtyPQXx3wZ'
PATENT='基於對話式介面之多源資訊整合與自動化內容生成之系統與方法'
TITLE='LINEBOT雲端管理！不只是聊天！AI功能超乎想像！零成本 LINE 智能助理與自動化工作流'

for en in [False,True]:
    suffix='_en' if en else ''
    name=f'showcase{suffix}.html'
    title='Featured work: LINE cloud assistant and patent' if en else '代表成果｜LINE雲端智能助理與專利'
    soup=BeautifulSoup((SITE/f'process{suffix}.html').read_text(encoding='utf-8'),'html.parser')
    soup.title.string=title
    soup.select_one('meta[name="description"]')['content']=title
    url='https://andrewshih1210.github.io/my-blog/linebot-course-site/'+name
    soup.select_one('link[rel="canonical"]')['href']=url
    soup.select_one('link[hreflang]')['href']=url.rsplit('/',1)[0]+'/showcase'+('' if en else '_en')+'.html'
    ld={'@context':'https://schema.org','@type':'CollectionPage','name':title,'url':url,'inLanguage':'en' if en else 'zh-Hant','author':{'@type':'Person','@id':'https://andrewshih1210.github.io/my-blog/#person','name':'施育廷'}}
    soup.select_one('script[type="application/ld+json"]').string=json.dumps(ld,ensure_ascii=False)
    soup.h1.string=title
    actions=soup.select_one('.hero-actions');actions.clear()
    for href,label,primary in [(PLAYLIST,'Watch the showcase playlist' if en else '觀看代表成果播放清單',True),('#patent','Patent certificate' if en else '查看專利證書',False),(f'index{suffix}.html','Course home' if en else '返回課程首頁',False)]:
        a=soup.new_tag('a',href=href);a['class']=['button']+(['primary'] if primary else []);a.string=label;actions.append(a)
    main=soup.main;main.clear()
    content=f'''<section class="panel" id="demonstration"><p class="section-label">Showcase</p><h2>{'From conversations to cloud workflows' if en else '從聊天介面延伸到雲端工作流程'}</h2><p>{'This page brings together Yu-Ting Shih’s patent certificate and the author-provided demonstration playlist. Use the videos to explore application examples, then return to the course for the underlying GAS, Sheets and Gemini learning steps.' if en else '本頁整合施育廷的專利證書與LINEBOT雲端管理示範播放清單。先透過影片認識應用情境，再回到教材理解GAS、Sheets與Gemini的操作和開發流程。'}</p><h3>{escape(TITLE)}</h3><div style="aspect-ratio:16/9;width:100%;margin:20px 0"><iframe title="LINEBOT cloud management showcase playlist" loading="lazy" style="width:100%;height:100%;border:0;border-radius:12px" src="https://www.youtube-nocookie.com/embed/videoseries?list=PL1BHO-AUVmwkB-mArAOehqNvtyPQXx3wZ" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div><p><a class="button primary" href="{PLAYLIST}">{'Open playlist on YouTube' if en else '在YouTube開啟播放清單'}</a></p><p class="muted">{'If embedding is unavailable, use the playlist link. “Zero cost” is part of the supplied playlist title, not a guarantee that every service or usage level is free; API pricing and quotas apply.' if en else '若影片無法嵌入播放，請使用上方YouTube連結。「零成本」為原播放清單標題，不表示所有服務或任何用量皆免費，仍須依API計價與配額評估。'}</p></section>
<section class="panel" id="patent"><p class="section-label">Patent I918530</p><h2>{'Invention patent certificate' if en else '發明專利證書'}</h2><div class="two-col"><figure class="figure-card"><a href="../certificates-site/items/item-035.jpg"><img loading="lazy" src="../certificates-site/items/item-035.jpg" alt="施育廷發明專利I918530證書"></a><figcaption>{'Open the original certificate image' if en else '點圖查看完整證書'}</figcaption></figure><div><h3>{PATENT}</h3><p>SYSTEM AND METHOD FOR MULTI-SOURCE INFORMATION INTEGRATION AND AUTOMATED CONTENT GENERATION BASED ON CONVERSATIONAL INTERFACE</p><dl><dt>{'Patent number' if en else '專利號碼'}</dt><dd>I918530</dd><dt>{'Inventor and patentee' if en else '發明人／專利權人'}</dt><dd>施育廷 Yu-Ting Shih</dd><dt>{'Issuing authority' if en else '發證機關'}</dt><dd>{'Taiwan Intellectual Property Office, Ministry of Economic Affairs' if en else '經濟部智慧財產局'}</dd><dt>{'Certificate date' if en else '證書日期'}</dt><dd>2026-03-11</dd></dl><p><a class="button" href="https://tiponet.tipo.gov.tw/twpat5/twpatc/twpatkm?!!FRURLI918530">{'Official patent record' if en else '官方專利資料'}</a></p><p class="muted">{'Certificate details are transcribed from the image. This page does not assess current legal status or claim coverage of every video feature; consult the official record and patent claims.' if en else '證書資料依原圖記載。本頁不判定目前法律狀態，也不將每項影片功能都視為專利涵蓋範圍；相關內容請以官方資料及專利請求項為準。'}</p></div></div></section>
<section class="panel"><h2>{'Connect the showcase to learning' if en else '從成果回到實作學習'}</h2><div class="unit-grid"><a class="unit-card" href="quickstart{suffix}.html"><strong>{'Slides and code' if en else '投影片與程式'}</strong><p>{'Trace the original course examples and page references.' if en else '對照原投影片頁碼與程式摘錄，理解資料如何流動。'}</p></a><a class="unit-card" href="process{suffix}.html"><strong>{'AI collaboration process' if en else 'AI協作開發流程'}</strong><p>{'Define requirements, test changes and hand over a working version.' if en else '練習需求釐清、提問、除錯與版本交接。'}</p></a><a class="unit-card" href="apps-script{suffix}.html#security-quotas"><strong>{'Quotas and security' if en else '配額與安全'}</strong><p>{'Review service limits before extending a prototype.' if en else '從示範擴充為服務前，先檢查配額與安全限制。'}</p></a></div></section>'''
    main.append(BeautifulSoup(content,'html.parser'))
    apply(SITE/name,str(soup))

for p in SITE.glob('*.html'):
    en=p.stem.endswith('_en');suffix='_en' if en else '';text=p.read_text(encoding='utf-8')
    soup=BeautifulSoup(text,'html.parser')
    for nav in soup.select('.unified-local-panel,.unified-mobile-panel'):
        if not nav.find('a',href=f'showcase{suffix}.html'):
            a=soup.new_tag('a',href=f'showcase{suffix}.html');a['class']=['unified-link'];a.string='Featured work' if en else '代表成果';nav.append(a)
    if p.name==f'index{suffix}.html' and not soup.find(id='featured-work'):
        sec=BeautifulSoup(f'<section class="panel" id="featured-work"><p class="section-label">Featured Work</p><h2>{"LINE cloud assistant and invention patent" if en else "代表成果：LINE雲端智能助理與發明專利"}</h2><p>{"Explore the showcase playlist alongside patent certificate I918530." if en else "結合LINEBOT雲端管理示範播放清單與I918530專利證書，認識從對話介面到自動化工作流程的應用。"}</p><a class="button primary" href="showcase{suffix}.html">{"View featured work" if en else "查看代表成果"}</a></section>','html.parser')
        text=re.sub(r'(<main\b[^>]*>)',lambda m:m[0]+str(sec),text,count=1)
    text=re.sub(r'<header class="unified-header">.*?</header>',lambda m:str(soup.select_one('.unified-header')),text,count=1,flags=re.S)
    p.write_text(text,encoding='utf-8')
    shutil.copy2(p,ROOT/'scripts/linebot-course-site-templates'/p.name)

p=ROOT/'sitemap.xml';text=p.read_text(encoding='utf-8')
for name in ['showcase.html','showcase_en.html']:
    url='https://andrewshih1210.github.io/my-blog/linebot-course-site/'+name
    if url not in text:text=text.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>2026-11-07</lastmod></url>\n</urlset>')
p.write_text(text,encoding='utf-8')
