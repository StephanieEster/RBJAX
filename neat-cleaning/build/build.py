#!/usr/bin/env python3
"""Static site generator for the Neat Cleaning website.

Copy and data live in content.py; this file holds the shared components and page
templates. Run `python3 build/build.py` from the neat-cleaning folder; the HTML is
written to site/. Missing business data is marked PREENCHER here and in LEIA-ME.md.
"""
from __future__ import annotations

import html
import json
import math
import re
from pathlib import Path

from content import (BIZ_ID, DIST, EMAIL, FAQ_GENERAL, IMG_ALT, LEGAL_PRIVACY, LEGAL_TERMS, NATICK, ORIGIN,
                     OWNER, PHONE, PHONE_E164, SERVICE_PAGES, SERVICES, SITE_ID, SMS, SVC, TEL, TOWN_LIST, TOWNS,
                     UPDATED, UPDATED_ISO)

OUT = Path(__file__).resolve().parent.parent / 'site'
e = html.escape

# ---------------------------------------------------------------- icons
# Line icons adapted from Lucide (ISC license), drawn on a 24px grid.
ICONS = {
    'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    'arrow-up-right': '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>',
    'chev': '<path d="m6 9 6 6 6-6"/>',
    'plus': '<path d="M5 12h14"/><path d="M12 5v14"/>',
    'check': '<path d="M20 6 9 17l-5-5"/>',
    'check-circle': '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    'help': '<circle cx="12" cy="12" r="10"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h10"/>',
    'home': '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    'sparkles': '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/><path d="M5 3v4M3 5h4M19 17v4M17 19h4"/>',
    'sparkle': '<path d="M12 2c.5 5 2 7 7 7.5-5 .5-6.5 2.5-7 7.5-.5-5-2-7-7-7.5 5-.5 6.5-2.5 7-7.5Z"/>',
    'key': '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/>',
    'truck': '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H9"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    'building': '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z"/><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2"/><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2"/><path d="M10 6h4M10 10h4M10 14h4M10 18h4"/>',
    'message': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M8 12h.01M12 12h.01M16 12h.01"/>',
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    'mail': '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-9 5.7a2 2 0 0 1-2 0L2 7"/>',
    'pin': '<path d="M20 10c0 5-5.5 10.2-7.4 11.8a1 1 0 0 1-1.2 0C9.5 20.2 4 15 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    'card': '<rect width="20" height="14" x="2" y="5" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/>',
    'user': '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
    'award': '<circle cx="12" cy="8" r="6"/><path d="M15.5 12.9 17 22l-5-3-5 3 1.5-9.1"/>',
    'shield': '<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    'calendar': '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/><path d="m9 16 2 2 4-4"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'clipboard': '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="M12 11h4M12 16h4M8 11h.01M8 16h.01"/>',
    'file': '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8M16 17H8M10 9H8"/>',
    'fridge': '<path d="M5 6a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2Z"/><path d="M5 10h14"/><path d="M15 7v6"/>',
    'spray': '<path d="M3 3h.01M7 5h.01M11 7h.01M3 7h.01M7 9h.01M3 11h.01"/><rect width="4" height="4" x="15" y="5"/><path d="m19 9 2 2v10c0 .6-.4 1-1 1h-6c-.6 0-1-.4-1-1V11l2-2"/><path d="m13 14 8-2M13 19l8-2"/>',
    'utensils': '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>',
    'bath': '<path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.7 3 4 3.7 4 4.5V17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/><path d="M10 5 8 7M2 12h20M7 19v2M17 19v2"/>',
    'bed': '<path d="M2 4v16"/><path d="M2 8h18a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/>',
    'sofa': '<path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3"/><path d="M2 16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z"/><path d="M4 18v2M20 18v2"/>',
    'door': '<path d="M13 4h3a2 2 0 0 1 2 2v14"/><path d="M2 20h3M13 20h9M10 12v.01"/><path d="M13 4.6v16.1a1 1 0 0 1-1.2 1L5 20V5.6a2 2 0 0 1 1.5-1.9l4-1A2 2 0 0 1 13 4.6Z"/>',
    'briefcase': '<path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/>',
    'box': '<path d="M11 21.7a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.7l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7z"/><path d="M12 22V12"/><path d="m3.3 7 7.7 4.7a2 2 0 0 0 2 0L20.7 7"/>',
    'maximize': '<path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"/>',
    'repeat': '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    'search': '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    'paw': '<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.8 1C6.5 17.5 4.5 16.8 4.5 16.8A3.5 3.5 0 0 1 5.5 10Z"/>',
    'tag': '<path d="M12.6 2.6A2 2 0 0 0 11.2 2H4a2 2 0 0 0-2 2v7.2a2 2 0 0 0 .6 1.4l8.7 8.7a2.4 2.4 0 0 0 3.4 0l6.6-6.6a2.4 2.4 0 0 0 0-3.4z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>',
    'send': '<path d="M14.5 21.7a.5.5 0 0 0 .9 0l6.5-19a.5.5 0 0 0-.6-.6l-19 6.5a.5.5 0 0 0 0 .9l7.9 3.2a2 2 0 0 1 1.1 1.1z"/><path d="m21.9 2.1-11 11"/>',
    'heart': '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7Z"/>',
    'compass': '<circle cx="12" cy="12" r="10"/><path d="m16.2 7.8-2.1 6.3-6.3 2.1 2.1-6.3z"/>',
    'list': '<path d="M3 12h.01M3 18h.01M3 6h.01M8 12h13M8 18h13M8 6h13"/>',
    'layers': '<path d="M12.8 2.2a2 2 0 0 0-1.6 0L2.6 6.1a1 1 0 0 0 0 1.8l8.6 3.9a2 2 0 0 0 1.6 0l8.6-3.9a1 1 0 0 0 0-1.8Z"/><path d="m2 12 9.2 4.2a2 2 0 0 0 1.6 0L22 12"/><path d="m2 17 9.2 4.2a2 2 0 0 0 1.6 0L22 17"/>',
    'lock': '<rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
}


def icon(name, cls='icon'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def chip(name, cls=''):
    return f'<span class="chip {cls}">{icon(name)}</span>'


def guess_icon(text):
    t = text.lower()
    rules = [('oven', 'fridge'), ('refrigerator', 'fridge'), ('appliance', 'fridge'), ('kitchenette', 'utensils'), ('kitchen', 'utensils'),
             ('bath', 'bath'), ('restroom', 'bath'), ('bedroom', 'bed'), ('guest', 'bed'), ('living', 'sofa'), ('floor', 'sparkles'),
             ('starting point', 'repeat'), ('frequency', 'repeat'), ('stays', 'calendar'), ('instruction', 'clipboard'),
             ('checklist', 'clipboard'), ('laundry', 'box'), ('timing', 'calendar'), ('schedule', 'calendar'), ('date', 'calendar'),
             ('window', 'clock'), ('hours', 'clock'), ('empty', 'door'), ('reception', 'door'), ('office', 'briefcase'),
             ('used', 'users'), ('size', 'maximize'), ('layout', 'maximize'), ('condition', 'search'), ('needing more', 'search'),
             ('pets', 'paw'), ('product', 'spray'), ('priorit', 'clipboard'), ('location', 'pin'), ('access', 'lock'),
             ('service type', 'layers')]
    for k, v in rules:
        if k in t:
            return v
    return 'check'


# ---------------------------------------------------------------- helpers
def img(name, alt=None, sizes='(max-width: 1020px) 100vw, 50vw', eager=False):
    alt = IMG_ALT.get(name, '') if alt is None else alt
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return (f'<img src="/assets/images/{name}-1024.webp" '
            f'srcset="/assets/images/{name}-640.webp 640w, /assets/images/{name}-1024.webp 1024w, /assets/images/{name}.webp 1536w" '
            f'sizes="{sizes}" width="1536" height="1024" alt="{e(alt)}" {load} decoding="async">')


def btn(href, label_text, kind='gold', ico='arrow'):
    return f'<a class="btn btn-{kind}" href="{href}">{icon(ico)}<span>{label_text}</span></a>'


def alink(href, text):
    return f'<a class="arrow-link" href="{href}">{text}{icon("arrow-up-right")}</a>'


def label(text, ico='sparkle'):
    return f'<p class="label">{icon(ico)}{text}</p>'


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'


def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))


