// Estimate form handler for the Vercel version (same rules as site/send.php on Hostinger).
// Sends through an SMTP mailbox set in the Vercel project's Environment Variables:
//   SMTP_USER  (required) e.g. no-reply@riocleaningservice.com
//   SMTP_PASS  (required) that mailbox's password
//   SMTP_HOST  (default smtp.hostinger.com)   SMTP_PORT (default 465)   SMTP_SECURE ssl|tls|none (default ssl)
//   LEAD_TO    (default riocleaningservices.m@gmail.com, comma separated for more)
//   MAIL_FROM  (default = SMTP_USER)
// No dependencies: a small SMTP client built on Node's net/tls modules.
'use strict';
const net = require('net');
const tls = require('tls');
const crypto = require('crypto');

const PHONE = '(267) 694-4609';
const CALL = '<a href="tel:+12676944609">' + PHONE + '</a>';
const SERVICES = ['Recurring Cleaning', 'Deep Cleaning', 'Move-In Cleaning', 'Move-Out Cleaning', 'Carpet Cleaning', 'Not Sure Yet'];
const FREQ = ['Weekly', 'Biweekly', 'Monthly', 'One-Time'];
const BEDS = ['1', '2', '3', '4', '5 or more'];
const BATHS = ['1', '1.5', '2', '2.5', '3', '3.5', '4 or more'];
const hits = new Map(); // best-effort rate limit per warm instance

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (s) => String(s).replace(/[\r\n]+/g, ' ').trim();
const encHeader = (s) => (/[^\x20-\x7e]/.test(s) ? '=?UTF-8?B?' + Buffer.from(s).toString('base64') + '?=' : s);
const b64 = (s) => Buffer.from(s, 'utf8').toString('base64').replace(/.{76}/g, '$&\r\n');

function readBody(req) {
  if (req.body && typeof req.body === 'object') return Promise.resolve(req.body);
  return new Promise((resolve) => {
    let raw = '';
    req.on('data', (c) => { raw += c; if (raw.length > 50000) req.destroy(); });
    req.on('end', () => {
      try { resolve(/json/.test(req.headers['content-type'] || '') ? JSON.parse(raw) : Object.fromEntries(new URLSearchParams(raw))); }
      catch (e) { resolve({}); }
    });
  });
}

