import { SITE, MESSAGES, smsHref, telHref, waHref } from '../config.mjs';
import { esc, icon, pic, imagePreload, btnText } from '../lib/html.mjs';
import { gauge, definition, faq, steps, finalCta, climateDial } from '../lib/sections.mjs';
import { ORG_ID, WEBSITE_ID } from '../lib/layout.mjs';

const HERO_SIZES = '(min-width: 1100px) 400px, (min-width: 768px) 38vw, 72vw';

export const FAQ_ITEMS = [
  {
    q: 'When should I consider replacing my HVAC system?',
    a: 'ENERGY STAR suggests having a professional look at replacement when a heat pump or air conditioner is more than 10 years old, or a furnace or boiler is more than 15 years old. Frequent repairs, rising energy bills and rooms that stay too hot or too cold are other signs. Age alone isn’t the whole story, so we look at condition, repair history and your goals before recommending anything.',
  },
  {
    q: 'What should I do if my heating or cooling system stops working?',
    a: 'Start with the basics: confirm the thermostat is in the right mode, set to the right temperature and has working batteries, and check that the system’s breaker hasn’t tripped. Look at the air filter, too — a badly clogged filter can shut a system down. If it still won’t run, or you notice burning smells, leaks or unusual noises, turn it off and text or call us at (862) 270-8862.',
  },
  {
    q: 'How can I contact Mountain Weather?',
    a: 'The fastest way is to text (862) 270-8862 — you can include photos of the equipment along with a short description. You can also call the same number, message us on WhatsApp, or email mountainweather63@gmail.com. We’re on Instagram and Facebook as @mountainweather63, too.',
  },
  {
    q: 'What is the difference between HVAC repair and replacement?',
    a: 'A repair fixes a specific failed part — such as a capacitor, fan motor or control board — so the existing system keeps running. Replacement swaps out the major equipment, like a furnace, air conditioner or heat pump, for new units. Repair usually makes sense for a newer system with an isolated problem; replacement is worth considering when equipment is aging, failing often or no longer keeping you comfortable.',
  },
  {
    q: 'How do I know if my system needs professional attention?',
    a: 'Call a professional if you notice warm air in cooling mode, cool air in heating mode, short cycling, ice on the refrigerant lines, water around the indoor unit, a tripping breaker, or banging, grinding or squealing sounds. A sudden jump in your energy bill without a change in how you use the system is another clue. Catching problems early can help prevent a bigger breakdown.',
  },
  {
    q: 'Do you offer emergency HVAC service?',
    a: 'Yes. Emergency heating and cooling service is one of our two core services. Text or call (862) 270-8862 and describe what’s happening — a photo of the equipment helps. We’ll talk it through with you and let you know when we can help based on our current schedule.',
  },
  {
    q: 'Where is Mountain Weather based?',
    a: 'We’re a family-owned HVAC company based in Kearny, New Jersey, in Hudson County. If you’re outside Kearny and aren’t sure whether we can reach you, text us your town or ZIP code before booking anything and we’ll give you an honest answer.',
  },
  {
    q: 'How long has Mountain Weather been in business?',
    a: 'Mountain Weather was founded on July 19, 2017, and has served more than 2,000 customers since then. Before opening the company, our founder completed technical training, earned his licenses and secured insurance. Today he is dedicated full-time to Mountain Weather and the customers who count on it.',
  },
  {
    q: 'Why don’t you list prices on the website?',
    a: 'Every heating and cooling job is different — the equipment, the problem and the home all change the work involved. Rather than post generic numbers that may not fit your situation, we prefer to understand what’s going on first. Text or call (862) 270-8862 to talk through your needs.',
  },
  {
    q: 'What should I include when I text you?',
    a: 'Let us know whether the problem is with heating or cooling, what the system is doing (or not doing) and when it started. Add your town and, if you can, a photo of the equipment’s model label and your thermostat. Those details help us understand the situation before we talk.',
  },
];

