import { SITE, MESSAGES, smsHref, telHref, waHref, mailHref } from '../config.mjs';
import { esc, icon } from '../lib/html.mjs';
import { breadcrumbs } from '../lib/sections.mjs';
import { ORG_ID, breadcrumbNode } from '../lib/layout.mjs';

const PATH = '/contact';
const TRAIL = [
  { href: '/', label: 'Home' },
  { href: PATH, label: 'Contact' },
];

export default {
  path: PATH,
  title: 'Contact Mountain Weather | HVAC in Kearny, NJ',
  description:
    'Text, call or WhatsApp Mountain Weather at (862) 270-8862, or email mountainweather63@gmail.com. Family-owned HVAC company based in Kearny, NJ.',
  render() {
    const body = `
<section class="contact-hero" aria-labelledby="contact-title">
  <div class="hero-contours" aria-hidden="true"></div>
  <div class="container">
    ${breadcrumbs(TRAIL)}
    <p class="eyebrow">${icon('message-square-text', { size: 16 })} We’re a text away</p>
    <h1 id="contact-title">Contact Mountain Weather</h1>
    <p class="lead">The quickest way to reach us is a text to <a href="${esc(smsHref(MESSAGES.general))}">${SITE.phoneDisplay}</a>. Tell us what’s going on — heating, cooling or a replacement question — and include a photo of the equipment if you can.</p>
  </div>
</section>

<section class="section contact-section" aria-label="Contact options">
  <div class="container contact-grid">
    <ul class="contact-cards">
      <li><a class="contact-card contact-card--primary" href="${esc(smsHref(MESSAGES.general))}" data-cta="sms">
        <span class="contact-card-icon">${icon('message-square-text', { size: 26 })}</span>
        <span class="contact-card-text"><strong>Text us</strong><span>${SITE.phoneDisplay}</span><small>Fastest — send photos too</small></span>
        ${icon('arrow-right', { size: 20, cls: 'contact-card-arrow' })}
      </a></li>
      <li><a class="contact-card" href="${telHref()}" data-cta="call">
        <span class="contact-card-icon">${icon('phone', { size: 26 })}</span>
        <span class="contact-card-text"><strong>Call us</strong><span>${SITE.phoneDisplay}</span><small>Talk it through directly</small></span>
        ${icon('arrow-right', { size: 20, cls: 'contact-card-arrow' })}
      </a></li>
      <li><a class="contact-card" href="${esc(waHref(MESSAGES.general))}" target="_blank" rel="noopener noreferrer" data-cta="whatsapp">
        <span class="contact-card-icon contact-card-icon--wa">${icon('whatsapp', { size: 26 })}</span>
        <span class="contact-card-text"><strong>WhatsApp</strong><span>${SITE.phoneDisplay}</span><small>Opens WhatsApp in a new tab</small></span>
        ${icon('arrow-up-right', { size: 20, cls: 'contact-card-arrow' })}
      </a></li>
      <li><a class="contact-card" href="${mailHref('Question for Mountain Weather')}" data-cta="email">
        <span class="contact-card-icon">${icon('mail', { size: 26 })}</span>
        <span class="contact-card-text"><strong>Email</strong><span class="break">${SITE.email}</span><small>For non-urgent questions</small></span>
        ${icon('arrow-right', { size: 20, cls: 'contact-card-arrow' })}
      </a></li>
    </ul>

    <div class="composer-wrap">
      <form class="composer" data-composer novalidate hidden aria-labelledby="composer-title" aria-describedby="composer-desc">
        <h2 id="composer-title">Write your message here</h2>
        <p id="composer-desc" class="composer-desc">Fill this in and we’ll open it in your texting app, WhatsApp or email — ready for you to review and send. Nothing is sent or stored by this website.</p>
        <div class="composer-errors" role="alert" data-errors hidden></div>
        <div class="field">
          <label for="c-topic">What do you need help with? <span class="req" aria-hidden="true">*</span></label>
          <select id="c-topic" name="topic" required aria-describedby="c-topic-err">
            <option value="">Choose one</option>
            <option>Emergency — no heat</option>
            <option>Emergency — no cooling</option>
            <option>HVAC replacement</option>
            <option>Other question</option>
          </select>
          <p class="field-error" id="c-topic-err" hidden>Please choose what you need help with.</p>
        </div>
        <div class="field-row">
          <div class="field">
            <label for="c-name">Your name <span class="opt">(optional)</span></label>
            <input id="c-name" name="name" type="text" autocomplete="name" maxlength="80">
          </div>
          <div class="field">
            <label for="c-town">Town or ZIP code <span class="opt">(optional)</span></label>
            <input id="c-town" name="town" type="text" autocomplete="postal-code" maxlength="60">
          </div>
        </div>
        <div class="field">
          <label for="c-msg">What’s happening? <span class="req" aria-hidden="true">*</span></label>
          <textarea id="c-msg" name="message" rows="5" required minlength="10" maxlength="1000" aria-describedby="c-msg-hint c-msg-err"></textarea>
          <p class="field-hint" id="c-msg-hint">For example: “Heat won’t turn on, thermostat shows 58°. Started this morning.”</p>
          <p class="field-error" id="c-msg-err" hidden>Please describe the problem in a few words (at least 10 characters).</p>
        </div>
        <div class="composer-actions">
          <button class="btn btn--warm" type="submit" value="sms">${icon('message-square-text')}<span>Open in Text Messages</span></button>
          <button class="btn btn--navy" type="submit" value="whatsapp">${icon('whatsapp')}<span>Open in WhatsApp</span></button>
          <button class="btn btn--ghost" type="submit" value="email">${icon('mail')}<span>Open in Email</span></button>
        </div>
        <p class="composer-status" role="status" data-status></p>
      </form>
      <noscript><p class="composer-desc">Use any of the contact options to reach us directly.</p></noscript>

      <aside class="contact-aside">
        <h2>Good to know</h2>
        <ul>
          <li>${icon('map-pin', { size: 20 })}<span>Based in <strong>Kearny, New Jersey</strong>. Outside Kearny? Include your town or ZIP and we’ll confirm whether we can help.</span></li>
          <li>${icon('circle-alert', { size: 20 })}<span><strong>Smell gas or hear a CO alarm?</strong> Leave the building and call 911 or your gas utility first.</span></li>
          <li>${icon('instagram', { size: 20 })}<span>Follow us on <a href="${SITE.instagram}" target="_blank" rel="noopener noreferrer">Instagram<span class="sr-only"> (opens in a new tab)</span></a> and <a href="${SITE.facebook}" target="_blank" rel="noopener noreferrer">Facebook<span class="sr-only"> (opens in a new tab)</span></a>.</span></li>
        </ul>
        <p class="contact-aside-links">Looking for something specific? <a href="/emergency-hvac-services">Emergency service</a> · <a href="/hvac-replacement">Replacement</a> · <a href="/about">Our story</a></p>
      </aside>
    </div>
  </div>
</section>
`;

    const schema = [
      {
        '@type': 'ContactPage',
        '@id': `${SITE.url}${PATH}#webpage`,
        url: `${SITE.url}${PATH}`,
        name: this.title,
        description: this.description,
        breadcrumb: { '@id': `${SITE.url}${PATH}#breadcrumb` },
        about: { '@id': ORG_ID() },
        dateModified: SITE.updated,
        inLanguage: 'en-US',
      },
      breadcrumbNode(TRAIL),
    ];
    return { body, schema };
  },
};
