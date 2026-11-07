import test from 'node:test';
import assert from 'node:assert/strict';
import { createHmac } from 'node:crypto';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const source = readFileSync(new URL('./Code.gs', import.meta.url), 'utf8');
const NOW = Date.parse('2026-11-07T00:00:00.000Z');
const SECRET = 'local-test-relay-secret-not-a-real-credential';
const HEADER = ['receivedAt', 'eventId', 'type', 'status'];
const REJECTED = { ok: false, error: 'REJECTED_OR_UNAVAILABLE' };
const row = (eventId = 'event-1') => ({ eventId, type: 'text', status: 'replied' });

function signed(data = row(), timestamp = NOW, secret = SECRET) {
  const payload = JSON.stringify(data);
  const signature = createHmac('sha256', secret)
    .update(`${timestamp}.${payload}`, 'utf8').digest('base64');
  return { timestamp, payload, signature };
}

function harness({ rows = [HEADER], missingSheet = false, lockFails = false } = {}) {
  const stored = rows.map(values => [...values]);
  const state = { writes: 0, flushes: 0, opens: 0, waits: [], releases: 0, held: false };
  const sheet = {
    getLastRow: () => stored.length,
    appendRow(values) { stored.push(Array.from(values)); state.writes++; },
    getRange(start, column, height, width) {
      assert(start >= 1 && column >= 1 && height >= 1 && width >= 1);
      return {
        getValues: () => stored.slice(start - 1, start - 1 + height)
          .map(values => values.slice(column - 1, column - 1 + width)),
        setValues(values) {
          assert.equal(state.held, true, 'writes must hold the script lock');
          assert.equal(values.length, height);
          values.forEach((cells, offset) => {
            assert.equal(cells.length, width);
            const target = stored[start - 1 + offset] ??= [];
            cells.forEach((value, index) => { target[column - 1 + index] = value; });
          });
          state.writes++;
        },
        createTextFinder(needle) {
          let exact = false;
          return {
            matchEntireCell(value) { exact = value; return this; },
            findNext() {
              assert.equal(exact, true, 'deduplication must match the entire cell');
              return stored.slice(start - 1, start - 1 + height)
                .some(values => String(values[column - 1]) === String(needle)) ? {} : null;
            }
          };
        }
      };
    }
  };
  const props = { SHEET_ID: 'local-sheet-id', RELAY_SECRET: SECRET };
  const context = vm.createContext({
    Date: class extends Date {
      constructor(...args) { super(...(args.length ? args : [NOW])); }
      static now() { return NOW; }
    },
    PropertiesService: { getScriptProperties: () => ({ getProperty: key => props[key] }) },
    Utilities: {
      Charset: { UTF_8: 'UTF-8' },
      computeHmacSha256Signature(message, secret, charset) {
        assert.equal(charset, 'UTF-8');
        // GAS returns signed bytes; Buffer.from restores their unsigned representation.
        return Array.from(createHmac('sha256', secret).update(message, 'utf8').digest(),
          value => value > 127 ? value - 256 : value);
      },
      base64Encode: bytes => Buffer.from(bytes).toString('base64')
    },
    LockService: { getScriptLock: () => ({
      waitLock(ms) {
        state.waits.push(ms);
        if (lockFails) throw new Error('mock lock timeout');
        state.held = true;
      },
      hasLock: () => state.held,
      releaseLock() { assert(state.held); state.held = false; state.releases++; }
    }) },
    SpreadsheetApp: {
      openById(id) {
        assert.equal(id, props.SHEET_ID); state.opens++;
        return {
          getSheetByName(name) { assert.equal(name, 'Events'); return missingSheet ? null : sheet; },
          insertSheet(name) { assert.equal(name, 'Events'); missingSheet = false; return sheet; }
        };
      },
      flush() { state.flushes++; }
    },
    ContentService: {
      MimeType: { JSON: 'application/json' },
      createTextOutput(text) {
        return { text, setMimeType(mime) { this.mime = mime; return this; } };
      }
    }
  });
  vm.runInContext(source, context, { timeout: 1000, filename: 'Code.gs' });
  function invoke(envelope) {
    context.request = { postData: { contents: JSON.stringify(envelope) } };
    const output = vm.runInContext('doPost(request)', context, { timeout: 1000 });
    assert.equal(output.mime, 'application/json');
    return JSON.parse(output.text);
  }
  return { invoke, stored, state, context };
}

