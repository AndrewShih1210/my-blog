# 動態圖室線上版

動態圖室是施育廷製作的純前端 SVG 教學動畫工具。公開版可直接在 GitHub Pages 執行，不需要安裝伺服器、Python 或本機套件。

## 線上使用

<https://andrewshih1210.github.io/my-blog/veo-crator/>

## 線上版功能

- 編輯文字、SVG 圖形、圖示、照片與圖層。
- 提供 12 種動畫效果與時間軸控制。
- 透過 Iconify 公開 API 搜尋 Tabler Icons 與 Material Design Icons。
- 下載專案 JSON、SVG、獨立 HTML 與 WebM。
- 使用瀏覽器 Web Speech API 預覽語音。

線上版不呼叫 `/api/*`，也不會顯示無法使用的 Edge TTS 或 MP4 按鈕。本機完整版才支援 Edge TTS、MP3、SRT 與含旁白 MP4。

## 本機完整版

需要 Edge TTS、MP3、SRT、ffmpeg MP4 或完整本機流程時，請前往 [`local-version/`](./local-version/)。原始碼位於 [`local-version/source/`](./local-version/source/)。

## 授權

veo-crator 採 [PolyForm Noncommercial License 1.0.0](./LICENSE)，屬於 source-available 非商業授權，不是 MIT License，也不宣稱為 OSI 開放原始碼。

- 個人學習、學術研究、一般非營利課堂與免費教學分享可免費使用。
- 可在非商業目的下查看、修改及分享程式碼；修改版須保留作者、著作權、原授權條款及變更說明。
- 收費課程、企業服務、代製、轉售、廣告營利、產品整合，以及以本工具產出成果從事商業服務，均須事先取得施育廷書面授權。
- 中文實例與使用界線請參閱[非商業授權說明頁](./license.html)。
- 第三方工具及素材仍適用各自條款，詳見[第三方授權說明](./THIRD_PARTY_NOTICES.md)。

本站其他論文、教材、證書、照片及個人網站內容不納入 veo-crator 授權，仍為保留所有權利。

## 主要檔案

- `index.html`：線上版介面。
- `styles.css`：視覺與版面。
- `app.js`：SVG 編輯、動畫、語音預覽與下載功能。
- `preview.png`：操作介面預覽。

## 作者

製作與維護：施育廷（Yu-Ting Shih）
