import { SITE, MESSAGES, smsHref } from '../config.mjs';
import { esc, icon, btnText, btnCall, btnWhatsApp, plain } from './html.mjs';

/* ------------------------------------------------------------------ */
/* Brand gauge — the arch from the logo, rebuilt as SVG.               */
/* ------------------------------------------------------------------ */

const CX = 240;
const CY = 285;
const R_OUT = 190;
const R_IN = 156;
const R_MID = (R_OUT + R_IN) / 2;
const pt = (deg, r) => {
  const a = (deg * Math.PI) / 180;
  return [+(CX + r * Math.cos(a)).toFixed(2), +(CY - r * Math.sin(a)).toFixed(2)];
};
const arc = (a1, a2, r) => {
  const [x1, y1] = pt(a1, r);
  const [x2, y2] = pt(a2, r);
  return `M${x1} ${y1}A${r} ${r} 0 0 1 ${x2} ${y2}`;
};

const SEGMENTS = [
  { from: 180, to: 136.6, c1: '#275db6', c2: '#348bd2' },
  { from: 133.4, to: 91.6, c1: '#348bd2', c2: '#45b0e7' },
  { from: 88.4, to: 46.6, c1: '#ffbb13', c2: '#f98f08' },
  { from: 43.4, to: 0, c1: '#f46e00', c2: '#ee3534' },
];

function spike(deg, len, half = 6) {
  const a = (deg * Math.PI) / 180;
  const px = Math.sin(a) * half;
  const py = Math.cos(a) * half;
  const [bx, by] = pt(deg, R_OUT - 4);
  const [tx, ty] = pt(deg, R_OUT + len);
  return `${(bx + px).toFixed(1)},${(by + py).toFixed(1)} ${tx},${ty} ${(bx - px).toFixed(1)},${(by - py).toFixed(1)}`;
}

/**
 * @param {object} o
 * @param {string} o.id       unique prefix for gradient ids
 * @param {boolean} o.needle  thermostat needle + ticks (interactive dial)
 * @param {number} o.height   viewBox height (hero uses a taller box for the photo window)
 */
export function gauge({ id, needle = false, height = 300, cls = '' }) {
  const grads = SEGMENTS.map((s, i) => {
    const [x1, y1] = pt(s.from, R_MID);
    const [x2, y2] = pt(s.to, R_MID);
    return `<linearGradient id="${id}-g${i}" gradientUnits="userSpaceOnUse" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}"><stop offset="0" stop-color="${s.c1}"/><stop offset="1" stop-color="${s.c2}"/></linearGradient>`;
  }).join('');
  const [ox1, oy1] = pt(180, R_OUT);
  const [ox2, oy2] = pt(0, R_OUT);
  const [ix2, iy2] = pt(0, R_IN);
  const [ix1, iy1] = pt(180, R_IN);
  const ring = `M${ox1} ${oy1}A${R_OUT} ${R_OUT} 0 0 1 ${ox2} ${oy2}L${ix2} ${iy2}A${R_IN} ${R_IN} 0 0 0 ${ix1} ${iy1}Z`;
  const segs = SEGMENTS.map(
    (s, i) =>
      `<path class="gauge-seg" style="--i:${i}" d="${arc(s.from, s.to, R_MID)}" stroke="url(#${id}-g${i})" stroke-width="${R_OUT - R_IN - 10}" fill="none" pathLength="1"/>`
  ).join('');

  let ticks = '';
  let needleSvg = '';
  if (needle) {
    for (let d = 6; d < 180; d += 6) {
      const major = d % 30 === 0;
      const [x1, y1] = pt(d, R_IN - 14);
      const [x2, y2] = pt(d, R_IN - (major ? 32 : 24));
      ticks += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" class="${major ? 'tick tick--major' : 'tick'}"/>`;
    }
    needleSvg = `<g class="dial-needle" data-needle>
      <polygon points="${CX - 7},${CY} ${CX},${CY - 128} ${CX + 7},${CY}" fill="#0b2433"/>
      <circle cx="${CX}" cy="${CY}" r="17" fill="#0b2433"/>
      <circle cx="${CX}" cy="${CY}" r="6" fill="#c7cdcf"/>
    </g>`;
  }

  return `<svg class="gauge ${cls}" viewBox="0 0 480 ${height}" aria-hidden="true" focusable="false">
  <defs>${grads}
    <linearGradient id="${id}-silver" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#aab2b3"/><stop offset=".6" stop-color="#8b9394"/><stop offset="1" stop-color="#6c6767"/></linearGradient>
  </defs>
  <polygon points="${CX - 6},${CY - R_OUT + 6} ${CX},2 ${CX + 6},${CY - R_OUT + 6}" fill="url(#${id}-silver)"/>
  <polygon points="${spike(135, 46)}" fill="url(#${id}-silver)"/>
  <polygon points="${spike(45, 46)}" fill="url(#${id}-silver)"/>
  <polygon points="${CX - R_OUT + 2},${CY - 5} 4,${CY + 3} ${CX - R_OUT + 2},${CY + 5}" fill="url(#${id}-silver)"/>
  <polygon points="${CX + R_OUT - 2},${CY - 5} 476,${CY + 3} ${CX + R_OUT - 2},${CY + 5}" fill="url(#${id}-silver)"/>
  <path d="${ring}" fill="url(#${id}-silver)"/>
  ${segs}
  ${ticks}
  ${needleSvg}
</svg>`;
}

