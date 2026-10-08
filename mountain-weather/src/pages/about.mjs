import { SITE, MESSAGES } from '../config.mjs';
import { icon, pic, imagePreload, btnText } from '../lib/html.mjs';
import { pageHero, definition, finalCta } from '../lib/sections.mjs';
import { ORG_ID, breadcrumbNode } from '../lib/layout.mjs';

const PATH = '/about';
const TRAIL = [
  { href: '/', label: 'Home' },
  { href: PATH, label: 'Our Story' },
];
const HERO_SIZES = '(min-width: 1000px) 460px, 92vw';

const CHAPTERS = [
  {
    mark: '2015',
    title: 'A new beginning',
    text: 'Our founder arrived in the United States in 2015 with no experience in the local market and no connections in the industry. What he did have was determination. Rather than trying a little of everything, he decided to focus on one trade and learn it properly.',
  },
  {
    mark: 'The groundwork',
    title: 'Learning the trade the right way',
    text: 'He enrolled in technical courses, studied heating and cooling systems, and worked through the requirements to earn his licenses and secure insurance. It wasn’t the fastest path, but it was the right one — and it’s the foundation of everything Mountain Weather does today.',
  },
  {
    mark: 'July 19, 2017',
    title: 'Mountain Weather is founded',
    text: 'With encouragement from a friend who worked as an accountant, he made it official: Mountain Weather opened on July 19, 2017. It has been a family business from day one.',
  },
  {
    mark: 'The early years',
    title: 'Two jobs, one goal',
    text: 'In the early years, he balanced his own company with work for other HVAC businesses — gaining experience on a wide range of jobs while steadily building a base of customers of his own.',
  },
  {
    mark: 'The leap',
    title: 'Going all-in on Mountain Weather',
    text: 'Then came the decision that took real courage: leaving the security of working for others to dedicate himself entirely to Mountain Weather. He took the risk to gain his independence — and to give every customer his full attention.',
  },
  {
    mark: 'Today',
    title: 'More than 2,000 customers served',
    text: 'Mountain Weather has now served more than 2,000 customers. The company is still family-owned, still based in Kearny, and still guided by a simple idea: learn it right, then do it right.',
  },
];

