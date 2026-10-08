// Local preview of dist/ with the same clean URLs as Vercel (/about → about.html).
// Usage: node scripts/serve.mjs [port]
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { gzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist');
const port = Number(process.argv[2] || 4173);
// Apply the same global headers as production (including the Content-Security-Policy).
const vercel = JSON.parse(await readFile(path.join(dist, '../vercel.json'), 'utf8'));
const globalHeaders = Object.fromEntries(
  vercel.headers.find((h) => h.source === '/(.*)').headers.map((h) => [h.key.toLowerCase(), h.value])
);
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml',
  '.webp': 'image/webp', '.avif': 'image/avif', '.png': 'image/png', '.jpg': 'image/jpeg', '.woff2': 'font/woff2',
  '.xml': 'application/xml', '.txt': 'text/plain', '.webmanifest': 'application/manifest+json',
};

async function resolve(urlPath) {
  const clean = decodeURIComponent(urlPath.split('?')[0]).replace(/\/+$/, '') || '/index';
  for (const candidate of [clean, `${clean}.html`]) {
    const file = path.join(dist, candidate);
    if (!file.startsWith(dist)) return null;
    try { if ((await stat(file)).isFile()) return file; } catch {}
  }
  return null;
}

createServer(async (req, res) => {
  const file = await resolve(req.url);
  if (!file) {
    res.writeHead(404, { 'content-type': TYPES['.html'] });
    return res.end(await readFile(path.join(dist, '404.html')));
  }
  const type = TYPES[path.extname(file)] ?? 'application/octet-stream';
  const headers = { ...globalHeaders, 'content-type': type };
  // Mirror production: long cache for fingerprinted assets, compression for text.
  if (req.url.startsWith('/assets/')) headers['cache-control'] = 'public, max-age=31536000, immutable';
  let body = await readFile(file);
  if (/text|javascript|svg|json|xml/.test(type) && /gzip/.test(req.headers['accept-encoding'] ?? '')) {
    body = gzipSync(body);
    headers['content-encoding'] = 'gzip';
  }
  res.writeHead(200, headers);
  res.end(body);
}).listen(port, () => console.log(`Preview: http://localhost:${port}`));
