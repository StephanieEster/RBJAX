#!/usr/bin/env python3
"""Static site generator for the Rio Cleaning Services website.

Copy and business data live in content.py; this file holds the shared components and
page templates. Run `python3 build/build.py` from the rio-cleaning folder. Output goes
to site/ (one folder per page, so every URL ends in a slash).
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

import content as C

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'site'
SIZES = json.loads((Path(__file__).resolve().parent / 'image_sizes.json').read_text())
e = html.escape
BIZ_ID = C.SITE_URL + '/#business'
SITE_ID = C.SITE_URL + '/#website'
ASSET_V = '1'
CUR = ' aria-current="page"'
HL = ' class="is-hl"'
POP = ' <span class="pill">Most popular</span>'  # bump when CSS/JS change so returning visitors skip the cached copy

# ---------------------------------------------------------------- icons
# Line icons in the Lucide style (ISC license), 24px grid, shared through one sprite.
ICONS = {
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-9 5.7a2 2 0 0 1-2 0L2 7"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'pin': '<path d="M20 10c0 5-5.5 10.2-7.4 11.8a1 1 0 0 1-1.2 0C9.5 20.2 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    'map': '<path d="M14.1 5.1 9.9 3a2 2 0 0 0-1.8 0L3.6 5.2A1 1 0 0 0 3 6.1v13.3a1 1 0 0 0 1.4.9L8 18.6a2 2 0 0 1 1.8 0l4.3 2.1a2 2 0 0 0 1.8 0l4.5-2.2a1 1 0 0 0 .6-.9V4.6a1 1 0 0 0-1.4-.9L16 5.3a2 2 0 0 1-1.9 0Z"/><path d="M15 5.8v15M9 3.2v15"/>',
    'calendar': '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    'repeat': '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    'shield': '<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    'sparkles': '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/><path d="M5 3v4M3 5h4M19 17v4M17 19h4"/>',
    'home': '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .7-1.5l7-6a2 2 0 0 1 2.6 0l7 6a2 2 0 0 1 .7 1.5v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    'key': '<path d="m15.5 7.5 2.3 2.3a1 1 0 0 0 1.4 0l2.1-2.1a1 1 0 0 0 0-1.4L19 4"/><path d="m21 2-9.6 9.6"/><circle cx="7.5" cy="15.5" r="5.5"/>',
    'carpet': '<rect x="5" y="4" width="14" height="16" rx="1"/><path d="M8 4V2M12 4V2M16 4V2M8 22v-2M12 22v-2M16 22v-2"/><path d="m9 9 3-2 3 2M9 13l3-2 3 2M9 17l3-2 3 2"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'check-circle': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    'arrow-up-right': '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    'chev': '<path d="m6 9 6 6 6-6"/>',
    'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'x': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    'clipboard': '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4M12 16h4M8 11h.01M8 16h.01"/>',
    'award': '<circle cx="12" cy="8" r="6"/><path d="M15.5 12.9 17 22l-5-3-5 3 1.5-9.1"/>',
    'eye': '<path d="M2.1 12.3a1 1 0 0 1 0-.7 10.8 10.8 0 0 1 19.8 0 1 1 0 0 1 0 .7 10.8 10.8 0 0 1-19.8 0"/><circle cx="12" cy="12" r="3"/>',
    'message': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    'badge': '<path d="M3.9 8.6a4 4 0 0 1 4.8-4.8 4 4 0 0 1 6.7 0 4 4 0 0 1 4.8 4.8 4 4 0 0 1 0 6.7 4 4 0 0 1-4.8 4.8 4 4 0 0 1-6.7 0 4 4 0 0 1-4.8-4.8 4 4 0 0 1 0-6.7Z"/><path d="m9 12 2 2 4-4"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
    'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    'utensils': '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    'bath': '<path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.7 3 4 3.7 4 4.5V17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/><path d="M10 5 8 7M2 12h20M7 19v2M17 19v2"/>',
    'sofa': '<path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/><path d="M2 16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z"/><path d="M4 18v2M20 18v2"/>',
    'door': '<path d="M13 4h3a2 2 0 0 1 2 2v14"/><path d="M2 20h3M13 20h9M10 12v.01"/><path d="M13 4.6v16.1a1 1 0 0 1-1.2 1L5 20V5.6a2 2 0 0 1 1.5-1.9l4-1A2 2 0 0 1 13 4.6Z"/>',
    'card': '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20M6 15h4"/>',
    'heart': '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
    'list': '<path d="M3 12h.01M3 18h.01M3 6h.01M8 12h13M8 18h13M8 6h13"/>',
    'instagram': '<rect width="20" height="20" x="2" y="2" rx="5"/><path d="M16 11.4A4 4 0 1 1 12.6 8 4 4 0 0 1 16 11.4z"/><path d="M17.5 6.5h.01"/>',
    'facebook': '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    'google': '<path d="M21.8 12.2c0-.7-.1-1.4-.2-2H12v3.9h5.5a4.7 4.7 0 0 1-2 3.1v2.5h3.3c1.9-1.8 3-4.4 3-7.5Z"/><path d="M12 22c2.7 0 5-.9 6.8-2.4l-3.3-2.5c-.9.6-2.1 1-3.5 1-2.7 0-4.9-1.8-5.7-4.2H2.9v2.6A10 10 0 0 0 12 22Z"/><path d="M6.3 13.9a6 6 0 0 1 0-3.8V7.5H2.9a10 10 0 0 0 0 9Z"/><path d="M12 5.9c1.5 0 2.8.5 3.9 1.5l2.9-2.9A10 10 0 0 0 2.9 7.5l3.4 2.6C7.1 7.7 9.3 5.9 12 5.9Z"/>',
}
FILLED = {'star4': '<path d="M12 1.5c.7 5.6 4.9 9.8 10.5 10.5-5.6.7-9.8 4.9-10.5 10.5C11.3 16.9 7.1 12.7 1.5 12 7.1 11.3 11.3 7.1 12 1.5Z"/>'}


def sprite() -> str:
    out = ['<svg xmlns="http://www.w3.org/2000/svg">']
    for k, v in ICONS.items():
        out.append(f'<symbol id="{k}" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.6" '
                   f'stroke-linecap="round" stroke-linejoin="round">{v}</g></symbol>')
    for k, v in FILLED.items():
        out.append(f'<symbol id="{k}" viewBox="0 0 24 24"><g fill="currentColor">{v}</g></symbol>')
    out.append('</svg>')
    return ''.join(out)


def icon(name: str, cls: str = 'ic') -> str:
    assert name in ICONS or name in FILLED, name
    return f'<svg class="{cls}" aria-hidden="true" focusable="false"><use href="/assets/icons.svg?v={ASSET_V}#{name}"/></svg>'


def stars3() -> str:
    """The three four-point sparkles from the brandbook, used as a small signature mark."""
    return f'<span class="mark3" aria-hidden="true">{icon("star4", "s")}{icon("star4", "s")}{icon("star4", "s")}</span>'


# ---------------------------------------------------------------- helpers
def url(slug: str = '') -> str:
    return f'/{slug}/' if slug else '/'


def abs_url(slug: str = '') -> str:
    return C.SITE_URL + url(slug)


def pic(name: str, alt: str, sizes: str = '(max-width: 900px) 100vw, 50vw', eager: bool = False, cls: str = '') -> str:
    w, h = SIZES[name]
    widths = [x for x in (640, 1024, 1600) if x <= w]
    srcset = ', '.join(f'/assets/img/{name}-{x}.webp {x}w' for x in widths)
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="/assets/img/{name}-1024.webp" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" '
            f'alt="{e(alt)}" {load} decoding="async">')


def call_btn(label: str = 'Call for a Free Estimate', cls: str = 'btn btn-primary', where: str = 'body') -> str:
    return (f'<a class="{cls}" href="{C.TEL}" data-track="phone_click" data-where="{where}">{icon("phone")}'
            f'<span>{label}</span></a>')


def estimate_btn(label: str = 'Request Your Estimate', cls: str = 'btn btn-ghost') -> str:
    return f'<a class="{cls}" href="#estimate">{icon("clipboard")}<span>{label}</span></a>'


def eyebrow(text: str, cls: str = '') -> str:
    return f'<p class="eyebrow {cls}">{stars3()}<span>{text}</span></p>'


def checklist(items, cls='checks') -> str:
    return f'<ul class="{cls}">' + ''.join(f'<li>{icon("check")}<span>{i}</span></li>' for i in items) + '</ul>'


def tracked_link(href: str, text: str, event: str, cls: str = '', label: str = '') -> str:
    c = f' class="{cls}"' if cls else ''
    a = f' aria-label="{e(label)}"' if label else ''
    return f'<a{c} href="{href}" data-track="{event}" target="_blank" rel="noopener"{a}>{text}</a>'


# ---------------------------------------------------------------- head / header / footer
def tracking_head() -> str:
    t = C.TRACKING
    out = []
    if t['gtm']:
        out.append("<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});"
                   "var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;"
                   "j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})"
                   f"(window,document,'script','dataLayer','{t['gtm']}');</script>")
    gtag_ids = [x for x in (t['ga4'], t['google_ads']) if x]
    if gtag_ids:
        cfg = ''.join(f"gtag('config','{x}');" for x in gtag_ids)
        out.append(f'<script async src="https://www.googletagmanager.com/gtag/js?id={gtag_ids[0]}"></script>'
                   "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
                   f"gtag('js',new Date());{cfg}</script>")
    if t['meta_pixel']:
        out.append("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?"
                   "n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;"
                   "n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];"
                   "s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');"
                   f"fbq('init','{t['meta_pixel']}');fbq('track','PageView');</script>")
    conf = {'adsId': t['google_ads'], 'adsFormLabel': t['google_ads_form_label'],
            'adsCallLabel': t['google_ads_call_label']}
    out.append(f'<script>window.RIO_TRACKING={json.dumps(conf)};</script>')
    return '\n'.join(out)


def head(p: dict) -> str:
    canonical = abs_url(p['slug'])
    og_img = f"{C.SITE_URL}/assets/img/og-{p.get('og', 'hero-kitchen')}.jpg"
    robots = '<meta name="robots" content="noindex, follow">' if p.get('noindex') else \
        '<meta name="robots" content="index, follow, max-image-preview:large">'
    preload = ''
    if p.get('lcp'):
        name = p['lcp']
        w = SIZES[name][0]
        widths = [x for x in (640, 1024, 1600) if x <= w]
        srcset = ', '.join(f'/assets/img/{name}-{x}.webp {x}w' for x in widths)
        preload = (f'<link rel="preload" as="image" type="image/webp" imagesrcset="{srcset}" '
                   f'imagesizes="{p.get("lcp_sizes", "(max-width: 900px) 100vw, 55vw")}" fetchpriority="high">')
    schema = json.dumps({'@context': 'https://schema.org', '@graph': p['schema']}, ensure_ascii=False, separators=(',', ':'))
    return f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p['title'])}</title>
<meta name="description" content="{e(p['desc'])}">
<link rel="canonical" href="{canonical}">
{robots}
<meta name="theme-color" content="#fbf8f3">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="{C.NAME}">
<meta property="og:title" content="{e(p['title'])}">
<meta property="og:description" content="{e(p['desc'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(p['title'])}">
<meta name="twitter:description" content="{e(p['desc'])}">
<meta name="twitter:image" content="{og_img}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/fraunces.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/montserrat.woff2" as="font" type="font/woff2" crossorigin>
{preload}
<link rel="stylesheet" href="/assets/css/style.css?v={ASSET_V}">
<script src="/assets/js/main.js?v={ASSET_V}" defer></script>
{tracking_head()}
<script type="application/ld+json">{schema}</script>
</head>'''


NAV = [('About', 'about'), ('Service Areas', 'service-areas'), ('Reviews', 'reviews'), ('FAQ', 'faq'),
       ('Contact', 'contact')]


def header(active: str) -> str:
    svc_active = active in ('residential-cleaning',) + tuple(C.SVC)
    sub = ''.join(f'<li><a href="{url(s["slug"])}"{CUR if active == s["slug"] else ""}>'
                  f'{icon(s["icon"])}<span>{s["short"]}</span></a></li>' for s in C.SERVICES)
    items = ''.join(f'<li><a class="nav-link" href="{url(slug)}"{CUR if active == slug else ""}>'
                    f'{label}</a></li>' for label, slug in NAV)
    gtm_ns = ''
    if C.TRACKING['gtm']:
        gtm_ns = (f'<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={C.TRACKING["gtm"]}" height="0" '
                  'width="0" style="display:none;visibility:hidden"></iframe></noscript>')
    hours = f'<span>{icon("clock")}{C.HOURS["short"]}</span>' if C.HOURS else ''
    return f'''<body>
{gtm_ns}<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap topbar-in">
<span>{icon("pin")}Based in Philadelphia, serving nearby PA, NJ &amp; DE communities</span>
{hours}<span>{icon("shield")}Insured</span>
</div></div>
<header class="site-header" id="top">
<div class="wrap header-in">
<a class="brand" href="/" aria-label="{C.NAME}, home"><img src="/assets/img/logo-240.webp" srcset="/assets/img/logo-240.webp 1x, /assets/img/logo-480.webp 2x" width="240" height="128" alt="{C.NAME}"></a>
<nav class="nav" id="site-nav" aria-label="Main">
<ul class="nav-list">
<li class="has-sub{' is-active' if svc_active else ''}">
<a class="nav-link" href="/residential-cleaning/"{' aria-current="page"' if active == 'residential-cleaning' else ''}>Services</a>
<button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-services"><span class="sr-only">Show service pages</span>{icon("chev")}</button>
<div class="sub" id="sub-services"><ul>
<li><a href="/residential-cleaning/">{icon("home")}<span>All residential cleaning</span></a></li>{sub}
</ul></div>
</li>
{items}
</ul>
<div class="nav-mobile-cta">{call_btn('Call ' + C.PHONE, 'btn btn-primary btn-block', 'menu')}
<a class="btn btn-ghost btn-block" href="/contact/">{icon("clipboard")}<span>Request an Estimate</span></a></div>
</nav>
<a class="btn btn-primary header-call" href="{C.TEL}" data-track="phone_click" data-where="header">{icon("phone")}<span>{C.PHONE}</span></a>
<a class="icon-btn header-call-sm" href="{C.TEL}" data-track="phone_click" data-where="header" aria-label="Call {C.PHONE}">{icon("phone")}</a>
<button class="icon-btn menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="sr-only">Menu</span>{icon("menu", "ic ic-open")}{icon("x", "ic ic-close")}</button>
</div>
</header>'''


def footer(has_estimate: bool = True) -> str:
    quote_href = '#estimate' if has_estimate else '/contact/'
    svc = ''.join(f'<li><a href="{url(s["slug"])}">{s["short"]}</a></li>' for s in C.SERVICES)
    hours = f'<li>{icon("clock")}<span>{C.HOURS["label"]}</span></li>' if C.HOURS else ''
    social = [tracked_link(C.INSTAGRAM, icon('instagram'), 'instagram_click', 'social', 'Rio Cleaning Services on Instagram'),
              tracked_link(C.FACEBOOK, icon('facebook'), 'facebook_click', 'social', 'Rio Cleaning Services on Facebook')]
    if C.GOOGLE_PROFILE:
        social.append(tracked_link(C.GOOGLE_PROFILE, icon('google'), 'google_profile_click', 'social',
                                   'Rio Cleaning Services on Google'))
    return f'''<footer class="site-footer">
<div class="wrap footer-grid">
<div class="footer-brand">
<img src="/assets/img/logo-240.webp" srcset="/assets/img/logo-240.webp 1x, /assets/img/logo-480.webp 2x" width="200" height="107" alt="{C.NAME}" loading="lazy">
<p>Residential house cleaning for Philadelphia-area families. Backed by nearly 25 years of hands-on experience. Proudly serving local homeowners since {C.FOUNDED}.</p>
<div class="socials">{''.join(social)}</div>
</div>
<div>
<p class="footer-h">Services</p>
<ul class="footer-links"><li><a href="/residential-cleaning/">Residential Cleaning</a></li>{svc}</ul>
</div>
<div>
<p class="footer-h">Company</p>
<ul class="footer-links"><li><a href="/about/">About</a></li><li><a href="/service-areas/">Service Areas</a></li>
<li><a href="/reviews/">Reviews</a></li><li><a href="/faq/">FAQ</a></li><li><a href="/contact/">Contact</a></li></ul>
</div>
<div>
<p class="footer-h">Get in touch</p>
<ul class="footer-contact">
<li><a href="{C.TEL}" data-track="phone_click" data-where="footer">{icon("phone")}<span>{C.PHONE}</span></a></li>
<li><a href="mailto:{C.EMAIL}">{icon("mail")}<span>{C.EMAIL}</span></a></li>
<li>{icon("pin")}<span>Based in Philadelphia, PA. Serving nearby communities in Pennsylvania, New Jersey and Delaware.</span></li>
{hours}
</ul>
</div>
</div>
<div class="wrap footer-base">
<p>&copy; 2026 {C.LEGAL_NAME}. All rights reserved.</p>
<p><a href="/privacy-policy/">Privacy Policy</a><a href="/terms-and-conditions/">Terms &amp; Conditions</a></p>
</div>
</footer>
<div class="mobile-bar" role="region" aria-label="Quick contact">
<a class="mb-call" href="{C.TEL}" data-track="phone_click" data-where="sticky_bar">{icon("phone")}<span>Call Now</span></a>
<a class="mb-quote" href="{quote_href}">{icon("clipboard")}<span>Free Estimate</span></a>
</div>
</body>
</html>
'''


def breadcrumb(trail) -> str:
    """trail: list of (label, slug) excluding Home."""
    items = ['<li><a href="/">Home</a></li>']
    for i, (label, slug) in enumerate(trail):
        last = i == len(trail) - 1
        items.append(f'<li><span aria-current="page">{label}</span></li>' if last else
                     f'<li><a href="{url(slug)}">{label}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'


# ---------------------------------------------------------------- schema
def area_served():
    areas = [{'@type': 'City', 'name': 'Philadelphia',
              'containedInPlace': {'@type': 'State', 'name': 'Pennsylvania'}}]
    for c in C.CONFIRMED_CITIES:
        areas.append({'@type': 'City', 'name': c['name'], 'containedInPlace': {'@type': 'State', 'name': c['state']}})
    return areas


def business_node() -> dict:
    same = [C.INSTAGRAM, C.FACEBOOK] + ([C.GOOGLE_PROFILE] if C.GOOGLE_PROFILE else [])
    node = {
        '@type': 'LocalBusiness', '@id': BIZ_ID, 'name': C.NAME, 'legalName': C.LEGAL_NAME,
        'description': 'Residential house cleaning company based in Philadelphia, PA, offering recurring, deep, '
                       'move-in/move-out and carpet cleaning.',
        'url': C.SITE_URL + '/', 'telephone': C.PHONE_E164, 'email': C.EMAIL,
        'logo': {'@type': 'ImageObject', 'url': C.SITE_URL + '/assets/img/logo.png'},
        'image': C.SITE_URL + '/assets/img/og-hero-kitchen.jpg',
        'foundingDate': C.FOUNDED, 'founder': {'@type': 'Person', 'name': C.OWNER},
        'address': {'@type': 'PostalAddress', 'addressLocality': C.BASE_CITY, 'addressRegion': C.BASE_REGION,
                    'addressCountry': 'US'},
        'areaServed': area_served(),
        'paymentAccepted': ', '.join(C.PAYMENTS), 'currenciesAccepted': 'USD',
        'sameAs': same,
    }
    if C.HOURS:
        node['openingHoursSpecification'] = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': C.HOURS['days'],
                                              'opens': C.HOURS['opens'], 'closes': C.HOURS['closes']}]
    return node


def webpage_node(p: dict, kind: str = 'WebPage') -> dict:
    u = abs_url(p['slug'])
    node = {'@type': kind, '@id': u + '#webpage', 'url': u, 'name': p['title'], 'description': p['desc'],
            'isPartOf': {'@id': SITE_ID}, 'about': {'@id': BIZ_ID}, 'inLanguage': 'en-US',
            'dateModified': C.UPDATED_ISO}
    if p['slug']:
        node['breadcrumb'] = {'@id': u + '#breadcrumb'}
    return node


def crumbs_node(slug: str, trail) -> dict:
    items = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': C.SITE_URL + '/'}]
    for i, (label, s) in enumerate(trail, start=2):
        items.append({'@type': 'ListItem', 'position': i, 'name': label, 'item': abs_url(s)})
    return {'@type': 'BreadcrumbList', '@id': abs_url(slug) + '#breadcrumb', 'itemListElement': items}


def faq_node(slug: str, keys) -> dict:
    return {'@type': 'FAQPage', '@id': abs_url(slug) + '#faq', 'mainEntity': [
        {'@type': 'Question', 'name': C.FAQ[k][0], 'acceptedAnswer': {'@type': 'Answer', 'text': C.FAQ[k][1]}}
        for k in keys]}


def service_node(slug: str, name: str, stype: str, desc: str) -> dict:
    return {'@type': 'Service', '@id': abs_url(slug) + '#service', 'name': name, 'serviceType': stype,
            'description': desc, 'url': abs_url(slug), 'provider': {'@id': BIZ_ID}, 'areaServed': area_served()}


# ---------------------------------------------------------------- shared sections
def trust_bar(cls: str = '') -> str:
    items = ''.join(f'<li>{icon(i)}<p><strong>{a}</strong> <span>{b}</span></p></li>' for i, a, b in C.TRUST)
    return f'<div class="trust {cls}"><ul class="wrap trust-list" aria-label="Why homeowners choose Rio">{items}</ul></div>'


def steps_section(title: str = 'Getting started is simple', intro: str = '') -> str:
    steps = ''.join(f'<li class="step"><span class="step-ic">{icon(i)}</span><h3>{t}</h3><p>{d}</p></li>'
                    for i, t, d in C.STEPS)
    intro_html = f'<p class="lead">{intro}</p>' if intro else ''
    return f'''<section class="section steps-sec" aria-labelledby="steps-h">
<div class="wrap">
<div class="sec-head">{eyebrow('How it works')}<h2 id="steps-h">{title}</h2>{intro_html}</div>
<ol class="steps">{steps}</ol>
</div>
</section>'''


def included_tabs(keys=('recurring', 'deep', 'move'), heading='What\'s included in your cleaning') -> str:
    tabs, panels = [], []
    for i, k in enumerate(keys):
        d = C.INCLUDED[k]
        sel = 'true' if i == 0 else 'false'
        tabs.append(f'<button class="tab" type="button" role="tab" id="tab-{k}" aria-controls="panel-{k}" '
                    f'aria-selected="{sel}" tabindex="{0 if i == 0 else -1}">{d["label"]}</button>')
        groups = ''.join(f'<div class="inc-group"><h3>{icon(ic)}{t}</h3>{checklist(items)}</div>'
                         for ic, t, items in d['groups'])
        hidden = '' if i == 0 else ' hidden'
        panels.append(f'<div class="tab-panel" role="tabpanel" id="panel-{k}" aria-labelledby="tab-{k}" tabindex="0"{hidden}>'
                      f'<p class="panel-intro">{d["intro"]}</p><div class="inc-grid">{groups}</div></div>')
    return f'''<section class="section included" aria-labelledby="inc-h">
<div class="wrap">
<div class="sec-head">{eyebrow('What\'s included')}<h2 id="inc-h">{heading}</h2></div>
<div class="tabs" role="tablist" aria-label="Cleaning types">{''.join(tabs)}</div>
{''.join(panels)}
<p class="note">{icon("clipboard")}<span>{C.ESTIMATE_NOTE}</span></p>
</div>
</section>'''


def included_single(key: str, heading: str) -> str:
    d = C.INCLUDED[key]
    groups = ''.join(f'<div class="inc-group"><h3>{icon(ic)}{t}</h3>{checklist(items)}</div>' for ic, t, items in d['groups'])
    return f'''<section class="section included" aria-labelledby="inc-h">
<div class="wrap">
<div class="sec-head">{eyebrow('What\'s included')}<h2 id="inc-h">{heading}</h2><p class="lead">{d["intro"]}</p></div>
<div class="inc-grid">{groups}</div>
<p class="note">{icon("clipboard")}<span>{C.ESTIMATE_NOTE}</span></p>
</div>
</section>'''


def factors_table(heading: str = 'What affects your estimate') -> str:
    rows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in C.ESTIMATE_FACTORS)
    return f'''<div class="factors">
<h2 class="h3">{heading}</h2>
<p>We don't publish flat prices because no two homes are the same. These are the things we ask about:</p>
<div class="table-wrap"><table class="table"><thead><tr><th scope="col">Factor</th><th scope="col">Why it matters</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="factors-cta">Every home is different. {call_btn('Call us for a personalized estimate', 'link-strong', 'factors')}</p>
</div>'''


def faq_list(keys, heading_level: int = 3) -> str:
    out = []
    for k in keys:
        q, a = C.FAQ[k]
        out.append(f'<div class="acc-item"><h{heading_level} class="acc-h"><button class="acc-btn" type="button" '
                   f'aria-expanded="false" aria-controls="faq-{k}" id="faq-{k}-btn"><span>{q}</span>{icon("chev")}'
                   f'</button></h{heading_level}><div class="acc-panel" id="faq-{k}" role="region" '
                   f'aria-labelledby="faq-{k}-btn" hidden><p>{e(a)}</p></div></div>')
    return f'<div class="acc">{"".join(out)}</div>'


def faq_section(keys, heading: str = 'Questions homeowners ask us', more: bool = True) -> str:
    more_html = f'<p class="sec-more"><a class="arrow-link" href="/faq/">See all frequently asked questions{icon("arrow")}</a></p>' if more else ''
    return f'''<section class="section faq-sec" aria-labelledby="faq-h">
<div class="wrap faq-layout">
<div class="faq-aside">{eyebrow('FAQ')}<h2 id="faq-h">{heading}</h2>
<p>Don't see your question? Call <a href="{C.TEL}" data-track="phone_click" data-where="faq">{C.PHONE}</a> and talk to us directly.</p></div>
<div>{faq_list(keys)}{more_html}</div>
</div>
</section>'''


def select(name, label, options, required=False, placeholder='Select one'):
    req = ' required' if required else ''
    star = '<span class="req" aria-hidden="true">*</span>' if required else '<span class="opt">(optional)</span>'
    opts = f'<option value="">{placeholder}</option>' + ''.join(f'<option>{o}</option>' for o in options)
    return (f'<div class="field"><label for="f-{name}">{label} {star}</label>'
            f'<select id="f-{name}" name="{name}"{req} aria-describedby="e-{name}">{opts}</select>'
            f'<p class="err" id="e-{name}" aria-live="polite"></p></div>')


def field(name, label, type_='text', required=False, attrs='', full=False):
    req = ' required' if required else ''
    star = '<span class="req" aria-hidden="true">*</span>' if required else '<span class="opt">(optional)</span>'
    cls = 'field full' if full else 'field'
    return (f'<div class="{cls}"><label for="f-{name}">{label} {star}</label>'
            f'<input id="f-{name}" name="{name}" type="{type_}"{req} {attrs} aria-describedby="e-{name}">'
            f'<p class="err" id="e-{name}" aria-live="polite"></p></div>')


def quote_form(page_name: str, preset: str = '') -> str:
    services = ['Recurring Cleaning', 'Deep Cleaning', 'Move-In Cleaning', 'Move-Out Cleaning', 'Carpet Cleaning',
                'Not Sure Yet']
    svc_opts = '<option value="">Select one</option>' + ''.join(
        f'<option{" selected" if o == preset else ""}>{o}</option>' for o in services)
    return f'''<form class="qform" id="quote-form" action="{C.FORM_ACTION}" method="POST" novalidate data-endpoint="{C.FORM_ENDPOINT}">
<div class="form-grid">
{field('name', 'Full name', 'text', True, 'autocomplete="name" autocapitalize="words" maxlength="80"')}
{field('phone', 'Phone number', 'tel', True, 'autocomplete="tel" inputmode="tel" maxlength="20"')}
{field('email', 'Email', 'email', False, 'autocomplete="email" inputmode="email" maxlength="120"')}
{field('zip', 'ZIP code', 'text', True, 'autocomplete="postal-code" inputmode="numeric" maxlength="5" pattern="[0-9]{5}"')}
<div class="field"><label for="f-service">Type of cleaning <span class="req" aria-hidden="true">*</span></label>
<select id="f-service" name="service" required aria-describedby="e-service">{svc_opts}</select><p class="err" id="e-service" aria-live="polite"></p></div>
{select('frequency', 'Cleaning frequency', ['Weekly', 'Biweekly', 'Monthly', 'One-Time'])}
{select('bedrooms', 'Bedrooms', ['1', '2', '3', '4', '5 or more'])}
{select('bathrooms', 'Bathrooms', ['1', '1.5', '2', '2.5', '3', '3.5', '4 or more'])}
<fieldset class="field full radios"><legend>Preferred contact method <span class="opt">(optional)</span></legend>
<label class="radio"><input type="radio" name="contact_method" value="Phone call" checked><span>Phone call</span></label>
<label class="radio"><input type="radio" name="contact_method" value="Email"><span>Email</span></label>
</fieldset>
<div class="field full"><label for="f-message">Anything we should know? <span class="opt">(optional)</span></label>
<textarea id="f-message" name="message" rows="3" maxlength="1500" placeholder="Pets, priority areas, preferred days, move date..."></textarea></div>
</div>
<div class="hp" aria-hidden="true"><label for="f-company">Company</label><input id="f-company" type="text" name="_honey" tabindex="-1" autocomplete="off"></div>
<input type="hidden" name="_subject" value="New estimate request - riocleanings.com">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_next" value="{C.SITE_URL}/contact/?sent=1">
<input type="hidden" name="page" value="{e(page_name)}">
<p class="consent">By submitting this form, you agree to be contacted by Rio Cleaning Services regarding your cleaning request. See our <a href="/privacy-policy/">Privacy Policy</a>.</p>
<button class="btn btn-primary btn-submit" type="submit">{icon("arrow")}<span class="btn-label">Request My Free Estimate</span></button>
<div class="form-status" role="status" aria-live="polite" tabindex="-1"></div>
</form>'''


def estimate_section(page_name: str, heading: str = 'Get your personalized cleaning estimate', preset: str = '') -> str:
    hours = f'<li>{icon("clock")}<span>{C.HOURS["label"]}</span></li>' if C.HOURS else ''
    return f'''<section class="section estimate" id="estimate" aria-labelledby="est-h">
<div class="wrap est-grid">
<div class="est-copy">
{eyebrow('Free estimate', 'on-dark')}
<h2 id="est-h">{heading}</h2>
<p>The fastest way to get started is a quick phone call. Prefer to write? Send the form and we'll get back to you to confirm the details.</p>
<a class="est-phone" href="{C.TEL}" data-track="phone_click" data-where="estimate">{icon("phone")}<span>{C.PHONE}</span></a>
<ul class="est-list">
<li>{icon("mail")}<a href="mailto:{C.EMAIL}">{C.EMAIL}</a></li>
{hours}
<li>{icon("pin")}<span>Philadelphia-based, serving nearby PA, NJ &amp; DE communities</span></li>
</ul>
</div>
<div class="est-form">{quote_form(page_name, preset)}</div>
</div>
</section>'''


def related_links(slugs, current: str) -> str:
    notes = {
        'recurring-cleaning': 'Ongoing weekly, biweekly or monthly visits that keep a lived-in home clean.',
        'deep-cleaning': 'A one-time, detailed clean for buildup. The usual first step before recurring visits.',
        'move-in-move-out-cleaning': 'For an empty home: inside cabinets, bathrooms and every baseboard.',
        'carpet-cleaning': 'Carpets, stairs and rugs, on their own or paired with another service.',
    }
    items = ''.join(f'<li><a href="{url(s)}"><span class="rel-ic">{icon(C.SVC[s]["icon"])}</span><span><strong>'
                    f'{C.SVC[s]["card_title"]}</strong><span>{notes[s]}</span></span>{icon("arrow")}</a></li>'
                    for s in slugs if s != current)
    return f'''<section class="section related" aria-labelledby="rel-h">
<div class="wrap">
<div class="sec-head">{eyebrow('Related services')}<h2 id="rel-h">Not quite what you need?</h2></div>
<ul class="rel-list">{items}</ul>
</div>
</section>'''


def page_hero(p, eyebrow_text, h1, lede, img, alt, cta_secondary=None, crumbs=None, small_note=None):
    crumbs_html = breadcrumb(crumbs) if crumbs else ''
    sec = cta_secondary or estimate_btn()
    note = f'<p class="hero-note">{small_note}</p>' if small_note else ''
    return f'''<section class="phero">
<div class="wrap phero-grid">
<div class="phero-copy">
{crumbs_html}
{eyebrow(eyebrow_text)}
<h1>{h1}</h1>
<p class="lede">{lede}</p>
<div class="cta-row">{call_btn()}{sec}</div>
{note}
</div>
<figure class="phero-media">{pic(img, alt, '(max-width: 900px) 100vw, 46vw', eager=True)}</figure>
</div>
</section>'''


def definition(text: str) -> str:
    return f'<div class="definition wrap"><p><strong>{text}</strong></p></div>'


# ---------------------------------------------------------------- pages
def render(p: dict, body: str) -> None:
    html_out = head(p) + '\n' + header(p['active']) + f'\n<main id="main">\n{body}\n</main>\n' + footer('id="estimate"' in body)
    path = OUT / p['slug'] / 'index.html' if p['slug'] else OUT / 'index.html'
    if p.get('file'):
        path = OUT / p['file']
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html_out, encoding='utf-8')
    PAGES.append(p)


PAGES: list = []


def page_home():
    p = {'slug': '', 'active': '', 'og': 'hero-kitchen', 'lcp': 'hero-kitchen',
         'title': 'House Cleaning Services in Philadelphia, PA | Rio Cleaning',
         'desc': 'Recurring, deep, move-in/move-out and carpet cleaning for Philadelphia-area homes. Insured, flexible '
                 'scheduling, nearly 25 years of experience. Free estimates.'}
    home_faq = ['cost', 'frequencies', 'regular-vs-deep', 'areas', 'insured']
    p['schema'] = [business_node(),
                   {'@type': 'WebSite', '@id': SITE_ID, 'url': C.SITE_URL + '/', 'name': C.NAME,
                    'publisher': {'@id': BIZ_ID}, 'inLanguage': 'en-US'},
                   webpage_node(p), faq_node('', home_faq)]
    diffs = ''.join(f'<li><span class="diff-ic">{icon(i)}</span><div><h3>{t}</h3><p>{d}</p></div></li>'
                    for i, t, d in C.DIFFERENTIATORS)
    rec, deep, move, carpet = (C.SVC[s] for s in ('recurring-cleaning', 'deep-cleaning', 'move-in-move-out-cleaning',
                                                  'carpet-cleaning'))
    minor = ''.join(f'''<li class="svc-row"><a href="{url(s["slug"])}" data-track="service_click" data-service="{s["slug"]}">
<span class="svc-thumb">{pic(s["img"], s["img_alt"], "(max-width: 700px) 30vw, 200px")}</span>
<span class="svc-txt"><span class="svc-name">{icon(s["icon"])}{s["card_title"]}</span><span class="svc-desc">{s["card_text"]}</span></span>
<span class="svc-go">{icon("arrow")}</span></a></li>''' for s in (deep, move, carpet))
    bw = [('repeat', 'A consistently clean home', 'Kitchens and bathrooms never get far from "just cleaned."'),
          ('sparkles', 'Easier upkeep', 'Two weeks is short enough that buildup never gets a head start.'),
          ('calendar', 'A predictable routine', 'Same rhythm, every other week. One less thing to plan.'),
          ('sun', 'Weekends back', 'Less Saturday scrubbing, more time for the people you live with.'),
          ('award', 'Professional maintenance', 'Experienced hands keep surfaces and fixtures in good shape.'),
          ('users', 'Flexible when needed', 'Two teams mean we can often rearrange a visit when your week changes.')]
    bw_html = ''.join(f'<li>{icon(i)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in bw)
    body = f'''
<section class="hero">
<div class="wrap hero-grid">
<div class="hero-copy">
{eyebrow('Residential cleaning · Since 2019')}
<h1>Philadelphia-area <em>house cleaning</em> for a home you'll love coming back to.</h1>
<p class="lede">Recurring and one-time cleaning from a local, insured team backed by nearly 25 years of hands-on experience, with flexible scheduling built around your week.</p>
<div class="cta-row">{call_btn('Call for a Free Estimate', 'btn btn-primary btn-lg', 'hero')}
<a class="arrow-link" href="#services">Explore Our Cleaning Services{icon("arrow")}</a></div>
<p class="hero-phone">Talk to us directly: <a href="{C.TEL}" data-track="phone_click" data-where="hero_text">{C.PHONE}</a></p>
</div>
<div class="hero-media">
<figure class="hero-img">{pic('hero-kitchen', 'Bright white kitchen with a large island and sunflowers on the dining table', '(max-width: 900px) 100vw, 55vw', eager=True)}</figure>
<a class="hero-tag" href="/recurring-cleaning/" data-track="service_click" data-service="recurring-cleaning">
<span class="hero-tag-k">Most requested</span><span class="hero-tag-v">Biweekly cleaning for family homes</span>{icon("arrow")}</a>
</div>
</div>
</section>
{trust_bar()}

<section class="section why" aria-labelledby="why-h">
<div class="wrap why-grid">
<div class="why-lead">
{eyebrow('Why Rio Cleaning')}
<h2 id="why-h">Cleaning you can count on, from people who <em>know the work</em>.</h2>
<p class="definition-inline"><strong>Rio Cleaning Services LLC is a Philadelphia-based residential cleaning company providing weekly, biweekly and monthly house cleaning, deep cleaning, move-in/move-out and carpet cleaning for nearby homes.</strong></p>
<p>We're a small, owner-led business. Marcia, our owner, spent years cleaning homes herself before founding the company in {C.FOUNDED}, and that experience shapes how every visit is done.</p>
<a class="arrow-link" href="/about/">Meet the owner{icon("arrow")}</a>
</div>
<ul class="diff-list">{diffs}</ul>
</div>
</section>

<section class="section services" id="services" aria-labelledby="svc-h">
<div class="wrap">
<div class="sec-head split">{eyebrow('Our services')}<h2 id="svc-h">Residential cleaning services, built around your home</h2>
<p class="lead">From regular visits to a one-time deep clean before a move, every service is focused on homes, not offices.</p></div>
<div class="svc-layout">
<a class="svc-feature" href="{url(rec['slug'])}" data-track="service_click" data-service="{rec['slug']}">
<span class="svc-feature-img">{pic(rec['img'], rec['img_alt'], '(max-width: 900px) 100vw, 50vw')}</span>
<span class="svc-feature-body">
<span class="badge">{icon("star4")}Most requested: biweekly</span>
<span class="svc-feature-title">{rec['card_title']}</span>
<span class="svc-feature-text">{rec['card_text']}</span>
<span class="svc-feature-freq"><span>Weekly</span><span class="is-on">Biweekly</span><span>Monthly</span></span>
<span class="arrow-link">Explore recurring cleaning{icon("arrow")}</span>
</span></a>
<ul class="svc-rows">{minor}</ul>
</div>
<p class="sec-more"><a class="arrow-link" href="/residential-cleaning/">Compare all residential cleaning services{icon("arrow")}</a></p>
</div>
</section>

<section class="section biweekly" aria-labelledby="bw-h">
<div class="wrap bw-grid">
<figure class="bw-media">{pic('family-time', 'Parents and their young daughter relaxing with mugs on the living room floor', '(max-width: 900px) 100vw, 45vw')}</figure>
<div class="bw-copy">
{eyebrow('Biweekly cleaning', 'on-dark')}
<h2 id="bw-h">Why so many families choose <em>every two weeks</em></h2>
<p class="lead">For a busy household in a 3-bedroom, 2–3 bathroom home, biweekly cleaning hits the sweet spot: the house stays clean, the routine stays simple, and your weekends stay yours.</p>
<ul class="bw-list">{bw_html}</ul>
<div class="cta-row">{call_btn('Ask About Biweekly Cleaning', 'btn btn-light', 'biweekly')}
<a class="arrow-link on-dark" href="/recurring-cleaning/">How recurring cleaning works{icon("arrow")}</a></div>
</div>
</div>
</section>

{included_tabs()}
{steps_section('Four simple steps to a cleaner home')}

<section class="section story" aria-labelledby="story-h">
<div class="wrap story-grid">
<figure class="story-media">{pic('vanity-wipe', 'Gloved hand wiping a white bathroom vanity next to the sink', '(max-width: 900px) 100vw, 40vw')}</figure>
<div class="story-copy">
{eyebrow('Our story')}
<h2 id="story-h">Built from real experience inside our clients' homes</h2>
<p>Rio Cleaning Services LLC was established in {C.FOUNDED}, but the work behind it started long before. Our owner, Marcia, has been cleaning homes in the United States since the 2000s, with nearly 25 years of hands-on residential cleaning experience.</p>
<p>Over that time she has cleaned more than 1,000 homes and built relationships with clients who have stayed with her for around eight years. Today she leads two teams, and she still knows exactly what a job well done looks like, because she has done it herself.</p>
<dl class="facts">
<div><dt>Nearly 25</dt><dd>years of hands-on cleaning experience</dd></div>
<div><dt>1,000+</dt><dd>homes cleaned over Marcia's career</dd></div>
<div><dt>Since {C.FOUNDED}</dt><dd>as Rio Cleaning Services LLC</dd></div>
</dl>
<a class="arrow-link" href="/about/">Read our story{icon("arrow")}</a>
</div>
</div>
</section>

<section class="section areas-band" aria-labelledby="area-h">
<div class="wrap area-grid">
<div class="area-copy">
{eyebrow('Where we work')}
<h2 id="area-h">Based in Philadelphia. Serving nearby communities.</h2>
<p>We clean homes in Philadelphia and nearby communities in Pennsylvania, New Jersey and Delaware. Availability depends on where you live and how our teams' routes fall that week, so the quickest way to check is to ask.</p>
<div class="cta-row">{call_btn('Check Your ZIP Code', 'btn btn-primary', 'areas')}<a class="arrow-link" href="/service-areas/">About our service area{icon("arrow")}</a></div>
</div>
<figure class="area-media">{pic('townhomes', 'Row of two-story townhomes with vinyl siding on a residential street', '(max-width: 900px) 100vw, 40vw')}</figure>
</div>
</section>

{faq_section(home_faq)}
{estimate_section('Home')}
'''
    render(p, body)


def page_hub():
    slug = 'residential-cleaning'
    p = {'slug': slug, 'active': slug, 'og': 'living-room', 'lcp': 'living-room', 'lcp_sizes': '(max-width: 900px) 100vw, 46vw',
         'title': 'Residential Cleaning Services in Philadelphia | Rio Cleaning',
         'desc': 'Recurring, deep, move-in/move-out and carpet cleaning for homes in the Philadelphia area. See what each '
                 'service includes and which one fits your home.'}
    trail = [('Residential Cleaning', slug)]
    faq_keys = ['cost', 'regular-vs-deep', 'first-deep', 'which-frequency', 'insured', 'make-right']
    p['schema'] = [business_node(), webpage_node(p, 'CollectionPage'), crumbs_node(slug, trail),
                   service_node(slug, 'Residential cleaning services', 'House cleaning',
                                'Residential house cleaning for Philadelphia-area homes: recurring, deep, move-in/move-out '
                                'and carpet cleaning.'),
                   faq_node(slug, faq_keys)]
    rows = []
    for i, s in enumerate(C.SERVICES):
        rows.append(f'''<article class="hub-row{' rev' if i % 2 else ''}">
<figure>{pic(s['img'], s['img_alt'], '(max-width: 900px) 100vw, 45vw')}</figure>
<div class="hub-copy">
<p class="hub-k">{icon(s['icon'])}{s['eyebrow']}</p>
<h2>{s['name']}</h2>
<p>{s['card_text']}</p>
{checklist(s['for_who'])}
<a class="arrow-link" href="{url(s['slug'])}" data-track="service_click" data-service="{s['slug']}">{ {'recurring-cleaning': 'Weekly, biweekly and monthly options', 'deep-cleaning': 'When a deep cleaning makes sense', 'move-in-move-out-cleaning': 'Planning a move-out or move-in clean', 'carpet-cleaning': 'Carpet cleaning details'}[s['slug']] }{icon("arrow")}</a>
</div>
</article>''')
    which = [('Your home is in good shape and you want it to stay that way', 'recurring-cleaning', 'Recurring cleaning'),
             ('It\'s been a while since a professional cleaning', 'deep-cleaning', 'Deep cleaning, then recurring'),
             ('You\'re starting recurring service for the first time', 'deep-cleaning', 'First-time deep cleaning'),
             ('You\'re moving out, or moving into an empty home', 'move-in-move-out-cleaning', 'Move-in / move-out cleaning'),
             ('Carpets, stairs or rugs need attention', 'carpet-cleaning', 'Carpet cleaning'),
             ('You\'re not sure', 'contact', 'Call us and we\'ll recommend one')]
    which_rows = ''.join(f'<tr><th scope="row">{a}</th><td><a href="{url(s)}">{b}</a></td></tr>' for a, s, b in which)
    crit = [('How much experience does the team have?', 'Experience shows in the details and in how consistent each visit is.',
             'Our owner has nearly 25 years of hands-on residential cleaning experience.'),
            ('Is the company insured?', 'Protects you and your home if something goes wrong.', 'Yes, Rio Cleaning Services LLC is insured.'),
            ('Who do I talk to when I have a request?', 'Requests get lost when there\'s no one accountable.', 'Marcia, the owner, stays personally involved with clients.'),
            ('What happens if my week changes?', 'Rigid schedules don\'t fit real family life.', 'With two teams, we can often rearrange a visit.'),
            ('How is the price set?', 'A clear estimate avoids surprises.', 'A personalized estimate based on your home, service and frequency.'),
            ('What if something is missed?', 'Good companies fix problems instead of arguing about them.', 'Let us know so we can make it right.')]
    crit_rows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in crit)
    body = f'''
{page_hero(p, 'Residential cleaning', 'Residential cleaning services for Philadelphia-area homes',
           'House cleaning for families who want a home that feels cared for: recurring visits, deep cleans, move-in/move-out and carpet cleaning, all from one insured local team.',
           'living-room', 'Open living room with a sectional sofa, ceiling fan and large windows', crumbs=trail)}
{trust_bar('trust-flat')}
{definition('Residential cleaning is professional house cleaning for occupied or empty homes, covering kitchens, bathrooms, bedrooms, living areas and floors on a recurring or one-time basis.')}
<section class="section hub-list" aria-label="Our services">
<div class="wrap">{''.join(rows)}</div>
</section>
<section class="section tables" aria-labelledby="which-h">
<div class="wrap tables-grid">
<div>
{eyebrow('Which service do I need?')}
<h2 id="which-h">Match your situation to the right cleaning</h2>
<div class="table-wrap"><table class="table"><thead><tr><th scope="col">Your situation</th><th scope="col">Start with</th></tr></thead><tbody>{which_rows}</tbody></table></div>
</div>
<div>
{factors_table()}
</div>
</div>
</section>
<section class="section criteria" aria-labelledby="crit-h">
<div class="wrap">
<div class="sec-head">{eyebrow('Before you hire anyone')}<h2 id="crit-h">What to ask any house cleaning company</h2>
<p class="lead">Six questions worth asking before someone cleans your home, and how we answer them.</p></div>
<div class="table-wrap"><table class="table table-3"><thead><tr><th scope="col">Question to ask</th><th scope="col">Why it matters</th><th scope="col">Rio Cleaning</th></tr></thead><tbody>{crit_rows}</tbody></table></div>
</div>
</section>
{included_tabs()}
{steps_section()}
{faq_section(faq_keys)}
{estimate_section('Residential Cleaning')}
'''
    render(p, body)


def page_service(s: dict):
    slug = s['slug']
    p = {'slug': slug, 'active': slug, 'og': s['og'], 'lcp': s['img'], 'lcp_sizes': '(max-width: 900px) 100vw, 46vw',
         'title': s['title'], 'desc': s['desc']}
    trail = [('Residential Cleaning', 'residential-cleaning'), (s['short'], slug)]
    p['schema'] = [business_node(), webpage_node(p), crumbs_node(slug, trail),
                   service_node(slug, s['name'], s['service_type'], s['definition']), faq_node(slug, s['faqs'])]
    pre, link_slug, link_text, post = s['not_for']
    preset = {'recurring-cleaning': 'Recurring Cleaning', 'deep-cleaning': 'Deep Cleaning',
              'carpet-cleaning': 'Carpet Cleaning'}.get(slug, '')
    extra = SERVICE_EXTRAS[slug]()
    included = included_single(s['included'], f'What\'s included in {s["short"].lower()}') if s['included'] else ''
    body = f'''
{page_hero(p, s['eyebrow'], s['h1'], s['lede'], s['img'], s['img_alt'], crumbs=trail)}
{trust_bar('trust-flat')}
{definition(s['definition'])}
<section class="section fit" aria-labelledby="fit-h">
<div class="wrap fit-grid">
<div>{eyebrow('Who it\'s for')}<h2 id="fit-h">A good fit for</h2>{checklist(s['for_who'], 'checks checks-lg')}</div>
<aside class="fit-alt">{icon('arrow-up-right')}<p>{pre}<a href="{url(link_slug)}">{link_text}</a>{post}</p></aside>
</div>
</section>
{extra}
{included}
<section class="section estimate-factors">
<div class="wrap narrow">{factors_table()}</div>
</section>
{steps_section()}
{owner_note()}
{faq_section(s['faqs'], f'{s["short"]}: common questions')}
{related_links(s['related'], slug)}
{estimate_section(s['name'], f'Get your {s["short"].lower()} estimate', preset)}
'''
    render(p, body)


def owner_note() -> str:
    return f'''<section class="section owner" aria-label="About the owner">
<div class="wrap owner-in">
<p class="owner-quote">Rio Cleaning Services is owner-led. Marcia, who has nearly 25 years of hands-on residential cleaning experience, stays personally involved with our clients and their homes.</p>
<p class="owner-meta">{icon('users')}<span>Rio Cleaning Services LLC · Philadelphia, PA · Page updated {C.UPDATED}</span></p>
</div>
</section>'''


def extra_recurring() -> str:
    rows = ''.join(f'<tr{HL if f == "Biweekly" else ""}><th scope="row">{f}{POP if f == "Biweekly" else ""}</th><td>{a}</td><td>{b}</td></tr>'
                   for f, a, b in C.FREQUENCIES)
    return f'''<section class="section freq" aria-labelledby="freq-h">
<div class="wrap">
<div class="sec-head">{eyebrow('Choose your frequency')}<h2 id="freq-h">Weekly, biweekly or monthly: which fits your home?</h2>
<p class="lead">There's no wrong answer, and you can change it later. Here's how each schedule tends to feel.</p></div>
<div class="table-wrap"><table class="table table-3"><thead><tr><th scope="col">Frequency</th><th scope="col">Best for</th><th scope="col">What it's like</th></tr></thead><tbody>{rows}</tbody></table></div>
</div>
</section>
<section class="section bw-split" aria-labelledby="bw2-h">
<div class="wrap bw2-grid">
<figure>{pic('family-time', 'Parents and their young daughter relaxing on the living room floor', '(max-width: 900px) 100vw, 45vw')}</figure>
<div>
{eyebrow('Biweekly cleaning')}
<h2 id="bw2-h">Why biweekly works so well for busy families</h2>
<p>Every two weeks is often enough that kitchens, bathrooms and floors never slide back to "needs a deep clean," and far enough apart that it fits comfortably into the household budget and routine.</p>
{checklist(['A consistently clean home, not a cycle of clean and messy', 'Easier upkeep between visits', 'A predictable routine you don\'t have to think about', 'Less weekend cleaning, more time for your family', 'Flexible scheduling when your week changes'])}
<div class="cta-row">{call_btn('Ask About Biweekly Cleaning', 'btn btn-primary', 'biweekly_page')}</div>
</div>
</div>
</section>'''


def extra_deep() -> str:
    rows = [('Goal', 'Keep a clean home clean', 'Reset a home with buildup'),
            ('When', 'Weekly, biweekly or monthly', 'First visit, seasonal or catch-up'),
            ('Focus', 'Kitchens, bathrooms, dusting, floors, trash', 'Everything in a regular clean, plus buildup, baseboards and detail work'),
            ('Time in your home', 'Shorter, consistent visits', 'A longer, more detailed visit'),
            ('Best next step', 'Stay on your schedule', 'Move to recurring visits to keep the results')]
    r = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    when = [('home', 'Before starting recurring service', 'Gets your home to a level regular visits can maintain.'),
            ('sun', 'Seasonal resets', 'Spring and fall are popular times to catch up on the details.'),
            ('users', 'Before guests or holidays', 'Kitchens and bathrooms ready for a full house.'),
            ('clock', 'After a busy stretch', 'A new baby, a renovation nearby or a few hectic months.')]
    w = ''.join(f'<li>{icon(i)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in when)
    return f'''<section class="section when" aria-labelledby="when-h">
<div class="wrap">
<div class="sec-head">{eyebrow('When to book')}<h2 id="when-h">When a deep cleaning makes sense</h2></div>
<ul class="icon-grid">{w}</ul>
</div>
</section>
<section class="section compare" aria-labelledby="cmp-h">
<div class="wrap">
<div class="sec-head">{eyebrow('Regular vs. deep')}<h2 id="cmp-h">Regular cleaning vs. deep cleaning</h2></div>
<div class="table-wrap"><table class="table table-3"><thead><tr><th scope="col"></th><th scope="col"><a href="/recurring-cleaning/">Regular cleaning</a></th><th scope="col">Deep cleaning</th></tr></thead><tbody>{r}</tbody></table></div>
</div>
</section>'''


def extra_move() -> str:
    tips = [('calendar', 'Book early', 'Call as soon as you know your moving dates, especially at the end of the month.'),
            ('box', 'Clean after the movers', 'Empty rooms let us reach inside cabinets, along baseboards and every corner.'),
            ('key', 'Plan access', 'Tell us how we\'ll get in and whether utilities will still be on.'),
            ('carpet', 'Add carpets if needed', 'Pair it with carpet cleaning in rooms with wall-to-wall carpet.')]
    t = ''.join(f'<li>{icon(i if i in ICONS else "check")}<div><h3>{a}</h3><p>{b}</p></div></li>' for i, a, b in tips)
    return f'''<section class="section when" aria-labelledby="tips-h">
<div class="wrap">
<div class="sec-head">{eyebrow('Moving checklist')}<h2 id="tips-h">Making your move-out or move-in clean go smoothly</h2></div>
<ul class="icon-grid">{t}</ul>
<div class="mo-split">
<div><h3>{icon('door')}Moving out</h3><p>Leave the home clean for the next residents or the owner. We focus on what's left behind once the furniture is gone: inside cabinets, bathrooms, baseboards and floors.</p></div>
<div><h3>{icon('home')}Moving in</h3><p>Start fresh before you unpack. Cleaning an empty home first means your dishes, clothes and furniture go into clean spaces.</p></div>
</div>
</div>
</section>'''


def extra_carpet() -> str:
    areas = [('sofa', 'Living rooms & family rooms', 'The rooms that see the most foot traffic.'),
             ('home', 'Bedrooms & hallways', 'Wall-to-wall carpet throughout the home.'),
             ('list', 'Stairs', 'Carpeted stairs and landings.'),
             ('carpet', 'Area rugs', 'Let us know the size and material when you call.')]
    a = ''.join(f'<li>{icon(i)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in areas)
    return f'''<section class="section when" aria-labelledby="ca-h">
<div class="wrap">
<div class="sec-head">{eyebrow('What we clean')}<h2 id="ca-h">Carpets and rugs throughout your home</h2>
<p class="lead">Tell us which rooms, stairs and rugs you'd like cleaned, and about any stains or pet areas. We'll talk through what to expect when preparing your estimate.</p></div>
<ul class="icon-grid">{a}</ul>
<div class="mo-split">
<div><h3>{icon('key')}Pair it with a move</h3><p>Carpet cleaning is a natural add-on to a <a href="/move-in-move-out-cleaning/">move-out or move-in clean</a>, when rooms are empty and every inch is reachable.</p></div>
<div><h3>{icon('sparkles')}Pair it with a deep clean</h3><p>Booking with a <a href="/deep-cleaning/">deep cleaning</a> refreshes the whole home at once, floors included.</p></div>
</div>
</div>
</section>'''


ICONS['box'] = '<path d="M11 21.7a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7z"/><path d="M12 22V12"/><path d="m3.3 7 7.7 4.7a2 2 0 0 0 2 0L20.7 7"/>'
SERVICE_EXTRAS = {'recurring-cleaning': extra_recurring, 'deep-cleaning': extra_deep,
                  'move-in-move-out-cleaning': extra_move, 'carpet-cleaning': extra_carpet}


def page_about():
    slug = 'about'
    p = {'slug': slug, 'active': slug, 'og': 'kitchen-open', 'lcp': 'kitchen-open', 'lcp_sizes': '(max-width: 900px) 100vw, 46vw',
         'title': 'About Rio Cleaning Services | Philadelphia House Cleaning',
         'desc': 'Meet Rio Cleaning Services: an owner-led Philadelphia house cleaning company, established in 2019 and '
                 'backed by nearly 25 years of hands-on cleaning experience.'}
    trail = [('About', slug)]
    p['schema'] = [business_node(), webpage_node(p, 'AboutPage'), crumbs_node(slug, trail)]
    values = [('eye', 'The details matter', 'Clean is in the corners, the handles and the baseboards. We clean the way we\'d want our own homes cleaned.'),
              ('repeat', 'Consistency over flash', 'Recurring clients should get the same careful work on visit fifty as on visit one.'),
              ('message', 'Clear, direct communication', 'You know who you\'re talking to, and requests reach someone who can act on them.'),
              ('calendar', 'Respect for your time', 'We show up as scheduled and work with you when plans change.'),
              ('badge', 'Making it right', 'If something doesn\'t meet expectations, let us know so we can make it right.')]
    v = ''.join(f'<li>{icon(i)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in values)
    body = f'''
{page_hero(p, 'About us', 'An owner-led house cleaning company, built on experience',
           'Rio Cleaning Services LLC has proudly served local homeowners since 2019, backed by nearly 25 years of hands-on residential cleaning experience.',
           'kitchen-open', 'Bright open kitchen with white cabinets leading into the dining area', crumbs=trail)}
{definition('Rio Cleaning Services LLC is a residential cleaning company based in Philadelphia, PA, founded in 2019 by Marcia, who has nearly 25 years of hands-on experience cleaning homes in the United States.')}
<section class="section about-story" aria-labelledby="as-h">
<div class="wrap about-grid">
<div class="about-copy">
{eyebrow('Our story')}
<h2 id="as-h">It started with one person doing the work, and doing it well</h2>
<p>Marcia has been cleaning homes in the United States since the 2000s. Long before there was a company name, there were kitchens, bathrooms and living rooms, cleaned one at a time, for families who came to rely on her.</p>
<p>Over nearly 25 years, she has cleaned more than 1,000 homes. Some of the families she works with have been clients for around eight years. That kind of relationship doesn't come from a sales pitch. It comes from showing up, doing careful work and caring about the people who live there.</p>
<p>In {C.FOUNDED}, Marcia formalized that work as Rio Cleaning Services LLC. She has since managed two teams and a schedule of up to about 230 active homes, and she stays personally involved with clients today.</p>
<p>The name and our colors are a quiet nod to Brazil, where our story began. The way we work is simple and local: reliable people, careful cleaning and a direct line to the owner.</p>
</div>
<aside class="about-facts">
<h2 class="h3">At a glance</h2>
<dl class="facts facts-col">
<div><dt>Nearly 25 years</dt><dd>of hands-on residential cleaning experience</dd></div>
<div><dt>{C.FOUNDED}</dt><dd>Rio Cleaning Services LLC established</dd></div>
<div><dt>1,000+ homes</dt><dd>cleaned over Marcia's career</dd></div>
<div><dt>~8 years</dt><dd>with some of our long-term clients</dd></div>
<div><dt>Two teams</dt><dd>for more flexible scheduling</dd></div>
</dl>
<p class="fine">{icon('shield')}Insured · Locally owned and operated</p>
</aside>
</div>
</section>
<section class="section values" aria-labelledby="val-h">
<div class="wrap">
<div class="sec-head">{eyebrow('How we work')}<h2 id="val-h">What you can expect from us</h2></div>
<ul class="icon-grid icon-grid-5">{v}</ul>
</div>
</section>
<section class="section about-services" aria-labelledby="asv-h">
<div class="wrap narrow center">
{eyebrow('What we do')}
<h2 id="asv-h">Focused on homes, and the families who live in them</h2>
<p>We specialize in residential cleaning: <a href="/recurring-cleaning/">weekly, biweekly and monthly visits</a>, <a href="/deep-cleaning/">first-time deep cleaning</a>, <a href="/move-in-move-out-cleaning/">move-in and move-out cleaning</a> and <a href="/carpet-cleaning/">carpet cleaning</a>. Many of our clients are families in 3-bedroom homes who choose biweekly service.</p>
</div>
</section>
{estimate_section('About', 'Talk to Rio Cleaning about your home')}
'''
    render(p, body)


def page_areas():
    slug = 'service-areas'
    p = {'slug': slug, 'active': slug, 'og': 'townhomes', 'lcp': 'townhomes', 'lcp_sizes': '(max-width: 900px) 100vw, 46vw',
         'title': 'Service Areas: Philadelphia & Nearby | Rio Cleaning Services',
         'desc': 'Rio Cleaning Services is based in Philadelphia and cleans homes in nearby Pennsylvania, New Jersey and '
                 'Delaware communities. Call to check your ZIP code.'}
    trail = [('Service Areas', slug)]
    faq_keys = ['areas', 'reschedule', 'home-during', 'cost']
    p['schema'] = [business_node(), webpage_node(p), crumbs_node(slug, trail), faq_node(slug, faq_keys)]
    cities = ''
    if C.CONFIRMED_CITIES:
        li = ''.join(f'<li>{icon("pin")}<span>{c["name"]}, {c["state_abbr"]}</span></li>' for c in C.CONFIRMED_CITIES)
        cities = f'<div class="city-list"><h2 class="h3">Communities we serve</h2><ul>{li}</ul></div>'
    states = [('Pennsylvania', 'Philadelphia, where we\'re based, and nearby communities.'),
              ('New Jersey', 'Communities within reach of the Philadelphia area.'),
              ('Delaware', 'Communities within reach of the Philadelphia area.')]
    st = ''.join(f'<li><h3>{icon("map")}{a}</h3><p>{b}</p></li>' for a, b in states)
    body = f'''
{page_hero(p, 'Service areas', 'House cleaning in Philadelphia and nearby communities',
           'We\'re a Philadelphia-based team cleaning homes in the city and nearby communities in Pennsylvania, New Jersey and Delaware.',
           'townhomes', 'Row of two-story townhomes with vinyl siding on a residential street', crumbs=trail,
           cta_secondary=estimate_btn('Send Your ZIP Code'))}
{definition('Rio Cleaning Services is a service-area business: we come to you. Our teams work out of Philadelphia, PA, and clean homes in nearby communities across the region.')}
<section class="section areas-main" aria-labelledby="am-h">
<div class="wrap areas-grid">
<div>
{eyebrow('Where we work')}
<h2 id="am-h">Focused on the Philadelphia area</h2>
<p>Our recurring clients are scheduled on regular routes, which is how we keep visits consistent and on time. That also means we stay close to home: we serve Philadelphia and communities near it rather than entire states.</p>
<p>If you live nearby in Pennsylvania, New Jersey or Delaware, there's a good chance we can help. Availability depends on your exact location and our teams' schedules, so the fastest way to know is to call <a href="{C.TEL}" data-track="phone_click" data-where="areas_text">{C.PHONE}</a> or include your ZIP code in an <a href="#estimate">estimate request</a>.</p>
{cities}
</div>
<ul class="state-list">{st}</ul>
</div>
</section>
<section class="section zip-band" aria-labelledby="zip-h">
<div class="wrap zip-in">
<div><h2 id="zip-h">Not sure if you're in our area?</h2><p>Give us your ZIP code and the type of cleaning you need. We'll tell you right away.</p></div>
<div class="cta-row">{call_btn('Call (267) 694-4609', 'btn btn-light', 'zip_band')}{estimate_btn('Send a Request', 'btn btn-outline-light')}</div>
</div>
</section>
{faq_section(faq_keys, 'Service area questions')}
{estimate_section('Service Areas', 'Check availability for your home')}
'''
    render(p, body)


def page_reviews():
    slug = 'reviews'
    p = {'slug': slug, 'active': slug, 'og': 'living-room-2', 'lcp': 'living-room-2', 'lcp_sizes': '(max-width: 900px) 100vw, 46vw',
         'title': 'Reviews & Client Relationships | Rio Cleaning Services',
         'desc': 'What working with Rio Cleaning Services looks like: long-term client relationships, an owner who stays '
                 'involved and a commitment to make things right.'}
    trail = [('Reviews', slug)]
    p['schema'] = [business_node(), webpage_node(p), crumbs_node(slug, trail)]
    if C.REVIEWS:
        cards = ''.join(f'<figure class="review"><blockquote><p>{e(r["text"])}</p></blockquote><figcaption>'
                        f'<strong>{e(r["name"])}</strong><a href="{r["url"]}" target="_blank" rel="noopener">{e(r["source"])}'
                        f'{icon("arrow-up-right")}</a></figcaption></figure>' for r in C.REVIEWS)
        reviews_block = f'<section class="section" aria-labelledby="rv-h"><div class="wrap"><div class="sec-head">{eyebrow("Client reviews")}<h2 id="rv-h">See what local homeowners are saying</h2></div><div class="reviews">{cards}</div></div></section>'
    else:
        reviews_block = ''
    links = [tracked_link(C.FACEBOOK, f'{icon("facebook")}<span>Facebook</span>', 'facebook_click', 'btn btn-ghost'),
             tracked_link(C.INSTAGRAM, f'{icon("instagram")}<span>Instagram</span>', 'instagram_click', 'btn btn-ghost')]
    if C.GOOGLE_PROFILE:
        links.insert(0, tracked_link(C.GOOGLE_PROFILE, f'{icon("google")}<span>Google</span>', 'google_profile_click', 'btn btn-ghost'))
    body = f'''
{page_hero(p, 'Reviews', 'Rio Cleaning Services reviews and client relationships',
           'We only share real feedback from real clients. Here\'s what working with us looks like, and where to find and leave reviews.',
           'living-room-2', 'Tidy American living room with a gray sectional, patterned rug and ceiling fan', crumbs=trail)}
{reviews_block}
<section class="section rel-facts" aria-labelledby="rf-h">
<div class="wrap about-grid">
<div class="about-copy">
{eyebrow('Long-term relationships')}
<h2 id="rf-h">The best review is a client who stays</h2>
<p>Some of the families Marcia cleans for have been with her for around eight years. Over nearly 25 years in residential cleaning, she has worked in more than 1,000 homes.</p>
<p>When you work with Rio Cleaning Services, you can expect the owner to stay involved, visits to be consistent, and any problem to be handled directly: if something doesn't meet expectations, let us know so we can make it right.</p>
</div>
<aside class="about-facts">
<h2 class="h3">Read and share reviews</h2>
<p>Find us on our official pages. If we've cleaned your home, we'd be grateful if you shared your experience.</p>
<div class="review-links">{''.join(links)}</div>
</aside>
</div>
</section>
{estimate_section('Reviews', 'See the difference in your own home')}
'''
    render(p, body)


def page_faq():
    slug = 'faq'
    p = {'slug': slug, 'active': slug, 'og': 'kitchen-open',
         'title': 'House Cleaning FAQ | Rio Cleaning Services, Philadelphia',
         'desc': 'Answers about house cleaning estimates, recurring and deep cleaning, scheduling, payment, insurance '
                 'and service areas from Rio Cleaning Services.'}
    trail = [('FAQ', slug)]
    keys = [k for _, ks in C.FAQ_GROUPS for k in ks]
    p['schema'] = [business_node(), webpage_node(p), crumbs_node(slug, trail), faq_node(slug, keys)]
    groups = ''.join(f'<section class="faq-group" aria-labelledby="g-{i}"><h2 id="g-{i}" class="h3">{g}</h2>{faq_list(ks, 3)}</section>'
                     for i, (g, ks) in enumerate(C.FAQ_GROUPS))
    nav = ''.join(f'<li><a href="#g-{i}">{g}</a></li>' for i, (g, _) in enumerate(C.FAQ_GROUPS))
    body = f'''
<section class="phero phero-slim">
<div class="wrap">
{breadcrumb(trail)}
{eyebrow('Frequently asked questions')}
<h1>House cleaning questions, answered</h1>
<p class="lede">Straight answers about estimates, scheduling, services and what to expect. Still have a question? Call <a href="{C.TEL}" data-track="phone_click" data-where="faq_hero">{C.PHONE}</a>.</p>
</div>
</section>
<section class="section faq-page">
<div class="wrap faq-page-grid">
<nav class="faq-nav" aria-label="FAQ topics"><p class="footer-h">Topics</p><ul>{nav}</ul></nav>
<div>{groups}</div>
</div>
</section>
{estimate_section('FAQ')}
'''
    render(p, body)


def page_contact():
    slug = 'contact'
    p = {'slug': slug, 'active': slug, 'og': 'kitchen-open',
         'title': 'Contact Us & Request an Estimate | Rio Cleaning Services',
         'desc': f'Call {C.PHONE} or send a request for a free, personalized house cleaning estimate from Rio Cleaning '
                 'Services in the Philadelphia area.'}
    trail = [('Contact', slug)]
    p['schema'] = [business_node(), webpage_node(p, 'ContactPage'), crumbs_node(slug, trail)]
    hours = f'<li>{icon("clock")}<div><strong>Office hours</strong><span>{C.HOURS["label"]}</span></div></li>' if C.HOURS else ''
    body = f'''
<section class="phero phero-slim contact-hero">
<div class="wrap">
{breadcrumb(trail)}
{eyebrow('Contact')}
<h1>Request your house cleaning estimate</h1>
<p class="lede">Call us for the quickest answer, or send the form below. Estimates are free and personalized to your home.</p>
<div class="sent-msg" id="sent-msg" hidden role="status"><p>{icon("check-circle")}<span>Thank you! Your request was sent. We'll get back to you soon. For anything urgent, call <a href="{C.TEL}">{C.PHONE}</a>.</span></p></div>
</div>
</section>
<section class="section contact-main" id="estimate" aria-labelledby="cm-h">
<div class="wrap contact-grid">
<div class="contact-info">
<h2 id="cm-h" class="h3">Talk to us</h2>
<a class="est-phone dark" href="{C.TEL}" data-track="phone_click" data-where="contact">{icon("phone")}<span>{C.PHONE}</span></a>
<ul class="info-list">
<li>{icon("mail")}<div><strong>Email</strong><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></div></li>
{hours}
<li>{icon("pin")}<div><strong>Service area</strong><span>Based in Philadelphia, PA. Serving nearby communities in Pennsylvania, New Jersey and Delaware. <a href="/service-areas/">More about our area</a></span></div></li>
<li>{icon("card")}<div><strong>Payment</strong><span>{', '.join(C.PAYMENTS)}</span></div></li>
</ul>
<div class="next-steps">
<h2 class="h3">What happens next</h2>
<ol>
<li>We review your request and reach out by your preferred contact method.</li>
<li>We confirm the details of your home, the service and how often you'd like it.</li>
<li>You receive your personalized estimate and choose a time that works.</li>
</ol>
</div>
</div>
<div class="contact-form">
<h2 class="h3">Send a request</h2>
{quote_form('Contact')}
</div>
</div>
</section>
'''
    render(p, body)


def legal_page(slug, title_tag, desc, h1, sections_html):
    p = {'slug': slug, 'active': slug, 'title': title_tag, 'desc': desc, 'og': 'hero-kitchen'}
    trail = [(h1, slug)]
    p['schema'] = [business_node(), webpage_node(p), crumbs_node(slug, trail)]
    body = f'''
<section class="phero phero-slim">
<div class="wrap">{breadcrumb(trail)}<h1>{h1}</h1><p class="lede">Last updated: {C.UPDATED}</p></div>
</section>
<section class="section legal"><div class="wrap narrow prose">{sections_html}</div></section>
'''
    render(p, body)


def page_privacy():
    s = f'''
<p>This Privacy Policy explains how {C.LEGAL_NAME} ("Rio Cleaning Services," "we," "us") collects and uses information when you visit riocleanings.com or contact us about our residential cleaning services.</p>
<h2>Information we collect</h2>
<p>When you call us, email us or submit our estimate form, we collect the information you choose to share, such as your name, phone number, email address, ZIP code, the type and frequency of cleaning you're interested in, the number of bedrooms and bathrooms in your home, your preferred contact method and any message you include.</p>
<p>Like most websites, our hosting provider may automatically record basic technical information such as your IP address, browser type and the pages you visit. If we enable analytics or advertising measurement tools (for example, Google Analytics, Google Ads or Meta Pixel), those tools may use cookies or similar technologies to understand how visitors use the site and how our advertising performs.</p>
<h2>How we use your information</h2>
<ul><li>To respond to your request and prepare your cleaning estimate.</li><li>To schedule, provide and follow up on cleaning services.</li><li>To communicate with you about your request or appointments.</li><li>To maintain records and improve our website and services.</li></ul>
<p>We do not sell your personal information. We do not send marketing text messages through this website.</p>
<h2>How your form submission is processed</h2>
<p>Our estimate form is delivered to our business email inbox through FormSubmit (formsubmit.co), a third-party form-processing service. Your submission is transmitted to that service only to deliver it to us.</p>
<h2>Sharing</h2>
<p>We share information only with service providers that help us operate our business (such as email, website hosting and form delivery), when required by law, or to protect our rights and safety.</p>
<h2>Data retention and security</h2>
<p>We keep information only as long as needed for the purposes above or as required by law, and we use reasonable measures to protect it. No method of transmission or storage is completely secure.</p>
<h2>Your choices</h2>
<p>You can ask us to access, correct or delete the personal information you've shared with us by emailing <a href="mailto:{C.EMAIL}">{C.EMAIL}</a> or calling <a href="{C.TEL}">{C.PHONE}</a>. You can also control cookies through your browser settings.</p>
<h2>Children's privacy</h2>
<p>Our website is not directed to children under 13, and we do not knowingly collect personal information from them.</p>
<h2>Changes to this policy</h2>
<p>We may update this Privacy Policy from time to time. The date at the top of this page shows when it was last updated.</p>
<h2>Contact</h2>
<p>{C.LEGAL_NAME}<br>Philadelphia, Pennsylvania<br><a href="{C.TEL}">{C.PHONE}</a> · <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>'''
    legal_page('privacy-policy', 'Privacy Policy | Rio Cleaning Services LLC',
               'How Rio Cleaning Services LLC collects, uses and protects the information you share through our website, '
               'phone and email.', 'Privacy Policy', s)


def page_terms():
    s = f'''
<p>These Terms &amp; Conditions apply to the use of riocleanings.com and to residential cleaning services provided by {C.LEGAL_NAME} ("Rio Cleaning Services," "we," "us"). By using this website or booking a service, you agree to these terms.</p>
<h2>Estimates</h2>
<p>Estimates are based on the information you provide, such as the size of your home, the type of cleaning, its condition and the frequency of service. If the home's size or condition differs significantly from what was described, or you request additional services, we will discuss any changes with you before proceeding.</p>
<h2>Scheduling and rescheduling</h2>
<p>Appointments are scheduled based on availability. If you need to reschedule or cancel, please let us know as early as possible so we can offer the time to another household. We will do the same if we ever need to adjust your appointment.</p>
<h2>Access, pets and safety</h2>
<p>Please make sure we can access your home at the scheduled time and let us know about any entry instructions, alarm systems and pets in advance. We may decline to clean areas that are unsafe, such as spaces with mold, pests, hazardous materials or biohazards.</p>
<h2>Valuables and fragile items</h2>
<p>We ask that you put away jewelry, cash, important documents and items of significant financial or sentimental value, and let us know about anything fragile you'd prefer we not handle.</p>
<h2>Payment</h2>
<p>We accept Zelle, Venmo, credit cards, checks and cash. Payment timing and method will be confirmed when your cleaning is scheduled.</p>
<h2>Satisfaction</h2>
<p>If something doesn't meet expectations, let us know as soon as possible so we can make it right. Reporting concerns promptly allows us to review and address them while the details are fresh.</p>
<h2>Insurance and liability</h2>
<p>{C.LEGAL_NAME} is insured. If you believe something was damaged during a cleaning, please notify us promptly so we can review the situation with you. To the extent permitted by law, our liability is limited to the cost of the service provided, and we are not responsible for pre-existing damage, normal wear, or items that were improperly secured.</p>
<h2>Website content</h2>
<p>Information on this website is provided for general purposes and may change without notice. Some photos on this website are representative stock images of homes and cleaning work.</p>
<h2>Governing law</h2>
<p>These terms are governed by the laws of the Commonwealth of Pennsylvania.</p>
<h2>Contact</h2>
<p>{C.LEGAL_NAME}<br>Philadelphia, Pennsylvania<br><a href="{C.TEL}">{C.PHONE}</a> · <a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>'''
    legal_page('terms-and-conditions', 'Terms & Conditions | Rio Cleaning Services LLC',
               'Terms for using riocleanings.com and booking residential cleaning with Rio Cleaning Services LLC: estimates, '
               'scheduling, payment and satisfaction.', 'Terms & Conditions', s)


def page_404():
    p = {'slug': '404', 'file': '404.html', 'active': '', 'noindex': True,
         'title': 'Page Not Found | Rio Cleaning Services', 'desc': 'The page you were looking for could not be found.'}
    p['schema'] = [business_node()]
    links = ''.join(f'<li><a href="{url(s["slug"])}">{s["short"]}</a></li>' for s in C.SERVICES)
    body = f'''
<section class="phero phero-slim">
<div class="wrap narrow">
{eyebrow('Page not found')}
<h1>This page has moved, or never existed</h1>
<p class="lede">Let's get you back on track. Start from the <a href="/">home page</a>, see our services below, or call <a href="{C.TEL}" data-track="phone_click" data-where="404">{C.PHONE}</a>.</p>
<ul class="pill-links"><li><a href="/residential-cleaning/">All services</a></li>{links}<li><a href="/contact/">Contact</a></li></ul>
</div>
</section>'''
    render(p, body)


# ---------------------------------------------------------------- site files
REDIRECTS = [('/about-us/', '/about/'), ('/services/', '/residential-cleaning/'), ('/service/', '/residential-cleaning/'),
             ('/contact-us/', '/contact/'), ('/hello-world/', '/'), ('/category/uncategorized/', '/'),
             ('/author/paulotmaqueara01gmail-com/', '/about/'), ('/feed/', '/'), ('/comments/feed/', '/'),
             ('/index.html', '/')]


def site_files():
    (OUT / 'assets' / 'icons.svg').write_text(sprite(), encoding='utf-8')
    urls = [pg for pg in PAGES if not pg.get('noindex')]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pg in urls:
        sm.append(f'<url><loc>{abs_url(pg["slug"])}</loc><lastmod>{C.UPDATED_ISO}</lastmod></url>')
    sm.append('</urlset>')
    (OUT / 'sitemap.xml').write_text('\n'.join(sm) + '\n', encoding='utf-8')
    (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {C.SITE_URL}/sitemap.xml\n', encoding='utf-8')
    manifest = {'name': C.NAME, 'short_name': 'Rio Cleaning', 'start_url': '/', 'display': 'browser',
                'background_color': '#fbf8f3', 'theme_color': '#fbf8f3',
                'icons': [{'src': '/assets/img/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                          {'src': '/assets/img/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}
    (OUT / 'site.webmanifest').write_text(json.dumps(manifest, indent=1), encoding='utf-8')
    # Vercel (project root = rio-cleaning/)
    vercel = {
        'outputDirectory': 'site', 'trailingSlash': True, 'cleanUrls': False,
        'redirects': [{'source': src, 'destination': b, 'permanent': True}
                      for a, b in REDIRECTS for src in ([a] if a.endswith('.html') else [a.rstrip('/'), a])],
        'headers': [
            {'source': '/assets/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=31536000, immutable'}]},
            {'source': '/(.*)', 'headers': [
                {'key': 'X-Content-Type-Options', 'value': 'nosniff'},
                {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'},
                {'key': 'X-Frame-Options', 'value': 'SAMEORIGIN'},
                {'key': 'Permissions-Policy', 'value': 'camera=(), microphone=(), geolocation=()'}]},
        ],
    }
    (ROOT / 'vercel.json').write_text(json.dumps(vercel, indent=2) + '\n', encoding='utf-8')
    # Apache / Hostinger
    rules = '\n'.join(f'RewriteRule ^{re.escape(a.strip("/"))}/?$ {b} [R=301,L]' for a, b in REDIRECTS if a != '/index.html')
    htaccess = f'''# Rio Cleaning Services - Apache / Hostinger configuration (generated by build/build.py)
Options -MultiViews -Indexes
DirectorySlash On
ErrorDocument 404 /404.html

<IfModule mod_rewrite.c>
RewriteEngine On
# Force HTTPS and the bare domain
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteCond %{{HTTP_HOST}} ^(?:www\\.)?(.+)$ [NC]
RewriteRule ^ https://%1%{{REQUEST_URI}} [R=301,L]
# /index.html -> /
RewriteCond %{{THE_REQUEST}} \\s/+(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^ /%1 [R=301,L]
# Old WordPress URLs -> new pages
{rules}
</IfModule>

<IfModule mod_headers.c>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set X-Frame-Options "SAMEORIGIN"
<FilesMatch "\\.(webp|png|jpg|ico|svg|woff2|css|js)$">
Header set Cache-Control "public, max-age=31536000, immutable"
</FilesMatch>
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/json text/plain application/xml
</IfModule>
AddType image/webp .webp
AddType application/manifest+json .webmanifest
'''
    (OUT / '.htaccess').write_text(htaccess, encoding='utf-8')


def check_meta():
    titles, descs = {}, {}
    for pg in PAGES:
        t, d = pg['title'], pg['desc']
        assert t not in titles, f'duplicate title {t}'
        assert d not in descs, f'duplicate description {d}'
        titles[t] = descs[d] = pg['slug']
        if pg.get('noindex'):
            continue
        if len(t) > 62 or len(d) > 160 or len(d) < 110:
            print(f'  ! length check {pg["slug"] or "home"}: title {len(t)}, desc {len(d)}')


def main():
    page_home()
    page_hub()
    for s in C.SERVICES:
        page_service(s)
    page_about()
    page_areas()
    page_reviews()
    page_faq()
    page_contact()
    page_privacy()
    page_terms()
    page_404()
    site_files()
    check_meta()
    print(f'{len(PAGES)} pages written to {OUT}')


if __name__ == '__main__':
    main()