export default {
  path: PATH,
  title: 'Our Story | Mountain Weather Cooling & Heating, Kearny NJ',
  description:
    'Meet Mountain Weather, a family-owned HVAC company in Kearny, NJ, founded July 19, 2017 and built on training, licensing and hard work. 2,000+ customers served.',
  ogType: 'website',
  render() {
    const body = `
${pageHero({
  trail: TRAIL,
  tone: 'cool',
  eyebrow: `${icon('house', { size: 16 })} Family-owned since 2017`,
  title: 'Mountain Weather: a family-owned HVAC company in Kearny, NJ',
  lead: 'Mountain Weather was built the way good HVAC work gets done — step by step, with patience and the right training. This is how a newcomer to the United States became the owner of a heating and cooling company that has served more than 2,000 customers.',
  image: pic('hand-tools', {
    alt: 'Wrenches, screwdrivers and pliers laid out on a light work surface',
    sizes: HERO_SIZES,
    eager: true,
  }),
})}

${definition(
  'Mountain Weather is a family-owned heating and cooling company founded on July 19, 2017 and based in Kearny, New Jersey, focused on emergency HVAC service and HVAC system replacement.'
)}

<section class="section" aria-labelledby="journey-title">
  <div class="container journey">
    <header class="section-head journey-head">
      <p class="eyebrow">The journey</p>
      <h2 id="journey-title">Built step by step, since 2015</h2>
      <p>No shortcuts and no big launch — just training, persistence and a lot of hard work.</p>
      <div class="journey-media reveal">
        ${pic('snowy-neighborhood', {
          alt: 'Snow-covered houses and evergreen trees in a quiet neighborhood after a winter storm',
          sizes: '(min-width: 1000px) 400px, 92vw',
        })}
      </div>
    </header>
    <ol class="timeline">
      ${CHAPTERS.map(
        (c, i) => `<li class="timeline-item reveal" style="--d:${i % 2}">
        <p class="timeline-mark">${c.mark}</p>
        <h3>${c.title}</h3>
        <p>${c.text}</p>
      </li>`
      ).join('\n      ')}
    </ol>
  </div>
</section>

<section class="trust" aria-label="Company facts">
  <div class="container">
    <ul class="trust-list">
      <li><span class="trust-num">2015</span><span class="trust-label">Founder arrives in the U.S.</span></li>
      <li><span class="trust-num">2017</span><span class="trust-label">Mountain Weather founded</span></li>
      <li><span class="trust-num">Family</span><span class="trust-label">Family-owned business</span></li>
      <li><span class="trust-num">2,000+</span><span class="trust-label">Customers served</span></li>
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="values-title">
  <div class="container">
    <header class="section-head section-head--center">
      <p class="eyebrow">What we stand for</p>
      <h2 id="values-title">The values behind every service call</h2>
    </header>
    <ul class="values">
      <li class="value reveal">${icon('graduation-cap', { size: 28 })}<h3>Learn it right</h3><p>The company was built on training, licensing and insurance — not shortcuts. That standard hasn’t changed.</p></li>
      <li class="value reveal" style="--d:1">${icon('badge-check', { size: 28 })}<h3>Do it right</h3><p>Careful, thorough work and honest recommendations — whether the answer is a repair or a replacement.</p></li>
      <li class="value reveal" style="--d:2">${icon('heart-handshake', { size: 28 })}<h3>Treat people like neighbors</h3><p>Clear communication, respect for your home and a direct line to the people doing the work.</p></li>
      <li class="value reveal" style="--d:3">${icon('house', { size: 28 })}<h3>Own the result</h3><p>As a family-owned business, our name is on every job. That’s a responsibility we take personally.</p></li>
    </ul>
  </div>
</section>

<section class="section section--tint" aria-labelledby="help-title">
  <div class="container about-services">
    <div>
      <p class="eyebrow">How we can help</p>
      <h2 id="help-title">Two services, one standard</h2>
      <p>Today, Mountain Weather focuses on the moments when heating and cooling matter most. When a system fails, our <a href="/emergency-hvac-services">emergency heating and cooling service</a> starts with a text or a call. When equipment is reaching the end of its life, our <a href="/hvac-replacement">system replacement guide</a> explains the signs, the benefits and the process.</p>
      <p>We’re based in Kearny — see <a href="/service-areas">where we work</a>, or reach out to ask about your address.</p>
      <div class="actions">
        ${btnText('Text Mountain Weather', MESSAGES.general, { variant: 'warm' })}
        <a class="btn btn--navy" href="/contact">All contact options ${icon('arrow-right')}</a>
      </div>
    </div>
    <div class="about-services-media reveal">
      ${pic('heating-system-service', {
        alt: 'Technician working on the components of a wall-mounted heating unit',
        sizes: '(min-width: 1000px) 480px, 92vw',
        position: '30% 50%',
      })}
    </div>
  </div>
</section>

${finalCta({ title: 'Put a family-owned HVAC team on your side.' })}
`;

    const schema = [
      {
        '@type': 'AboutPage',
        '@id': `${SITE.url}${PATH}#webpage`,
        url: `${SITE.url}${PATH}`,
        name: this.title,
        description: this.description,
        breadcrumb: { '@id': `${SITE.url}${PATH}#breadcrumb` },
        about: { '@id': ORG_ID() },
        mainEntity: { '@id': ORG_ID() },
        dateModified: SITE.updated,
        inLanguage: 'en-US',
      },
      breadcrumbNode(TRAIL),
    ];
    return { body, schema, preload: imagePreload('hand-tools', HERO_SIZES) };
  },
};
