# 動態圖室線上版

動態圖室是施育廷製作的純前端 SVG 教學動畫工具。公開版可直接在 GitHub Pages 執行，不需要安裝伺服器、Python 或本機套件。

## 線上使用

<https://andrewshih1210.github.io/my-blog/veo-crator/>

## 線上版功能

- 編輯文字、SVG 圖形、背景與圖層時間軸。
- 12 種動畫效果：淡入、四方向滑入、彈出、縮放、旋轉、彈跳、擺動、漂浮與無動畫。
- 透過 Iconify 公開 API 搜尋 Tabler Icons 與 Material Design Icons，加入後會嵌入專案。
- 下載專案 JSON、SVG、獨立 HTML 與 WebM。
- 使用瀏覽器 Web Speech API 預覽旁白文字；語音不會寫入 WebM。

公開版不呼叫 `/api/*`，也沒有無法執行的 Edge TTS 或 MP4 按鈕。本機完整版才支援 Edge TTS、MP3、SRT 與含旁白 MP4。

## 本機完整版

安裝方式、相依套件與完整原始碼位於 [`local-version/`](./local-version/)；實際執行檔位於 [`local-version/source/`](./local-version/source/)。

## 主要檔案

- `index.html`：線上版介面。
- `styles.css`：工具視覺樣式。
- `app.js`：純前端編輯、動畫、素材與輸出邏輯。
- `preview.png`：工具預覽圖。

## 作者

製作與維護：施育廷（Yu-Ting Shih）