# ---------------------------------------------------------------- schema
def business_node():
    return {
        '@type': 'LocalBusiness', '@id': BIZ_ID, 'name': 'Neat Cleaning', 'url': ORIGIN + '/',
        'logo': ORIGIN + '/assets/images/logo-gold.png', 'image': ORIGIN + '/assets/images/og-home-hero.jpg',
        'description': 'Owner-led regular, deep, Airbnb, move-in and move-out, and commercial cleaning based in Natick, Massachusetts, serving locations within 25 miles.',
        'telephone': PHONE_E164, 'email': EMAIL, 'foundingDate': '2021',
        'founder': {'@type': 'Person', 'name': OWNER},
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Natick', 'addressRegion': 'MA', 'addressCountry': 'US'},
        'areaServed': {'@type': 'GeoCircle', 'geoMidpoint': {'@type': 'GeoCoordinates', 'latitude': NATICK[0], 'longitude': NATICK[1]}, 'geoRadius': '40234'},
        'paymentAccepted': 'Zelle, Cash, Check', 'currenciesAccepted': 'USD',
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Cleaning services', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', '@id': f'{ORIGIN}/{s["slug"]}.html#service', 'name': s['name']}} for s in SERVICES]},
        # PREENCHER: add "sameAs" with the Google Business Profile / Instagram / Facebook URLs when available.
    }


def breadcrumb_node(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': ORIGIN + u} for i, (n, u) in enumerate(items)]}


def faq_node(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(a)}} for q, a in faqs]}


def webpage_node(path, title, desc, kind='WebPage'):
    return {'@type': kind, '@id': ORIGIN + path + '#webpage', 'url': ORIGIN + path, 'name': title, 'description': desc,
            'isPartOf': {'@id': SITE_ID}, 'about': {'@id': BIZ_ID}, 'inLanguage': 'en-US', 'dateModified': UPDATED_ISO}


def graph(*nodes):
    return ld({'@context': 'https://schema.org', '@graph': [business_node(), *nodes]})


# ---------------------------------------------------------------- layout
def head(p):
    robots = 'noindex,follow' if p.get('noindex') else 'index,follow,max-image-preview:large'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0d0c0c">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["desc"])}">
<meta name="twitter:card" content="summary_large_image">
<!--AUTO_SEO-->
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/images/icon-192.png">
<link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/cinzel.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/montserrat.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v=3">
<script>document.documentElement.classList.add('js')</script>
<script src="/assets/js/main.js?v=3" defer></script>
{p.get("schema", "")}
</head>
'''


def header(active):
    svc_current = active in SVC or active == 'services'

    def a(href, text):
        cur = ' aria-current="page"' if href == active else ''
        return f'<a href="{href}"{cur}>{text}</a>'
    dd = ''.join(f'<a href="/{s["slug"]}.html">{chip(s["icon"], "light sm")}<span><b>{s["name"]}</b><small>{s["blurb"]}</small></span></a>' for s in SERVICES)
    return f'''<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
 <div class="tb-left"><span>{icon("pin")}Natick, MA &amp; up to 25 miles</span><span>{icon("card")}Zelle · Cash · Check</span></div>
 <a href="{SMS}">{icon("message")}Text {PHONE}</a>
</div></div>
<header class="site-header">
 <div class="wrap header-inner">
  <a class="brand" href="/" aria-label="Neat Cleaning, home"><img src="/assets/images/logo-gold-200.webp" width="207" height="200" alt="Neat Cleaning"></a>
  <nav class="nav" id="primary-nav" aria-label="Main">
   {a("/", "Home")}
   <div class="dd{" is-current" if svc_current else ""}">
    <button class="dd-toggle" type="button" aria-expanded="false" aria-controls="services-menu">Services{icon("chev")}</button>
    <div class="dd-menu" id="services-menu">{dd}<a class="all" href="/services.html"><b>Compare all services</b>{icon("arrow")}</a></div>
   </div>
   {a("/about.html", "About")}
   {a("/service-areas.html", "Service Area")}
   {a("/faq.html", "FAQ")}
   {a("/contact.html", "Contact")}
   <div class="nav-extra">{btn(SMS, "Text " + PHONE, "gold", "message")}{btn(TEL, "Call " + PHONE, "glass", "phone")}</div>
  </nav>
  <div class="header-cta">
   <a class="btn btn-gold" href="{SMS}" aria-label="Text Neat Cleaning for a quote">{icon("message")}<span>Text for a quote</span></a>
   <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">{icon("menu")}</button>
  </div>
 </div>
</header>
'''


def cta_block():
    return f'''<section class="section-sm" aria-labelledby="cta-title">
 <div class="wrap">
  <div class="cta reveal">
   <div class="bgimg">{img("contact-hero", alt="", sizes="100vw")}</div>
   {label("Let’s make it Neat")}
   <h2 id="cta-title">Ready for a cleaner home? Start with one text.</h2>
   <p>Send your town, the service you need and what matters most. Daiane replies to talk through the scope and your quote.</p>
   <div class="actions">{btn(SMS, "Text " + PHONE, "gold", "message")}{btn("/contact.html", "Request a quote online", "glass", "send")}</div>
  </div>
 </div>
</section>'''


def footer(cta=True):
    svc_links = ''.join(f'<a href="/{s["slug"]}.html">{s["name"]}</a>' for s in SERVICES)
    return f'''{cta_block() if cta else ""}
<footer class="site-footer{"" if cta else " flush"}">
 <div class="wrap footer-grid">
  <div class="footer-brand">
   <a href="/" aria-label="Neat Cleaning, home"><img src="/assets/images/logo-gold-200.webp" width="207" height="200" alt="Neat Cleaning logo" loading="lazy"></a>
   <p>Owner-led house cleaning based in Natick, Massachusetts. Caring for homes and workspaces within 25 miles since 2021.</p>
  </div>
  <nav aria-label="Cleaning services"><h2>Services</h2>{svc_links}<a href="/services.html">Compare services</a></nav>
  <nav aria-label="Company"><h2>Company</h2><a href="/about.html">About Neat Cleaning</a><a href="/service-areas.html">Service area</a><a href="/faq.html">FAQ</a><a href="/contact.html">Request a quote</a></nav>
  <div class="f-contact"><h2>Contact</h2>
   <a href="{SMS}">{icon("message")}Text {PHONE}</a><a href="{TEL}">{icon("phone")}Call {PHONE}</a><a href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a>
   <p>{icon("pin")}Natick, MA · up to 25 miles</p><p>{icon("card")}Zelle · Cash · Check</p>
   <!-- PREENCHER: business hours (e.g. Mon–Fri 8am–5pm) -->
  </div>
 </div>
 <div class="wrap footer-bottom">
  <span>© 2026 Neat Cleaning · Natick, Massachusetts · Interior images are illustrative.</span>
  <nav aria-label="Legal"><a href="/privacy-policy.html">Privacy Policy</a><a href="/terms-of-use.html">Terms of Use</a></nav>
 </div>