/* ------------------------------------------------------------------ */

export function breadcrumbs(trail) {
  return `<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>${trail
    .map((t, i) =>
      i === trail.length - 1
        ? `<li><span aria-current="page">${t.label}</span></li>`
        : `<li><a href="${t.href}">${t.label}</a></li>`
    )
    .join('')}</ol></nav>`;
}

/** Inner-page hero. */
export function pageHero({ trail, eyebrow, title, lead, image, actions, tone = 'cool' }) {
  return `<section class="page-hero page-hero--${tone}">
  <div class="container page-hero-grid">
    <div class="page-hero-copy">
      ${breadcrumbs(trail)}
      ${eyebrow ? `<p class="eyebrow">${eyebrow}</p>` : ''}
      <h1>${title}</h1>
      <p class="lead">${lead}</p>
      ${actions ? `<div class="actions">${actions}</div>` : ''}
    </div>
    <div class="page-hero-media reveal">${image}</div>
  </div>
</section>`;
}

/** The definitional sentence: one plain statement right after the hero. */
export function definition(html) {
  return `<section class="definition" aria-label="Summary"><div class="container"><p><strong>${html}</strong></p></div></section>`;
}

/** Accessible FAQ built on <details>; JS adds a height animation. Returns { html, schema }. */
export function faq({ id = 'faq', title, intro, items, aside = '' }) {
  const html = `<section class="section faq" id="${id}" aria-labelledby="${id}-title">
  <div class="container faq-grid">
    <div class="faq-head">
      <p class="eyebrow">Questions &amp; answers</p>
      <h2 id="${id}-title">${title}</h2>
      ${intro ? `<p>${intro}</p>` : ''}
      ${aside}
    </div>
    <div class="faq-list">
      ${items
        .map(
          (q) => `<details class="faq-item">
        <summary><h3>${q.q}</h3><span class="faq-icon" aria-hidden="true"></span></summary>
        <div class="faq-answer"><p>${q.a}</p></div>
      </details>`
        )
        .join('\n      ')}
    </div>
  </div>
</section>`;
  const schema = {
    '@type': 'FAQPage',
    mainEntity: items.map((q) => ({
      '@type': 'Question',
      name: plain(q.q),
      acceptedAnswer: { '@type': 'Answer', text: plain(q.a) },
    })),
  };
  return { html, schema };
}

export function steps(list) {
  return `<ol class="steps">${list
    .map(
      (s, i) => `<li class="step reveal" style="--d:${i}">
      <span class="step-num" aria-hidden="true">${String(i + 1).padStart(2, '0')}</span>
      <h3>${s.title}</h3>
      <p>${s.text}</p>
    </li>`
    )
    .join('')}</ol>`;
}

