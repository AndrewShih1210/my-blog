# LINE reply bot + signed GAS log / LINE回覆Bot與GAS簽名紀錄

## 中文

此範例以Node入口驗證LINE原始請求簽章並傳送固定回覆，再選擇性地將HMAC簽名紀錄送到GAS與Sheets。GAS不是直接驗證LINE簽章的入口。完整部署流程見[快速實作](../../quickstart.html)。

### 程式檔

| 檔案 | 用途 |
| --- | --- |
| `server.mjs` | Node HTTP伺服器；`/healthz`健康檢查與`/webhook`驗簽、回覆、relay紀錄。 |
| `Code.gs` | GAS簽名紀錄端；`setupLogSheet()`建立Events表頭，`doPost(e)`驗證relay、去重及限制筆數。 |
| `test.mjs` | Node入口測試，以本機HTTP及mock fetch代替LINE與GAS服務。 |
| `test-gas.mjs` | 以Node VM載入實際`Code.gs`，mock Properties、Utilities、Sheets、Lock及Content服務。 |
| `.env.example` | 本機環境變數範本，不含真實憑證。 |
| `package.json` | Node版本與啟動、測試指令；`npm test`執行Node入口與GAS模擬測試。 |
| `Dockerfile` | Node容器入口。 |
| `.gitignore`、`.gcloudignore` | 版本控制及部署排除規則；發布前仍須檢查秘密是否被包含。 |

### 本機測試

需要Node.js 22以上，測試只用內建模組，不需安裝套件或設定真實憑證。於此目錄執行：

```powershell
node --test test-gas.mjs
node --test test.mjs test-gas.mjs
```

GAS測試涵蓋有效HMAC、本文／時間／簽章篡改、錯誤共享密鑰、正負5分鐘時效邊界、重複事件、錯誤工作表表頭、缺少工作表、鎖逾時、公式型ID、初始化，以及5,000筆保護。5,000筆不含表頭，第5,000筆可寫入，第5,001筆拒絕；滿額時已存在事件仍回覆`duplicate: true`。「錯誤header」在此指Events工作表表頭；LINE的HTTP `x-line-signature`檢查由`test.mjs`負責，GAS事件物件沒有此標頭欄位。

修正紀錄：`Code.gs`已先確認`eventId`為字串，避免正規表示式隱式接受數字。回歸測試確認數字型事件識別碼會被拒絕；測試不代表完整安全稽核。

本機啟動可將`.env.example`複製為未納入版本控制的`.env`，填入自己的設定後執行：

```powershell
node --env-file=.env server.mjs
```

LINE入口需另部署至可連線的HTTPS網址；本機啟動不代表部署或串接驗證完成。

### 安全邊界與驗證限制

- Token、Channel Secret及API金鑰不得存於Sheets；使用伺服器環境變數或秘密管理器。GAS Script Properties放`RELAY_SECRET`與`SHEET_ID`，不是vault，編輯者可取得內容，必須限制編輯權限。
- LINE簽章與relay HMAC不同；relay使用獨立共享密鑰，驗證`timestamp + '.' + payload`。GAS公開`doPost(e)`不能直接讀取LINE的`x-line-signature`，不可用純GAS取代Node驗簽入口。
- Sheets只寫入`receivedAt`、`eventId`、`type`、`status`，不寫訊息、使用者ID或憑證；仍應限制存取並訂定保留期限。5,000筆是課堂範例保護值，不是Google配額或安全人數上限。
- GAS錯誤以JSON的`ok: false`表示，不能只看HTTP成功狀態。Node回覆成功但紀錄失敗時只警告，可能漏紀錄；沒有持久化補送佇列或端到端exactly-once保證。
- Node去重只在單一程序記憶體中；GAS去重依賴保留中的Events資料與鎖。刪除紀錄、重啟或多實例情境不等同持久化交易去重，高併發與交易需求應另設計資料庫／佇列。
- VM mock只驗證本機邏輯，不模擬Google真實配額、網路、部署權限或多請求鎖競爭，也不是執行不可信程式的安全沙箱。此測試工作未實際驗證LINE、Cloud Run、GAS部署或Sheets寫入。

## English

This example verifies the original LINE request at a Node entry point, sends a fixed reply, and optionally forwards an HMAC-signed log to GAS and Sheets. GAS is not the direct LINE signature verifier. See the [complete quickstart](../../quickstart_en.html) for deployment.

### Files and local testing

`server.mjs` provides `/healthz`, `/webhook`, LINE verification, replies, and signed logging. `Code.gs` initializes the Events header and validates relay requests before deduplication and writes. `test.mjs` tests the Node endpoint with local HTTP and mocked external fetches. `test-gas.mjs` loads the actual GAS source in Node VM with mocked Properties, Utilities, Sheets, Lock, and Content services. `.env.example` documents configuration; `Dockerfile` provides the container entry point; `.gitignore` and `.gcloudignore` define exclusions. Inspect deployment contents for secrets regardless of these rules.

Use Node.js 22 or later. Tests need no installed packages or real credentials. From this directory run:

```powershell
node --test test-gas.mjs
node --test test.mjs test-gas.mjs
```

`npm test` runs both Node and GAS mock tests. GAS tests cover valid HMAC, payload/timestamp/signature tampering, wrong shared secret, both five-minute time boundaries, duplicates, incorrect worksheet headers, missing sheets, lock timeout, formula-like IDs, initialization, and the 5,000-record cap. The cap excludes the header: record 5,000 succeeds, record 5,001 is rejected, and duplicates still succeed without writing at capacity. Here, "incorrect header" means the Events column header; `test.mjs` handles the LINE HTTP signature header, which is not available in the GAS event object.

Correction: `Code.gs` now checks that `eventId` is a string before applying the regular expression. A regression test confirms rejection of numeric identifiers. Tests are not a complete security audit.

For local startup, copy `.env.example` to an untracked `.env`, supply your own configuration, and run `node --env-file=.env server.mjs`. LINE still requires a reachable HTTPS deployment; local startup is not integration verification.

### Security boundaries and validation status

- Keep tokens, Channel Secret, and API keys out of Sheets; use server environment variables or a secret manager. GAS Script Properties holds `RELAY_SECRET` and `SHEET_ID`, is not a vault, and is accessible to project editors. Restrict editor access.
- Relay HMAC uses a separate shared secret over `timestamp + '.' + payload`; it is not LINE signature verification. Public GAS `doPost(e)` does not expose `x-line-signature`; retain the Node verification entry point.
- Only `receivedAt`, `eventId`, `type`, and `status` are stored, not message text, user IDs, or credentials. Apply access controls and retention. The 5,000-record guard is a classroom policy, not a Google quota or a safe user-count estimate.
- Read the GAS JSON `ok` field, not just the HTTP status. A successful reply followed by a failed log only produces a warning; records can be lost. There is no durable retry queue or end-to-end exactly-once guarantee.
- Node deduplication is per-process and in-memory; GAS deduplication relies on retained Events rows and a lock. Deletions, restarts, and multiple instances require separate consideration. Use database/queue designs for transactional or high-concurrency workloads.
- VM mocks check local logic only, not Google quotas, real network behavior, permissions, deployment, or concurrent lock contention. VM is not a security sandbox for untrusted code. This test task has not performed live LINE, Cloud Run, GAS, or Sheets integration validation.
