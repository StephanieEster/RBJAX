import { SITE, NAV, MESSAGES, smsHref, telHref, waHref, mailHref } from '../config.mjs';
import { esc, icon, jsonLd } from './html.mjs';

export const ORG_ID = () => `${SITE.url}/#organization`;
export const WEBSITE_ID = () => `${SITE.url}/#website`;

/** The business entity, repeated on every page with the same @id. No street address (client request). */
export function organizationNode() {
  return {
    '@type': 'HVACBusiness',
    '@id': ORG_ID(),
    name: SITE.name,
    alternateName: SITE.legalishName,
    url: `${SITE.url}/`,
    logo: { '@type': 'ImageObject', url: `${SITE.url}/assets/brand/logo-full.png`, width: 600, height: 434 },
    image: `${SITE.url}/assets/brand/og-image.jpg`,
    description:
      'Family-owned HVAC company based in Kearny, New Jersey, providing emergency heating and cooling service and HVAC system replacement since 2017.',
    telephone: SITE.phoneSchema,
    email: SITE.email,
    foundingDate: SITE.founded,
    address: { '@type': 'PostalAddress', addressLocality: SITE.city, addressRegion: SITE.state, addressCountry: 'US' },
    areaServed: {
      '@type': 'City',
      name: 'Kearny',
      containedInPlace: { '@type': 'State', name: 'New Jersey' },
    },
    knowsAbout: ['Emergency HVAC service', 'HVAC system replacement', 'Heating systems', 'Air conditioning systems'],
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: SITE.phoneSchema,
      email: SITE.email,
      contactType: 'customer service',
      areaServed: 'US',
      availableLanguage: ['English'],
    },
    sameAs: [SITE.instagram, SITE.facebook],
  };
}

export function breadcrumbNode(trail) {
  return {
    '@type': 'BreadcrumbList',
    '@id': `${SITE.url}${trail.at(-1).href === '/' ? '' : trail.at(-1).href}#breadcrumb`,
    itemListElement: trail.map((t, i) => ({
      '@type': 'ListItem',
      position: i + 1,
      name: t.label,
      item: `${SITE.url}${t.href === '/' ? '/' : t.href}`,
    })),
  };
}

function header(path) {
  const links = NAV.map(
    (n) =>
      `<li><a href="${n.href}"${path === n.href ? ' aria-current="page"' : ''}>${n.label}</a></li>`
  ).join('');
  return `<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="${esc(SITE.legalishName)} — home">
      <img class="brand-mark" src="/assets/brand/logo-emblem-200.webp" srcset="/assets/brand/logo-emblem-200.webp 200w, /assets/brand/logo-emblem-400.webp 400w" sizes="84px" width="200" height="104" alt="">
      <span class="brand-word" aria-hidden="true">
        <span class="brand-name">Mountain Weather</span>
        <span class="brand-sub"><span class="t-cool">Cooling</span> &amp; <span class="t-heat">Heating</span></span>
      </span>
    </a>
    <nav class="primary-nav" aria-label="Main">
      <ul>${links}</ul>
    </nav>
    <div class="header-actions">
      <a class="header-phone" href="${telHref()}" data-cta="call">${icon('phone', { size: 18 })}<span>${SITE.phoneDisplay}</span></a>
      <a class="btn btn--warm btn--sm header-text" href="${esc(smsHref(MESSAGES.general))}" data-cta="sms">${icon('message-square-text', { size: 18 })}<span>Text Us</span></a>
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mobile-menu" data-menu-toggle>
        <span class="menu-toggle-bars" aria-hidden="true"><span></span><span></span></span>
        <span class="sr-only">Open menu</span>
      </button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" data-menu hidden>
  <nav aria-label="Mobile">
    <ul class="mobile-menu-links">
      <li><a href="/"${path === '/' ? ' aria-current="page"' : ''}>Home</a></li>
      ${NAV.map((n) => `<li><a href="${n.href}"${path === n.href ? ' aria-current="page"' : ''}>${n.label}${icon('arrow-right', { size: 22 })}</a></li>`).join('')}
    </ul>
  </nav>
  <div class="mobile-menu-cta">
    <a class="btn btn--warm btn--block" href="${esc(smsHref(MESSAGES.general))}" data-cta="sms">${icon('message-square-text')}<span>Text ${SITE.phoneDisplay}</span></a>
    <a class="btn btn--navy btn--block" href="${telHref()}" data-cta="call">${icon('phone')}<span>Call Now</span></a>
    <a class="btn btn--ghost btn--block" href="${esc(waHref(MESSAGES.general))}" target="_blank" rel="noopener noreferrer" data-cta="whatsapp">${icon('whatsapp')}<span>WhatsApp</span></a>
  </div>
  <p class="mobile-menu-note">Family-owned HVAC company · Kearny, NJ · Since 2017</p>
</div>`;
}

