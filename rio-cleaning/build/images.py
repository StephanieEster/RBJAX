#!/usr/bin/env python3
"""One-off image pipeline for the Rio Cleaning site.

Usage: python3 build/images.py <source-dir>

<source-dir> holds the original photos (named as in PHOTOS below, .jpg) plus the
brandbook logo layers (logo-rgb.png + logo-mask.png). Writes responsive WebP files,
Open Graph JPEGs, the logo and the favicons into site/assets/img/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

OUT = Path(__file__).resolve().parent.parent / 'site' / 'assets' / 'img'
WIDTHS = (640, 1024, 1600)

# name -> Pexels photo id (Pexels License: free for commercial use, no attribution required)
PHOTOS = {
    'hero-kitchen': 1080721, 'living-room': 8583748, 'family-time': 3875141, 'wiping-table': 6195198,
    'bathroom-faucet': 4239123, 'vanity-wipe': 4239037, 'moving-boxes': 7203788,
    'carpet-vacuum': 9462316, 'townhomes': 18093637, 'kitchen-open': 4682120,
    'living-room-2': 15580493,
}
OG = ('hero-kitchen', 'living-room', 'family-time', 'bathroom-faucet', 'moving-boxes', 'carpet-vacuum',
      'townhomes', 'kitchen-open', 'living-room-2')


def photos(src: Path) -> dict:
    sizes = {}
    for name in PHOTOS:
        im = ImageOps.exif_transpose(Image.open(src / f'{name}.jpg')).convert('RGB')
        for w in WIDTHS:
            if w > im.width:
                continue
            h = round(im.height * w / im.width)
            im.resize((w, h), Image.LANCZOS).save(OUT / f'{name}-{w}.webp', 'WEBP', quality=76, method=6)
        sizes[name] = [im.width, im.height]
        if name in OG:
            ImageOps.fit(im, (1200, 630), Image.LANCZOS).save(OUT / f'og-{name}.jpg', 'JPEG', quality=82,
                                                              optimize=True, progressive=True)
    return sizes


def logo(src: Path) -> None:
    rgb = Image.open(src / 'logo-rgb.png').convert('RGB')
    mask = Image.open(src / 'logo-mask.png').convert('L')
    full = rgb.copy()
    full.putalpha(mask)
    full = full.crop(full.getbbox())
    full.save(OUT / 'logo.png', optimize=True)
    for w in (240, 480):
        h = round(full.height * w / full.width)
        full.resize((w, h), Image.LANCZOS).save(OUT / f'logo-{w}.webp', 'WEBP', quality=90, method=6)
    # A round crop of the logo's illustration (statue, Sugarloaf and beach) becomes the favicon;
    # the circle stays clear of the wordmark. Coordinates are in the cropped logo's pixel space.
    cx, cy, r = 110, 170, 150
    mark = full.crop((cx - r, cy - r, cx + r, cy + r))
    disc = Image.new('L', mark.size, 0)
    draw = ImageDraw.Draw(disc)
    draw.ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    draw.rectangle((236 - (cx - r), 0, 2 * r, 142 - (cy - r)), fill=0)  # drop the edge of the "R"
    alpha = Image.composite(mark.getchannel('A'), disc, disc)
    mark.putalpha(alpha)
    for px, name in ((32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (192, 'icon-192.png'),
                     (512, 'icon-512.png')):
        canvas = Image.new('RGBA', (px, px), (255, 255, 255, 0 if px == 32 else 255))
        m = mark.resize((px, px), Image.LANCZOS)
        canvas.alpha_composite(m)
        canvas.save(OUT / name, optimize=True)
    mark.resize((48, 48), Image.LANCZOS).save(OUT.parent.parent / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])


if __name__ == '__main__':
    source = Path(sys.argv[1])
    OUT.mkdir(parents=True, exist_ok=True)
    meta = photos(source)
    logo(source)
    (Path(__file__).resolve().parent / 'image_sizes.json').write_text(json.dumps(meta, indent=1, sort_keys=True))
    print(f'{len(meta)} photos written to {OUT}')
