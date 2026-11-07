// GAS is a signed log sink, NOT the public LINE webhook signature verifier.
function jsonOutput_(value) {
  return ContentService.createTextOutput(JSON.stringify(value))
    .setMimeType(ContentService.MimeType.JSON);
}

function setupLogSheet() {
  var props = PropertiesService.getScriptProperties();
  var book = SpreadsheetApp.openById(props.getProperty('SHEET_ID'));
  var sheet = book.getSheetByName('Events') || book.insertSheet('Events');
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(['receivedAt', 'eventId', 'type', 'status']);
  }
}

function doPost(e) {
  var lock;
  try {
    var props = PropertiesService.getScriptProperties();
    var secret = props.getProperty('RELAY_SECRET');
    if (!secret || !props.getProperty('SHEET_ID')) throw new Error('configuration');
    var raw = e && e.postData && e.postData.contents;
    if (!raw || raw.length > 4096) throw new Error('body');
    var envelope = JSON.parse(raw);
    if (!Number.isSafeInteger(envelope.timestamp) ||
        Math.abs(Date.now() - envelope.timestamp) > 300000 ||
        typeof envelope.payload !== 'string' ||
        typeof envelope.signature !== 'string') throw new Error('envelope');
    var expected = Utilities.base64Encode(Utilities.computeHmacSha256Signature(
      String(envelope.timestamp) + '.' + envelope.payload, secret, Utilities.Charset.UTF_8));
    if (expected.length !== envelope.signature.length) throw new Error('signature');
    var mismatch = 0;
    for (var i = 0; i < expected.length; i++) {
      mismatch |= expected.charCodeAt(i) ^ envelope.signature.charCodeAt(i);
    }
    if (mismatch !== 0) throw new Error('signature');
    var row = JSON.parse(envelope.payload);
    // Restrict stored strings; never write untrusted formulas or message text.
    if (typeof row.eventId !== 'string' || !/^[A-Za-z0-9_-]{1,128}$/.test(row.eventId) ||
        row.type !== 'text' || row.status !== 'replied') throw new Error('schema');
    lock = LockService.getScriptLock();
    lock.waitLock(5000);
    var sheet = SpreadsheetApp.openById(props.getProperty('SHEET_ID')).getSheetByName('Events');
    if (!sheet || sheet.getRange(1, 1, 1, 4).getValues()[0].join('|') !==
        'receivedAt|eventId|type|status') throw new Error('sheet setup');
    var last = sheet.getLastRow();
    // Full-column lookup is acceptable only for this capped classroom log.
    if (last > 1 && sheet.getRange(2, 2, last - 1, 1).createTextFinder(row.eventId)
        .matchEntireCell(true).findNext()) return jsonOutput_({ ok: true, duplicate: true });
    if (last >= 5001) return jsonOutput_({ ok: false, error: 'CLASSROOM_LOG_CAP' });
    sheet.getRange(last + 1, 1, 1, 4).setValues([
      [new Date().toISOString(), row.eventId, row.type, row.status]
    ]);
    SpreadsheetApp.flush();
    return jsonOutput_({ ok: true });
  } catch (error) {
    // TextOutput cannot set a custom HTTP status. The caller MUST read ok.
    return jsonOutput_({ ok: false, error: 'REJECTED_OR_UNAVAILABLE' });
  } finally {
    if (lock && lock.hasLock()) lock.releaseLock();
  }
}
