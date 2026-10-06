#!/usr/bin/env python3
"""Static site generator for the Neat Cleaning website.

Every page shares one header, footer, form and schema builder, so the site stays
consistent. Run `python3 build/build.py` from the neat-cleaning folder; the HTML
files are written to site/.

Rules followed in the copy: only facts supplied by the business are stated
(no invented prices, reviews, licenses or insurance). Missing business data is
left as <!-- PREENCHER: ... --> comments and listed in LEIA-ME.md.
"""
from __future__ import annotations

import html
import json
import math
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'site'

# ---------------------------------------------------------------- business data
PHONE = '(508) 202-8132'
PHONE_E164 = '+15082028132'
SMS = 'sms:+15082028132'
TEL = 'tel:+15082028132'
EMAIL = 'Neatcleaningservicesusa@gmail.com'
OWNER = 'Daiane Ventura de Oliveira Hotis'
UPDATED = 'October 2026'
UPDATED_ISO = '2026-10-06'
ORIGIN = '{{ORIGIN}}'  # replaced by render-page.php with the live https origin
BIZ_ID = ORIGIN + '/#business'
SITE_ID = ORIGIN + '/#website'
NATICK = (42.2834, -71.3495)

SERVICES = [
    # slug, name, short, nav blurb, best for, hero image, detail image, preview caption
    dict(slug='regular-cleaning', name='Regular Cleaning', short='Regular cleaning',
         blurb='Recurring visits that keep a lived-in home in order.',
         fit='Homes that are mostly in order and need steady upkeep.',
         hero='regular-hero', detail='regular-detail', core=True),
    dict(slug='deep-cleaning', name='Deep Cleaning', short='Deep cleaning',
         blurb='A detailed reset for build-up that routine upkeep misses.',
         fit='First visits, long gaps between cleans, a start before regular care.',
         hero='deep-hero', detail='deep-detail', core=True),
    dict(slug='airbnb-cleaning', name='Airbnb Cleaning', short='Airbnb cleaning',
         blurb='Turnovers planned around check-out and check-in.',
         fit='Short-term rental hosts within 25 miles of Natick.',
         hero='airbnb-hero', detail='airbnb-detail', core=False),
    dict(slug='move-in-move-out-cleaning', name='Move-In & Move-Out', short='Move-in & move-out cleaning',
         blurb='One clean for the home you are leaving or moving into.',
         fit='Tenants, owners and landlords between occupants.',
         hero='move-hero', detail='move-detail', core=False),
    dict(slug='commercial-cleaning', name='Commercial Cleaning', short='Commercial cleaning',
         blurb='Offices and workspaces, with timing agreed in advance.',
         fit='Local offices, reception areas and shared workspaces.',
         hero='commercial-hero', detail='commercial-detail', core=False),
]
SVC = {s['slug']: s for s in SERVICES}

IMG_ALT = {
    'home-hero': 'Bright living room with linen sofas, fireplace and oak coffee table',
    'home-kitchen': 'Cream kitchen with marble island, brass pendant lights and wood stools',
    'regular-hero': 'Living room with sofa, armchair and fireplace in soft afternoon light',
    'regular-detail': 'Round dining table with wishbone chairs beside tall windows',
    'deep-hero': 'Blue-grey kitchen with marble island, brass pendants and range hood',
    'deep-detail': 'Open oven with clean racks in a white kitchen',
    'airbnb-hero': 'Guest bedroom with made bed, wool throw and bedside lamps',
    'airbnb-detail': 'Open-plan living area and kitchen ready for the next guest',
    'move-hero': 'Empty entry hall with wood floors and a white staircase',
    'move-detail': 'Empty kitchen with island, stainless refrigerator and stone floor',
    'commercial-hero': 'Office with glass partitions, desks and task chairs',
    'commercial-detail': 'Reception lounge with armchairs and a wood front desk',
    'about-hero': 'Dining room with long wood table, rush chairs and a chandelier',
    'contact-hero': 'Front entry with bench, open door and a view to the garden',
    'area-hero': 'Colonial houses on a tree-lined Massachusetts street in autumn',
}

TOWNS = {
    'Wellesley': (42.2968, -71.2924), 'Sherborn': (42.2390, -71.3698), 'Framingham': (42.2793, -71.4162),
    'Dover': (42.2459, -71.2828), 'Wayland': (42.3626, -71.3614), 'Needham': (42.2809, -71.2378),
    'Ashland': (42.2612, -71.4634), 'Weston': (42.3668, -71.3031), 'Holliston': (42.2001, -71.4245),
    'Medfield': (42.1876, -71.3064), 'Sudbury': (42.3834, -71.4162), 'Westwood': (42.2140, -71.2245),
    'Millis': (42.1676, -71.3579), 'Newton': (42.3370, -71.2092), 'Waltham': (42.3765, -71.2356),
    'Southborough': (42.3057, -71.5245), 'Hopkinton': (42.2287, -71.5226), 'Dedham': (42.2418, -71.1662),
    'Norwood': (42.1945, -71.1995), 'Medway': (42.1418, -71.3967), 'Lincoln': (42.4259, -71.3040),
    'Watertown': (42.3709, -71.1828), 'Marlborough': (42.3459, -71.5523), 'Brookline': (42.3318, -71.1212),
    'Concord': (42.4604, -71.3489), 'Lexington': (42.4473, -71.2245), 'Milford': (42.1398, -71.5162),
    'Westborough': (42.2695, -71.6162), 'Franklin': (42.0834, -71.3967),
}


def miles(a, b):
    r = 3958.8
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def bearing(a, b):
    dx = (b[1] - a[1]) * math.cos(math.radians(a[0]))
    dy = b[0] - a[0]
    ang = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    return ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest'][round(ang / 45) % 8]


TOWN_LIST = sorted(((t, miles(NATICK, c), bearing(NATICK, c)) for t, c in TOWNS.items()), key=lambda x: x[1])
DIST = {t: d for t, d, _ in TOWN_LIST}

# ---------------------------------------------------------------- tiny helpers
e = html.escape


def icon(name, cls='icon'):
    paths = {
        'arrow': '<path d="M4 12h16m-6-6 6 6-6 6"/>',
        'sms': '<path d="M20 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2Z"/><path d="M8 9h8M8 13h5"/>',
        'phone': '<path d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 7 7L16 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z"/>',
        'mail': '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="m3 6 9 7 9-7"/>',
        'pin': '<path d="M19 10c0 6-7 11-7 11s-7-5-7-11a7 7 0 0 1 14 0Z"/><circle cx="12" cy="10" r="2.5"/>',
        'chev': '<path d="m6 9 6 6 6-6"/>',
        'check': '<path d="m4 12.5 5 5L20 6.5"/>',
        'menu': '<path d="M3 7h18M3 12h18M3 17h18"/>',
        'spark': '<path d="M12 2c.4 4.6 2.4 6.6 7 7-4.6.4-6.6 2.4-7 7-.4-4.6-2.4-6.6-7-7 4.6-.4 6.6-2.4 7-7Z"/>',
        'home': '<path d="m3 11 9-7 9 7"/><path d="M5 10v10h14V10"/>',
        'card': '<rect x="3" y="6" width="18" height="13" rx="1"/><path d="M3 10h18"/>',
        'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        'diamond': '<path d="m12 3 4 9-4 9-4-9Z"/>',
    }
    fill = 'currentColor' if name in ('spark', 'diamond') else 'none'
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="{fill}" stroke="currentColor" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


def img(name, alt=None, sizes='(max-width: 1020px) 100vw, 50vw', eager=False, cls=''):
    alt = IMG_ALT.get(name, '') if alt is None else alt
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ''
    return (f'<img{c} src="/assets/images/{name}-1024.webp" '
            f'srcset="/assets/images/{name}-640.webp 640w, /assets/images/{name}-1024.webp 1024w, /assets/images/{name}.webp 1536w" '
            f'sizes="{sizes}" width="1536" height="1024" alt="{e(alt)}" {load} decoding="async">')


def btn(href, label, kind='', ico='arrow', extra=''):
    k = f' btn-{kind}' if kind else ''
    return f'<a class="btn{k}" href="{href}"{extra}>{icon(ico)}<span>{label}</span></a>'


def link(href, label):
    return f'<a class="link" href="{href}">{label}{icon("arrow")}</a>'


def kicker(num, label):
    n = f'<span class="num">{num}</span>' if num else ''
    return f'<p class="kicker">{n}{label}</p>'


def ornament():
    return f'<div class="ornament" aria-hidden="true">{icon("diamond")}</div>'


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'


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
        'knowsLanguage': ['en', 'pt'],
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


def strip_tags(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s))


def webpage_node(path, title, desc, kind='WebPage'):
    return {'@type': kind, '@id': ORIGIN + path + '#webpage', 'url': ORIGIN + path, 'name': title, 'description': desc,
            'isPartOf': {'@id': SITE_ID}, 'about': {'@id': BIZ_ID}, 'inLanguage': 'en-US', 'dateModified': UPDATED_ISO}


# ---------------------------------------------------------------- layout
def head(p):
    robots = '<meta name="robots" content="noindex,follow">' if p.get('noindex') else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
{robots}
<meta name="theme-color" content="#0e0d0d">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{e(p.get("og_title", p["title"]))}">
<meta property="og:description" content="{e(p["desc"])}">
<meta name="twitter:card" content="summary_large_image">
<!--AUTO_SEO-->
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/images/icon-192.png">
<link rel="apple-touch-icon" href="/assets/images/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/cinzel.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/montserrat.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css?v=2">
<script>document.documentElement.classList.add('js')</script>
<script src="/assets/js/main.js?v=2" defer></script>
{p.get("schema", "")}
</head>
'''


NAV = [('/', 'Home'), ('/about.html', 'About'), ('/service-areas.html', 'Service Area'), ('/faq.html', 'FAQ'), ('/contact.html', 'Contact')]


def header(active):
    svc_current = active in SVC or active == 'services'

    def a(href, label):
        cur = ' aria-current="page"' if href == active else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    dd_items = ''.join(
        f'<a href="/{s["slug"]}.html"><span class="n">0{i + 1}</span><b>{s["name"]}</b><span>{s["blurb"]}</span></a>'
        for i, s in enumerate(SERVICES))
    return f'''<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
 <div class="wrap header-inner">
  <a class="brand" href="/" aria-label="Neat Cleaning, home">
   <img src="/assets/images/mark-gold.webp" width="172" height="98" alt="">
   <span class="brand-word"><b>NEAT</b><small>Cleaning</small></span>
  </a>
  <nav class="nav" id="primary-nav" aria-label="Main">
   {a("/", "Home")}
   <div class="dd{" is-current" if svc_current else ""}">
    <button class="dd-toggle" type="button" aria-expanded="false" aria-controls="services-menu">Services {icon("chev")}</button>
    <div class="dd-menu" id="services-menu">{dd_items}<a class="all" href="/services.html">Compare all services</a></div>
   </div>
   {a("/about.html", "About")}
   {a("/service-areas.html", "Service Area")}
   {a("/faq.html", "FAQ")}
   {a("/contact.html", "Contact")}
   <p class="nav-extra mobile-only">Text or call <a href="{SMS}">{PHONE}</a><br>Natick, MA · up to 25 miles</p>
  </nav>
  <div class="header-cta">
   <div class="header-phone"><small>Text or call</small><a href="{TEL}">{PHONE}</a></div>
   <a class="btn btn-gold" href="{SMS}" aria-label="Text Neat Cleaning for a quote">{icon("sms")}<span>Text for a quote</span></a>
   <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Open menu">{icon("menu")}</button>
  </div>
 </div>