function smtpSend({ to, subject, html, text, replyTo, replyName }) {
  const host = process.env.SMTP_HOST || 'smtp.hostinger.com';
  const port = Number(process.env.SMTP_PORT || 465);
  const secure = (process.env.SMTP_SECURE || 'ssl').toLowerCase();
  const user = process.env.SMTP_USER;
  const pass = process.env.SMTP_PASS;
  const from = process.env.MAIL_FROM || user;
  if (!user || !pass) return Promise.reject(new Error('SMTP_USER / SMTP_PASS not set'));

  const boundary = 'b' + crypto.randomBytes(12).toString('hex');
  const headers = [
    'From: ' + encHeader('Rio Cleaning Website') + ' <' + clean(from) + '>',
    'To: ' + to.join(', '),
    'Subject: ' + encHeader(clean(subject)),
    'Date: ' + new Date().toUTCString(),
    'Message-ID: <' + crypto.randomBytes(10).toString('hex') + '@riocleaningservice.com>',
    'MIME-Version: 1.0',
    'Content-Type: multipart/alternative; boundary="' + boundary + '"',
  ];
  if (replyTo) headers.push('Reply-To: ' + (replyName ? encHeader(clean(replyName)) + ' ' : '') + '<' + clean(replyTo) + '>');
  const body = headers.join('\r\n') + '\r\n\r\n' +
    '--' + boundary + '\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n' + b64(text) + '\r\n' +
    '--' + boundary + '\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n' + b64(html) + '\r\n' +
    '--' + boundary + '--';

  return new Promise((resolve, reject) => {
    let sock = secure === 'ssl' ? tls.connect({ host, port, servername: host }) : net.connect({ host, port });
    let buf = '';
    let waiter = null;
    const timer = setTimeout(() => { sock.destroy(); reject(new Error('SMTP timeout')); }, 15000);
    // A reply is complete when its last line is "NNN text" (multi-line replies use "NNN-text").
    const flush = () => {
      if (!waiter || !buf.endsWith('\r\n')) return;
      const lines = buf.trim().split('\r\n');
      if (!/^\d{3}( |$)/.test(lines[lines.length - 1])) return;
      const w = waiter; const r = buf; waiter = null; buf = ''; w(r);
    };
    const onData = (d) => { buf += d.toString(); flush(); };
    sock.on('data', onData);
    sock.on('error', (e) => { clearTimeout(timer); reject(e); });
    const read = () => new Promise((r) => { waiter = r; flush(); });
    const cmd = async (line, expect) => {
      if (line !== null) sock.write(line + '\r\n');
      const reply = await read();
      const lines = reply.trim().split('\r\n');
      const code = Number(lines[lines.length - 1].slice(0, 3));
      if (!expect.includes(code)) throw new Error('SMTP ' + (line ? line.split(' ')[0] : 'greeting') + ': ' + reply.trim());
      return reply;
    };
    (async () => {
      await cmd(null, [220]);
      await cmd('EHLO riocleaningservice.com', [250]);
      if (secure === 'tls') {
        await cmd('STARTTLS', [220]);
        sock.removeListener('data', onData);
        sock = tls.connect({ socket: sock, servername: host });
        sock.on('data', onData);
        await new Promise((r, j) => { sock.once('secureConnect', r); sock.once('error', j); });
        await cmd('EHLO riocleaningservice.com', [250]);
      }
      await cmd('AUTH LOGIN', [334]);
      await cmd(Buffer.from(user).toString('base64'), [334]);
      await cmd(Buffer.from(pass).toString('base64'), [235]);
      await cmd('MAIL FROM:<' + clean(from) + '>', [250]);
      for (const r of to) await cmd('RCPT TO:<' + clean(r) + '>', [250, 251]);
      await cmd('DATA', [354]);
      await cmd(body.replace(/^\./gm, '..') + '\r\n.', [250]);
      sock.write('QUIT\r\n');
      sock.end();
    })().then(() => { clearTimeout(timer); resolve(true); }, (e) => { clearTimeout(timer); sock.destroy(); reject(e); });
  });
}

