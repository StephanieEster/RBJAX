import { SITE, MESSAGES } from '../config.mjs';
import { icon, pic, imagePreload, btnText, btnCall } from '../lib/html.mjs';
import { pageHero, definition, faq, finalCta } from '../lib/sections.mjs';
import { ORG_ID, breadcrumbNode } from '../lib/layout.mjs';

const PATH = '/service-areas';
const TRAIL = [
  { href: '/', label: 'Home' },
  { href: PATH, label: 'Service Area' },
];
const HERO_SIZES = '(min-width: 1000px) 460px, 92vw';
const ZIP_MSG = 'Hi Mountain Weather, can you service my area? My town/ZIP is:';

const FAQ_ITEMS = [
  {
    q: 'Do you serve all of New Jersey?',
    a: 'No. Mountain Weather is a family-owned company based in Kearny, in Hudson County, and that’s where our focus is. We’d rather tell you upfront than overpromise coverage. If you’re nearby, text us your town or ZIP code and we’ll let you know whether we can help.',
  },
  {
    q: 'How do I check whether you can service my address?',
    a: 'Send a text to (862) 270-8862 with your town or ZIP code and a quick note about what you need — emergency service or a replacement. You can also call, message us on WhatsApp or email mountainweather63@gmail.com. Asking is free, and we’ll give you a straight answer.',
  },
  {
    q: 'Do you have an office I can visit?',
    a: 'We don’t list a public office address on our website. HVAC work happens at your home or property, so the best way to reach us is by text, phone, WhatsApp or email. Our number is (862) 270-8862, and we’re based in Kearny, New Jersey.',
  },
  {
    q: 'Which services are available in Kearny?',
    a: 'In Kearny we provide our two core services: emergency heating and cooling service when a system stops working, and HVAC system replacement when older equipment is ready to retire. If you have a different HVAC question, text us and we’ll let you know whether it’s something we handle.',
  },
];

export default {
  path: PATH,
  title: 'HVAC Service in Kearny, NJ | Service Area | Mountain Weather',
  description:
    'Mountain Weather is a family-owned HVAC company based in Kearny, NJ, in Hudson County. Emergency heating & cooling service and HVAC replacement. Text (862) 270-8862.',
  render() {
    const faqBlock = faq({ title: 'Service area questions', items: FAQ_ITEMS });

    const body = `
${pageHero({
  trail: TRAIL,
  tone: 'cool',
  eyebrow: `${icon('map-pin', { size: 16 })} Hudson County, New Jersey`,
  title: 'HVAC Service Area: Kearny, New Jersey',
  lead: 'We’re based in Kearny — and that’s where our focus is. Here’s what to know about our local heating and cooling service, and how to quickly check whether we can reach your address.',
  actions: `${btnText('Text Us Your ZIP Code', ZIP_MSG, { variant: 'warm', cls: 'btn--lg' })}${btnCall('Call Now', { variant: 'navy', cls: 'btn--lg' })}`,
  image: pic('victorian-home', {
    alt: 'Traditional multi-story home with a turret and a brick neighbor on a residential street',
    sizes: HERO_SIZES,
    eager: true,
    position: '45% 50%',
  }),
})}

${definition(
  'Mountain Weather provides emergency HVAC service and HVAC system replacement from its base in Kearny, a town in Hudson County, New Jersey, serving local customers since 2017.'
)}

<section class="section" aria-labelledby="local-title">
  <div class="container local-grid">
    <div>
      <p class="eyebrow">Why local matters</p>
      <h2 id="local-title">Heating and cooling for a two-season climate</h2>
      <p>Kearny sits between the Passaic and Hackensack rivers in northern New Jersey, where cold winters and humid summers mean both heating and cooling systems put in serious hours. A system that limps through one season often shows it in the next.</p>
      <p>Local homes range from older houses to newer construction, and the equipment inside them varies just as much. Being based in town means we know the kinds of systems and conditions you’re likely dealing with.</p>
    </div>
    <ul class="local-facts">
      <li>${icon('map-pin', { size: 22 })}<div><strong>Based in Kearny, NJ</strong><span>Hudson County</span></div></li>
      <li>${icon('calendar-check', { size: 22 })}<div><strong>Serving customers since 2017</strong><span>Founded July 19, 2017</span></div></li>
      <li>${icon('users', { size: 22 })}<div><strong>2,000+ customers served</strong><span>Family-owned business</span></div></li>
    </ul>
  </div>
</section>

<section class="section section--tint" aria-labelledby="local-services-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow">Services in Kearny</p>
      <h2 id="local-services-title">What we provide locally</h2>
    </header>
    <div class="link-cards">
      <a class="link-card link-card--heat reveal" href="/emergency-hvac-services">
        ${icon('circle-alert', { size: 26 })}
        <h3>Emergency heating &amp; cooling repair</h3>
        <p>For a furnace, AC or heat pump that has stopped working or is running unsafely. Text or call and describe the problem.</p>
        <span class="link-arrow">See emergency service ${icon('arrow-right', { size: 18 })}</span>
      </a>
      <a class="link-card link-card--cool reveal" style="--d:1" href="/hvac-replacement">
        ${icon('sparkles', { size: 26 })}
        <h3>Replacing an aging HVAC system</h3>
        <p>For equipment that’s older, unreliable or no longer keeping you comfortable. Learn the signs and how replacement works.</p>
        <span class="link-arrow">Explore replacement ${icon('arrow-right', { size: 18 })}</span>
      </a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="outside-title">
  <div class="container">
    <div class="outside-card reveal">
      <div class="outside-icon" aria-hidden="true">${icon('map-pin', { size: 34 })}</div>
      <div>
        <h2 id="outside-title">Outside Kearny? Just ask.</h2>
        <p>We only list areas we’ve confirmed, so you won’t find a long list of towns here. If you’re in a nearby community, text us your town or ZIP code — we’ll tell you straight whether we can help before anything is scheduled.</p>
      </div>
      ${btnText('Text your town or ZIP', ZIP_MSG, { variant: 'warm' })}
    </div>
  </div>
</section>

${faqBlock.html}

${finalCta({ message: MESSAGES.general })}
`;

    const schema = [
      {
        '@type': 'WebPage',
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
      faqBlock.schema,
    ];
    return { body, schema, preload: imagePreload('victorian-home', HERO_SIZES) };
  },
};