</footer>
<div class="mobile-bar"><a href="{SMS}">{icon("message")}Text for a quote</a><a href="{TEL}">{icon("phone")}Call</a></div>
</body>
</html>
'''


def crumbs(items):
    lis = ''.join(f'<li><span aria-current="page">{n}</span></li>' if i == len(items) - 1 else f'<li><a href="{u}">{n}</a></li>'
                  for i, (n, u) in enumerate(items))
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{lis}</ol></nav>'


def hero_page(trail, h1, lead, image, actions=True, badge=None, quote_href='#quote', trust=True):
    acts = f'<div class="actions">{btn(SMS, "Text for a quote", "gold", "message")}{btn(quote_href, "Request a quote online", "glass", "send")}</div>' if actions else ''
    bg = f'<div class="hero-bg">{img(image, alt="", sizes="100vw", eager=True)}</div>' if image else ''
    bdg = f'<span class="hero-badge"><span class="dot">{icon(badge[0])}</span>{badge[1]}</span>' if badge else ''
    cls = ' has-trust' if trust else ''
    return f'''<section class="hero page-hero{cls}" aria-labelledby="hero-title">
 {bg}
 <div class="wrap"><div class="hero-copy">
  {crumbs(trail)}{bdg}
  <h1 id="hero-title">{h1}</h1>
  <p class="lead">{lead}</p>
  {acts}
 </div></div>
</section>'''


TRUST = [('user', 'Owner-led since 2021', 'You text Daiane, who cleans'), ('fridge', 'Oven & fridge included', 'No separate add-on charge'),
         ('spray', 'Our own products', 'Nothing for you to stock'), ('shield', 'Quote confirmed first', 'Scope agreed before booking')]


def trust_bar():
    items = ''.join(f'<div>{chip(i, "soft")}<p><b>{t}</b><span>{d}</span></p></div>' for i, t, d in TRUST)
    return f'<div class="trust"><div class="wrap"><div class="trust-card">{items}</div></div></div>'


def bento(level='h3', help_tile=True, exclude=None, compact=False):
    tiles = []
    for s in SERVICES:
        if s['slug'] == exclude:
            continue
        tag = '<span class="tag">Core service</span>' if s['core'] and not compact else ''
        tiles.append(f'''<a class="tile reveal" href="/{s["slug"]}.html">{img(s["hero"], alt="", sizes="(max-width: 680px) 100vw, 50vw")}
 {chip(s["icon"])}{tag}<div class="txt"><{level}>{s["name"]}</{level}><p>{s["blurb"]}</p></div><span class="go">{icon("arrow-up-right")}</span></a>''')
    if help_tile and not compact:
        tiles.append(f'''<div class="tile help reveal">{chip("message")}<div><{level}>Not sure which one?</{level}><p>Describe your home and when it was last cleaned. Daiane will suggest where to start.</p><div class="actions" style="margin-top:18px">{btn(SMS, "Ask by text", "gold", "message")}</div></div></div>''')
    return f'<div class="bento{" compact" if compact else ""}">{"".join(tiles)}</div>'


STEPS = [
    ('message', 'Text or send the form', 'Share your town or ZIP code, the service and what matters most in your home.', 'Your request in one message'),
    ('clipboard', 'Talk through the scope', 'Daiane confirms rooms, priorities, pets, product preferences and access.', 'A clear, agreed scope'),
    ('file', 'Receive your quote', 'Price and timing are confirmed with you before anything is booked.', 'No surprises on the day'),
    ('sparkles', 'Enjoy the clean', 'The agreed visit, with our own products and the oven and fridge included.', 'A home ready for you'),
]


def steps_section(title='From first text to a finished home', sid='steps-title'):
    items = ''.join(f'<li class="step reveal"><span class="chip">{icon(i)}</span><h3>{t}</h3><p>{d}</p><span class="out">{icon("check-circle")}{o}</span></li>' for i, t, d, o in STEPS)
    return f'''<section class="section dark" aria-labelledby="{sid}">
 <div class="wrap">
  <div class="head-row"><div class="head">{label("How it works", "compass")}<h2 id="{sid}">{title}</h2></div>
   <p style="max-width:30em">Booking happens in a conversation, not a checkout page. That is how the quote ends up matching your actual home.</p></div>
  <ol class="steps">{items}</ol>
 </div>
</section>'''


def quote_form(form_id, preselect=None, details=True, heading='Request your quote', level='h2'):
    opts = ''.join(f'<option value="{s["slug"]}"{" selected" if s["slug"] == preselect else ""}>{s["name"]}</option>' for s in SERVICES)
    det = (f'<div class="field full"><label for="{form_id}-details">About your space</label><textarea id="{form_id}-details" name="details" maxlength="2500" '
           f'placeholder="Bedrooms and bathrooms, preferred dates or frequency, pets, areas that need attention"></textarea></div>') if details else ''
    return f'''<div class="form-card">
 <div class="fc-head">{chip("send")}<div><{level} id="{form_id}-title">{heading}</{level}><p>Daiane replies by text to confirm your quote.</p></div></div>
 <form class="quote-form" id="{form_id}" aria-labelledby="{form_id}-title" novalidate>
  <input type="hidden" name="form_id" value="{form_id}">
  <div class="honeypot" aria-hidden="true"><label>Leave empty<input type="text" name="botcheck" tabindex="-1" autocomplete="off"></label></div>
  <div class="form-grid">
   <div class="field"><label for="{form_id}-name">Full name <span>*</span></label><input id="{form_id}-name" name="name" autocomplete="name" required minlength="2" maxlength="100" placeholder="Your name"></div>
   <div class="field"><label for="{form_id}-phone">Mobile phone <span>*</span></label><input id="{form_id}-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required minlength="10" maxlength="30" placeholder="(508) 000-0000"></div>
   <div class="field full"><label for="{form_id}-email">Email <span>*</span></label><input id="{form_id}-email" name="email" type="email" autocomplete="email" required maxlength="254" placeholder="you@example.com"></div>
   <div class="field"><label for="{form_id}-service">Service <span>*</span></label><select id="{form_id}-service" name="service" required><option value="">Select a service</option>{opts}</select></div>
   <div class="field"><label for="{form_id}-location">Town or ZIP <span>*</span></label><input id="{form_id}-location" name="location" autocomplete="postal-code" required minlength="2" maxlength="100" placeholder="Natick or 01760"></div>
   {det}
  </div>
  <label class="consent" for="{form_id}-consent"><input id="{form_id}-consent" type="checkbox" name="consent" value="1" required><span>By submitting, you agree to receive calls and text messages from Neat Cleaning about your request. Consent is not a condition of purchase. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. See our <a href="/terms-of-use.html">Terms</a> and <a href="/privacy-policy.html">Privacy Policy</a>.</span></label>
  <button class="btn btn-dark btn-block submit-btn" type="submit"><span>Get my cleaning quote</span>{icon("arrow")}</button>
  <div class="form-message" role="status" aria-live="polite"></div>
  <div class="form-foot"><span>{icon("message")}Prefer to text? <a href="{SMS}">{PHONE}</a></span><span>{icon("tag")}Ask about 10% off</span></div>
 </form>
</div>'''


def contact_cards(email=False):
    out = f'<a href="{SMS}">{chip("message", "sm")}<span><small>Text · fastest reply</small><b>{PHONE}</b></span></a>'
    out += f'<a href="{TEL}">{chip("phone", "sm")}<span><small>Call</small><b>{PHONE}</b></span></a>'
    if email:
        out += f'<a href="mailto:{EMAIL}">{chip("mail", "sm")}<span><small>Email</small><b>{EMAIL}</b></span></a>'
    out += f'<div>{chip("pin", "sm")}<span><small>Service area</small><b>Natick, MA + 25 miles</b></span></div>'
    return f'<div class="contact-cards">{out}</div>'


def byline(light=False):
    return f'<div class="byline{" light" if light else ""}">{chip("user", "sm")}<span>Your contact: <b>{OWNER}</b>, owner of Neat Cleaning · Page updated <time datetime="{UPDATED_ISO}">{UPDATED}</time></span></div>'


def quote_section(form_id, preselect=None, image='contact-hero', title='Tell us about your space', lead=None, show_byline=False, details=True):
    lead = lead or 'Text is the fastest way to reach Daiane. Prefer the form? Send it and she will text you back to talk through the scope and your quote.'
    by = byline() if show_byline else ''
    return f'''<section class="quote-sec section dark" id="quote" aria-labelledby="{form_id}-sec">
 <div class="bgimg">{img(image, alt="", sizes="100vw")}</div>
 <div class="wrap quote-grid">
  <div>{label("Request a quote", "send")}<h2 id="{form_id}-sec">{title}</h2><p class="lead" style="margin-top:16px">{lead}</p>{contact_cards()}{by}</div>
  {quote_form(form_id, preselect=preselect, details=details, heading="Get your quote", level="h3")}
 </div>
