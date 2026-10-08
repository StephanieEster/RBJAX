// Pre-publish QA for dist/: SEO basics, links, images, headings, structured data.
// Usage: node scripts/check.mjs   (run after the build; exits with code 1 on any error)
import { readdir, readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const dist = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist');
const errors = [];
const warn = [];
const err = (file, msg) => errors.push(`${file}: ${msg}`);

const decode = (s) =>
  s.replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>');
const text = (s) => decode(s.replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
const exists = async (p) => stat(p).then((s) => s.isFile(), () => false);

async function resolveInternal(href) {
  const clean = href.split('#')[0].split('?')[0];
  if (clean === '' || clean === '/') return exists(path.join(dist, 'index.html'));
  const p = path.join(dist, clean);
  return (await exists(p)) || (await exists(`${p}.html`));
}

const files = (await readdir(dist)).filter((f) => f.endsWith('.html'));
const robots = await readFile(path.join(dist, 'robots.txt'), 'utf8');
const sitemap = await readFile(path.join(dist, 'sitemap.xml'), 'utf8');
const siteUrl = (robots.match(/Sitemap: (.+)\/sitemap\.xml/) || [])[1];
if (!siteUrl) errors.push('robots.txt: missing Sitemap line');

for (const file of files) {
  const html = await readFile(path.join(dist, file), 'utf8');
  const noindex = /<meta name="robots" content="noindex/.test(html);

  const h1s = html.match(/<h1[\s>]/g) || [];
  if (h1s.length !== 1) err(file, `expected 1 <h1>, found ${h1s.length}`);

  const title = text((html.match(/<title>([\s\S]*?)<\/title>/) || [])[1] || '');
  if (!title) err(file, 'missing <title>');
  else if (!noindex && (title.length < 30 || title.length > 65)) warn.push(`${file}: title length ${title.length} — "${title}"`);

  const desc = decode((html.match(/<meta name="description" content="([^"]*)"/) || [])[1] || '');
  if (!desc) err(file, 'missing meta description');
  else if (!noindex && (desc.length < 70 || desc.length > 165)) warn.push(`${file}: description length ${desc.length}`);

  if (!noindex) {
    const canonical = (html.match(/<link rel="canonical" href="([^"]+)"/) || [])[1];
    const expected = `${siteUrl}${file === 'index.html' ? '/' : `/${file.replace(/\.html$/, '')}`}`;
    if (canonical !== expected) err(file, `canonical ${canonical} ≠ ${expected}`);
    if (!sitemap.includes(`<loc>${expected}</loc>`)) err(file, 'not listed in sitemap.xml');
    if (!/property="og:image"/.test(html)) err(file, 'missing og:image');
  }

  // Headings never skip a level.
  const levels = [...html.matchAll(/<h([1-6])[\s>]/g)].map((m) => +m[1]);
  levels.forEach((l, i) => {
    if (i > 0 && l > levels[i - 1] + 1) err(file, `heading jumps from h${levels[i - 1]} to h${l}`);
  });

  // Images
  for (const [tag] of html.matchAll(/<img\b[^>]*>/g)) {
    if (!/\balt="/.test(tag)) err(file, `img without alt: ${tag.slice(0, 80)}`);
    if (/\balt=""/.test(tag) && !/class="brand-mark"/.test(tag)) err(file, `empty alt on non-decorative img: ${tag.slice(0, 80)}`);
    if (!/\bwidth="\d+"/.test(tag) || !/\bheight="\d+"/.test(tag)) err(file, `img without width/height: ${tag.slice(0, 80)}`);
    const src = (tag.match(/\bsrc="([^"]+)"/) || [])[1];
    if (src && src.startsWith('/') && !(await exists(path.join(dist, src)))) err(file, `missing image ${src}`);
  }
  for (const [, set] of html.matchAll(/srcset="([^"]+)"/g)) {
    for (const part of set.split(',')) {
      const u = part.trim().split(' ')[0];
      if (u.startsWith('/') && !(await exists(path.join(dist, u)))) err(file, `missing srcset file ${u}`);
    }
  }

  // Links
  for (const [tag, href] of html.matchAll(/<a\b[^>]*href="([^"]*)"[^>]*>/g)) {
    if (href === '' || href === '#') err(file, `empty link: ${tag.slice(0, 80)}`);
    else if (href.startsWith('/') && !(await resolveInternal(href))) err(file, `broken internal link ${href}`);
    else if (/^https?:/.test(href) && !href.startsWith(siteUrl) && /target="_blank"/.test(tag) && !/rel="[^"]*noopener/.test(tag)) err(file, `target=_blank without noopener: ${href}`);
    else if (href.startsWith('sms:') && !href.startsWith('sms:+18622708862')) err(file, `unexpected sms number ${href}`);
    else if (href.startsWith('tel:') && href !== 'tel:+18622708862') err(file, `unexpected tel ${href}`);
    else if (href.includes('wa.me') && !href.startsWith('https://wa.me/18622708862')) err(file, `unexpected WhatsApp link ${href}`);
  }
  for (const [, ref] of html.matchAll(/<(?:link|script)\b[^>]*(?:href|src)="(\/[^"]+)"/g)) {
    if (!(await exists(path.join(dist, ref)))) err(file, `missing asset ${ref}`);
  }

  // Duplicate ids
  const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]);
  const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dup.length) err(file, `duplicate ids: ${[...new Set(dup)].join(', ')}`);

  // Leftovers
  if (/lorem ipsum|\bTODO\b|\[PREENCHER|placeholder text/i.test(html)) err(file, 'placeholder text found');

  // Structured data
  const ld = (html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/) || [])[1];
  if (!ld) { err(file, 'missing JSON-LD'); continue; }
  let graph;
  try { graph = JSON.parse(ld)['@graph']; } catch (e) { err(file, `invalid JSON-LD: ${e.message}`); continue; }
  if (!graph.some((n) => n['@id'] === `${siteUrl}/#organization`)) err(file, 'JSON-LD missing organization node');
  if (/streetAddress|273 Devon/i.test(ld) || /273 Devon/i.test(html)) err(file, 'street address must not be published');
  const faqNode = graph.find((n) => n['@type'] === 'FAQPage');
  const visibleQs = [...html.matchAll(/<summary><h3>([\s\S]*?)<\/h3>/g)].map((m) => text(m[1]));
  if (faqNode) {
    const schemaQs = faqNode.mainEntity.map((q) => q.name);
    if (JSON.stringify(schemaQs) !== JSON.stringify(visibleQs)) err(file, 'FAQPage questions differ from visible FAQ');
    const visibleAs = [...html.matchAll(/<div class="faq-answer"><p>([\s\S]*?)<\/p><\/div>/g)].map((m) => text(m[1]));
    const schemaAs = faqNode.mainEntity.map((q) => q.acceptedAnswer.text);
    if (JSON.stringify(schemaAs) !== JSON.stringify(visibleAs)) err(file, 'FAQPage answers differ from visible FAQ');
  } else if (visibleQs.length) err(file, 'visible FAQ without FAQPage schema');
  const crumbs = graph.find((n) => n['@type'] === 'BreadcrumbList');
  if (crumbs && !/class="breadcrumbs"/.test(html)) err(file, 'BreadcrumbList schema without visible breadcrumbs');
}

// Inline scripts must match the CSP hashes in vercel.json, or browsers will block them.
const vercel = JSON.parse(await readFile(path.join(dist, '../vercel.json'), 'utf8'));
const csp = JSON.stringify(vercel.headers);
for (const file of files) {
  const html = await readFile(path.join(dist, file), 'utf8');
  for (const [, body] of html.matchAll(/<script>([\s\S]*?)<\/script>/g)) {
    const h = createHash('sha256').update(body).digest('base64');
    if (!csp.includes(`'sha256-${h}'`)) err(file, `inline script not allowed by CSP (sha256-${h})`);
  }
}

for (const [, loc] of sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)) {
  if (!(await resolveInternal(loc.replace(siteUrl, '') || '/'))) errors.push(`sitemap.xml: ${loc} has no page`);
}

warn.forEach((w) => console.log(`warn  ${w}`));
errors.forEach((e) => console.log(`ERROR ${e}`));
console.log(`\nChecked ${files.length} pages: ${errors.length} error(s), ${warn.length} warning(s).`);
process.exit(errors.length ? 1 : 0);