/** Closing conversion band used on every page. */
export function finalCta({
  title = 'Heat out? AC down? Let’s get it handled.',
  text = 'Send us a text with what’s going on — a quick description or a photo of the equipment helps. Prefer to talk? Call or message us on WhatsApp.',
  message = MESSAGES.general,
} = {}) {
  return `<section class="final-cta" aria-labelledby="final-cta-title">
  <div class="final-cta-glow" aria-hidden="true"></div>
  <div class="container final-cta-inner">
    <div>
      <p class="eyebrow eyebrow--light">Mountain Weather · Kearny, NJ</p>
      <h2 id="final-cta-title">${title}</h2>
      <p>${text}</p>
    </div>
    <div class="final-cta-actions">
      ${btnText(`Text ${SITE.phoneDisplay}`, message, { variant: 'warm', cls: 'btn--lg' })}
      ${btnCall('Call Now', { variant: 'light', cls: 'btn--lg' })}
      ${btnWhatsApp('Message on WhatsApp', message, { variant: 'outline-light', cls: 'btn--lg' })}
      <p class="final-cta-note">${icon('mail', { size: 16 })} Prefer email? <a href="mailto:${SITE.email}">${SITE.email}</a></p>
    </div>
  </div>
</section>`;
}

/** Cooling vs. heating symptom explorer with the thermostat dial. Signature element. */
export function climateDial({ headingLevel = 2 } = {}) {
  const H = `h${headingLevel}`;
  const panel = (kind, items, msg) => `<div class="dial-panel" id="dial-${kind}" role="tabpanel" aria-labelledby="dial-tab-${kind}" data-panel="${kind}">
      <ul class="symptoms">${items.map((s) => `<li>${icon(kind === 'cooling' ? 'snowflake' : 'flame', { size: 18 })}<span>${s}</span></li>`).join('')}</ul>
      <div class="dial-panel-cta">
        <a class="btn btn--${kind === 'cooling' ? 'cool' : 'warm'}" href="${esc(smsHref(msg))}" data-cta="sms">${icon('message-square-text')}<span>Text us about your ${kind === 'cooling' ? 'AC' : 'heat'}</span></a>
        <a class="link-arrow" href="/emergency-hvac-services">Emergency service details ${icon('arrow-right', { size: 18 })}</a>
      </div>
    </div>`;
  return `<section class="section dial-section" aria-labelledby="dial-title" data-dial data-mode="neutral">
  <div class="dial-bg" aria-hidden="true"></div>
  <div class="container dial-grid">
    <div class="dial-visual">
      ${gauge({ id: 'dial', needle: true })}
      <p class="dial-readout" aria-hidden="true"><span class="dial-readout-cool">Cooling</span><span class="dial-readout-heat">Heating</span></p>
    </div>
    <div class="dial-copy">
      <p class="eyebrow">Too hot or too cold?</p>
      <${H} id="dial-title">Tell us which way your system is failing.</${H}>
      <p class="dial-intro">These are some of the most common signs that a heating or cooling system needs professional attention. If one sounds familiar, send us a quick text describing it.</p>
      <div class="dial-tabs" role="tablist" aria-label="Choose a problem type">
        <button type="button" role="tab" id="dial-tab-cooling" aria-controls="dial-cooling" aria-selected="false" data-tab="cooling">${icon('snowflake', { size: 18 })}<span>Cooling<span class="tab-extra"> problem</span></span></button>
        <button type="button" role="tab" id="dial-tab-heating" aria-controls="dial-heating" aria-selected="false" data-tab="heating">${icon('flame', { size: 18 })}<span>Heating<span class="tab-extra"> problem</span></span></button>
      </div>
      ${panel(
        'cooling',
        [
          'The AC runs, but the air from the vents isn’t cold',
          'The outdoor unit won’t turn on, or hums without starting',
          'Ice is forming on the refrigerant lines or indoor coil',
          'Water is leaking around the indoor unit',
          'The breaker trips when the system starts',
        ],
        MESSAGES.cooling
      )}
      ${panel(
        'heating',
        [
          'The furnace or boiler won’t start when the thermostat calls for heat',
          'The vents are blowing cool air in heating mode',
          'The system turns on and off in short, frequent cycles',
          'You hear banging, grinding or squealing from the equipment',
          'Some rooms stay cold no matter how high you set it',
        ],
        MESSAGES.heating
      )}
      <p class="safety-note">${icon('circle-alert', { size: 18 })}<span><strong>Smell gas?</strong> Leave the building right away and call 911 or your gas utility from outside. Don’t switch lights or equipment on or off.</span></p>
    </div>
  </div>
</section>`;
}

/** Thin brand gradient divider. */
export const tempRule = () => `<div class="temp-rule" aria-hidden="true"></div>`;