module.exports = async function handler(req, res) {
  const wantsJson = /application\/json/.test(req.headers.accept || '');
  const respond = (ok, message, errors, code) => {
    if (wantsJson) {
      res.statusCode = ok ? 200 : (code || 400);
      res.setHeader('Content-Type', 'application/json; charset=UTF-8');
      res.setHeader('Cache-Control', 'no-store');
      return res.end(JSON.stringify({ ok, message: message || '', errors: errors || {} }));
    }
    res.statusCode = 303;
    res.setHeader('Location', ok ? '/contact/?sent=1' : '/contact/?form_error=1#estimate');
    return res.end();
  };
  if (req.method !== 'POST') { res.statusCode = 303; res.setHeader('Location', '/contact/'); return res.end(); }

  const b = await readBody(req);
  const val = (k, max) => String(b[k] == null ? '' : b[k]).replace(/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/g, '').trim().slice(0, max || 200);
  const pick = (v, list) => (list.includes(v) ? v : '');

  // spam: honeypot and minimum fill time get a silent success
  if (val('website')) return respond(true);
  const started = Number(val('started')) || 0;
  if (started && Date.now() - started < 2500) return respond(true);

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const now = Date.now();
  const recent = (hits.get(ip) || []).filter((t) => t > now - 600000);
  if (recent.length >= 5) return respond(false, 'Too many requests. Please call us at ' + CALL + '.', {}, 429);

  const d = {
    name: val('name', 80), phone: val('phone', 25), email: val('email', 120), zip: val('zip', 10),
    service: pick(val('service', 40), SERVICES), frequency: pick(val('frequency', 20), FREQ),
    bedrooms: pick(val('bedrooms', 12), BEDS), bathrooms: pick(val('bathrooms', 12), BATHS),
    contact_method: pick(val('contact_method', 20), ['Phone call', 'Email']) || 'Phone call',
    message: val('message', 1500), page: val('page', 60), page_url: val('page_url', 300),
  };
  const errors = {};
  if (d.name.length < 2) errors.name = 'Please enter your name.';
  let digits = d.phone.replace(/\D/g, '');
  if (digits.length === 11 && digits[0] === '1') digits = digits.slice(1);
  if (!/^[2-9]\d{2}[2-9]\d{6}$/.test(digits)) errors.phone = 'Please enter a valid 10-digit U.S. phone number.';
  else d.phone = '(' + digits.slice(0, 3) + ') ' + digits.slice(3, 6) + '-' + digits.slice(6);
  if (d.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email)) errors.email = 'Please enter a valid email address.';
  else if (!d.email && d.contact_method === 'Email') errors.email = 'Please enter your email so we can reply by email.';
  if (!/^\d{5}$/.test(d.zip)) errors.zip = 'Please enter a 5-digit ZIP code.';
  if (!d.service) errors.service = 'Please choose the type of cleaning.';
  if ((d.message.match(/https?:\/\/|www\./gi) || []).length > 2) errors.message = 'Please remove links from your message.';
  if (Object.keys(errors).length) return respond(false, 'Please check the highlighted fields.', errors, 422);
  recent.push(now);
  hits.set(ip, recent);

  const rows = [['Name', d.name], ['Phone', d.phone], ['Email', d.email || '—'], ['ZIP code', d.zip],
    ['Type of cleaning', d.service], ['Frequency', d.frequency || '—'], ['Bedrooms', d.bedrooms || '—'],
    ['Bathrooms', d.bathrooms || '—'], ['Preferred contact', d.contact_method], ['Details', d.message || '—'],
    ['Sent from', (d.page + ' ' + d.page_url).trim()]];
  const html = '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#16212c">' +
    '<h2 style="margin:0 0 6px;font-size:20px">New estimate request</h2>' +
    '<p style="margin:0 0 16px">Call back: <a href="tel:+1' + digits + '" style="font-weight:bold">' + esc(d.phone) + '</a></p>' +
    '<table cellpadding="8" cellspacing="0" style="border-collapse:collapse;max-width:640px">' +
    rows.map(([k, v]) => '<tr><td style="border-bottom:1px solid #e2d9ca;font-weight:bold;vertical-align:top;white-space:nowrap">' +
      esc(k) + '</td><td style="border-bottom:1px solid #e2d9ca">' + esc(v).replace(/\n/g, '<br>') + '</td></tr>').join('') +
    '</table><p style="color:#66707a;font-size:12px;margin-top:16px">Sent from riocleaningservice.com</p></div>';
  const text = 'New estimate request\n\n' + rows.map(([k, v]) => k + ': ' + v).join('\n') + '\n';
  const leadTo = (process.env.LEAD_TO || 'riocleaningservices.m@gmail.com').split(',').map((s) => s.trim()).filter(Boolean);

  try {
    await smtpSend({ to: leadTo, subject: 'New estimate request: ' + d.service + ' - ' + d.name, html, text,
      replyTo: d.email, replyName: d.name });
  } catch (e) {
    console.error('[Rio form] send failed:', e.message);
    return respond(false, 'Sorry, your request could not be sent right now. Please call us at ' + CALL + '.', {}, 500);
  }
  if (d.email) {
    const first = d.name.split(' ')[0];
    const reply = 'Hi ' + first + ',\n\nThank you for contacting Rio Cleaning Services. We received your request for ' +
      d.service.toLowerCase() + ' and will get back to you soon to confirm the details and prepare your estimate.\n\n' +
      'If you need us sooner, call ' + PHONE + '.\n\nRio Cleaning Services\nhttps://riocleaningservice.com\n';
    try {
      await smtpSend({ to: [d.email], subject: 'We received your estimate request - Rio Cleaning Services',
        html: '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#16212c">' +
          esc(reply).replace(/\n/g, '<br>') + '</div>', text: reply, replyTo: leadTo[0], replyName: 'Rio Cleaning Services' });
    } catch (e) { console.error('[Rio form] autoreply failed:', e.message); }
  }
  return respond(true, 'Thank you! Your estimate request was sent.');
};