</section>'''


def faq_list(faqs, open_first=True):
    return '<div class="faq">' + ''.join(
        f'<details{" open" if (i == 0 and open_first) else ""}><summary>{q}<span class="pm">{icon("plus")}</span></summary><div class="answer"><p>{a}</p></div></details>'
        for i, (q, a) in enumerate(faqs)) + '</div>'


def faq_section(faqs, title, intro='Products, pricing, payment and how booking works.', more=True):
    m = f'<p style="margin-top:22px">{alink("/faq.html", "See all questions")}</p>' if more else ''
    return f'''<section class="section" aria-labelledby="faq-title">
 <div class="wrap faq-wrap">
  <div class="faq-side">{label("FAQ", "help")}<h2 id="faq-title">{title}</h2><p style="margin-top:14px">{intro}</p>{m}
   <div class="help-card">{chip("message")}<h3>Still have a question?</h3><p>Text Daiane directly and get an answer about your home.</p>{btn(SMS, "Text " + PHONE, "gold", "message")}</div>
  </div>
  {faq_list(faqs)}
 </div>
</section>'''


def offer_section():
    return f'''<section class="section-sm" aria-label="Offer">
 <div class="wrap"><div class="offer reveal">
  <div class="pct">10%<small>OFF</small></div>
  <div><h2>Ask about 10% off your cleaning</h2><p>Mention the offer by text or in the quote form. Daiane confirms how it applies to your booking before you agree to the service.</p></div>
  {btn(SMS, "Ask by text", "dark", "message")}
 </div></div>
</section>'''


def factor_cards(factors, cta=True):
    cards = ''.join(f'<div class="factor reveal">{chip(guess_icon(a), "soft sm")}<b>{a}</b><span>{b}</span></div>' for a, b in factors)
    if cta:
        cards += (f'<div class="factor reveal" style="background:var(--black);border-color:var(--black)">{chip("tag", "sm")}'
                  f'<b style="color:#fff">Ask about 10% off</b><span style="color:var(--on-dark-2)">Mention it when you request your quote.</span></div>')
    return f'<div class="cards c3">{cards}</div>'


def page(p, body, active='', cta=True):
    markup = head(p) + header(active) + '<main id="main">\n' + body + '\n</main>\n' + footer(cta)
    # PREENCHER notes stay in the build sources and LEIA-ME.md, never in the published HTML.
    return re.sub(r'\s*<!-- PREENCHER:.*?-->', '', markup)


# ---------------------------------------------------------------- pages
CRITERIA = [
    ('user', 'Who will actually clean my home?', 'Many services send whoever is on the schedule that day.', 'Daiane, the owner, does the cleaning herself. Additional help is arranged only when demand requires it.'),
    ('message', 'Who do I talk to?', 'Details get lost when requests pass through several people.', 'You text Daiane directly. Her daughter helps answer phone calls.'),
    ('fridge', 'Are the oven and refrigerator extra?', 'Appliance add-ons often raise the final bill.', 'Both are included without a separate charge.'),
    ('spray', 'Who brings the supplies?', 'You should not have to stock products for the visit.', 'Neat brings its own products. Specific products can be requested in advance.'),
    ('file', 'When is the price confirmed?', 'Vague scope is where surprises come from.', 'Scope, quote and timing are confirmed with you before booking.'),
    ('card', 'How do I pay?', 'Know the methods before the visit, not after.', 'Zelle, cash or check.'),
    ('pin', 'Do you cover my town?', 'Travel limits decide real availability.', 'Natick and locations up to 25 miles away, confirmed by town or ZIP code.'),
]

HOME_FACTORS = [('Size of the home', 'Bedrooms, bathrooms and living areas set most of the time.'),
                ('Service type', 'A deep or move-out clean covers more detail than a regular visit.'),
                ('Frequency', 'Recurring visits are planned differently from a one-time clean.'),
                ('Current condition', 'Time since the last professional clean changes the work.'),
                ('Pets and products', 'Specific products, pets or focus areas are discussed in advance.')]


def page_home():
    path = '/'
    title = 'House Cleaning in Natick, MA – Regular & Deep | Neat Cleaning'
    desc = 'Owner-led house cleaning in Natick, MA since 2021. Regular and deep cleaning within 25 miles, oven and refrigerator included. Text (508) 202-8132 for a quote.'
    p = dict(title=title, desc=desc, schema=graph(
        {'@type': 'WebSite', '@id': SITE_ID, 'url': ORIGIN + '/', 'name': 'Neat Cleaning', 'inLanguage': 'en-US', 'publisher': {'@id': BIZ_ID}},
        webpage_node(path, title, desc)))
    rows = ''.join(f'<tr><th scope="row"><span class="q">{icon(i)}{q}</span></th><td data-label="Why it matters">{w}</td><td class="ours" data-label="At Neat Cleaning"><span class="ok">{icon("check-circle")}{a}</span></td></tr>' for i, q, w, a in CRITERIA)
    home_faq = [FAQ_GENERAL['Booking & quotes'][1], FAQ_GENERAL['During the visit'][0], FAQ_GENERAL['During the visit'][2], FAQ_GENERAL['Booking & quotes'][3], FAQ_GENERAL['Payment & offer'][0]]
    towns = '<li class="base">' + icon('home') + 'Natick <small>base</small></li>' + ''.join(f'<li>{icon("pin")}{t} <small>~{DIST[t]:.0f} mi</small></li>' for t, _, _ in TOWN_LIST[:13])
    why = [('user', 'Owner-led', 'Daiane cleans your home herself; help is added only when demand requires it.'),
           ('message', 'Direct by text', 'No call center. Your preferences go straight to the person doing the work.'),
           ('fridge', 'Appliances included', 'Oven and refrigerator are part of the visit, without an extra charge.'),
           ('spray', 'Products brought', 'Neat brings its own supplies; special requests are agreed in advance.')]
    why_cards = ''.join(f'<div class="card row reveal">{chip(i, "soft sm")}<div><h3 style="font-size:1rem;margin-bottom:4px">{t}</h3><p>{d}</p></div></div>' for i, t, d in why)
    body = f'''<section class="hero" aria-labelledby="hero-title">
 <div class="hero-bg">{img("home-hero", alt="", sizes="100vw", eager=True)}</div>
 <div class="wrap"><div class="hero-copy">
  <span class="hero-badge"><span class="dot">{icon("award")}</span>Owner-led cleaning in Natick since 2021</span>
  <h1 id="hero-title">House Cleaning in Natick, MA</h1>
  <p class="lead">Regular and deep cleaning for homes in Natick and up to 25 miles around it. You talk directly with Daiane, the owner, who takes care of the cleaning herself.</p>
  <div class="actions">{btn(SMS, "Text for a quote", "gold", "message")}{btn("#quote", "Request a quote online", "glass", "send")}</div>
 </div></div>
</section>
{trust_bar()}

<section class="section" aria-labelledby="intro-title">
 <div class="wrap intro">
  <div>{label("Welcome to Neat Cleaning")}<h2 id="intro-title">Personal care for the homes of Natick</h2></div>
  <div>
   <p class="defn"><strong>House cleaning in Natick is a scheduled in-home service that cleans kitchens, bathrooms, bedrooms, living areas and floors for households within 25 miles, with oven and refrigerator cleaning included in the visit.</strong></p>
   <p style="margin-top:18px">Neat Cleaning has grown through referrals since 2021, one conversation and one clean at a time. Every visit starts with a text: you tell Daiane what matters in your home, and the quote is confirmed before anything is booked.</p>
   <div class="actions" style="margin-top:22px">{alink("/about.html", "Meet Daiane")}</div>
  </div>
 </div>
