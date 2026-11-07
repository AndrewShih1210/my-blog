import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { createBot, validSignature } from './server.mjs';
const env = { LINE_CHANNEL_SECRET: 'test-secret-not-real', LINE_CHANNEL_ACCESS_TOKEN: 'test-token-not-real' };
const sign = raw => createHmac('sha256', env.LINE_CHANNEL_SECRET).update(raw).digest('base64');
const event = id => ({ type: 'message', webhookEventId: id, replyToken: 'test-reply',
  source: { userId: 'MUST_NOT_BE_LOGGED' }, message: { type: 'text', text: 'PRIVATE_TEXT' } });
test('signature binds exact raw bytes', () => {
  assert(validSignature(Buffer.from('{}'), sign('{}'), env.LINE_CHANNEL_SECRET));
  assert(!validSignature(Buffer.from('{ }'), sign('{}'), env.LINE_CHANNEL_SECRET));
  assert(!validSignature(Buffer.from('{}'), '', env.LINE_CHANNEL_SECRET));
});
test('webhook, duplicate, non-text, log privacy and failures', async t => {
  let calls = []; let failReply = false; let failLog = false; let warnings = 0;
  const fetcher = async (url, options) => {
    calls.push({ url, options });
    if (url.includes('api.line.me')) return { ok: !failReply, status: failReply ? 401 : 200 };
    return { ok: true, json: async () => ({ ok: !failLog }) };
  };
  const logEnv = { ...env, GAS_LOG_URL: 'https://script.google.com/macros/s/TEST/exec', RELAY_SECRET: 'test-relay' };
  const server = createBot(logEnv, fetcher, { warn: () => warnings++, error() {} });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  t.after(() => new Promise(resolve => server.close(resolve)));
  const base = `http://127.0.0.1:${server.address().port}`;
  async function send(body, signature = sign(body)) {
    return fetch(base + '/webhook', { method: 'POST', headers: { 'x-line-signature': signature }, body });
  }
  assert.equal((await fetch(base + '/healthz')).status, 200);
  assert.equal((await send('{}', 'wrong')).status, 401);
  assert.equal((await send('{')).status, 400);
  assert.equal((await send('{}')).status, 400);
  assert.equal((await send('null')).status, 400);
  assert.equal((await send('{"events":[null]}')).status, 400);
  assert.equal((await send('{"events":[]}')).status, 200);
  assert.equal(calls.length, 0);
  const body = JSON.stringify({ events: [event('event-1')] });
  assert.equal((await send(body)).status, 200);
  assert.equal(calls.length, 2);
  const envelope = JSON.parse(calls[1].options.body);
  assert(!envelope.payload.includes('PRIVATE_TEXT'));
  assert(!envelope.payload.includes('MUST_NOT_BE_LOGGED'));
  assert(validSignature(Buffer.from(`${envelope.timestamp}.${envelope.payload}`), envelope.signature, 'test-relay'));
  await send(body); assert.equal(calls.length, 2);
  await send(JSON.stringify({ events: [{ type: 'follow' }] })); assert.equal(calls.length, 2);
  failLog = true;
  assert.equal((await send(JSON.stringify({ events: [event('event-2')] }))).status, 200);
  assert.equal(warnings, 1);
  failReply = true;
  assert.equal((await send(JSON.stringify({ events: [event('event-3')] }))).status, 502);
});
