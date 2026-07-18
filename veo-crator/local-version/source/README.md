# 動態圖室

以 HTML、SVG 與 CSS animation 為核心的免費教學動畫製作器。可製作課程解說、概念圖、影片片頭片尾，並輸出 SVG、獨立 HTML、WebM 或 MP4。

這個資料夾是本機完整版原始碼。若只需要免安裝的編輯與 WebM、SVG、HTML 輸出，請使用[線上版](../../index.html)。

## 安裝需求

- Node.js 18 或更新版本。
- Python 3，並執行 `python -m pip install edge-tts`。
- ffmpeg，需可從命令列執行；也可用 `PYTHON_PATH`、`FFMPEG_PATH` 指定程式位置。

## 啟動

在 PowerShell 執行：

```powershell
.\start-server.ps1
```

接著開啟 <http://127.0.0.1:8765/>。

若從 GitHub clone 整個網站，請先切換至本資料夾：

```powershell
cd .\veo-crator\local-version\source
.\start-server.ps1
```

## 主要功能

- 文字、形狀、圖示、教學模板與背景色。
- 可搜尋 Iconify 免費素材庫，使用 Tabler Icons（MIT）與 Material Design Icons（Apache 2.0）；選取後會把 SVG 內容嵌入專案。
- 12 種進場與動態效果：四方向滑入、彈出、縮放、旋轉、彈跳、擺動、漂浮、淡入與無動畫。
- Edge TTS 中文／英文 AI 旁白，可調語速並下載 MP3、SRT。
- 預覽、時間軸、圖層排序、專案 JSON 儲存與讀取。
- 下載單格 SVG、可播放的獨立 HTML、WebM，以及瀏覽器內直接轉換的 MP4。

## Edge TTS 與影片聲音

Edge TTS 不需付費 API 金鑰，但產生語音時需要網路。先在「AI 旁白」面板產生旁白，錄製 WebM 或 MP4 時會把該音訊一併錄入影片。

免費素材庫搜尋同樣需要網路；素材加入後會成為專案內的 SVG 圖層，可改色、套用動畫並隨專案 JSON 儲存。

MP4 由本機 ffmpeg 轉成 H.264、yuv420p、AAC 與 fast-start，適合一般播放器、PowerPoint 與影音平台。

若瀏覽器內轉檔失敗，也可先下載 WebM，再執行：

```powershell
.\convert-to-mp4.ps1 -InputWebM "C:\path\animation.webm"
```

## 快捷鍵

- `Space`：播放／暫停
- `Ctrl + S`：下載專案 JSON
- `Ctrl + Z`：復原
- `Delete`：刪除選取圖層

## 檔案

- `app-local.html`：本機版介面與 SVG 工作區，由 `server.js` 在根網址提供
- `styles.css`：視覺設計
- `app.js`：編輯、動畫、錄影與旁白控制
- `server.js`：本機靜態伺服器、Edge TTS 與 MP4 轉檔端點
- `convert-to-mp4.ps1`：命令列轉檔備援
- `preview.png`：工具預覽圖

產生的 MP3、SRT 與轉檔暫存資料會放在 `.generated/`，此目錄已由 `.gitignore` 排除，不會提交至 GitHub。