</section>

<section class="section bg-white" aria-labelledby="svc-title">
 <div class="wrap">
  <div class="head-row"><div class="head">{label("Our services")}<h2 id="svc-title">Cleaning services for every stage of home</h2></div>
   <p style="max-width:30em">Regular and deep cleaning are what Neat does most. Rentals, moves and workspaces follow the same approach.</p></div>
  {bento()}
 </div>
</section>

<section class="section" aria-labelledby="why-title">
 <div class="wrap split">
  <div class="collage reveal">
   <div class="main">{img("about-hero", sizes="(max-width: 1020px) 100vw, 45vw")}</div>
   <div class="small">{img("regular-detail", alt="", sizes="25vw")}</div>
   <div class="badge">{chip("award", "sm")}<div><b>2021</b><span>Serving Natick homes since</span></div></div>
  </div>
  <div>
   {label("Why Neat Cleaning", "heart")}
   <h2 id="why-title">The person you text is the person who cleans</h2>
   <p class="lead" style="margin:16px 0 28px">Neat Cleaning is led by {OWNER}. Her daughter helps answer calls, and every quote is discussed directly with you.</p>
   <div class="cards c2">{why_cards}</div>
  </div>
 </div>
</section>

<section class="section bg-white" aria-labelledby="criteria-title">
 <div class="wrap">
  <div class="head center">{label("Before you hire anyone", "search")}<h2 id="criteria-title">What to ask any house cleaner</h2><p>Use these questions with any company you are considering. Here is how Neat Cleaning answers each one.</p></div>
  <div class="table-card reveal"><table class="dtable">
   <thead><tr><th scope="col">Question to ask</th><th scope="col">Why it matters</th><th scope="col" class="ours">At Neat Cleaning</th></tr></thead>
   <tbody>{rows}</tbody>
  </table></div>
 </div>
</section>

{steps_section()}

<section class="section" aria-labelledby="price-title">
 <div class="wrap">
  <div class="head-row"><div class="head">{label("Pricing", "tag")}<h2 id="price-title">How your quote is put together</h2></div>
   <p style="max-width:32em">Two homes with the same bedroom count can need very different time, so each quote is built from your home’s details and confirmed before booking.</p></div>
  <!-- PREENCHER: dated reference price range (e.g. "Regular cleaning, 3-bed / 2-bath in Natick, Oct 2026: $X–$Y") -->
  {factor_cards(HOME_FACTORS)}
 </div>
</section>

{quote_section("home-quote", details=False)}

{offer_section()}

<section class="section" aria-labelledby="area-title">
 <div class="wrap split">
  <div>{label("Service area", "pin")}<h2 id="area-title">Natick and the towns around it</h2>
   <p class="lead" style="margin:16px 0 24px">Neat Cleaning serves Natick and locations within 25 miles. Send your town or ZIP code and availability is confirmed for your address and date.</p>
   {alink("/service-areas.html", "See the full service area")}</div>
  <div><ul class="chips reveal">{towns}</ul><p class="muted" style="margin-top:14px;font-size:.82rem">Approximate straight-line distance from Natick center.</p></div>
 </div>
</section>

{faq_section(home_faq, "Questions homeowners ask")}'''
    return 'index.html', page(p, body, '/')


def page_service(slug):
    s, d = SVC[slug], SERVICE_PAGES[slug]
    path = f'/{slug}.html'
    trail = [('Home', '/'), ('Services', '/services.html'), (s['name'], path)]
    p = dict(title=d['title'], desc=d['desc'], schema=graph(
        webpage_node(path, d['title'], d['desc']),
        {'@type': 'Service', '@id': ORIGIN + path + '#service', 'name': s['short'].capitalize() + ' in Natick, MA', 'serviceType': s['name'],
         'description': strip_tags(d['define']), 'provider': {'@id': BIZ_ID}, 'url': ORIGIN + path, 'image': f'{ORIGIN}/assets/images/og-{s["hero"]}.jpg',
         'areaServed': [{'@type': 'City', 'name': 'Natick', 'containedInPlace': {'@type': 'State', 'name': 'Massachusetts'}}] + [{'@type': 'City', 'name': t} for t, _, _ in TOWN_LIST[:10]]},
        breadcrumb_node(trail), faq_node(d['faqs'])))
    focus = ''.join(f'<li>{chip(guess_icon(a), "soft sm")}<p><b>{a}</b><span>{b}</span></p></li>' for a, b in d['focus'])
    yes = ''.join(f'<li>{icon("check-circle")}<span>{t}</span></li>' for t in d['fit_yes'])
    no = ''.join(f'<li>{icon("arrow-up-right")}<span>{t}</span></li>' for t in d['fit_no'])
    body = f'''{hero_page(trail, d["h1"], d["lead"], s["hero"], badge=(s["icon"], d["kick"] + " · Natick, MA"))}
{trust_bar()}

<section class="section" aria-labelledby="focus-title">
 <div class="wrap split">
  <div class="photo reveal">{img(s["detail"])}<div class="float">{chip("fridge", "sm")}<p><b>Oven &amp; refrigerator included</b><span>No separate charge on any visit</span></p></div></div>
  <div>
   {label(s["name"], s["icon"])}
   <h2 id="focus-title">{d["focus_title"]}</h2>
   <p class="defn" style="margin-top:16px;color:var(--ink)"><strong>{d["define"]}</strong></p>
   <p style="margin:14px 0 24px">{d["focus_text"]}</p>
   <ul class="ilist focus">{focus}</ul>
  </div>
 </div>
</section>

<section class="section bg-white" aria-labelledby="fit-title">
 <div class="wrap">
  <div class="head center">{label("Is it the right service?", "help")}<h2 id="fit-title">Who {s["short"].lower()} is for</h2><p>Booking the right service first saves time for everyone.</p></div>
  <div class="fit">
   <div class="card yes reveal"><h3>{chip("check-circle", "soft sm")}A good fit if</h3><ul>{yes}</ul></div>
   <div class="card no reveal"><h3>{chip("compass", "soft sm")}Consider instead</h3><ul>{no}</ul></div>
  </div>
 </div>
</section>

<section class="section" aria-labelledby="price-title">
 <div class="wrap">
  <div class="head-row"><div class="head">{label("Pricing", "tag")}<h2 id="price-title">What sets the price of {s["short"].lower()}</h2></div>
   <p style="max-width:32em">Every quote is prepared for the specific property, from the details you share by text or through the form. Payment by Zelle, cash or check.</p></div>
  <!-- PREENCHER: dated reference price range for this service (region + month/year) -->
  {factor_cards(d["factors"])}
 </div>
</section>

{steps_section()}

{faq_section(d["faqs"], s["short"].capitalize() + " questions", "Straight answers about scope, pricing and scheduling.")}

<section class="section bg-white" aria-labelledby="related-title">
 <div class="wrap">
  <div class="head">{label("Related services")}<h2 id="related-title">Other ways we can help</h2></div>
  <p class="related-text">{d["related"]}</p>
  {bento(exclude=slug, compact=True)}
 </div>
</section>

