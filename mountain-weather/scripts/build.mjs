// Static site build: renders every page to plain HTML in dist/ (no runtime framework).
// Usage: node scripts/build.mjs   (set SITE_URL=https://your-domain.com to override the canonical domain)
import { mkdir, rm, cp, readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
const { SITE } = await import(pathToFileURL(path.join(root, 'src/config.mjs')));
const { renderPage } = await import(pathToFileURL(path.join(root, 'src/lib/layout.mjs')));

const PAGES = ['home', 'emergency', 'replacement', 'about', 'service-areas', 'contact', 'privacy', 'not-found'];

const hash = (s) => createHash('sha256').update(s).digest('hex').slice(0, 10);

function minifyCss(css) {
  return css
    .replace(/\/\*[\s\S]*?\*\//g, '')
    .replace(/\s+/g, ' ')
    .replace(/\s*([{};,>])\s*/g, '$1')
    .replace(/;}/g, '}')
    .trim();
}

/** Deterministic topographic contour texture (the “mountain” motif). */
function contours(stroke, opacity) {
  let seed = 7;
  const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const W = 1400;
  const H = 900;
  const peaks = [
    [260, 220, 8],
    [980, 300, 9],
    [620, 760, 7],
    [1300, 820, 5],
    [40, 820, 5],
  ];
  const paths = [];
  for (const [cx, cy, rings] of peaks) {
    const p1 = rand() * Math.PI * 2;
    const p2 = rand() * Math.PI * 2;
    for (let k = 1; k <= rings; k++) {
      const r = 30 * k + rand() * 8;
      const pts = [];
      const n = 30;
      for (let i = 0; i < n; i++) {
        const t = (i / n) * Math.PI * 2;
        const rr = r * (1 + 0.16 * Math.sin(3 * t + p1 + k * 0.18) + 0.08 * Math.sin(5 * t + p2 - k * 0.11));
        pts.push([cx + rr * Math.cos(t), cy + rr * 0.78 * Math.sin(t)]);
      }
      // Closed Catmull-Rom → cubic Bézier
      let d = `M${Math.round(pts[0][0])} ${Math.round(pts[0][1])}`;
      for (let i = 0; i < n; i++) {
        const p0 = pts[(i - 1 + n) % n];
        const a = pts[i];
        const b = pts[(i + 1) % n];
        const p3 = pts[(i + 2) % n];
        const c1 = [a[0] + (b[0] - p0[0]) / 6, a[1] + (b[1] - p0[1]) / 6];
        const c2 = [b[0] - (p3[0] - a[0]) / 6, b[1] - (p3[1] - a[1]) / 6];
        d += `C${[...c1, ...c2, ...b].map(Math.round).join(' ')}`;
      }
      paths.push(`<path d="${d}Z"/>`);
    }
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}"><g fill="none" stroke="${stroke}" stroke-opacity="${opacity}" stroke-width="1.2">${paths.join('')}</g></svg>`;
}

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });
await cp(path.join(root, 'public'), dist, { recursive: true });

// Hashed CSS/JS for long-term caching (vercel.json marks /assets/* immutable).
const css = minifyCss(await readFile(path.join(root, 'src/styles.css'), 'utf8'));
const js = await readFile(path.join(root, 'src/main.js'), 'utf8');
const cssName = `assets/css/styles.${hash(css)}.css`;
const jsName = `assets/js/main.${hash(js)}.js`;
await mkdir(path.join(dist, 'assets/css'), { recursive: true });
await mkdir(path.join(dist, 'assets/js'), { recursive: true });
await writeFile(path.join(dist, cssName), css);
await writeFile(path.join(dist, jsName), js);
await writeFile(path.join(dist, 'assets/img/contours.svg'), contours('#11648a', 0.13));
await writeFile(path.join(dist, 'assets/img/contours-light.svg'), contours('#ffffff', 0.06));
const assets = { css: `/${cssName}`, js: `/${jsName}` };

const sitemap = [];
for (const name of PAGES) {
  const mod = (await import(pathToFileURL(path.join(root, `src/pages/${name}.mjs`)))).default;
  const rendered = mod.render();
  const html = renderPage({ ...mod, ...rendered }, assets);
  const file = mod.output ?? (mod.path === '/' ? 'index.html' : `${mod.path.slice(1)}.html`);
  await writeFile(path.join(dist, file), html);
  if (mod.sitemap !== false && !mod.noindex) sitemap.push(mod.path);
  console.log(`  ${file.padEnd(32)} ${(html.length / 1024).toFixed(1)} KB`);
}

await writeFile(
  path.join(dist, 'sitemap.xml'),
  `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${sitemap
  .map((p) => `  <url><loc>${SITE.url}${p === '/' ? '/' : p}</loc><lastmod>${SITE.updated}</lastmod></url>`)
  .join('\n')}
</urlset>
`
);
await writeFile(path.join(dist, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${SITE.url}/sitemap.xml\n`);
await writeFile(
  path.join(dist, 'site.webmanifest'),
  JSON.stringify(
    {
      name: SITE.legalishName,
      short_name: SITE.name,
      start_url: '/',
      display: 'browser',
      background_color: '#ffffff',
      theme_color: '#0b2433',
      icons: [
        { src: '/assets/brand/icon-192.png', sizes: '192x192', type: 'image/png' },
        { src: '/assets/brand/icon-512.png', sizes: '512x512', type: 'image/png' },
      ],
    },
    null,
    2
  ) + '\n'
);

console.log(`Built ${PAGES.length} pages → dist/  (site URL: ${SITE.url})`);
if (!SITE.license.number || !SITE.license.masterName) {
  console.warn('WARNING: src/config.mjs → license is empty. New Jersey requires the master HVACR contractor name and license number on advertising.');
}
