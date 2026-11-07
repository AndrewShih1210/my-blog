// Learning example: verified LINE ingress, fixed reply, optional signed GAS log.
import http from 'node:http';
import { createHmac, timingSafeEqual } from 'node:crypto';
import { pathToFileURL } from 'node:url';

export function validSignature(raw, signature, secret) {
  if (typeof signature !== 'string' || !secret) return false;
  const expected = createHmac('sha256', secret).update(raw).digest('base64');
  const a = Buffer.from(signature); const b = Buffer.from(expected);
  return a.length === b.length && timingSafeEqual(a, b);
}

export function createBot(env, fetcher = fetch, log = console) {
  if (!env.LINE_CHANNEL_SECRET || !env.LINE_CHANNEL_ACCESS_TOKEN) {
    throw new Error('Set LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN');
  }
  if (env.GAS_LOG_URL && (!env.RELAY_SECRET || !/^https:\/\/script\.google\.com\/macros\/s\/[^/]+\/exec$/.test(env.GAS_LOG_URL))) {
    throw new Error('GAS logging needs a valid /exec URL and RELAY_SECRET');
  }
  // This bounded in-memory cache is NOT durable deduplication across instances.
  const recent = new Map();
  const pending = new Map();
  async function processEvent(event) {
    if (event.type !== 'message' || event.message?.type !== 'text') return;
    if (!event.replyToken || typeof event.webhookEventId !== 'string') return;
    const id = event.webhookEventId;
    const now = Date.now();
    for (const [key, expiry] of recent) if (expiry < now) recent.delete(key);
    if (recent.has(id)) return;
    if (pending.has(id)) return pending.get(id);
    const task = (async () => {
      const response = await fetcher('https://api.line.me/v2/bot/message/reply', {
        method: 'POST', headers: { 'Content-Type': 'application/json',
          Authorization: `Bearer ${env.LINE_CHANNEL_ACCESS_TOKEN}` },
        body: JSON.stringify({ replyToken: event.replyToken,
          messages: [{ type: 'text', text: '收到訊息了！Your bot is connected.' }] }),
        signal: AbortSignal.timeout(8000)
      });
      if (!response.ok) throw new Error(`LINE_REPLY_HTTP_${response.status}`);
      recent.set(id, now + 10 * 60 * 1000);
      if (recent.size > 2000) recent.delete(recent.keys().next().value);
      if (env.GAS_LOG_URL) {
        // Do not send user ID, message text, reply token or access token to Sheets.
        const payload = JSON.stringify({ eventId: id, type: 'text', status: 'replied' });
        const timestamp = Date.now();
        const signature = createHmac('sha256', env.RELAY_SECRET)
          .update(`${timestamp}.${payload}`).digest('base64');
        try {
          const result = await fetcher(env.GAS_LOG_URL, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ timestamp, payload, signature }),
            redirect: 'follow', signal: AbortSignal.timeout(8000)
          });
          if (!result.ok || !(await result.json()).ok) throw new Error('GAS rejected log');
        } catch {
          // Reply has already succeeded: do not retry the reply just for logging.
          log.warn('GAS_LOG_FAILED: reply sent; record may be missing');
        }
      }
    })();
    pending.set(id, task);
    try { await task; } finally { pending.delete(id); }
  }
  return http.createServer(async (req, res) => {
    const answer = (status, message) => {
      res.writeHead(status, { 'Content-Type': 'text/plain; charset=utf-8' }); res.end(message);
    };
    if (req.method === 'GET' && req.url === '/healthz') return answer(200, 'ok');
    if (req.method !== 'POST' || req.url !== '/webhook') return answer(404, 'not found');
    let raw;
    try {
      const chunks = []; let size = 0;
      for await (const chunk of req) {
        size += chunk.length;
        if (size > 1024 * 1024) return answer(413, 'payload too large');
        chunks.push(chunk);
      }
      raw = Buffer.concat(chunks);
    } catch { return answer(400, 'invalid body'); }
    if (!validSignature(raw, req.headers['x-line-signature'], env.LINE_CHANNEL_SECRET)) {
      return answer(401, 'invalid signature');
    }
    let body;
    try { body = JSON.parse(raw.toString('utf8')); } catch { return answer(400, 'invalid JSON'); }
    if (!body || !Array.isArray(body.events) || body.events.length > 100 ||
        body.events.some(event => !event || typeof event !== 'object')) {
      return answer(400, 'invalid events');
    }
    try {
      // Empty events is LINE's verification request; no reply call is needed.
      await Promise.all(body.events.map(processEvent));
      answer(200, 'ok');
    } catch {
      log.error('LINE_REPLY_FAILED: inspect configuration, quota and network');
      answer(502, 'reply failed');
    }
  });
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const server = createBot(process.env);
  server.requestTimeout = 20000;
  server.listen(Number(process.env.PORT || 8080), '0.0.0.0', () => console.log('Bot server ready'));
}