{quote_section(slug + "-quote", preselect=slug, image=s["hero"], title="Get your " + s["short"].lower() + " quote", show_byline=True)}'''
    return f'{slug}.html', page(p, body, slug, cta=False)


def page_services():
    path = '/services.html'
    title = 'Compare Cleaning Services in Natick, MA | Neat Cleaning'
    desc = 'Compare regular, deep, Airbnb, move-in/move-out and commercial cleaning in Natick, MA. Owner-led since 2021, oven and fridge included. Request your quote.'
    trail = [('Home', '/'), ('Services', path)]
    p = dict(title=title, desc=desc, schema=graph(
        webpage_node(path, title, desc, 'CollectionPage'), breadcrumb_node(trail),
        {'@type': 'ItemList', 'name': 'Cleaning services in Natick, MA', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': f'{ORIGIN}/{s["slug"]}.html', 'name': s['name']} for i, s in enumerate(SERVICES)]}))
    compare = [('Homes already in good shape', 'Recurring: weekly, every two weeks or monthly', 'Kitchen, bathrooms, bedrooms, living areas, floors'),
               ('Build-up, first visits, long gaps', 'One-time, or before regular visits', 'Kitchen details, appliances, bathrooms, priority rooms'),
               ('Short-term rental hosts', 'Each turnover, by arrangement', 'Guest bedrooms, kitchen, bathrooms, host checklist'),
               ('Homes between occupants', 'One-time, around moving dates', 'Kitchen, appliances, bathrooms, empty rooms, floors'),
               ('Offices and workspaces', 'Agreed schedule and access hours', 'Work areas, reception, kitchenette, restrooms')]
    rows = ''.join(f'<tr><th scope="row"><a class="q" href="/{SERVICES[i]["slug"]}.html">{icon(SERVICES[i]["icon"])}{SERVICES[i]["name"]}</a></th><td data-label="Best for">{a}</td><td data-label="How it is scheduled">{b}</td><td class="ours" data-label="Typical focus">{c}</td></tr>' for i, (a, b, c) in enumerate(compare))
    paths = [('search', 'Home hasn’t had professional cleaning in months', 'Start with <a class="inline-link" href="/deep-cleaning.html">a deep cleaning visit</a>, then keep the result with <a class="inline-link" href="/regular-cleaning.html">recurring visits</a>.'),
             ('truck', 'The home is about to be empty', 'Book <a class="inline-link" href="/move-in-move-out-cleaning.html">move-in or move-out cleaning</a>, planned around your dates and access.'),
             ('key', 'You host guests or run an office', 'Plan <a class="inline-link" href="/airbnb-cleaning.html">turnovers between guests</a> or <a class="inline-link" href="/commercial-cleaning.html">workspace cleaning</a> around your hours.')]
    path_cards = ''.join(f'<div class="card reveal">{chip(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in paths)
    body = f'''{hero_page(trail, "Cleaning Services in Natick, MA", "Five services for homes, rentals and workspaces around Natick. Regular and deep cleaning are the core; each one is quoted for your property and confirmed before booking.", "home-kitchen", badge=("sparkles", "5 services · 25-mile radius"), quote_href="/contact.html")}
{trust_bar()}

<section class="section" aria-labelledby="all-title">
 <div class="wrap">
  <div class="head-row"><div class="head">{label("All services")}<h2 id="all-title">Choose the care your space needs</h2></div>
   <p class="defn" style="max-width:34em"><strong>Residential and commercial cleaning services around Natick cover recurring upkeep, detailed resets, short-term rental turnovers, moves and workspaces, each quoted per property and confirmed before booking.</strong></p></div>
  {bento(level="h2")}
 </div>
</section>

<section class="section bg-white" aria-labelledby="compare-title">
 <div class="wrap">
  <div class="head center">{label("Compare", "list")}<h2 id="compare-title">Which service fits your situation?</h2><p>Every service includes oven and refrigerator cleaning without a separate charge, and Neat brings its own products.</p></div>
  <div class="table-card reveal"><table class="dtable">
   <thead><tr><th scope="col">Service</th><th scope="col">Best for</th><th scope="col">How it is scheduled</th><th scope="col" class="ours">Typical focus</th></tr></thead>
   <tbody>{rows}</tbody>
  </table></div>
 </div>
</section>

<section class="section" aria-labelledby="start-title">
 <div class="wrap">
  <div class="head">{label("Not sure where to begin?", "compass")}<h2 id="start-title">A simple way to decide</h2></div>
  <div class="cards c3">{path_cards}</div>
 </div>
</section>

{steps_section()}
{offer_section()}'''
    return 'services.html', page(p, body, 'services')


def page_about():
    path = '/about.html'
    title = 'About Neat Cleaning | Owner-Led House Cleaning in Natick, MA'
    desc = 'Meet Daiane and Neat Cleaning, an owner-led cleaning business in Natick, MA since 2021. Direct communication, own products, oven and fridge included.'
    trail = [('Home', '/'), ('About', path)]
    p = dict(title=title, desc=desc, schema=graph(
        webpage_node(path, title, desc, 'AboutPage') | {'mainEntity': {'@id': BIZ_ID}},
        {'@type': 'Person', '@id': ORIGIN + '/about.html#owner', 'name': OWNER, 'jobTitle': 'Owner', 'worksFor': {'@id': BIZ_ID}},
        breadcrumb_node(trail)))
    stats = [('award', '2021', 'Caring for homes in the Natick area since'), ('pin', '25 mi', 'Service radius around Natick, MA'),
             ('fridge', 'Included', 'Oven and refrigerator, on every visit'), ('message', 'Direct', 'You text the owner, who does the cleaning')]
    stat_cards = ''.join(f'<div class="card reveal">{chip(i, "soft")}<p class="h2" style="font-size:1.9rem;color:var(--ink);margin:0 0 6px">{v}</p><p>{t}</p></div>' for i, v, t in stats)
    values = [('sparkles', 'Attention to detail', 'Oven and refrigerator cleaning are included, because a kitchen is not clean without them.'),
              ('message', 'Clear communication', 'Your quote and preferences are discussed directly by text and confirmed before booking.'),
              ('clipboard', 'Organization', 'Neat brings its own products and plans each visit around your priorities, pets and access.'),
              ('home', 'A local approach', 'Based in Natick and serving locations within up to 25 miles, close to the homes it cares for.')]
    val_cards = ''.join(f'<div class="card reveal">{chip(i)}<h3>{t}</h3><p>{d}</p></div>' for i, t, d in values)
    expect = [('message', f'You text or call {PHONE}', 'Text is the fastest way to reach Daiane directly.'),
              ('clipboard', 'Your home is discussed before any price', 'Rooms, priorities, pets, products and access.'),
              ('file', 'Scope, quote and timing are confirmed', 'Nothing is booked until you agree.'),
              ('card', 'You pay by Zelle, cash or check', 'Payment details are confirmed when the appointment is arranged.')]
    exp = ''.join(f'<li>{chip(i, "soft sm")}<p><b>{t}</b><span>{d}</span></p></li>' for i, t, d in expect)
    body = f'''{hero_page(trail, "About Neat Cleaning", "An owner-led cleaning business in Natick, Massachusetts, grown through referrals since 2021, one conversation and one clean at a time.", "about-hero", badge=("award", "Owner-led since 2021"), quote_href="/contact.html")}
{trust_bar()}

<section class="section" aria-labelledby="owner-title">
 <div class="wrap split">
  <div class="collage reveal">
   <div class="main">{img("regular-detail", sizes="(max-width: 1020px) 100vw, 45vw")}</div>
   <div class="small">{img("home-kitchen", alt="", sizes="25vw")}</div>
   <div class="badge">{chip("user", "sm")}<div><b>Daiane</b><span>Owner &amp; your contact</span></div></div>
  </div>
  <div class="prose">
   {label("The person behind the care", "heart")}
   <h2 id="owner-title" style="margin:0 0 18px">Meet Daiane</h2>
   <p class="defn" style="color:var(--ink)"><strong>Neat Cleaning is an owner-led cleaning business in Natick, Massachusetts, founded in 2021, providing regular, deep, Airbnb, move-in and move-out, and commercial cleaning within 25 miles.</strong></p>
   <p>Neat Cleaning is led by {OWNER}. She takes care of the cleaning herself, with additional help arranged as demand requires. The person who hears how you like your home cared for is the person responsible for doing it.</p>
   <p>Daiane responds to text messages, and her daughter helps answer calls. You can discuss your home, your priorities and the service you need before an appointment is confirmed.</p>
   <p>Regular and deep cleaning are the primary focus. Neat also offers <a href="/airbnb-cleaning.html">Airbnb turnovers</a>, <a href="/move-in-move-out-cleaning.html">move-in and move-out cleaning</a> and <a href="/commercial-cleaning.html">commercial cleaning</a> for local workspaces.</p>
   <!-- PREENCHER: photo of Daiane (real), languages spoken, Google reviews link -->
  </div>
 </div>
