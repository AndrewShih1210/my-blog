"use strict";

const http = require("http");
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawn, spawnSync } = require("child_process");
const { randomUUID } = require("crypto");

const root = __dirname;
const port = Number(process.env.PORT || process.argv[2] || 8765);
const generatedDir = path.join(root, ".generated");
const pythonPath = process.env.PYTHON_PATH || (process.platform === "win32" ? "python.exe" : "python3");
const ffmpegPath = process.env.FFMPEG_PATH || (process.platform === "win32" ? "ffmpeg.exe" : "ffmpeg");
const allowedVoices = new Set([
  "zh-TW-HsiaoChenNeural",
  "zh-TW-YunJheNeural",
  "en-US-JennyNeural"
]);
const mime = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".mp3": "audio/mpeg",
  ".srt": "application/x-subrip; charset=utf-8",
  ".png": "image/png"
};

fs.mkdirSync(generatedDir, { recursive: true });

function sendJson(response, status, payload) {
  const body = Buffer.from(JSON.stringify(payload));
  response.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Content-Length": body.length,
    "Cache-Control": "no-store"
  });
  response.end(body);
}

function collectBody(request, limit) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    request.on("data", chunk => {
      size += chunk.length;
      if (size > limit) {
        reject(new Error("上傳資料超過容量限制。"));
        request.destroy();
        return;
      }
      chunks.push(chunk);
    });
    request.on("end", () => resolve(Buffer.concat(chunks)));
    request.on("error", reject);
  });
}

function runProcess(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { windowsHide: true });
    let stderr = "";
    child.stderr.on("data", chunk => { stderr = (stderr + chunk.toString()).slice(-12000); });
    child.on("error", reject);
    child.on("close", code => {
      if (code === 0) resolve();
      else reject(new Error(stderr || `${path.basename(command)} 執行失敗，代碼 ${code}`));
    });
  });
}

function commandWorks(command, args) {
  const result = spawnSync(command, args, { windowsHide: true, stdio: "ignore" });
  return !result.error && result.status === 0;
}

async function handleTts(request, response) {
  if (!commandWorks(pythonPath, ["-c", "import edge_tts"])) {
    sendJson(response, 503, { error: "找不到 Python 或 edge-tts。請先安裝 Python，再執行 python -m pip install edge-tts。" });
    return;
  }
  const body = await collectBody(request, 1024 * 1024);
  let data;
  try {
    data = JSON.parse(body.toString("utf8"));
  } catch {
    sendJson(response, 400, { error: "旁白資料格式不正確。" });
    return;
  }
  const text = String(data.text || "").trim();
  const voice = allowedVoices.has(data.voice) ? data.voice : "zh-TW-HsiaoChenNeural";
  const rateValue = Math.max(-50, Math.min(50, Number(data.rate) || 0));
  const rate = `${rateValue >= 0 ? "+" : ""}${rateValue}%`;
  if (!text || text.length > 3000) {
    sendJson(response, 400, { error: "旁白文字需為 1 至 3000 個字元。" });
    return;
  }

  const id = `narration-${Date.now()}-${randomUUID().slice(0, 8)}`;
  const audioPath = path.join(generatedDir, `${id}.mp3`);
  const subtitlePath = path.join(generatedDir, `${id}.srt`);
  await runProcess(pythonPath, [
    "-m", "edge_tts",
    "--voice", voice,
    "--rate", rate,
    "--text", text,
    "--write-media", audioPath,
    "--write-subtitles", subtitlePath
  ]);
  sendJson(response, 200, {
    audioUrl: `/.generated/${path.basename(audioPath)}`,
    subtitleUrl: `/.generated/${path.basename(subtitlePath)}`,
    voice,
    rate: rateValue
  });
}

async function handleMp4(request, response) {
  const webm = await collectBody(request, 250 * 1024 * 1024);
  if (!webm.length) {
    sendJson(response, 400, { error: "沒有收到 WebM 影片資料。" });
    return;
  }
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), "motion-studio-"));
  const inputPath = path.join(tempDir, "input.webm");
  const outputPath = path.join(tempDir, "output.mp4");
  try {
    fs.writeFileSync(inputPath, webm);
    await runProcess(ffmpegPath, [
      "-y", "-i", inputPath,
      "-c:v", "libx264", "-preset", "medium", "-crf", "18",
      "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
      "-movflags", "+faststart", outputPath
    ]);
    const stat = fs.statSync(outputPath);
    response.writeHead(200, {
      "Content-Type": "video/mp4",
      "Content-Length": stat.size,
      "Content-Disposition": "attachment; filename=\"motion-studio.mp4\"",
      "Cache-Control": "no-store"
    });
    const stream = fs.createReadStream(outputPath);
    stream.pipe(response);
    stream.on("close", () => fs.rmSync(tempDir, { recursive: true, force: true }));
  } catch (error) {
    fs.rmSync(tempDir, { recursive: true, force: true });
    throw error;
  }
}

function serveFile(requestPath, response) {
  const relative = requestPath === "/" ? "app-local.html" : requestPath.replace(/^\/+/, "");
  const filePath = path.resolve(root, relative);
  const insideRoot = filePath === root || filePath.startsWith(`${root}${path.sep}`);
  if (!insideRoot || !fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    sendJson(response, 404, { error: "找不到檔案。" });
    return;
  }
  response.writeHead(200, {
    "Content-Type": mime[path.extname(filePath).toLowerCase()] || "application/octet-stream",
    "Cache-Control": "no-store"
  });
  fs.createReadStream(filePath).pipe(response);
}

const server = http.createServer(async (request, response) => {
  const requestPath = decodeURIComponent(new URL(request.url, `http://${request.headers.host}`).pathname);
  try {
    if (request.method === "GET" && requestPath === "/api/status") {
      sendJson(response, 200, {
        edgeTts: commandWorks(pythonPath, ["-c", "import edge_tts"]),
        ffmpeg: commandWorks(ffmpegPath, ["-version"]),
        maxNarrationLength: 3000
      });
      return;
    }
    if (request.method === "POST" && requestPath === "/api/tts") {
      await handleTts(request, response);
      return;
    }
    if (request.method === "POST" && requestPath === "/api/convert-mp4") {
      await handleMp4(request, response);
      return;
    }
    if (request.method !== "GET") {
      sendJson(response, 405, { error: "不支援這個請求方法。" });
      return;
    }
    serveFile(requestPath, response);
  } catch (error) {
    console.error(error);
    if (!response.headersSent) sendJson(response, 500, { error: error.message || "伺服器處理失敗。" });
    else response.destroy(error);
  }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`動態圖室：http://127.0.0.1:${port}`);
});