function footer() {
  const year = new Date(SITE.updated).getFullYear();
  return `<footer class="site-footer">
  <div class="temp-rule" aria-hidden="true"></div>
  <div class="container footer-grid">
    <div class="footer-brand">
      <a class="footer-logo" href="/" aria-label="${esc(SITE.legalishName)} — home">
        <img src="/assets/brand/logo-full-320.webp" srcset="/assets/brand/logo-full-320.webp 320w, /assets/brand/logo-full-640.webp 640w" sizes="200px" width="320" height="232" alt="${esc(SITE.legalishName)} logo" loading="lazy" decoding="async">
      </a>
      <p>A family-owned HVAC company based in Kearny, New Jersey. Emergency heating and cooling service and HVAC replacement, since 2017.</p>
      <ul class="social" aria-label="Social media">
        <li><a href="${SITE.instagram}" target="_blank" rel="noopener noreferrer">${icon('instagram')}<span class="sr-only">Mountain Weather on Instagram (opens in a new tab)</span></a></li>
        <li><a href="${SITE.facebook}" target="_blank" rel="noopener noreferrer">${icon('facebook')}<span class="sr-only">Mountain Weather on Facebook (opens in a new tab)</span></a></li>
      </ul>
    </div>
    <nav class="footer-col" aria-label="Services">
      <h2 class="footer-title">Services</h2>
      <ul>
        <li><a href="/emergency-hvac-services">Emergency HVAC Services</a></li>
        <li><a href="/hvac-replacement">HVAC Replacement</a></li>
      </ul>
    </nav>
    <nav class="footer-col" aria-label="Company">
      <h2 class="footer-title">Company</h2>
      <ul>
        <li><a href="/about">Our Story</a></li>
        <li><a href="/service-areas">Service Area</a></li>
        <li><a href="/contact">Contact</a></li>
        <li><a href="/privacy-policy">Privacy Policy</a></li>
      </ul>
    </nav>
    <div class="footer-col">
      <h2 class="footer-title">Get in touch</h2>
      <ul class="footer-contact">
        <li><a href="${esc(smsHref(MESSAGES.general))}">${icon('message-square-text', { size: 18 })}<span>Text ${SITE.phoneDisplay}</span></a></li>
        <li><a href="${telHref()}">${icon('phone', { size: 18 })}<span>Call ${SITE.phoneDisplay}</span></a></li>
        <li><a href="${esc(waHref(MESSAGES.general))}" target="_blank" rel="noopener noreferrer">${icon('whatsapp', { size: 18 })}<span>WhatsApp</span><span class="sr-only"> (opens in a new tab)</span></a></li>
        <li><a href="${mailHref('Question for Mountain Weather')}">${icon('mail', { size: 18 })}<span>${SITE.email}</span></a></li>
        <li class="footer-place">${icon('map-pin', { size: 18 })}<span>Based in Kearny, New Jersey</span></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; ${year} ${esc(SITE.legalishName)}. All rights reserved.</p>
    ${SITE.license.number ? `<p>${esc(SITE.license.masterName)} · Master HVACR Contractor Lic. # ${esc(SITE.license.number)}</p>` : ''}
    <p>Photography on this site is licensed stock imagery used for illustration.</p>
    <p><a href="/privacy-policy">Privacy Policy</a></p>
  </div>
</footer>
<nav class="mobile-cta" aria-label="Quick contact">
  <a href="${esc(smsHref(MESSAGES.general))}" class="mobile-cta-primary" data-cta="sms">${icon('message-square-text')}<span>Text</span></a>
  <a href="${telHref()}" data-cta="call">${icon('phone')}<span>Call</span></a>
  <a href="${esc(waHref(MESSAGES.general))}" target="_blank" rel="noopener noreferrer" data-cta="whatsapp">${icon('whatsapp')}<span>WhatsApp</span><span class="sr-only"> (opens in a new tab)</span></a>
</nav>`;
}

/**
 * Full HTML document.
 * page: { path, title, description, body, schema: [], preload: '', noindex, ogType }
 */
export function renderPage(page, assets) {
  const canonical = `${SITE.url}${page.path === '/' ? '/' : page.path}`;
  const graph = [organizationNode(), ...(page.schema ?? [])];
  return `<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>document.documentElement.classList.add('js')</script>
<title>${esc(page.title)}</title>
<meta name="description" content="${esc(page.description)}">
${page.noindex ? '<meta name="robots" content="noindex, follow">' : `<link rel="canonical" href="${canonical}">`}
<meta name="theme-color" content="#0b2433">
<meta property="og:type" content="${page.ogType ?? 'website'}">
<meta property="og:locale" content="${SITE.locale}">
<meta property="og:site_name" content="${esc(SITE.legalishName)}">
<meta property="og:title" content="${esc(page.ogTitle ?? page.title)}">
<meta property="og:description" content="${esc(page.description)}">
<meta property="og:url" content="${canonical}">
<meta property="og:image" content="${SITE.url}/assets/brand/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Mountain Weather Cooling &amp; Heating logo beside an HVAC technician at an outdoor condenser">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/archivo-display.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/figtree-latin.woff2" as="font" type="font/woff2" crossorigin>
${page.preload ?? ''}
<link rel="stylesheet" href="${assets.css}">
<script src="${assets.js}" defer></script>
${jsonLd(graph)}
</head>
<body class="${page.bodyClass ?? ''}">
${header(page.path)}
<main id="main" tabindex="-1">
${page.body}
</main>
${footer()}
</body>
</html>
`;
}