</section>

<section class="section-sm" aria-label="Neat Cleaning in numbers"><div class="wrap"><div class="cards c4">{stat_cards}</div></div></section>

<section class="section dark" aria-labelledby="values-title">
 <div class="wrap">
  <div class="head center">{label("What guides the work", "shield")}<h2 id="values-title">Trust, quality, organization and care</h2><p>The pillars of the brand, and what they look like in practice.</p></div>
  <div class="cards c4">{val_cards}</div>
 </div>
</section>

<section class="section" aria-labelledby="how-title">
 <div class="wrap split top">
  <div>{label("Working with Neat", "compass")}<h2 id="how-title">What to expect when you reach out</h2>{byline(light=True)}</div>
  <ul class="ilist focus">{exp}</ul>
 </div>
</section>'''
    return 'about.html', page(p, body, '/about.html')


def area_map():
    size = 640
    c = size / 2
    scale = 292 / 16.0
    lat0 = NATICK[0]

    def xy(coord):
        dx = (coord[1] - NATICK[1]) * math.cos(math.radians(lat0)) * 69.17
        dy = (coord[0] - NATICK[0]) * 69.0
        return c + dx * scale, c - dy * scale
    dash = ' stroke-dasharray="3 6"'
    rings = ''.join(f'<circle cx="{c}" cy="{c}" r="{rr * scale:.1f}" fill="none" stroke="rgba(233,208,115,{.22 if rr < 15 else .5})" stroke-width="1"{"" if rr == 15 else dash}/>'
                    f'<text x="{c + 4}" y="{c - rr * scale - 6:.1f}" fill="#b5ada4" font-size="10" font-family="Montserrat, sans-serif" letter-spacing="1">{rr} MI</text>' for rr in (5, 10, 15))
    left_side = {'Framingham', 'Ashland', 'Holliston', 'Hopkinton', 'Southborough', 'Marlborough', 'Milford', 'Medway', 'Sudbury', 'Sherborn', 'Millis', 'Wayland'}
    nudge = {'Wellesley': (0, -4), 'Dover': (0, 10), 'Needham': (0, 2), 'Westwood': (0, 10), 'Sherborn': (0, 10), 'Weston': (0, -2), 'Framingham': (0, -4),
             'Norwood': (0, 10), 'Dedham': (0, 2), 'Watertown': (0, 4), 'Newton': (0, 4), 'Millis': (0, 10), 'Ashland': (0, 10)}
    dots = ''
    for t, coord in TOWNS.items():
        x, y = xy(coord)
        nx, ny = nudge.get(t, (0, 0))
        anchor = 'end' if t in left_side else 'start'
        tx = x - 8 if anchor == 'end' else x + 8
        dots += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#d2b25f"/>'
                 f'<text x="{tx + nx:.1f}" y="{y + 4 + ny:.1f}" text-anchor="{anchor}" fill="#efe9e1" font-size="13" font-family="Montserrat, sans-serif">{t}</text>')
    return f'''<figure class="map-card reveal">
 <svg viewBox="0 0 {size} {size}" role="img" aria-labelledby="map-t map-d">
  <title id="map-t">Neat Cleaning service radius around Natick, Massachusetts</title>
  <desc id="map-d">Schematic map with Natick at the center and rings at 5, 10 and 15 miles, inside a 25-mile service radius, showing nearby towns such as Framingham, Wellesley, Needham, Wayland and Newton.</desc>
  <rect width="{size}" height="{size}" fill="#0d0c0c"/>
  {rings}{dots}
  <text x="{size - 30}" y="34" fill="#d2b25f" font-size="12" font-family="Cinzel, serif" text-anchor="middle">N</text><path d="M{size - 30} 40v26" stroke="#d2b25f"/>
  <circle cx="{c}" cy="{c}" r="7" fill="#bc9246"/><circle cx="{c}" cy="{c}" r="14" fill="none" stroke="#bc9246"/>
  <text x="{c}" y="{c - 22}" text-anchor="middle" fill="#fff" font-size="15" font-family="Cinzel, serif" letter-spacing="2">NATICK</text>
  <text x="{c}" y="{size - 14}" text-anchor="middle" fill="#d2b25f" font-size="10" font-family="Montserrat, sans-serif" letter-spacing="2">SERVICE RADIUS CONTINUES TO 25 MILES</text>
 </svg>
 <figcaption>Schematic, not to road scale. Distances are approximate straight lines from Natick center; availability is confirmed for each address.</figcaption>
</figure>'''


def page_area():
    path = '/service-areas.html'
    title = 'House Cleaning Near Natick, MA – Service Area | Neat Cleaning'
    desc = 'Neat Cleaning serves Natick, MA and towns within 25 miles: Framingham, Wellesley, Needham, Wayland, Sudbury, Newton and more. Text your ZIP to confirm.'
    trail = [('Home', '/'), ('Service Area', path)]
    faqs = [
        ('Which towns near Natick do you serve?', 'Neat Cleaning serves Natick and locations up to 25 miles away. Towns within that radius include Framingham, Wellesley, Needham, Sherborn, Dover, Wayland, Weston, Sudbury, Ashland, Holliston, Southborough, Newton, Medfield, Hopkinton and Waltham, among others. Availability depends on the exact address and the schedule, so send your town or ZIP code to confirm.'),
        ('How do I confirm you can reach my address?', f'Send your town or ZIP code by text to {PHONE} or in the quote form. You do not need to share a full street address in the first message. We confirm whether your location fits the service radius and the schedule, then discuss the cleaning service, scope and timing with you.'),
        ('Do you clean homes in Framingham and Wellesley?', f'Yes, both are inside the service radius. Framingham is about {DIST["Framingham"]:.1f} miles west of Natick center and Wellesley about {DIST["Wellesley"]:.1f} miles east, measured in a straight line. Availability still depends on the schedule, so include your ZIP code and preferred dates when you request your quote.'),
        ('Do all five services cover the same area?', 'The 25-mile radius around Natick applies to the services offered: regular, deep, Airbnb, move-in and move-out, and commercial cleaning. Timing matters more for some of them, such as rental turnovers between guests, so location and scheduling are confirmed together before anything is booked.'),
    ]
    p = dict(title=title, desc=desc, schema=graph(webpage_node(path, title, desc), breadcrumb_node(trail), faq_node(faqs)))
    towns = '<li class="base">' + icon('home') + 'Natick <small>base</small></li>' + ''.join(f'<li>{icon("pin")}{t} <small>~{dd:.1f} mi {b}</small></li>' for t, dd, b in TOWN_LIST)
    steps = [('pin', 'Send your town or ZIP code', 'A full street address is not needed in the first message.'),
             ('layers', 'Tell us the service you need', 'Regular, deep, Airbnb, move-in/out or commercial.'),
             ('calendar', 'Confirm availability and timing', 'Scope and schedule are agreed before booking.')]
    st = ''.join(f'<li>{chip(i, "soft sm")}<p><b>{t}</b><span>{d}</span></p></li>' for i, t, d in steps)
    body = f'''{hero_page(trail, "House Cleaning Near Natick, MA", "Based in Natick, Massachusetts, and caring for homes and workspaces in the towns within 25 miles. Send your town or ZIP code and availability is confirmed for your address.", "area-hero", badge=("pin", "Natick + 25-mile radius"))}
{trust_bar()}

