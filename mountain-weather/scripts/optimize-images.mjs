// Generates responsive AVIF/WebP photo variants, brand assets and icons.
//
// Usage:  npm install && node scripts/optimize-images.mjs <photos-dir> <brand-dir>
//   <photos-dir>  full-size JPGs named after the image keys (see CREDITS.md)
//   <brand-dir>   logo-full.png, logo-emblem.png, icon-tile.png (transparent PNGs)
//
// Output goes to public/assets and src/data/images.json (read by the build).
import sharp from 'sharp';
import { readdir, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const [photosDir, brandDir] = process.argv.slice(2);
if (!photosDir || !brandDir) {
  console.error('Usage: node scripts/optimize-images.mjs <photos-dir> <brand-dir>');
  process.exit(1);
}

const imgOut = path.join(root, 'public/assets/img');
const brandOut = path.join(root, 'public/assets/brand');
await mkdir(imgOut, { recursive: true });
await mkdir(brandOut, { recursive: true });

// The hero photo gets a larger top width; everything else tops out at 1600px.
const WIDTHS = { default: [480, 800, 1200, 1600], 'hvac-technician-condenser': [640, 960, 1280, 1920] };

const manifest = {};
for (const file of (await readdir(photosDir)).filter((f) => /\.(jpe?g|png)$/i.test(f)).sort()) {
  const key = file.replace(/\.[^.]+$/, '');
  const input = sharp(path.join(photosDir, file)).rotate();
  const { width, height } = await input.metadata();
  const widths = (WIDTHS[key] ?? WIDTHS.default).filter((w) => w <= width);
  for (const w of widths) {
    const resized = input.clone().resize({ width: w });
    await resized.clone().avif({ quality: 50, effort: 6 }).toFile(path.join(imgOut, `${key}-${w}.avif`));
    await resized.clone().webp({ quality: 72 }).toFile(path.join(imgOut, `${key}-${w}.webp`));
  }
  manifest[key] = { width, height, widths };
  console.log('photo', key, widths.join(','));
}
await mkdir(path.join(root, 'src/data'), { recursive: true });
await writeFile(path.join(root, 'src/data/images.json'), JSON.stringify(manifest, null, 2) + '\n');

// Brand: full logo and emblem in WebP (with PNG fallback for the full logo used in schema/OG).
const logo = path.join(brandDir, 'logo-full.png');
const emblem = path.join(brandDir, 'logo-emblem.png');
const tile = path.join(brandDir, 'icon-tile.png');
for (const w of [320, 640]) {
  await sharp(logo).resize({ width: w }).webp({ quality: 90 }).toFile(path.join(brandOut, `logo-full-${w}.webp`));
}
await sharp(logo).resize({ width: 600 }).png({ compressionLevel: 9, palette: true }).toFile(path.join(brandOut, 'logo-full.png'));
for (const w of [200, 400]) {
  await sharp(emblem).resize({ width: w }).webp({ quality: 90 }).toFile(path.join(brandOut, `logo-emblem-${w}.webp`));
}

// Icons
await sharp(tile).resize(32).png().toFile(path.join(root, 'public/favicon-32.png'));
await sharp(tile).resize(180).flatten({ background: '#ffffff' }).png().toFile(path.join(root, 'public/apple-touch-icon.png'));
await sharp(tile).resize(192).png().toFile(path.join(brandOut, 'icon-192.png'));
await sharp(tile).resize(512).png().toFile(path.join(brandOut, 'icon-512.png'));

// Open Graph image (1200x630): logo on white, hero photo on the right, temperature bar along the bottom.
const ogPhoto = await sharp(path.join(photosDir, 'hvac-technician-condenser.jpg'))
  .resize({ width: 560, height: 630, fit: 'cover', position: 'right' })
  .toBuffer();
const ogLogo = await sharp(logo).resize({ width: 520 }).toBuffer();
const bar = Buffer.from(
  `<svg width="1200" height="14" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g">
  <stop offset="0" stop-color="#275db6"/><stop offset=".35" stop-color="#45b0e7"/><stop offset=".5" stop-color="#ffbb13"/>
  <stop offset=".75" stop-color="#f46e00"/><stop offset="1" stop-color="#ee3534"/></linearGradient></defs>
  <rect width="1200" height="14" fill="url(#g)"/></svg>`
);
await sharp({ create: { width: 1200, height: 630, channels: 3, background: '#ffffff' } })
  .composite([
    { input: ogLogo, left: 60, top: 128 },
    { input: ogPhoto, left: 640, top: 0 },
    { input: bar, left: 0, top: 616 },
  ])
  .jpeg({ quality: 82, mozjpeg: true })
  .toFile(path.join(brandOut, 'og-image.jpg'));

console.log('done');