</header>
'''


def footer(cta=True):
    band = ''
    if cta:
        band = f'''<section class="cta-band dark" aria-labelledby="cta-title">
 <div class="wrap">
  <div>
   {kicker("", "Let’s make it Neat")}
   <h2 id="cta-title">A cleaner home starts with one <em>text.</em></h2>
   <p>Send your town, the service you need and what matters most. Daiane replies to talk through the scope and your quote.</p>
  </div>
  <div class="actions">{btn(SMS, "Text " + PHONE, "gold", "sms")}{btn("/contact.html#quote", "Request a quote online", "ghost")}</div>
 </div>
</section>'''
    svc_links = ''.join(f'<a href="/{s["slug"]}.html">{s["name"]}</a>' for s in SERVICES)
    return f'''{band}
<footer class="site-footer">
 <div class="footer-top">
  <div class="wrap footer-grid">
   <div class="footer-brand">
    <a href="/" aria-label="Neat Cleaning, home"><img src="/assets/images/logo-gold.png" width="350" height="338" alt="Neat Cleaning logo" loading="lazy"></a>
    <p>Owner-led house cleaning based in Natick, Massachusetts. Serving homes and workspaces within 25 miles since 2021.</p>
   </div>
   <nav aria-label="Cleaning services"><h2>Services</h2>{svc_links}<a href="/services.html">Compare services</a></nav>
   <nav aria-label="Company"><h2>Neat Cleaning</h2><a href="/about.html">About Daiane &amp; Neat</a><a href="/service-areas.html">Service area</a><a href="/faq.html">Questions &amp; answers</a><a href="/contact.html">Request a quote</a></nav>
   <div class="footer-contact"><h2>Contact</h2>
    <a href="{SMS}">Text {PHONE}</a><a href="{TEL}">Call {PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a>
    <p>Natick, MA · up to 25 miles</p><p>Zelle · Cash · Check</p>
    <!-- PREENCHER: business hours (e.g. Mon–Fri 8am–5pm) -->
   </div>
  </div>
 </div>
 <div class="wrap footer-bottom">
  <span>© 2026 Neat Cleaning, Natick, Massachusetts. Interior images are illustrative.</span>
  <nav aria-label="Legal"><a href="/privacy-policy.html">Privacy Policy</a><a href="/terms-of-use.html">Terms of Use</a></nav>
 </div>
</footer>
<div class="mobile-bar"><a href="{SMS}">{icon("sms")}Text for a quote</a><a href="{TEL}">{icon("phone")}Call</a></div>
</body>
</html>
'''


def crumbs(items):
    lis = []
    for i, (name, url) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li><span aria-current="page">{name}</span></li>')
        else:
            lis.append(f'<li><a href="{url}">{name}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def definition(text, label='In short'):
    return f'''<section class="definition ivory" aria-label="Summary">
 <div class="wrap">
  <p class="small-caps label" style="color:var(--gold-700)">{label}</p>
  <div><p><strong>{text}</strong></p></div>
 </div>
</section>'''


def facts_band():
    return f'''<div class="facts">
 <div><b>2021</b><span>Caring for homes in the Natick area since</span></div>
 <div><b>25 mi</b><span>Service radius around Natick, MA</span></div>
 <div><b>Included</b><span>Oven and refrigerator, without a separate charge</span></div>
 <div><b>Direct</b><span>You text the owner, who does the cleaning</span></div>
</div>'''


STEPS = [
    ('Text or send the form', 'Share your town or ZIP code, the service and what matters most in your home.', 'Your request in one message'),
    ('Talk through the scope', 'Daiane confirms the rooms, priorities, pets, product preferences and access.', 'A clear, agreed scope'),
    ('Receive your quote', 'The price and timing are confirmed with you before anything is booked.', 'No surprises on the day'),
    ('Enjoy the clean', 'The agreed visit, with Neat’s own products and the oven and refrigerator included.', 'A home ready for you'),
]


def steps_block(dark=True, num='', title='From the first text<br>to a finished home.'):
    lis = ''.join(f'<li><span class="n">{["I", "II", "III", "IV"][i]}</span><h3>{t}</h3><p>{d}</p><span class="out">{o}</span></li>' for i, (t, d, o) in enumerate(STEPS))
    cls = 'section dark' if dark else 'section ivory light-steps'
    return f'''<section class="{cls}" aria-labelledby="steps-title">
 <div class="wrap">
  <div class="section-head">
   <div>{kicker(num, "How it works")}<h2 id="steps-title">{title}</h2></div>
   <p>Booking is handled in a conversation, not a checkout page. That is how the quote ends up matching your actual home.</p>
  </div>
  <ol class="steps reveal">{lis}</ol>
 </div>
</section>'''


def quote_form(form_id, preselect=None, details=True, heading='Request your quote', level='h2'):
    opts = ''.join(f'<option value="{s["slug"]}"{" selected" if s["slug"] == preselect else ""}>{s["name"]}</option>' for s in SERVICES)
    det = ''
    if details:
        det = f'''<div class="field full"><label for="{form_id}-details">About your space</label><textarea id="{form_id}-details" name="details" maxlength="2500" placeholder="Bedrooms and bathrooms, preferred dates or frequency, pets, areas that need attention"></textarea></div>'''
    return f'''<div class="form-card">
 <{level} class="h2" id="{form_id}-title">{heading}</{level}>
 <p class="sub">Daiane will contact you by text to discuss your space and confirm your quote. Fields marked * are required.</p>
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
  <button class="btn btn-block submit-btn" type="submit"><span>Get my cleaning quote</span>{icon("arrow")}</button>
  <div class="form-message" role="status" aria-live="polite"></div>
  <div class="form-foot"><span>Prefer to text? <a href="{SMS}">{PHONE}</a></span><span>Ask about 10% off</span></div>
 </form>
</div>'''


def faq_list(faqs, open_first=True):
    out = []
    for i, (q, a) in enumerate(faqs):
        op = ' open' if (i == 0 and open_first) else ''
        out.append(f'<details{op}><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="answer"><p>{a}</p></div></details>')
    return '<div class="faq">' + ''.join(out) + '</div>'


def byline():
    return f'''<div class="byline"><span>Your contact: <b>{OWNER}</b>, owner of Neat Cleaning</span><span>Natick, Massachusetts</span><span>Page updated <time datetime="{UPDATED_ISO}">{UPDATED}</time></span></div>'''


def offer_block():
    return f'''<div class="offer reveal">
 <div class="pct">10%<small>OFF</small></div>
 <div><h2>Ask about 10% off your cleaning.</h2><p>Mention the offer by text or in the quote form. Daiane confirms how it applies to your booking before you agree to the service.</p></div>
 {btn(SMS, "Ask by text", "", "sms")}
</div>'''


def page(p, body, active='', cta=True):
    markup = head(p) + header(active) + '<main id="main">\n' + body + '\n</main>\n' + footer(cta)
    # PREENCHER notes stay in this source file and in LEIA-ME.md, never in the published HTML.
    markup = re.sub(r'\s*<!-- PREENCHER:.*?-->', '', markup)
    return markup.replace('<br>', ' <br>')


# ---------------------------------------------------------------- FAQ content
FAQ_GENERAL = {
    'Booking & quotes': [
        ('How do I get a cleaning quote?', f'Text {PHONE} or send the quote form with your name, phone, email, service and town or ZIP code. Daiane replies by text to go over your home, the areas that matter most, pets and access. Price, scope and timing are confirmed with you before anything is booked, so the quote reflects your actual home rather than a generic package.'),
        ('How much does house cleaning cost?', 'Neat Cleaning quotes each home individually instead of publishing a flat rate. The main factors are the size of the home, the service you choose, how often you want visits, its current condition and special requests such as specific products. Share those details by text or in the form and you receive a quote before booking. Ask about the 10% off offer at the same time.'),
        ('What cleaning services do you offer?', 'Neat Cleaning offers regular cleaning, deep cleaning, Airbnb and short-term rental cleaning, move-in and move-out cleaning, and commercial cleaning for local workspaces. Regular and deep cleaning are the main focus. If you are unsure which fits, describe your home and when it was last professionally cleaned, and Daiane will suggest where to start.'),
        ('How far from Natick do you travel?', 'Neat Cleaning is based in Natick, Massachusetts, and serves locations up to 25 miles away. That radius includes towns such as Framingham, Wellesley, Needham, Wayland, Sudbury, Holliston and Newton. Availability depends on your exact location and the schedule, so send your town or ZIP code and we will confirm before you book.'),
        ('What happens after I send the form?', 'Your request goes to Neat Cleaning with the service, town and details you shared. You are contacted by text or phone at the number you provided to talk through the scope and confirm your quote. Sending the form is an inquiry, not a booking: nothing is scheduled until you agree to the price and timing.'),
        ('Can I change my appointment?', f'Yes. Text {PHONE} as soon as you know you need a change. The sooner you reach out, the easier it is to find another time that works. New availability and any arrangements related to the change are confirmed directly with you by text, so you always know where your appointment stands.'),
    ],
    'During the visit': [
        ('Who will clean my home?', f'Neat Cleaning is led by {OWNER}, who takes care of the cleaning herself. When demand requires it, additional help is arranged. You talk with Daiane directly by text before the visit, so the preferences you share are heard by the person responsible for the cleaning.'),
        ('Do you bring your own cleaning products?', 'Yes. Neat Cleaning brings its own products to every visit, so you do not need to stock anything. If you prefer a specific product, for example because of allergies, pets or surfaces that need special care, tell us before booking. Special product requests are discussed in advance and may affect the quote.'),
        ('Are the oven and refrigerator an extra charge?', 'No. Oven and refrigerator cleaning are included without a separate extra charge, where many services sell them as add-ons. Mention them when you request your quote so access and preparation can be planned, including how full the refrigerator will be on the day of the visit.'),
        ('Can you use products I provide?', 'Yes, specific product requests can be discussed in advance. Neat usually brings its own products, but if you would like something particular used in your home, mention it when you request your quote. Exceptions to the usual products may affect the quote, and everything is confirmed with you before the appointment is booked.'),
        ('What if I have a pet at home?', 'Mention your pets before booking, along with any product concerns and the rooms they use most. We will discuss access and the preferences you would like considered on the day. Letting us know in advance helps the visit go smoothly for you, your pet and the cleaning itself.'),
    ],
    'Payment & offer': [
        ('What payment methods do you accept?', f'Neat Cleaning accepts Zelle, cash and check. Payment details are confirmed directly when your appointment is arranged, so you know how and when to pay before the visit. If you have a question about paying for recurring visits or for a commercial space, text {PHONE}.'),
        ('How does the 10% off offer work?', 'Mention the 10% off offer by text or in the details field of the quote form. Daiane confirms how it applies to your booking before you agree to the service, so there is no guesswork about the final amount. The offer is applied according to what is confirmed for your appointment.'),
    ],
    'Text messages': [
        ('How do I stop text messages?', f'Reply STOP to any message to opt out of texts from Neat Cleaning. You may receive one final message confirming that you have been unsubscribed. Reply HELP for help, or contact Neat Cleaning at {PHONE} or {EMAIL}. Texts that follow a form request are about your request only, not promotions.'),
    ],
}

SERVICE_PAGES = {
    'regular-cleaning': dict(
        title='Regular House Cleaning in Natick, MA | Neat Cleaning',
        desc='Recurring house cleaning in Natick, MA and within 25 miles. Owner-led, own products, oven and fridge included. Text (508) 202-8132 for your quote.',
        h1='Regular house cleaning<br>in Natick, <em>MA.</em>',
        kick='Recurring home care',
        lead='Weekly, every-two-week or monthly visits for homes in Natick and the towns around it. You plan the routine with Daiane by text, and the same priorities are followed every time.',
        define='Regular house cleaning is a recurring in-home visit that cleans kitchens, bathrooms, bedrooms, living areas and floors on a set schedule, keeping a Natick-area home at a consistent level between visits.',
        fit_yes=['Your home is in reasonably good shape and you want it kept that way.', 'You want a set rhythm: weekly, every two weeks or monthly.', 'You prefer one person you can text about how your home should be cared for.'],
        fit_no=['It has been months since a professional clean: start with <a class="inline-link" href="/deep-cleaning.html">a deep cleaning visit</a>.', 'You are moving in or out: see <a class="inline-link" href="/move-in-move-out-cleaning.html">cleaning between occupants</a>.'],
        focus_title='Care for the rooms you use every day.',
        focus_text='Regular cleaning is the core of Neat Cleaning. It covers the spaces your household uses daily, and the details that make a home feel looked after again.',
        focus=[('Kitchen and everyday surfaces', 'Counters, fronts and the surfaces you touch most.'), ('Bathrooms and frequently used spaces', 'The rooms that need attention every visit.'), ('Bedrooms and living areas', 'Where the household actually spends its time.'), ('Floors and finishing touches', 'The final pass that makes the home feel finished.'), ('Oven and refrigerator', 'Included without a separate extra charge.')],
        factors=[('Size of the home', 'Bedrooms, bathrooms and living areas set most of the time per visit.'), ('Frequency', 'Weekly, every-two-week and monthly visits are planned differently.'), ('Current condition', 'If there is significant build-up, a deep clean may be suggested first.'), ('Priorities and requests', 'Specific products or focus areas can change the scope.'), ('Pets and access', 'Shared before booking so the visit is planned correctly.')],
        related=f'This page covers recurring visits for a home that is already in good shape. When there is build-up to remove first, <a class="inline-link" href="/deep-cleaning.html">deep cleaning in Natick</a> is the better starting point, and regular visits then keep the result. Hosts preparing a listing between guests should look at <a class="inline-link" href="/airbnb-cleaning.html">turnover cleaning for short-term rentals</a>, and if you are packing up, <a class="inline-link" href="/move-in-move-out-cleaning.html">move-out cleaning</a> is planned around empty rooms and moving dates. Not sure which one fits? <a class="inline-link" href="/services.html">Compare the five services side by side</a>.',
        faqs=[
            ('How often should I schedule regular cleaning?', 'It depends on how the home is used. Many households choose weekly, every two weeks or monthly visits; homes with children, pets or a lot of cooking usually benefit from more frequent care. Tell us your preferred frequency by text or in the quote form, and we will confirm a schedule based on your home and availability.'),
            ('How much does regular cleaning cost in Natick?', f'Regular cleaning is quoted per home. The size of the home, the number of bathrooms, how often you want visits and any special requests set the price. Share those details by text at {PHONE} or in the form on this page and you receive a quote before anything is booked. Mention the 10% off offer when you ask.'),
            ('Should I start with a deep cleaning?', 'If your home has not had professional cleaning in a while, a deep cleaning first is usually the better starting point. It removes the build-up, and regular visits then keep the home at that level. Describe the current condition and we will discuss the scope of the first visit before you commit to a routine.'),
            ('What does a regular cleaning visit focus on?', 'Regular visits focus on the spaces you use every day: the kitchen and everyday surfaces, bathrooms, bedrooms and living areas, and floors with the finishing touches. Oven and refrigerator cleaning are included without extra charge. You can set priorities when you request your quote, and the final scope is confirmed before booking.'),
            ('Do I need to provide cleaning supplies?', 'No. Neat Cleaning brings its own cleaning products to every visit. If you would like a specific product used, because of allergies, pets or delicate surfaces, tell us before booking. Special product requests are discussed in advance and may affect the quote, so the visit is planned with the right supplies from the start.'),
            ('Who cleans my home on each visit?', 'Neat Cleaning is owner-led. Daiane takes care of the cleaning herself, with additional help arranged when demand requires it. The person you text about your preferences is the person responsible for your home, rather than a rotating crew you meet for the first time at the door.'),
            ('Do you offer regular cleaning in towns near Natick?', 'Yes. Regular cleaning is available in Natick and locations up to 25 miles away, including towns such as Framingham, Wellesley, Needham, Sherborn, Wayland and Holliston. Availability depends on your exact location and the schedule, so include your town or ZIP code in your request and we will confirm.'),
        ]),
    'deep-cleaning': dict(
        title='Deep Cleaning in Natick, MA | Home Reset | Neat Cleaning',
        desc='Deep house cleaning in Natick, MA and within 25 miles: kitchens, bathrooms and appliance build-up, oven and fridge included. Text (508) 202-8132 for a quote.',
        h1='Deep cleaning<br>in Natick, <em>MA.</em>',
        kick='The detailed reset',
        lead='For build-up that everyday upkeep does not reach. A deep cleaning gives your home a fresh starting point, as a one-time visit or before regular care begins.',
        define='Deep cleaning is a detailed one-time visit that removes build-up in kitchens, bathrooms, appliances and areas routine upkeep misses, giving a home a reset before regular cleaning begins.',
        fit_yes=['Kitchens and bathrooms show build-up that everyday cleaning does not reach.', 'It is your first visit with Neat, or a long time since the last professional clean.', 'You want a solid starting point before switching to regular visits.'],
        fit_no=['Your home is already well kept: <a class="inline-link" href="/regular-cleaning.html">recurring visits</a> will cost you less time and effort.', 'The home will be empty between occupants: see <a class="inline-link" href="/move-in-move-out-cleaning.html">move-in and move-out cleaning</a>.'],
        focus_title='Where a deep clean makes the difference.',
        focus_text='Deep cleaning and regular cleaning work together: a more detailed first visit creates the baseline that ongoing care maintains. Describe the areas you want prioritized so the quote reflects your home.',
        focus=[('Kitchen details and appliance priorities', 'The areas where build-up shows first.'), ('Bathrooms that need extra attention', 'Detail work beyond a routine wipe-down.'), ('Spaces needing more than routine upkeep', 'The rooms you name when you request your quote.'), ('Oven and refrigerator', 'Included without a separate extra charge.'), ('A starting point for regular cleaning', 'Optional: keep the result with recurring visits.')],
        factors=[('Size of the home', 'Bedrooms, bathrooms and living areas set the base time.'), ('Current condition', 'Time since the last professional clean changes the work involved.'), ('Priority areas', 'The rooms and details you want the visit to focus on.'), ('Appliances', 'Oven and refrigerator are included; their condition helps plan the time.'), ('Products, pets and access', 'Special requests are discussed in advance and may affect the quote.')],
        related=f'Deep cleaning is a one-time, detailed reset. Once the build-up is gone, <a class="inline-link" href="/regular-cleaning.html">regular house cleaning</a> keeps the home at that level with less work per visit. If the property is about to be empty, <a class="inline-link" href="/move-in-move-out-cleaning.html">move-out cleaning</a> is planned around moving dates instead, and offices and studios are covered by <a class="inline-link" href="/commercial-cleaning.html">commercial cleaning for workspaces</a>. You can also <a class="inline-link" href="/faq.html">read the common questions about products, payment and timing</a>.',
        faqs=[
            ('What is the difference between deep cleaning and regular cleaning?', 'Regular cleaning maintains a home that is already in good shape. Deep cleaning is a more detailed visit for build-up that everyday upkeep does not reach, in kitchens, bathrooms and areas that need more than routine attention. A common approach is to book a deep clean first, then switch to regular visits to keep the result.'),
            ('Is there a fixed deep cleaning price?', 'No fixed price is published, because deep cleaning depends heavily on the home. Size, number of bathrooms, current condition and the areas you want prioritized all change the time needed. Share those details and you receive a quote for your space, confirmed before booking. Ask about the 10% off offer at the same time.'),
            ('Are oven and refrigerator cleaning extra?', 'No. Neat Cleaning includes oven and refrigerator cleaning without a separate extra charge. Mention them when you request your quote so access and preparation can be planned. Appliances are often where a deep clean makes the most visible difference in a kitchen, so it is worth describing their condition.'),
            ('When does a home need a deep cleaning?', 'Common moments are the first visit with a new cleaner, after a long stretch without professional cleaning, before or after hosting, at the change of seasons and before starting regular service. If surfaces look fine but the kitchen and bathrooms still show build-up, a deep cleaning is usually the right reset.'),
            ('How long does a deep cleaning take?', 'It depends on the size and condition of the home and the areas you prioritize, so timing is discussed when your quote is prepared. A deep cleaning takes longer than a regular visit because it covers more detail. You will know the expected timing before your appointment is confirmed.'),
            ('Can I book a deep cleaning once, without a recurring plan?', 'Yes. Deep cleaning can be booked as a one-time visit. If you later want to keep the home at that level, you can discuss regular cleaning visits; the deep clean then becomes a starting point for ongoing care rather than a commitment you have to make upfront.'),
            ('How should I prepare for a deep cleaning?', 'Tell us about access instructions, pets, product preferences and the rooms that matter most. Clearing countertops and personal items from the areas you want cleaned lets the visit focus on cleaning rather than tidying. Mention the oven and refrigerator so their preparation can be discussed beforehand.'),
        ]),
    'airbnb-cleaning': dict(
        title='Airbnb Cleaning in Natick, MA | Turnovers | Neat Cleaning',
        desc='Airbnb and short-term rental turnover cleaning in Natick, MA and within 25 miles, planned around check-out and check-in. Text (508) 202-8132 for a quote.',
        h1='Airbnb cleaning<br>in Natick, <em>MA.</em>',
        kick='Short-term rental turnovers',
        lead='Turnover cleaning planned around your guests’ check-out and check-in, following your listing’s own standards so the next arrival finds the place ready.',
        define='Airbnb cleaning is a turnover service that resets a short-term rental between check-out and check-in, preparing bedrooms, bathrooms and the kitchen to the host’s standard for the next guest.',
        fit_yes=['You host a short-term rental within 25 miles of Natick.', 'You need cleaning planned around check-out and check-in times.', 'You have a checklist or house standards you want followed.'],
        fit_no=['It is your own home on a routine: see <a class="inline-link" href="/regular-cleaning.html">recurring house cleaning</a>.', 'A long-term tenant is leaving: <a class="inline-link" href="/move-in-move-out-cleaning.html">move-out cleaning</a> fits better.'],
        focus_title='Plan the clean around the stay.',
        focus_text='Every rental has its own layout and turnover window. A conversation before the first turnover sets priorities for guest spaces, bathrooms and the kitchen, and confirms availability for your calendar.',
        focus=[('Guest bedrooms and shared spaces', 'Rooms reset to the way your listing presents them.'), ('Kitchen and bathroom priorities', 'The areas guests notice first.'), ('Your property’s cleaning instructions', 'Your checklist, reviewed before the first turnover.'), ('Timing between departures and arrivals', 'Confirmed against your booking calendar.'), ('Laundry, linens and restocking', 'Discussed before booking, never assumed.')],
        factors=[('Size of the rental', 'Bedrooms and bathrooms set the base time per turnover.'), ('Turnover window', 'The time between check-out and check-in affects scheduling.'), ('Frequency of stays', 'How often turnovers happen across the month.'), ('Laundry and restocking', 'Included only when agreed in the confirmed scope.'), ('Location', 'Confirmed within the 25-mile radius together with timing.')],
        related=f'Airbnb cleaning is built around turnover windows and host checklists. If you live in the home and want steady upkeep, <a class="inline-link" href="/regular-cleaning.html">regular cleaning visits</a> are the better match. Before a new listing goes live, or after a long season of bookings, a <a class="inline-link" href="/deep-cleaning.html">detailed deep clean</a> can set the baseline. For towns covered, see <a class="inline-link" href="/service-areas.html">the Natick-area service radius</a>.',
        faqs=[
            ('Can you clean between guest stays?', 'Airbnb cleaning is available by arrangement. Share the guest check-out and check-in times along with your booking calendar so we can confirm whether your turnover window can be accommodated. Turnovers depend on availability, so the earlier your calendar is shared, the easier it is to plan around your bookings.'),
            ('Are laundry and restocking included?', 'Laundry, linens, guest supplies and restocking are discussed before booking rather than assumed. Tell us what your listing needs between stays, and the quote and confirmed scope will state what is included. This keeps expectations clear for you and avoids surprises when the next guest arrives.'),
            ('How is Airbnb cleaning priced?', 'Each property is quoted individually. The size of the rental, the number of bedrooms and bathrooms, how often turnovers happen and any laundry or restocking requests set the price. Share your listing details by text or in the form on this page and you receive a quote before the first turnover is booked.'),
            ('Can I share my own cleaning checklist?', 'Yes, and it is encouraged. Every rental has its own layout and host standards. Share your property’s cleaning instructions, access details and the priorities for guest bedrooms, the kitchen and bathrooms. They are reviewed with you before the first turnover so each visit follows the same standard.'),
            ('Do you clean short-term rentals outside Natick?', 'Yes, within the service radius. Neat Cleaning serves short-term rentals in Natick and locations up to 25 miles away, such as Framingham, Wellesley and Needham. Send the property’s town or ZIP code with your request; location and turnover timing are confirmed together before booking.'),
            ('Do you bring the cleaning products?', 'Yes. Neat Cleaning brings its own cleaning products. If your listing uses specific products, for example fragrance-free options for guests with sensitivities, tell us before booking. Specific product requests are discussed in advance and may affect the quote.'),
        ]),
    'move-in-move-out-cleaning': dict(
        title='Move-In & Move-Out Cleaning in Natick, MA | Neat Cleaning',
        desc='Move-in and move-out cleaning in Natick, MA and within 25 miles. Kitchen, appliances, bathrooms and floors, oven and fridge included. Text for a quote.',
        h1='Move-in &amp; move-out cleaning<br>in Natick, <em>MA.</em>',
        kick='Between occupants',
        lead='Moving brings enough to organize. Book one clean for the home you are leaving or the one you are moving into, planned around your dates and access.',
        define='Move-in and move-out cleaning is a one-time clean of a home between occupants, covering the kitchen, appliances, bathrooms, rooms and floors so the property is ready to hand over or move into.',
        fit_yes=['You are leaving a rental or sold home and want it cleaned before handing over the keys.', 'You are moving into a home and want it cleaned before your things arrive.', 'You are a landlord or owner preparing a property between occupants.'],
        fit_no=['You are staying put and want a full reset: book <a class="inline-link" href="/deep-cleaning.html">a deep clean of your home</a>.', 'It is a guest turnover: see <a class="inline-link" href="/airbnb-cleaning.html">Airbnb cleaning</a>.'],
        focus_title='Care for the space between chapters.',
        focus_text='Whether you are preparing a new home or leaving one, the needs are different from an everyday visit. Let us know if the space will be empty, which areas need attention and how access will be coordinated.',
        focus=[('Kitchen and appliance priorities', 'Usually the first thing checked at a handover.'), ('Oven and refrigerator', 'Included without a separate extra charge.'), ('Bathrooms and interior living spaces', 'Every room the next occupant will use.'), ('Empty rooms and accessible floors', 'More surfaces are reachable once furniture is out.'), ('Access and your moving schedule', 'Keys, lockboxes and dates agreed beforehand.')],
        factors=[('Size of the property', 'Bedrooms, bathrooms and living areas set the base time.'), ('Empty or furnished', 'What remains in the rooms changes what can be reached.'), ('Current condition', 'Time since the last thorough clean affects the work.'), ('Date and access', 'Closing, lease and moving dates are confirmed with availability.'), ('Appliances', 'Included; their condition helps plan the visit.')],
        related=f'This page covers homes between occupants. If you are not moving and simply want a thorough reset, <a class="inline-link" href="/deep-cleaning.html">deep house cleaning</a> is the right service, and once you are settled in, <a class="inline-link" href="/regular-cleaning.html">recurring cleaning for your new home</a> keeps it that way. Hosts between guests should see <a class="inline-link" href="/airbnb-cleaning.html">short-term rental turnovers</a>.',
        faqs=[
            ('Does the home need to be empty?', 'Not necessarily. Tell us whether furniture or belongings will still be there on the cleaning day. Empty rooms allow more surfaces and floors to be reached, so the scope changes depending on what remains. We discuss access and the scope with you before confirming your appointment.'),
            ('Can you guarantee my security deposit?', 'No cleaning service can determine a landlord’s deposit decision, so no deposit return is promised. What we can do is go over the property’s cleaning priorities with you, including kitchen, appliances, bathrooms and floors, and agree on the scope before the visit, so you know exactly what will be cleaned before you hand back the keys.'),
            ('Is oven and refrigerator cleaning included in a move-out?', 'Yes. Oven and refrigerator cleaning are included without a separate extra charge. In a move-in or move-out, appliances are often one of the first things checked, so mention their condition when you request your quote and we will plan access and preparation.'),
            ('When should I schedule a move-out cleaning?', 'Ideally after your belongings are out and before the keys are returned or the new occupants arrive. Share your moving schedule, closing or lease dates and access details when you request your quote, and timing is discussed based on availability. Reaching out early gives you more flexibility around moving day.'),
            ('Can a landlord or owner book the cleaning?', 'Yes. Move-in and move-out cleaning is available to tenants, owners and landlords preparing a property between occupants within 25 miles of Natick. Share the property’s town, its condition, whether it will be empty and how access is handled, and scope and timing are confirmed before booking.'),
            ('How is move-in or move-out cleaning priced?', 'Each property is quoted individually. Size, number of bathrooms, current condition, whether the rooms will be empty and the date you need all affect the price. Share those details by text or in the form on this page and you receive a quote before booking. Ask about the 10% off offer when you request it.'),
        ]),
    'commercial-cleaning': dict(
        title='Office & Commercial Cleaning in Natick, MA | Neat Cleaning',
        desc='Office and workspace cleaning in Natick, MA and within 25 miles. Reception, kitchenette and restroom care, timing agreed in advance. Text for a quote.',
        h1='Commercial cleaning<br>in Natick, <em>MA.</em>',
        kick='Offices & workspaces',
        lead='Cleaning for local offices and shared workspaces, with the scope, schedule and access agreed in advance so your team arrives to a clean space.',
        define='Commercial cleaning is a scheduled service that cleans offices, reception areas, kitchenettes and bathrooms in a workspace, timed to the business’s access hours so staff and visitors arrive to a clean space.',
        fit_yes=['Offices, reception areas and shared workspaces near Natick.', 'You need cleaning timed around when the space is in use.', 'You want one direct contact for scope and scheduling.'],
        fit_no=['Specialized industrial cleaning: ask first, as it may be outside the scope offered.', 'A home office inside your house is covered by <a class="inline-link" href="/regular-cleaning.html">regular house cleaning</a>.'],
        focus_title='Your workspace. Your priorities.',
        focus_text='A commercial space needs a cleaning plan that reflects how it is used. Share the layout, shared areas and access requirements, and we confirm the service that fits your request.',
        focus=[('Office and shared workspace priorities', 'Desks and work areas, as agreed in the scope.'), ('Reception and common areas', 'The first impression for visitors.'), ('Kitchenette and bathroom needs', 'The shared rooms that need regular care.'), ('Access instructions and preferred timing', 'Keys, alarm codes and hours agreed beforehand.')],
        factors=[('Size and layout', 'Square footage, rooms and shared areas set the base time.'), ('How the space is used', 'Staff count and visitor traffic change the work.'), ('Kitchens and restrooms', 'The number of shared rooms affects each visit.'), ('Frequency', 'Recurring schedules are planned around your week.'), ('Access hours', 'Cleaning times are confirmed with availability before booking.')],
        related=f'Commercial cleaning is for workspaces used by a team and their visitors. For a home, including a home office, <a class="inline-link" href="/regular-cleaning.html">residential cleaning on a routine</a> is the better fit, and a property changing tenants is covered by <a class="inline-link" href="/move-in-move-out-cleaning.html">cleaning between occupants</a>. To check whether your business address is within reach, see <a class="inline-link" href="/service-areas.html">towns within 25 miles of Natick</a>.',
        faqs=[
            ('Can cleaning be arranged around business hours?', 'Share your preferred times when you request a quote. Scheduling and access arrangements are confirmed before booking, based on availability. Cleaning outside your busiest hours is often easiest for staff and visitors, so tell us when the space is open, when it is quiet and how access will be provided.'),
            ('What kinds of workspaces do you clean?', 'Neat Cleaning provides commercial cleaning for local workspaces in the Natick area, covering offices and shared work areas, reception and common areas, and the kitchenettes and bathrooms used by staff. Tell us the type of property and how it is used, and we confirm whether the request fits the commercial cleaning offered.'),
            ('Do you provide specialized industrial cleaning?', 'Contact us with the exact type of property and cleaning required. Neat Cleaning’s commercial service is designed for everyday workspaces. Specialized industrial cleaning may fall outside that scope, and we will tell you clearly whether your request is something we can take on before any quote is given.'),
            ('How is commercial cleaning priced?', 'Each workspace is quoted individually. The size of the space, how it is used, the number of bathrooms and kitchen areas, how often you need cleaning and the access hours all affect the price. Share those details and you receive a quote confirmed before booking. Payment is accepted by Zelle, cash or check.'),
            ('Can you clean on a recurring schedule?', 'Recurring commercial cleaning can be discussed when you request your quote. Tell us the frequency you have in mind, such as weekly or every other week, and your preferred days and times. The schedule is confirmed based on availability before booking, so your team knows when to expect each visit.'),
            ('Do you bring cleaning products?', 'Yes, Neat Cleaning brings its own cleaning products. If your business requires specific products, for example for certain surfaces or for staff with sensitivities, tell us when you request your quote. Special product requests are discussed in advance and may affect the quote.'),
        ]),
}


# ---------------------------------------------------------------- pages
def page_home():
    path = '/'
    title = 'House Cleaning in Natick, MA – Regular & Deep | Neat Cleaning'
    desc = 'Owner-led house cleaning in Natick, MA since 2021. Regular and deep cleaning within 25 miles, oven and refrigerator included. Text (508) 202-8132 for a quote.'
    graph = [business_node(),
             {'@type': 'WebSite', '@id': SITE_ID, 'url': ORIGIN + '/', 'name': 'Neat Cleaning', 'inLanguage': 'en-US', 'publisher': {'@id': BIZ_ID}},
             webpage_node(path, title, desc)]
    p = dict(title=title, desc=desc, schema=ld({'@context': 'https://schema.org', '@graph': graph}))

    rows, pics = [], []
    for i, s in enumerate(SERVICES):
        tag = '<span class="tag">Core</span>' if s['core'] else ''
        rows.append(f'''<a class="svc-row" href="/{s["slug"]}.html" data-index="{i}" data-caption="{s['name']}">
 <span class="n">0{i + 1}</span><h3>{s["name"]}{tag}</h3><span class="arrow">{icon("arrow")}</span>
 <p>{s["blurb"]}</p><span class="fit"><b>Best for</b>{s["fit"]}</span>
</a>''')
        pics.append(img(s['hero'], sizes='40vw', cls='is-active' if i == 0 else ''))

    criteria = [
        ('Who will actually clean my home?', 'Many services send whoever is on the schedule that day.', 'Daiane, the owner, does the cleaning herself. Additional help is arranged only when demand requires it.'),
        ('Who do I talk to?', 'Details get lost when requests pass through several people.', 'You text Daiane directly. Her daughter helps answer phone calls.'),
        ('Are the oven and refrigerator extra?', 'Appliance add-ons often raise the final bill.', 'Both are included without a separate charge.'),
        ('Who brings the supplies?', 'You should not have to stock products for the visit.', 'Neat brings its own products. Specific products can be requested in advance.'),
        ('When is the price confirmed?', 'Vague scope is where surprises come from.', 'Scope, quote and timing are confirmed with you before booking.'),
        ('How do I pay?', 'Know the methods before the visit, not after.', 'Zelle, cash or check.'),
        ('Do you cover my town?', 'Travel limits decide real availability.', 'Natick and locations up to 25 miles away, confirmed by town or ZIP code.'),
    ]
    crit_rows = ''.join(f'<tr><th scope="row">{q}</th><td data-label="Why it matters">{w}</td><td class="ours" data-label="At Neat Cleaning">{a}</td></tr>' for q, w, a in criteria)

    home_faq = [FAQ_GENERAL['Booking & quotes'][1], FAQ_GENERAL['During the visit'][0], FAQ_GENERAL['During the visit'][2], FAQ_GENERAL['Booking & quotes'][3], FAQ_GENERAL['Payment & offer'][0]]
    near = [t for t, d, _ in TOWN_LIST[:12]]
    town_items = '<li class="base">Natick <span>Base</span></li>' + ''.join(f'<li>{t} <span>~{DIST[t]:.0f} mi</span></li>' for t in near[:11])

    body = f'''<section class="hero dark" aria-labelledby="hero-title">
 <div class="hero-copy">
  {kicker("", "Natick, Massachusetts · Since 2021")}
  <h1 id="hero-title">House cleaning<br>in Natick, <em>kept personal.</em></h1>
  <p class="lead">Regular and deep cleaning for homes in Natick and up to 25 miles around it. You talk directly with Daiane, the owner, who takes care of the cleaning herself. The oven and refrigerator are part of the visit, not an add-on.</p>
  <div class="actions">{btn(SMS, "Text for a quote", "gold", "sms")}{btn("#quote", "Request a quote online", "ghost")}</div>
  <ul class="hero-facts">
   <li>{icon("user")}Owner-led since 2021</li>
   <li>{icon("spark")}Oven &amp; fridge included</li>
   <li>{icon("home")}Own cleaning products</li>
   <li>{icon("card")}Zelle · cash · check</li>
  </ul>
 </div>
 <div class="hero-media">{img("home-hero", eager=True, sizes="(max-width: 1020px) 100vw, 50vw")}</div>
</section>
{definition("House cleaning in Natick is a scheduled in-home service that cleans kitchens, bathrooms, bedrooms, living areas and floors for households within 25 miles, with oven and refrigerator cleaning included in the visit.")}

<section class="section" aria-labelledby="svc-title">
 <div class="wrap">
  <div class="section-head">
   <div>{kicker("I", "Services")}<h2 id="svc-title">Five services.<br>Two at the <em>heart</em> of it.</h2></div>
   <p>Regular and deep cleaning are what Neat does most. Rentals, moves and workspaces follow the same approach: the scope and timing are confirmed with you before booking.</p>
  </div>
  <div class="svc-index">
   <figure class="svc-preview" aria-hidden="true">{"".join(pics)}<figcaption>{SERVICES[0]["name"]}</figcaption></figure>
   <div><div class="svc-list">{"".join(rows)}</div><p style="margin-top:28px">{link("/services.html", "Compare all services")}</p></div>
  </div>
 </div>
</section>

<section class="section ivory" aria-labelledby="criteria-title">
 <div class="wrap">
  <div class="section-head">
   <div>{kicker("II", "Before you hire anyone")}<h2 id="criteria-title">What to ask any house cleaner, and <em>how we answer.</em></h2></div>
   <p>Use these questions with any company you are considering. They are the ones that decide how a cleaning service feels after the third visit, not the first.</p>
  </div>
  <div class="table-wrap reveal">
   <table class="dtable">
    <thead><tr><th scope="col">Question to ask</th><th scope="col">Why it matters</th><th scope="col">At Neat Cleaning</th></tr></thead>
    <tbody>{crit_rows}</tbody>
   </table>
  </div>
 </div>
</section>

<section class="section" aria-labelledby="price-title">
 <div class="wrap split">
  <figure class="split-media reveal">{img("home-kitchen")}<span class="frame" aria-hidden="true"></span><figcaption>Oven and refrigerator · included in the visit</figcaption></figure>
  <div>
   {kicker("III", "Pricing")}
   <h2 id="price-title">How your quote<br>is <em>put together.</em></h2>
   <p class="lead" style="margin-top:22px">Two homes with the same number of bedrooms can need very different time. So each quote is built from the details of your home, shared by text or through the form, and confirmed before anything is booked.</p>
   <!-- PREENCHER: dated reference price range (e.g. "Regular cleaning, 3-bed / 2-bath in Natick, Oct 2026: $X–$Y") -->
   <ul class="factors">
    <li><b>Size of the home</b><span>Bedrooms, bathrooms and living areas set most of the time.</span></li>
    <li><b>Service type</b><span>A deep or move-out clean covers more detail than a regular visit.</span></li>
    <li><b>Frequency</b><span>Recurring visits are planned differently from a one-time clean.</span></li>
    <li><b>Current condition</b><span>Time since the last professional clean changes the work.</span></li>
    <li><b>Special requests</b><span>Specific products, pets or focus areas are discussed in advance.</span></li>
   </ul>
   <p class="note"><strong>Ask about 10% off</strong> when you request your quote.</p>
  </div>
 </div>
</section>

{steps_block(True, "IV")}

<section class="section ivory" aria-labelledby="quote-title" id="quote">
 <div class="wrap quote">
  <div>
   {kicker("V", "Request a quote")}
   <h2>Tell us about<br>your <em>space.</em></h2>
   <p class="lead" style="margin-top:22px">Text is the fastest way to reach Daiane. If you prefer, send the form and she will text you back to talk through the scope and your quote.</p>
   <div class="contact-lines">
    <a href="{SMS}">{icon("sms")}<small>Text · preferred</small><b>{PHONE}</b></a>
    <a href="{TEL}">{icon("phone")}<small>Call</small><b>{PHONE}</b></a>
    <div>{icon("pin")}<small>Service area</small><b>Natick, MA + 25 miles</b></div>
   </div>
  </div>
  {quote_form("home-quote", details=False, heading="Request your quote", level="h3")}
 </div>
</section>

<section class="section dark" aria-labelledby="owner-title">
 <div class="wrap owner">
  <figure class="owner-media reveal">{img("about-hero", sizes="(max-width: 1020px) 100vw, 40vw")}</figure>
  <div>
   {kicker("VI", "Who you will talk to")}
   <h2 id="owner-title" class="sr-only">Meet the owner of Neat Cleaning</h2>
   <blockquote><p>The person who hears how you want your home cared for is the person who cleans it.</p></blockquote>
   <div class="sig"><div><b>{OWNER}</b><span>Owner, Neat Cleaning · Natick, MA</span></div></div>
   <p style="margin-top:30px;max-width:36em">Neat Cleaning has grown through referrals since 2021, one conversation and one clean at a time. Daiane answers your texts and takes care of the cleaning herself, with additional help arranged when demand requires it. Her daughter helps answer phone calls.</p>
   <p style="margin-top:26px">{link("/about.html", "Read the Neat story")}</p>
  </div>
 </div>
</section>

<section class="section-tight" aria-label="Offer">
 <div class="wrap">{offer_block()}</div>
</section>

<section class="section ivory" aria-labelledby="area-title">
 <div class="wrap split">
  <div>
   {kicker("VII", "Service area")}
   <h2 id="area-title">Natick, and the<br>towns <em>around it.</em></h2>
   <p class="lead" style="margin-top:22px">Neat Cleaning serves Natick and locations within 25 miles. Send your town or ZIP code and availability is confirmed for your address and date.</p>
   <p style="margin-top:26px">{link("/service-areas.html", "See the full service area")}</p>
  </div>
  <div><ul class="towns" style="columns:2">{town_items}</ul><p class="note">Approximate straight-line distance from Natick center.</p></div>
 </div>
</section>

<section class="section" aria-labelledby="faq-title">
 <div class="wrap faq-layout">
  <div class="sticky">{kicker("VIII", "Questions")}<h2 id="faq-title">Good questions,<br><em>clear answers.</em></h2><p style="margin-top:20px">Products, pricing, payment and how booking works.</p><p style="margin-top:26px">{link("/faq.html", "All questions")}</p></div>
  {faq_list(home_faq)}
 </div>
</section>'''
    return 'index.html', page(p, body, '/')


def page_service(slug):
    s, d = SVC[slug], SERVICE_PAGES[slug]
    path = f'/{slug}.html'
    trail = [('Home', '/'), ('Services', '/services.html'), (s['name'], path)]
    graph = [business_node(), webpage_node(path, d['title'], d['desc']),
             {'@type': 'Service', '@id': ORIGIN + path + '#service', 'name': s['short'].capitalize() + ' in Natick, MA', 'serviceType': s['name'],
              'description': strip_tags(d['define']), 'provider': {'@id': BIZ_ID}, 'url': ORIGIN + path,
              'image': f'{ORIGIN}/assets/images/og-{s["hero"]}.jpg',
              'areaServed': [{'@type': 'City', 'name': 'Natick', 'containedInPlace': {'@type': 'State', 'name': 'Massachusetts'}}] +
                            [{'@type': 'City', 'name': t} for t, _, _ in TOWN_LIST[:10]]},
             breadcrumb_node(trail), faq_node(d['faqs'])]
    p = dict(title=d['title'], desc=d['desc'], schema=ld({'@context': 'https://schema.org', '@graph': graph}))
    focus = ''.join(f'<li>{icon("check")}<span>{a}<small>{b}</small></span></li>' for a, b in d['focus'])
    factors = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in d['factors'])
    others = [x for x in SERVICES if x['slug'] != slug]
    rel = ''.join(f'<a href="/{x["slug"]}.html"><span class="n">0{SERVICES.index(x) + 1}</span><b>{x["name"]}</b><span>{x["blurb"]}</span></a>' for x in others)
    yes = ''.join(f'<li>{t}</li>' for t in d['fit_yes'])
    no = ''.join(f'<li>{t}</li>' for t in d['fit_no'])
    body = f'''<section class="hero page-hero dark" aria-labelledby="hero-title">
 <div class="hero-copy">
  {crumbs(trail)}
  {kicker("", d["kick"] + " · Natick, MA")}
  <h1 id="hero-title">{d["h1"]}</h1>
  <p class="lead">{d["lead"]}</p>
  <div class="actions">{btn(SMS, "Text for a quote", "gold", "sms")}{btn("#quote", "Request a quote online", "ghost")}</div>
  <ul class="hero-facts">
   <li>{icon("user")}Owner-led since 2021</li><li>{icon("spark")}Oven &amp; fridge included</li>
   <li>{icon("pin")}Natick + 25 miles</li><li>{icon("card")}Zelle · cash · check</li>
  </ul>
 </div>
 <div class="hero-media">{img(s["hero"], eager=True)}</div>
</section>
{definition(d["define"])}

<section class="section" aria-labelledby="fit-title">
 <div class="wrap">
  <div class="section-head">
   <div>{kicker("I", "Is it the right service?")}<h2 id="fit-title">Who {s["short"].lower()}<br>is <em>for.</em></h2></div>
   <p>Booking the right service first saves time for everyone. If one of the cases on the right sounds like you, the linked page will serve you better.</p>
  </div>
  <div class="fit-grid reveal">
   <div class="yes"><h3>A good fit if</h3><ul>{yes}</ul></div>
   <div class="no"><h3>Consider instead</h3><ul>{no}</ul></div>
  </div>
 </div>
</section>

<section class="section ivory" aria-labelledby="focus-title">
 <div class="wrap split reverse">
  <figure class="split-media reveal">{img(s["detail"])}<span class="frame" aria-hidden="true"></span></figure>
  <div>
   {kicker("II", "What the visit covers")}
   <h2 id="focus-title">{d["focus_title"]}</h2>
   <p class="lead" style="margin:22px 0 30px">{d["focus_text"]}</p>
   <ul class="checklist">{focus}</ul>
   <p class="note">The final scope and timing are confirmed with you before booking.</p>
  </div>
 </div>
</section>

<section class="section" aria-labelledby="price-title">
 <div class="wrap split">
  <div>
   {kicker("III", "Pricing")}
   <h2 id="price-title">What sets the price of {s["short"].lower()}.</h2>
   <p class="lead" style="margin-top:22px">Every quote is prepared for the specific property, from the details you share by text or through the form. These are the factors that move it.</p>
   <p class="note"><strong>Ask about 10% off</strong> when you request your quote. Payment by Zelle, cash or check.</p>
   <!-- PREENCHER: dated reference price range for this service (region + month/year) -->
  </div>
  <ul class="factors reveal" style="margin-top:0">{factors}</ul>
 </div>
</section>

{steps_block(True, "IV")}

<section class="section" aria-labelledby="faq-title">
 <div class="wrap faq-layout">
  <div class="sticky">
   {kicker("V", "Questions")}
   <h2 id="faq-title">{s["short"].capitalize()}: <em>answers.</em></h2>
   <p style="margin-top:20px">Still unsure? Text <a class="inline-link" href="{SMS}">{PHONE}</a>.</p>
  </div>
  {faq_list(d["faqs"])}
 </div>
</section>

<section class="section-tight ivory" aria-labelledby="related-title">
 <div class="wrap">
  {kicker("VI", "Related services")}
  <h2 id="related-title" class="sr-only">How {s["short"].lower()} compares with other services</h2>
  <p class="related-text">{d["related"]}</p>
  <nav class="related-grid" aria-label="Other cleaning services">{rel}</nav>
 </div>
</section>

<section class="section" aria-labelledby="{slug}-quote-title" id="quote">
 <div class="wrap quote">
  <div>
   {kicker("VII", "Request a quote")}
   <h2>Your {s["short"].lower()} <em>quote.</em></h2>
   <p class="lead" style="margin-top:22px">Send the details and Daiane will text you to confirm the scope, timing and price. Prefer to talk first? Text or call directly.</p>
   <div class="contact-lines">
    <a href="{SMS}">{icon("sms")}<small>Text · preferred</small><b>{PHONE}</b></a>
    <a href="{TEL}">{icon("phone")}<small>Call</small><b>{PHONE}</b></a>
    <a href="mailto:{EMAIL}">{icon("mail")}<small>Email</small><b>{EMAIL}</b></a>
   </div>
   <div style="margin-top:36px">{byline()}</div>
  </div>
  {quote_form(slug + "-quote", preselect=slug, heading="Request your quote", level="h3")}
 </div>
</section>'''
    return f'{slug}.html', page(p, body, slug)


def page_services():
    path = '/services.html'
    title = 'Compare Cleaning Services in Natick, MA | Neat Cleaning'
    desc = 'Compare regular, deep, Airbnb, move-in/move-out and commercial cleaning in Natick, MA. Owner-led since 2021, oven and fridge included. Request your quote.'
    trail = [('Home', '/'), ('Services', path)]
    item_list = {'@type': 'ItemList', 'name': 'Cleaning services in Natick, MA', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'url': f'{ORIGIN}/{s["slug"]}.html', 'name': s['name']} for i, s in enumerate(SERVICES)]}
    graph = [business_node(), webpage_node(path, title, desc, 'CollectionPage'), breadcrumb_node(trail), item_list]
    p = dict(title=title, desc=desc, schema=ld({'@context': 'https://schema.org', '@graph': graph}))
    compare = [
        ('Regular Cleaning', 'Homes already in good shape', 'Recurring: weekly, every two weeks or monthly', 'Kitchen, bathrooms, bedrooms, living areas, floors'),
        ('Deep Cleaning', 'Build-up, first visits, long gaps', 'One-time, or before regular visits', 'Kitchen details, appliances, bathrooms, priority rooms'),
        ('Airbnb Cleaning', 'Short-term rental hosts', 'Each turnover, by arrangement', 'Guest bedrooms, kitchen, bathrooms, host checklist'),
        ('Move-In & Move-Out', 'Homes between occupants', 'One-time, around moving dates', 'Kitchen, appliances, bathrooms, empty rooms, floors'),
        ('Commercial Cleaning', 'Offices and workspaces', 'Agreed schedule and access hours', 'Work areas, reception, kitchenette, restrooms'),
    ]
    rows = ''.join(f'<tr><th scope="row"><a class="inline-link" href="/{SERVICES[i]["slug"]}.html">{a}</a></th><td data-label="Best for">{b}</td><td data-label="How it is scheduled">{c}</td><td data-label="Typical focus">{dd}</td></tr>' for i, (a, b, c, dd) in enumerate(compare))
    cards = ''
    for i, s in enumerate(SERVICES):
        lg = ' lg' if i < 2 else ''
        cards += f'''<article class="svc-card{lg} reveal"><a class="img" href="/{s["slug"]}.html" tabindex="-1" aria-hidden="true">{img(s["hero"], sizes="(max-width: 720px) 100vw, 50vw")}</a>
<div class="body"><span class="n">0{i + 1}{" · Core service" if s["core"] else ""}</span><h2><a href="/{s["slug"]}.html">{s["name"]}</a></h2><p>{s["blurb"]} Best for {s["fit"][0].lower() + s["fit"][1:]}</p>{link("/" + s["slug"] + ".html", "Explore " + s["short"].lower())}</div></article>'''
    body = f'''<section class="hero page-hero dark" aria-labelledby="hero-title">
 <div class="hero-copy">
  {crumbs(trail)}
  {kicker("", "Natick, MA · 25-mile radius")}
  <h1 id="hero-title">Cleaning services<br>in Natick, <em>MA.</em></h1>
  <p class="lead">Five services for homes, rentals and workspaces around Natick. Regular and deep cleaning are the core; each one is quoted for your property and confirmed before booking.</p>
  <div class="actions">{btn(SMS, "Text for a quote", "gold", "sms")}{btn("/contact.html#quote", "Request a quote online", "ghost")}</div>
 </div>
 <div class="hero-media">{img("home-kitchen", eager=True)}</div>
</section>
{definition("Residential and commercial cleaning services around Natick cover recurring upkeep, detailed resets, short-term rental turnovers, moves and workspaces, each quoted per property and confirmed before booking.")}

<section class="section" aria-labelledby="compare-title">
 <div class="wrap">
  <div class="section-head">
   <div>{kicker("I", "Compare")}<h2 id="compare-title">Which service<br>fits your <em>situation?</em></h2></div>
   <p>Start from where your home is today. If you are between two options, describe the space by text and Daiane will suggest where to begin.</p>
  </div>
  <div class="table-wrap reveal">
   <table class="dtable">
    <thead><tr><th scope="col">Service</th><th scope="col">Best for</th><th scope="col">How it is scheduled</th><th scope="col">Typical focus</th></tr></thead>
    <tbody>{rows}</tbody>
   </table>
  </div>
  <p class="note">Every service includes oven and refrigerator cleaning without a separate charge, and Neat brings its own products.</p>
 </div>
</section>

<section class="section ivory" aria-labelledby="all-title">
 <div class="wrap">
  <div class="section-head stack">{kicker("II", "The services")}<h2 id="all-title" class="sr-only">All cleaning services</h2></div>
  <div class="svc-cards">{cards}</div>
 </div>
</section>

<section class="section" aria-labelledby="start-title">
 <div class="wrap split">
  <div>
   {kicker("III", "Not sure where to begin?")}
   <h2 id="start-title">A simple way<br>to <em>decide.</em></h2>
  </div>
  <div class="prose">
   <p>If your home has not had professional cleaning in months, start with <a href="/deep-cleaning.html">a deep cleaning visit</a>, then move to <a href="/regular-cleaning.html">recurring visits</a> to keep the result. If the home is about to be empty, book <a href="/move-in-move-out-cleaning.html">move-in or move-out cleaning</a> instead.</p>
   <p>Hosts plan <a href="/airbnb-cleaning.html">turnovers between guests</a> around the booking calendar, and businesses arrange <a href="/commercial-cleaning.html">workspace cleaning</a> around access hours. Whichever you choose, the scope and price are confirmed with you before booking.</p>
   <div class="actions">{btn(SMS, "Help me choose", "", "sms")}</div>
  </div>
 </div>
</section>

{steps_block(True, "IV")}

<section class="section-tight" aria-label="Offer"><div class="wrap">{offer_block()}</div></section>'''
    return 'services.html', page(p, body, 'services')


def page_about():
    path = '/about.html'
    title = 'About Neat Cleaning | Owner-Led House Cleaning in Natick, MA'
    desc = 'Meet Daiane and Neat Cleaning, an owner-led cleaning business in Natick, MA since 2021. Direct communication, own products, oven and fridge included.'
    trail = [('Home', '/'), ('About', path)]
    person = {'@type': 'Person', '@id': ORIGIN + '/about.html#owner', 'name': OWNER, 'jobTitle': 'Owner', 'worksFor': {'@id': BIZ_ID},
              'homeLocation': {'@type': 'Place', 'name': 'Natick, Massachusetts'}}
    graph = [business_node(), webpage_node(path, title, desc, 'AboutPage') | {'mainEntity': {'@id': BIZ_ID}}, person, breadcrumb_node(trail)]
    p = dict(title=title, desc=desc, schema=ld({'@context': 'https://schema.org', '@graph': graph}))
    body = f'''<section class="hero page-hero dark" aria-labelledby="hero-title">
 <div class="hero-copy">
  {crumbs(trail)}
  {kicker("", "About Neat Cleaning")}
  <h1 id="hero-title">Owner-led cleaning<br>in Natick, <em>since 2021.</em></h1>
  <p class="lead">Neat Cleaning is a Natick-based business that has grown through referrals, one conversation and one clean at a time. It is led by Daiane, who takes care of the cleaning herself.</p>
  <div class="actions">{btn(SMS, "Text Daiane", "gold", "sms")}{btn("/services.html", "See the services", "ghost")}</div>
 </div>
 <div class="hero-media">{img("about-hero", eager=True)}</div>
</section>
{definition("Neat Cleaning is an owner-led cleaning business in Natick, Massachusetts, founded in 2021, providing regular, deep, Airbnb, move-in and move-out, and commercial cleaning within 25 miles.", "Who we are")}

<section class="section" aria-labelledby="facts-title">
 <div class="wrap">
  <h2 id="facts-title" class="sr-only">Neat Cleaning in numbers</h2>
  {facts_band()}
 </div>
</section>

<section class="section ivory" aria-labelledby="owner-title">
 <div class="wrap split">
  <figure class="split-media reveal">{img("regular-detail")}<span class="frame" aria-hidden="true"></span></figure>
  <div class="prose">
   {kicker("I", "The person behind the care")}
   <h2 id="owner-title" style="margin-top:0">Meet <em>Daiane.</em></h2>
   <p>Neat Cleaning is led by {OWNER}. She takes care of the cleaning herself, with additional help arranged as demand requires. That is a deliberate choice: the person who hears how you like your home cared for is the person responsible for doing it.</p>
   <p>Direct communication is part of that approach. Daiane responds to text messages, and her daughter helps answer calls. You can discuss your home, your priorities and the service you need before an appointment is confirmed.</p>
   <p>Regular cleaning, together with deep cleaning, is the primary focus. Neat also offers <a href="/airbnb-cleaning.html">Airbnb turnovers</a>, <a href="/move-in-move-out-cleaning.html">move-in and move-out cleaning</a> and <a href="/commercial-cleaning.html">commercial cleaning</a> for local workspaces.</p>
   <!-- PREENCHER: photo of Daiane (real), languages spoken, Google reviews link -->
  </div>
 </div>
</section>

<section class="section dark" aria-labelledby="values-title">
 <div class="wrap">
  <div class="section-head">
   <div>{kicker("II", "What guides the work")}<h2 id="values-title">Care you can talk<br>to someone <em>about.</em></h2></div>
   <p>Trust, quality, organization and professionalism are the pillars of the brand. In practice, they look like this.</p>
  </div>
  <ol class="steps reveal">
   <li><span class="n">I</span><h3>Attention to detail</h3><p>Oven and refrigerator cleaning are included without a separate extra charge, because a kitchen is not clean without them.</p></li>
   <li><span class="n">II</span><h3>Clear communication</h3><p>Your quote and preferences are discussed directly by text before the visit, and confirmed before booking.</p></li>
   <li><span class="n">III</span><h3>Organization</h3><p>Neat brings its own products and plans each visit around your priorities, pets and access instructions.</p></li>
   <li><span class="n">IV</span><h3>A local approach</h3><p>Based in Natick and serving locations within up to 25 miles, so the business stays close to the homes it cares for.</p></li>
  </ol>
 </div>
</section>

<section class="section" aria-labelledby="how-title">
 <div class="wrap split">
  <div>{kicker("III", "Working with Neat")}<h2 id="how-title">What to expect<br>when you <em>reach out.</em></h2></div>
  <div>
   <ul class="checklist">
    <li>{icon("check")}<span>You text or call {PHONE}<small>Text is the fastest way to reach Daiane directly.</small></span></li>
    <li>{icon("check")}<span>Your home is discussed before any price<small>Rooms, priorities, pets, products and access.</small></span></li>
    <li>{icon("check")}<span>Scope, quote and timing are confirmed<small>Nothing is booked until you agree.</small></span></li>
    <li>{icon("check")}<span>You pay by Zelle, cash or check<small>Payment details are confirmed when the appointment is arranged.</small></span></li>
   </ul>
   <div style="margin-top:32px">{byline()}</div>
  </div>
 </div>
</section>'''
    return 'about.html', page(p, body, '/about.html')


def area_map():
    size = 640
    c = size / 2
    scale = 292 / 16.0  # the towns listed sit within ~15 miles; the radius continues to 25
    lat0 = NATICK[0]

    def xy(coord):
        dx = (coord[1] - NATICK[1]) * math.cos(math.radians(lat0)) * 69.17
        dy = (coord[0] - NATICK[0]) * 69.0
        return c + dx * scale, c - dy * scale
    dash = ' stroke-dasharray="2 5"'
    rings = ''.join(f'<circle cx="{c}" cy="{c}" r="{rr * scale:.1f}" fill="none" stroke="rgba(233,208,115,{.22 if rr < 15 else .5})" stroke-width="1"{"" if rr == 15 else dash}/>'
                    f'<text x="{c + 4}" y="{c - rr * scale - 6:.1f}" fill="#a9a19a" font-size="10" font-family="Montserrat, sans-serif" letter-spacing="1">{rr} MI</text>' for rr in (5, 10, 15))
    dots = ''
    left_side = {'Framingham', 'Ashland', 'Holliston', 'Hopkinton', 'Southborough', 'Marlborough', 'Milford', 'Medway', 'Sudbury', 'Sherborn', 'Millis', 'Wayland'}
    nudge = {'Wellesley': (0, -4), 'Dover': (0, 10), 'Needham': (0, 2), 'Westwood': (0, 10), 'Sherborn': (0, 10), 'Weston': (0, -2), 'Framingham': (0, -4), 'Norwood': (0, 10), 'Dedham': (0, 2), 'Watertown': (0, 4), 'Newton': (0, 4), 'Millis': (0, 10), 'Ashland': (0, 10)}
    for t, coord in TOWNS.items():
        x, y = xy(coord)
        nx, ny = nudge.get(t, (0, 0))
        anchor = 'end' if t in left_side else 'start'
        tx = x - 8 if anchor == 'end' else x + 8
        dots += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#d2b25f"/>'
                 f'<text x="{tx + nx:.1f}" y="{y + 4 + ny:.1f}" text-anchor="{anchor}" fill="#ece6de" font-size="13" font-family="Montserrat, sans-serif">{t}</text>')
    compass = f'<text x="{size - 30}" y="34" fill="#d2b25f" font-size="12" font-family="Cinzel, serif" text-anchor="middle">N</text><path d="M{size - 30} 40v26" stroke="#d2b25f" stroke-width="1"/>'
    return f'''<figure class="map-card reveal">
 <svg viewBox="0 0 {size} {size}" role="img" aria-labelledby="map-title map-desc">
  <title id="map-title">Neat Cleaning service radius around Natick, Massachusetts</title>
  <desc id="map-desc">Schematic map with Natick at the center and rings at 5, 10 and 15 miles, inside a 25-mile service radius, showing nearby towns such as Framingham, Wellesley, Needham, Wayland and Newton.</desc>
  <rect width="{size}" height="{size}" fill="#0e0d0d"/>
  {rings}{dots}{compass}
  <circle cx="{c}" cy="{c}" r="7" fill="#bc9246"/><circle cx="{c}" cy="{c}" r="13" fill="none" stroke="#bc9246" stroke-width="1"/>
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
    graph = [business_node(), webpage_node(path, title, desc), breadcrumb_node(trail), faq_node(faqs)]
    p = dict(title=title, desc=desc, schema=ld({'@context': 'https://schema.org', '@graph': graph}))
    trs = '<li class="base">Natick <span>Base</span></li>' + ''.join(f'<li>{t} <span>~{dd:.1f} mi {b}</span></li>' for t, dd, b in TOWN_LIST)
    body = f'''<section class="hero page-hero dark" aria-labelledby="hero-title">
 <div class="hero-copy">
  {crumbs(trail)}
  {kicker("", "Service area")}
  <h1 id="hero-title">House cleaning in Natick<br>and towns within <em>25 miles.</em></h1>
  <p class="lead">Based in Natick, Massachusetts, and caring for homes and workspaces in the towns around it. Send your town or ZIP code and availability is confirmed for your address.</p>
  <div class="actions">{btn(SMS, "Text my ZIP code", "gold", "sms")}{btn("#quote", "Check by form", "ghost")}</div>
 </div>
 <div class="hero-media">{img("area-hero", eager=True)}</div>
</section>
{definition("The Neat Cleaning service area is Natick, Massachusetts, and locations within 25 miles, a radius that includes Framingham, Wellesley, Needham, Wayland, Sudbury, Holliston and Newton.")}

<section class="section" aria-labelledby="map-title-h">
 <div class="wrap split">
  {area_map()}
  <div>
   {kicker("I", "The radius")}
   <h2 id="map-title-h">Close to home,<br>by <em>design.</em></h2>
   <p class="lead" style="margin:22px 0 28px">Staying within 25 miles of Natick keeps travel short and the schedule realistic. Most of the towns below are within 15 miles in a straight line.</p>
   <ul class="checklist">
    <li>{icon("check")}<span>Send your town or ZIP code<small>A full street address is not needed in the first message.</small></span></li>
    <li>{icon("check")}<span>Tell us which service you need<small>Regular, deep, Airbnb, move-in/out or commercial.</small></span></li>
    <li>{icon("check")}<span>Confirm availability, scope and timing<small>Before anything is booked.</small></span></li>
   </ul>
  </div>
 </div>
</section>

<section class="section ivory" aria-labelledby="towns-title">
 <div class="wrap">
  <div class="section-head">
   <div>{kicker("II", "Towns in the radius")}<h2 id="towns-title">Towns around<br><em>Natick.</em></h2></div>
   <p>Approximate straight-line distance from Natick center. Road distance is longer. Your town is not listed? If it is within 25 miles, send your ZIP code anyway.</p>
  </div>
  <ul class="towns reveal">{trs}</ul>
 </div>
</section>

<section class="section" aria-labelledby="faq-title">
 <div class="wrap faq-layout">
  <div class="sticky">{kicker("III", "Questions")}<h2 id="faq-title">Service area <em>questions.</em></h2></div>
  {faq_list(faqs)}
 </div>
</section>

<section class="section ivory" aria-labelledby="area-quote-title" id="quote">
 <div class="wrap quote">
  <div>
   {kicker("IV", "Check your address")}
   <h2>Are you <em>nearby?</em></h2>
   <p class="lead" style="margin-top:22px">Your town or ZIP code is enough to start. Daiane will text you back to confirm availability and talk through your quote.</p>
   <div style="margin-top:36px">{byline()}</div>
  </div>
  {quote_form("area-quote", details=True, heading="Check availability", level="h3")}
 </div>
</section>'''
    return 'service-areas.html', page(p, body, '/service-areas.html')


def page_contact():
    path = '/contact.html'
    title = 'Request a Cleaning Quote in Natick, MA | Contact Neat Cleaning'
    desc = 'Text (508) 202-8132 or request your Neat Cleaning quote online. Regular, deep, Airbnb, move and commercial cleaning in Natick, MA and within 25 miles.'
    trail = [('Home', '/'), ('Contact', path)]
    graph = [business_node(), webpage_node(path, title, desc, 'ContactPage'), breadcrumb_node(trail)]
    p = dict(title=title, desc=desc, schema=ld({'@context': 'https://schema.org', '@graph': graph}))
    body = f'''<section class="section ivory light-crumbs" aria-labelledby="hero-title" id="quote" style="padding-top:clamp(40px,5vw,72px)">
 <div class="wrap quote">
  <div>
   {crumbs(trail)}
   {kicker("", "Request a quote · Natick, MA")}
   <h1 id="hero-title">Request a house<br>cleaning <em>quote.</em></h1>
   <p class="lead" style="margin-top:24px">Send your details and Daiane will text you to talk through your space and confirm your quote. Text is the quickest way to reach her.</p>
   <div class="contact-lines">
    <a href="{SMS}">{icon("sms")}<small>Text · preferred</small><b>{PHONE}</b></a>
    <a href="{TEL}">{icon("phone")}<small>Prefer a call?</small><b>{PHONE}</b></a>
    <a href="mailto:{EMAIL}">{icon("mail")}<small>Email</small><b>{EMAIL}</b></a>
    <div>{icon("pin")}<small>Based in</small><b>Natick, MA · up to 25 miles</b></div>
    <div>{icon("card")}<small>Payment</small><b>Zelle · Cash · Check</b></div>
   </div>
   <!-- PREENCHER: business hours and typical reply time -->
  </div>
  {quote_form("contact-quote", details=True, heading="Tell us what you need", level="h2")}
 </div>
</section>

{steps_block(True, "", "What happens<br>after you <em>send it.</em>")}

<section class="section-tight" aria-label="Offer"><div class="wrap">{offer_block()}</div></section>'''
    return 'contact.html', page(p, body, '/contact.html', cta=False)


def page_faq():
    path = '/faq.html'
    title = 'House Cleaning FAQ: Quotes, Products & Pay | Neat Cleaning'
    desc = 'Answers about Neat Cleaning in Natick, MA: how quotes work, pricing factors, products, oven and fridge cleaning, service area, payment and text messages.'
    trail = [('Home', '/'), ('FAQ', path)]
    all_faqs = [qa for group in FAQ_GENERAL.values() for qa in group]
    graph = [business_node(), webpage_node(path, title, desc), breadcrumb_node(trail), faq_node(all_faqs)]
    p = dict(title=title, desc=desc, schema=ld({'@context': 'https://schema.org', '@graph': graph}))
    groups = ''
    toc = ''
    for i, (g, qs) in enumerate(FAQ_GENERAL.items()):
        gid = 'faq-' + g.lower().replace(' & ', '-').replace(' ', '-')
        toc += f'<a href="#{gid}">{g}</a>'
        groups += f'<div class="faq-group" id="{gid}"><h2>{g}</h2>{faq_list(qs, open_first=(i == 0))}</div>'
    body = f'''<section class="hero page-hero dark" aria-labelledby="hero-title">
 <div class="hero-copy">
  {crumbs(trail)}
  {kicker("", "Questions & answers")}
  <h1 id="hero-title">House cleaning questions,<br><em>answered.</em></h1>
  <p class="lead">How quotes work, what is included, products, payment and text messages. If your question is not here, text {PHONE}.</p>
 </div>
 <div class="hero-media">{img("contact-hero", eager=True)}</div>
</section>

<section class="section" aria-label="Frequently asked questions">
 <div class="wrap legal">
  <nav aria-label="FAQ topics">{toc}</nav>
  <div>{groups}<div style="margin-top:56px">{byline()}</div></div>
 </div>
</section>'''
    return 'faq.html', page(p, body, '/faq.html')


LEGAL_PRIVACY = [
    ('Information you provide', 'When you request a quote, we collect your name, phone number, email address, chosen service, town or ZIP code, any details you submit, and your consent to contact. Avoid sending sensitive personal information in the details field.'),
    ('How the information is used', 'We use your information to respond to your request, discuss a cleaning quote, coordinate appointments and provide customer care. Quote requests are emailed to Neat Cleaning’s designated mailbox.'),
    ('Calls, text messages and consent', 'Submitting the form requires explicit consent to calls and text messages about your request. Consent is not a condition of purchase. Message frequency varies, and message and data rates may apply. Reply STOP to opt out or HELP for help. You may also contact us by phone or email to discuss communication preferences.</p><p>This form does not request marketing consent. Any future promotional text program would require a separate opt-in. Mobile phone numbers and SMS opt-in data or consent will not be sold or shared with third parties or affiliates for their marketing or promotional purposes.'),
    ('Consent records and protection', 'The email generated by your submission includes the consent wording, the consent status, the form source and the submission time. Neat Cleaning uses these records to document the request and consent. Access should be limited to people handling customer communications.'),
    ('Service providers and disclosures', 'Website hosting and email providers process information as needed to operate the website and deliver requests. Information may also be disclosed when required by applicable law. SMS opt-in data and consent are excluded from sharing for third-party marketing.'),
    ('Technical information', 'The form endpoint temporarily uses an IP-derived identifier and a short submission interval to help prevent abuse. Hosting providers may maintain server access logs. The website does not include advertising trackers or analytics scripts. Fonts are served from this website, so no font requests are sent to third parties.'),
    ('Retention and your choices', 'We retain inquiry and consent information as needed to handle the request, maintain customer records and satisfy applicable obligations. Contact us to request access, correction or deletion of your information, subject to applicable retention requirements.'),
    ('Security', 'The form validates submissions and restricts the recipient on the server. No internet transmission or email storage can be guaranteed completely secure. Use the published HTTPS website when submitting personal information.'),
    ('Contact', f'For privacy or consent questions, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call <a href="{TEL}">{PHONE}</a>.'),
]
LEGAL_TERMS = [
    ('Website and quote requests', 'This website provides information about Neat Cleaning and lets you request a cleaning quote. Submitting the form is an inquiry, not a confirmed appointment or a payment transaction.'),
    ('Scope, pricing and appointments', 'Availability, the final cleaning scope, pricing, access instructions and timing are discussed directly before an appointment is confirmed. Special product requests or property requirements may affect the quote. Oven and refrigerator cleaning are included without a separate extra charge; discuss access and preparation when requesting your quote.'),
    ('Offer', 'A 10% OFF offer is available to discuss with Neat Cleaning. Mention it when you request your quote. Its application to your booking is confirmed directly before you agree to the service.'),
    ('Payments and changes', 'Payment methods are Zelle, cash and check. Contact Neat Cleaning directly to discuss payment arrangements, scheduling changes or questions about the service.'),
    ('SMS Terms', f'Program name: Neat Cleaning Customer Care Text Messages.</p><p>Description: By opting in, you may receive customer care messages about your cleaning quote, appointment coordination, confirmations, reminders and service questions. This website form does not enroll you in promotional marketing messages.</p><p>Message frequency varies. Message and data rates may apply. Consent is not a condition of purchase. You may contact us by phone or email if you prefer another way to make an inquiry.</p><p>To stop receiving text messages, reply STOP at any time. You may receive one final message confirming that you have been unsubscribed. For help, reply HELP or contact <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="{TEL}">{PHONE}</a>. Carriers are not liable for delayed or undelivered messages.</p><p>Mobile numbers, SMS opt-in data and consent are not sold or shared with third parties or affiliates for marketing or promotional purposes. See the <a href="/privacy-policy.html">Privacy Policy</a> for information about how inquiry and consent data are handled.'),
    ('Website imagery and content', 'The website uses generated illustrative images of homes and workspaces. They are not photographs of completed Neat Cleaning projects, customer properties or team members. Service information should be confirmed directly if you have a specific request.'),
    ('Contact', f'For questions about these terms, contact Neat Cleaning at <a href="mailto:{EMAIL}">{EMAIL}</a> or <a href="{TEL}">{PHONE}</a>.'),
]


def page_legal(fname, h1, title, desc, sections):
    path = '/' + fname
    trail = [('Home', '/'), (h1, path)]
    graph = [business_node(), webpage_node(path, title, desc), breadcrumb_node(trail)]
    p = dict(title=title, desc=desc, schema=ld({'@context': 'https://schema.org', '@graph': graph}))
    toc, secs = '', ''
    for i, (h, t) in enumerate(sections):
        sid = f's{i + 1}'
        toc += f'<a href="#{sid}">{h}</a>'
        secs += f'<h2 id="{sid}">{h}</h2><p>{t}</p>'
    body = f'''<section class="section-tight ivory light-crumbs" aria-labelledby="hero-title">
 <div class="wrap">
  {crumbs(trail)}
  <h1 id="hero-title">{h1}</h1>
  <p style="margin-top:18px;color:var(--muted)">Neat Cleaning · Last updated <time datetime="{UPDATED_ISO}">October 6, 2026</time></p>
 </div>
</section>
<section class="section" aria-label="{h1}">
 <div class="wrap legal"><nav aria-label="Sections">{toc}</nav><div class="prose">{secs}</div></div>
</section>'''
    return fname, page(p, body, path)


def page_center(fname, title, desc, kick, h1, text, actions, noindex=True):
    p = dict(title=title, desc=desc, noindex=noindex)
    body = f'''<section class="center-hero dark" aria-labelledby="hero-title">
 <div class="wrap inner">
  <img src="/assets/images/logo-gold.png" width="350" height="338" alt="" loading="eager">
  {kicker("", kick)}
  <h1 id="hero-title">{h1}</h1>
  <p class="lead" style="margin:22px auto 0">{text}</p>
  <div class="actions">{actions}</div>
 </div>
</section>'''
    return fname, page(p, body, '')


def build():
    pages = [page_home(), page_services(), page_about(), page_area(), page_contact(), page_faq()]
    pages += [page_service(s['slug']) for s in SERVICES]
    pages.append(page_legal('privacy-policy.html', 'Privacy Policy', 'Privacy Policy | Neat Cleaning', 'How Neat Cleaning in Natick, MA handles quote information, contact details, text message consent, consent records and privacy requests.', LEGAL_PRIVACY))
    pages.append(page_legal('terms-of-use.html', 'Terms of Use', 'Terms of Use & SMS Terms | Neat Cleaning', 'Neat Cleaning website terms, quote and booking information, customer care SMS terms, STOP and HELP instructions and contact details.', LEGAL_TERMS))
    pages.append(page_center('thank-you.html', 'Thank You | Neat Cleaning', 'Your quote request has been sent to Neat Cleaning.', 'Your request is on its way',
                             'Thank you. We’ll be <em>in touch.</em>', 'Your cleaning quote request was sent successfully. Daiane will contact you to discuss your space and the next step. Want to add something? Send a text.',
                             btn(SMS, 'Send a follow-up text', 'gold', 'sms') + btn('/', 'Back to home', 'ghost')))
    pages.append(page_center('404.html', 'Page Not Found | Neat Cleaning', 'This page could not be found. Explore Neat Cleaning services in Natick, MA.', 'Page not found',
                             'Let’s find your <em>way home.</em>', 'This page could not be found. Explore the cleaning services or get in touch about your request.',
                             btn('/services.html', 'See the services', 'gold') + btn('/', 'Back to home', 'ghost')))
    for name, markup in pages:
        (OUT / name).write_text(markup, encoding='utf-8')
        print('wrote', name, len(markup))


if __name__ == '__main__':
    build()