<section class="section" aria-labelledby="map-title-h">
 <div class="wrap split">
  {area_map()}
  <div>
   {label("The radius", "compass")}
   <h2 id="map-title-h">Close to home, by design</h2>
   <p class="defn" style="margin:16px 0 14px;color:var(--ink)"><strong>The Neat Cleaning service area is Natick, Massachusetts, and locations within 25 miles, a radius that includes Framingham, Wellesley, Needham, Wayland, Sudbury, Holliston and Newton.</strong></p>
   <p style="margin-bottom:26px">Staying close to Natick keeps travel short and the schedule realistic.</p>
   <ul class="ilist focus">{st}</ul>
  </div>
 </div>
</section>

<section class="section bg-white" aria-labelledby="towns-title">
 <div class="wrap">
  <div class="head-row"><div class="head">{label("Towns in the radius", "pin")}<h2 id="towns-title">Towns around Natick</h2></div>
   <p style="max-width:32em">Approximate straight-line distance from Natick center; road distance is longer. Town not listed? If it is within 25 miles, send your ZIP code anyway.</p></div>
  <ul class="chips reveal">{towns}</ul>
 </div>
</section>

{faq_section(faqs, "Service area questions", "Coverage, distances and how availability is confirmed.", more=False)}

{quote_section("area-quote", image="area-hero", title="Check availability for your address", lead="Your town or ZIP code is enough to start. Daiane will text you back to confirm availability and talk through your quote.", show_byline=True)}'''
    return 'service-areas.html', page(p, body, '/service-areas.html', cta=False)


def page_contact():
    path = '/contact.html'
    title = 'Request a Cleaning Quote in Natick, MA | Contact Neat Cleaning'
    desc = 'Text (508) 202-8132 or request your Neat Cleaning quote online. Regular, deep, Airbnb, move and commercial cleaning in Natick, MA and within 25 miles.'
    trail = [('Home', '/'), ('Contact', path)]
    p = dict(title=title, desc=desc, schema=graph(webpage_node(path, title, desc, 'ContactPage'), breadcrumb_node(trail)))
    body = f'''<section class="quote-sec section dark page-top" id="quote" aria-labelledby="hero-title">
 <div class="bgimg">{img("contact-hero", alt="", sizes="100vw", eager=True)}</div>
 <div class="wrap quote-grid">
  <div>
   {crumbs(trail)}
   {label("Request a quote", "send")}
   <h1 id="hero-title">Request a House Cleaning Quote</h1>
   <p class="lead" style="margin-top:16px">Send your details and Daiane will text you to talk through your space and confirm your quote. Text is the quickest way to reach her.</p>
   {contact_cards(email=True)}
   <!-- PREENCHER: business hours and typical reply time -->
  </div>
  {quote_form("contact-quote", details=True, heading="Tell us what you need", level="h2")}
 </div>
</section>

{steps_section("What happens after you send it")}
{offer_section()}'''
    return 'contact.html', page(p, body, '/contact.html', cta=False)


def page_faq():
    path = '/faq.html'
    title = 'House Cleaning FAQ: Quotes, Products & Pay | Neat Cleaning'
    desc = 'Answers about Neat Cleaning in Natick, MA: how quotes work, pricing factors, products, oven and fridge cleaning, service area, payment and text messages.'
    trail = [('Home', '/'), ('FAQ', path)]
    all_faqs = [qa for group in FAQ_GENERAL.values() for qa in group]
    p = dict(title=title, desc=desc, schema=graph(webpage_node(path, title, desc), breadcrumb_node(trail), faq_node(all_faqs)))
    gicons = {'Booking & quotes': 'file', 'During the visit': 'home', 'Payment & offer': 'card', 'Text messages': 'message'}
    toc, groups = '', ''
    for i, (g, qs) in enumerate(FAQ_GENERAL.items()):
        gid = 'faq-' + g.lower().replace(' & ', '-').replace(' ', '-')
        toc += f'<a href="#{gid}">{icon(gicons[g])}{g}</a>'
        groups += f'<div class="faq-group" id="{gid}"><h2>{chip(gicons[g], "sm")}{g}</h2>{faq_list(qs, open_first=(i == 0))}</div>'
    body = f'''{hero_page(trail, "House Cleaning Questions, Answered", f"How quotes work, what is included, products, payment and text messages. If your question is not here, text {PHONE}.", "contact-hero", actions=False, badge=("help", f"{len(all_faqs)} answers · updated {UPDATED}"), trust=False)}

<section class="section" aria-label="Frequently asked questions">
 <div class="wrap faq-wrap">
  <div class="faq-side">
   <nav class="topic-nav" aria-label="FAQ topics" style="flex-direction:column;align-items:flex-start">{toc}</nav>
   <div class="help-card">{chip("message")}<h2 class="h3">Didn’t find your answer?</h2><p>Text Daiane directly about your home.</p>{btn(SMS, "Text " + PHONE, "gold", "message")}</div>
  </div>
  <div>{groups}<div style="margin-top:40px">{byline(light=True)}</div></div>
 </div>
</section>'''
    return 'faq.html', page(p, body, '/faq.html')


def page_legal(fname, h1, title, desc, sections):
    path = '/' + fname
    trail = [('Home', '/'), (h1, path)]
    p = dict(title=title, desc=desc, schema=graph(webpage_node(path, title, desc), breadcrumb_node(trail)))
    toc = ''.join(f'<a href="#s{i + 1}">{h}</a>' for i, (h, _) in enumerate(sections))
    secs = ''.join(f'<h2 id="s{i + 1}">{h}</h2><p>{t}</p>' for i, (h, t) in enumerate(sections))
    body = f'''{hero_page(trail, h1, 'Neat Cleaning · Last updated <time datetime="' + UPDATED_ISO + '">October 6, 2026</time>', None, actions=False, trust=False)}
<section class="section" aria-label="{h1}">
 <div class="wrap legal"><nav aria-label="Sections">{toc}</nav><div class="prose">{secs}</div></div>
</section>'''
    return fname, page(p, body, path)


def page_center(fname, title, desc, ico, h1, text, actions):
    p = dict(title=title, desc=desc, noindex=True)
    body = f'''<section class="center-hero dark" aria-labelledby="hero-title">
 <div class="wrap inner">{chip(ico)}<h1 id="hero-title">{h1}</h1><p class="lead" style="margin:18px auto 0">{text}</p><div class="actions">{actions}</div></div>
</section>'''
    return fname, page(p, body, '')


def build():
    pages = [page_home(), page_services(), page_about(), page_area(), page_contact(), page_faq()]
    pages += [page_service(s['slug']) for s in SERVICES]
    pages.append(page_legal('privacy-policy.html', 'Privacy Policy', 'Privacy Policy | Neat Cleaning', 'How Neat Cleaning in Natick, MA handles quote information, contact details, text message consent, consent records and privacy requests.', LEGAL_PRIVACY))
    pages.append(page_legal('terms-of-use.html', 'Terms of Use', 'Terms of Use & SMS Terms | Neat Cleaning', 'Neat Cleaning website terms, quote and booking information, customer care SMS terms, STOP and HELP instructions and contact details.', LEGAL_TERMS))
    pages.append(page_center('thank-you.html', 'Thank You | Neat Cleaning', 'Your quote request has been sent to Neat Cleaning.', 'check-circle',
                             'Thank you. We’ll be in touch.', 'Your cleaning quote request was sent successfully. Daiane will contact you to discuss your space and the next step. Want to add something? Send a text.',
                             btn(SMS, 'Send a follow-up text', 'gold', 'message') + btn('/', 'Back to home', 'glass', 'home')))
    pages.append(page_center('404.html', 'Page Not Found | Neat Cleaning', 'This page could not be found. Explore Neat Cleaning services in Natick, MA.', 'compass',
                             'Let’s find your way home', 'This page could not be found. Explore the cleaning services or get in touch about your request.',
                             btn('/services.html', 'See the services', 'gold', 'sparkles') + btn('/', 'Back to home', 'glass', 'home')))
    for name, markup in pages:
        (OUT / name).write_text(markup, encoding='utf-8')
        print('wrote', name, len(markup))


if __name__ == '__main__':
    build()