export default {
  path: '/',
  title: 'HVAC Services in Kearny, NJ | Mountain Weather',
  ogTitle: 'Mountain Weather Cooling & Heating — HVAC Services in Kearny, NJ',
  description:
    'Family-owned HVAC company in Kearny, NJ since 2017. Emergency heating & cooling service and HVAC replacement. 2,000+ customers served. Text (862) 270-8862.',
  render() {
    const faqBlock = faq({
      title: 'HVAC questions we hear all the time',
      intro: 'Straight answers to the questions Kearny homeowners ask most. Don’t see yours? Text it to us.',
      items: FAQ_ITEMS,
      aside: `<a class="btn btn--navy" href="${esc(smsHref(MESSAGES.general))}" data-cta="sms">${icon('message-square-text')}<span>Text us a question</span></a>`,
    });

    const body = `
<section class="hero" aria-labelledby="hero-title">
  <div class="hero-contours" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">${icon('map-pin', { size: 16 })} Family-owned HVAC company · Kearny, NJ</p>
      <h1 id="hero-title">Emergency <span class="t-grad">HVAC</span> service &amp; system replacement in Kearny, NJ</h1>
      <p class="lead">When the heat quits in January or the AC gives out in July, you want a straight answer from people who know the equipment. Mountain Weather is a family-owned heating and cooling company that has served more than 2,000 customers since 2017.</p>
      <div class="actions">
        ${btnText('Text for Emergency Service', MESSAGES.emergency, { variant: 'warm', cls: 'btn--lg' })}
        ${btnText('Ask About a Replacement', MESSAGES.replacement, { variant: 'navy', cls: 'btn--lg' })}
      </div>
      <p class="hero-alt">Prefer to talk? <a href="${telHref()}" data-cta="call">Call ${SITE.phoneDisplay}</a> or <a href="${esc(waHref(MESSAGES.general))}" target="_blank" rel="noopener noreferrer" data-cta="whatsapp">message us on WhatsApp<span class="sr-only"> (opens in a new tab)</span></a>.</p>
      <ul class="proof-chips" aria-label="Highlights">
        <li>${icon('users', { size: 18 })}<span><strong>2,000+</strong> customers served</span></li>
        <li>${icon('house', { size: 18 })}<span>Family-owned since <strong>2017</strong></span></li>
        <li>${icon('thermometer', { size: 18 })}<span>Heating <em>&amp;</em> cooling</span></li>
      </ul>
    </div>
    <div class="hero-visual">
      ${gauge({ id: 'hero', height: 600, cls: 'gauge--hero' })}
      <div class="hero-window">
        ${pic('hvac-technician-condenser', {
          alt: 'HVAC technician servicing an outdoor air conditioning condenser beside a sided home',
          sizes: HERO_SIZES,
          eager: true,
          position: '80% 50%',
        })}
      </div>
      <div class="hero-plaque">
        <p class="hero-plaque-num">2,000+ <span>customers served</span></p>
        <p class="hero-plaque-sub"><span class="t-cool">Since 2017</span> · <span class="t-heat">Family-owned</span></p>
      </div>
    </div>
  </div>
</section>

${definition(
  'Mountain Weather is a family-owned HVAC company based in Kearny, New Jersey, providing emergency heating and cooling service and HVAC system replacement, with more than 2,000 customers served since July 2017.'
)}

<section class="trust" aria-label="Company facts">
  <div class="container">
    <ul class="trust-list">
      <li class="reveal" style="--d:0"><span class="trust-num">2017</span><span class="trust-label">Founded July 19, 2017</span></li>
      <li class="reveal" style="--d:1"><span class="trust-num">Family</span><span class="trust-label">Family-owned business</span></li>
      <li class="reveal" style="--d:2"><span class="trust-num">2,000+</span><span class="trust-label">Customers served</span></li>
      <li class="reveal" style="--d:3"><span class="trust-num">HVAC</span><span class="trust-label">Professional heating &amp; cooling service</span></li>
    </ul>
  </div>
</section>

<section class="section services" aria-labelledby="services-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow">What we do</p>
      <h2 id="services-title">HVAC help for the two moments that matter most</h2>
      <p>We focus on the situations where getting it right counts: a system that has stopped working, and a system that’s ready to be replaced.</p>
    </header>
    <div class="service-cards">
      <article class="service-card service-card--heat reveal">
        <div class="service-card-media">
          ${pic('ac-service-gauges', {
            alt: 'Technician connecting refrigerant gauges to an outdoor air conditioning unit',
            sizes: '(min-width: 1000px) 560px, 92vw',
            position: '40% 50%',
          })}
          <span class="service-tag">${icon('circle-alert', { size: 16 })} Urgent</span>
        </div>
        <div class="service-card-body">
          <p class="service-num" aria-hidden="true">01</p>
          <h3><a href="/emergency-hvac-services">Emergency HVAC Services</a></h3>
          <p>No heat, no cooling, strange noises or a system that won’t turn on? Text or call and tell us what’s happening. We’ll talk it through, let you know when we can help, and put a trained technician on the problem.</p>
          <ul class="ticks">
            <li>${icon('check', { size: 18 })} Heating breakdowns</li>
            <li>${icon('check', { size: 18 })} AC and cooling failures</li>
            <li>${icon('check', { size: 18 })} Systems that won’t start or keep shutting off</li>
          </ul>
          <div class="service-card-actions">
            ${btnText('Text for emergency service', MESSAGES.emergency, { variant: 'warm' })}
            <a class="link-arrow" href="/emergency-hvac-services">What to expect ${icon('arrow-right', { size: 18 })}<span class="sr-only"> from emergency HVAC service</span></a>
          </div>
        </div>
      </article>
      <article class="service-card service-card--cool reveal" style="--d:1">
        <div class="service-card-media">
          ${pic('refrigerant-line-service', {
            alt: 'Technician working on the refrigerant line connections of a ductless air conditioning unit',
            sizes: '(min-width: 1000px) 560px, 92vw',
            position: '50% 35%',
          })}
          <span class="service-tag service-tag--cool">${icon('sparkles', { size: 16 })} Long-term</span>
        </div>
        <div class="service-card-body">
          <p class="service-num" aria-hidden="true">02</p>
          <h3><a href="/hvac-replacement">HVAC Replacement</a></h3>
          <p>When an older system keeps breaking down or can’t keep your home comfortable, replacing it may be the smarter long-term move. We’ll explain your options in plain language so you can decide with confidence.</p>
          <ul class="ticks">
            <li>${icon('check', { size: 18 })} Aging or unreliable equipment</li>
            <li>${icon('check', { size: 18 })} Rising energy bills</li>
            <li>${icon('check', { size: 18 })} Uneven temperatures from room to room</li>
          </ul>
          <div class="service-card-actions">
            ${btnText('Ask about replacement', MESSAGES.replacement, { variant: 'cool' })}
            <a class="link-arrow" href="/hvac-replacement">How replacement works ${icon('arrow-right', { size: 18 })}</a>
          </div>
        </div>
      </article>
    </div>
  </div>
</section>

${climateDial()}

<section class="section why" aria-labelledby="why-title">
  <div class="container why-grid">
    <div class="why-media reveal">
      ${pic('heating-system-service', {
        alt: 'Technician inspecting the controls of a wall-mounted heating system',
        sizes: '(min-width: 1000px) 480px, 92vw',
        position: '35% 50%',
      })}
      <div class="why-badge"><span class="why-badge-num">Since 2017</span><span>Rooted in Kearny, NJ</span></div>
    </div>
    <div class="why-copy">
      <p class="eyebrow">Why Mountain Weather</p>
      <h2 id="why-title">A family business that earned its place one job at a time</h2>
      <ul class="why-list">
        <li class="reveal">${icon('graduation-cap', { size: 22 })}<div><h3>Trained the right way</h3><p>Our founder learned the trade from the ground up — technical courses, licensing and insurance — before opening the company in 2017.</p></div></li>
        <li class="reveal">${icon('house', { size: 22 })}<div><h3>Family-owned</h3><p>When your family’s name is on the business, every job is personal. You’re working with a local family company, not a faceless call center.</p></div></li>
        <li class="reveal">${icon('users', { size: 22 })}<div><h3>2,000+ customers served</h3><p>Years of heating and cooling work in and around Kearny have built real-world experience with the systems in local homes.</p></div></li>
        <li class="reveal">${icon('message-circle', { size: 22 })}<div><h3>Easy to reach</h3><p>Text, call or WhatsApp the same number. Clear explanations of what we find, in plain English.</p></div></li>
        <li class="reveal">${icon('heart-handshake', { size: 22 })}<div><h3>All-in commitment</h3><p>Mountain Weather isn’t a side job. Our founder chose to dedicate himself full-time to this company and the people who rely on it.</p></div></li>
        <li class="reveal">${icon('badge-check', { size: 22 })}<div><h3>Quality first</h3><p>We’d rather do it right than do it twice — careful work and honest recommendations about repair or replacement.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section story-teaser" aria-labelledby="story-title">
  <div class="container story-grid">
    <div class="story-copy">
      <p class="eyebrow eyebrow--light">Our story</p>
      <h2 id="story-title">From new arrival to business owner — one skill at a time.</h2>
      <p>Our founder came to the United States in 2015 with no experience in the local market. Instead of chasing shortcuts, he picked one trade and committed to learning it properly: technical training, the required licenses and insurance.</p>
      <p>In 2017, encouraged by a friend who worked as an accountant, he founded Mountain Weather. For years he balanced the new company with work for other HVAC businesses — until he took the leap to run Mountain Weather full-time.</p>
      <ol class="mini-timeline">
        <li><span class="mt-year">2015</span><span>Arrives in the U.S.</span></li>
        <li><span class="mt-year">2017</span><span>Founds Mountain Weather</span></li>
        <li><span class="mt-year">Today</span><span>2,000+ customers served</span></li>
      </ol>
      <a class="btn btn--light" href="/about">Read our story ${icon('arrow-right')}</a>
    </div>
    <div class="story-media reveal">
      ${pic('american-flag-home', {
        alt: 'American flag flying in front of a traditional two-story house with a wraparound porch',
        sizes: '(min-width: 1000px) 440px, 92vw',
        position: '50% 40%',
      })}
    </div>
  </div>
</section>

<section class="section how" aria-labelledby="how-title">
  <div class="container">
    <header class="section-head section-head--center">
      <p class="eyebrow">How it works</p>
      <h2 id="how-title">Getting help is simple</h2>
    </header>
    ${steps([
      {
        title: 'Contact our team',
        text: `Text, call or WhatsApp <a href="${telHref()}">${SITE.phoneDisplay}</a>. A photo of the equipment or a short description helps us understand the situation.`,
      },
      {
        title: 'Discuss your HVAC needs',
        text: 'We’ll ask a few questions about your system and what it’s doing, then explain the next steps clearly.',
      },
      {
        title: 'Get professional assistance',
        text: 'A trained technician works on your heating or cooling system and walks you through what was found and what comes next.',
      },
    ])}
  </div>
</section>

<section class="section proof" aria-labelledby="proof-title">
  <div class="container proof-grid">
    <div class="proof-figure reveal">
      <h2 id="proof-title"><span class="proof-num">2,000<span>+</span></span> customers served since 2017</h2>
      <p>Mountain Weather grew one service call at a time — from a new company balancing outside work to a full-time, family-owned HVAC business based in Kearny.</p>
    </div>
    <div class="proof-social">
      <p class="proof-social-lead">Follow along and see what we’re working on:</p>
      <a class="social-card social-card--ig reveal" href="${SITE.instagram}" target="_blank" rel="noopener noreferrer">
        ${icon('instagram', { size: 28 })}
        <span><strong>Instagram</strong><span>@mountainweather63</span></span>
        ${icon('arrow-up-right', { size: 20, cls: 'social-card-arrow' })}<span class="sr-only"> (opens in a new tab)</span>
      </a>
      <a class="social-card social-card--fb reveal" style="--d:1" href="${SITE.facebook}" target="_blank" rel="noopener noreferrer">
        ${icon('facebook', { size: 28 })}
        <span><strong>Facebook</strong><span>Mountain Weather</span></span>
        ${icon('arrow-up-right', { size: 20, cls: 'social-card-arrow' })}<span class="sr-only"> (opens in a new tab)</span>
      </a>
    </div>
  </div>
</section>

<section class="section area" aria-labelledby="area-title">
  <div class="container area-grid">
    <div class="area-media reveal">
      ${pic('victorian-home', {
        alt: 'Traditional multi-story home with a turret on a tree-lined residential street',
        sizes: '(min-width: 1000px) 560px, 92vw',
        position: '50% 45%',
      })}
      <div class="area-pin">${icon('map-pin', { size: 22 })}<span><strong>Kearny, NJ</strong>Hudson County</span></div>
    </div>
    <div class="area-copy">
      <p class="eyebrow">Service area</p>
      <h2 id="area-title">Local HVAC service, based in Kearny</h2>
      <p>Mountain Weather is based in Kearny, New Jersey. New Jersey winters push heating systems hard, and humid summers do the same to air conditioners — so a local team that knows both seasons matters.</p>
      <p>Not sure whether we can reach your address? Text us your town or ZIP code and we’ll give you an honest answer before anything is scheduled.</p>
      <div class="actions">
        ${btnText('Text us your ZIP code', 'Hi Mountain Weather, can you service my area? My town/ZIP is:', { variant: 'navy' })}
        <a class="link-arrow" href="/service-areas">More about our service area ${icon('arrow-right', { size: 18 })}</a>
      </div>
    </div>
  </div>
</section>

${faqBlock.html}

${finalCta()}
`;

    const schema = [
      {
        '@type': 'WebSite',
        '@id': WEBSITE_ID(),
        url: `${SITE.url}/`,
        name: SITE.legalishName,
        publisher: { '@id': ORG_ID() },
        inLanguage: 'en-US',
      },
      {
        '@type': 'WebPage',
        '@id': `${SITE.url}/#webpage`,
        url: `${SITE.url}/`,
        name: this.title,
        description: this.description,
        isPartOf: { '@id': WEBSITE_ID() },
        about: { '@id': ORG_ID() },
        dateModified: SITE.updated,
        inLanguage: 'en-US',
      },
      faqBlock.schema,
    ];

    return { body, schema, preload: imagePreload('hvac-technician-condenser', HERO_SIZES), bodyClass: 'page-home' };
  },
};