test('valid relay HMAC writes only the four approved columns and releases the lock', () => {
  const h = harness();
  assert.deepEqual(h.invoke(signed()), { ok: true });
  assert.deepEqual(h.stored, [HEADER, [new Date(NOW).toISOString(), 'event-1', 'text', 'replied']]);
  assert.equal(h.state.flushes, 1);
  assert.deepEqual(h.state.waits, [5000]);
  assert.equal(h.state.releases, 1);
  assert.equal(h.state.held, false);
});

test('payload, timestamp, signature tampering and wrong shared secret are rejected before Sheets access', () => {
  const original = signed();
  for (const envelope of [
    { ...original, payload: JSON.stringify(row('tampered')) },
    { ...original, timestamp: NOW - 1 },
    { ...original, signature: (original.signature[0] === 'A' ? 'B' : 'A') + original.signature.slice(1) },
    { ...original, signature: 'short' },
    signed(row(), NOW, 'wrong-secret')
  ]) {
    const h = harness();
    assert.deepEqual(h.invoke(envelope), REJECTED);
    assert.equal(h.state.opens, 0);
    assert.equal(h.state.writes, 0);
  }
});

test('timestamp window accepts exactly five minutes and rejects older or future envelopes beyond it', () => {
  for (const offset of [-300000, 300000]) {
    assert.deepEqual(harness().invoke(signed(row(), NOW + offset)), { ok: true });
  }
  for (const offset of [-300001, 300001]) {
    const h = harness();
    assert.deepEqual(h.invoke(signed(row(), NOW + offset)), REJECTED);
    assert.equal(h.state.opens, 0);
  }
});

test('replaying an event does not write twice; substring IDs remain distinct', () => {
  const h = harness();
  assert.deepEqual(h.invoke(signed()), { ok: true });
  assert.deepEqual(h.invoke(signed()), { ok: true, duplicate: true });
  assert.deepEqual(h.invoke(signed(row('event-10'))), { ok: true });
  assert.equal(h.state.writes, 2);
  assert.equal(h.state.flushes, 2);
  assert.equal(h.state.releases, 3);
});

test('incorrect worksheet header or missing Events sheet rejects writes and releases the lock', () => {
  for (const options of [{ rows: [['eventId', 'receivedAt', 'type', 'status']] }, { missingSheet: true }]) {
    const h = harness(options);
    assert.deepEqual(h.invoke(signed()), REJECTED);
    assert.equal(h.state.writes, 0);
    assert.equal(h.state.releases, 1);
    assert.equal(h.state.held, false);
  }
});

test('5000-record guard excludes the header, permits record 5000, and still recognizes duplicates at capacity', () => {
  const rows = [HEADER, ...Array.from({ length: 4999 }, (_, i) => ['time', `seed-${i}`, 'text', 'replied'])];
  const h = harness({ rows });
  assert.deepEqual(h.invoke(signed(row('record-5000'))), { ok: true });
  assert.equal(h.stored.length, 5001);
  assert.deepEqual(h.invoke(signed(row('record-5001'))), { ok: false, error: 'CLASSROOM_LOG_CAP' });
  assert.deepEqual(h.invoke(signed(row('record-5000'))), { ok: true, duplicate: true });
  assert.equal(h.state.writes, 1);
  assert.equal(h.state.flushes, 1);
  assert.equal(h.state.releases, 3);
});

test('lock timeout refuses writes without releasing an unowned lock', () => {
  const h = harness({ lockFails: true });
  assert.deepEqual(h.invoke(signed()), REJECTED);
  assert.equal(h.state.writes, 0);
  assert.equal(h.state.releases, 0);
});

test('formula-like event ID is rejected even with a valid HMAC', () => {
  const h = harness();
  assert.deepEqual(h.invoke(signed(row('=IMPORTXML()'))), REJECTED);
  assert.equal(h.state.opens, 0);
});

test('setup creates the header once', () => {
  const h = harness({ rows: [], missingSheet: true });
  vm.runInContext('setupLogSheet(); setupLogSheet();', h.context, { timeout: 1000 });
  assert.deepEqual(h.stored, [HEADER]);
  assert.equal(h.state.writes, 1);
});

test('eventId must be a string, not a coerced number', () => {
  const h = harness();
  assert.deepEqual(h.invoke(signed(row(123))), REJECTED);
  assert.equal(h.state.writes, 0);
});
