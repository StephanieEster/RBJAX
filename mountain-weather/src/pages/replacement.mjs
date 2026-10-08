import { SITE, MESSAGES } from '../config.mjs';
import { icon, pic, imagePreload, btnText, btnCall } from '../lib/html.mjs';
import { pageHero, definition, faq, steps, finalCta } from '../lib/sections.mjs';
import { ORG_ID, breadcrumbNode } from '../lib/layout.mjs';

const PATH = '/hvac-replacement';
const TRAIL = [
  { href: '/', label: 'Home' },
  { href: PATH, label: 'HVAC Replacement' },
];
const HERO_SIZES = '(min-width: 1000px) 460px, 92vw';
const ENERGY_STAR = 'https://www.energystar.gov/saveathome/heating-cooling/replace';

const FAQ_ITEMS = [
  {
    q: 'How long does an HVAC system last?',
    a: 'Lifespans vary with the type of equipment, how hard it works and how well it’s maintained. As a general guideline, ENERGY STAR suggests evaluating replacement once an air conditioner or heat pump passes 10 years, or a furnace or boiler passes 15. Many systems run longer with good care — condition matters more than the date on the label.',
  },
  {
    q: 'Should I replace my furnace and air conditioner at the same time?',
    a: 'Not always, but it’s often worth considering. In a split system, the indoor and outdoor components are designed to work together, so replacing only one can limit efficiency or compatibility — especially if the remaining unit is older. We’ll look at the age and condition of both and explain the trade-offs before you decide.',
  },
  {
    q: 'How long does an HVAC replacement take?',
    a: 'It depends on the equipment and the home. Swapping like-for-like equipment is usually a much shorter project than one that changes system types or modifies ductwork. We’ll give you a realistic timeline for your specific project when we go over your options, so you can plan around it.',
  },
  {
    q: 'Will a new system lower my energy bills?',
    a: 'Often, especially when it replaces older equipment. Federal minimum efficiency standards for new central air conditioners and heat pumps were raised in 2023, and ENERGY STAR notes that certified equipment, installed correctly, can save up to 20% on heating and cooling costs. Actual savings depend on your old system, your home and how you use it.',
  },
  {
    q: 'What size system does my home need?',
    a: 'The right size depends on your home’s heating and cooling load — not square footage alone. Insulation, windows, layout and air leaks all play a role. An oversized system can short-cycle and control humidity poorly, while an undersized one may struggle on the hottest and coldest days. Sizing is a key part of any replacement conversation.',
  },
  {
    q: 'My system uses R-22 refrigerant. Do I have to replace it?',
    a: 'No — you can keep using a working R-22 system. But production and import of R-22 ended in the United States on January 1, 2020, so if the system leaks or needs more refrigerant, service can become expensive. If an R-22 system needs a major repair, that is usually a good moment to compare it with replacement.',
  },
  {
    q: 'Why don’t you list replacement prices online?',
    a: 'Replacement cost depends on the equipment, the home and the scope of work, so a generic number wouldn’t be accurate for your situation. We’d rather understand your system and your goals first. Text or call (862) 270-8862 to talk through your options with us.',
  },
  {
    q: 'My system just broke down. Can you replace it?',
    a: 'Yes — sometimes a breakdown is the moment replacement becomes the right choice. If a failed system is older or the repair is major, we’ll explain what a replacement would involve so you can compare. For an urgent failure, start with our emergency HVAC services.',
  },
];

const CRITERIA = [
  ['Are you licensed and insured in New Jersey?', 'New Jersey licenses HVACR contractors. Licensing and insurance protect you and your property if something goes wrong.'],
  ['How will you size the new equipment?', 'Bigger isn’t better. Equipment should match the home’s heating and cooling load; an industry-standard load calculation (such as ACCA Manual J) is the usual method.'],
  ['Does the job need a permit, and who handles it?', 'Equipment replacement often requires a construction permit and inspection in New Jersey. Know who is responsible before work begins.'],
  ['What exactly is included?', 'Ask about removal and disposal of the old equipment, connections, thermostat, any ductwork or line-set changes, and cleanup.'],
  ['What warranties apply, and do they require registration?', 'Manufacturer warranties often require product registration within a set time after installation. Make sure it gets done.'],
  ['What maintenance will the new system need?', 'Filter changes and periodic professional maintenance help new equipment keep its efficiency and protect warranty coverage.'],
];

const COMPARE = [
  ['Equipment age', 'AC or heat pump under 10 years; furnace or boiler under 15', 'Past those ages, especially with other warning signs'],
  ['Repair history', 'First significant problem, good service record', 'Repeated breakdowns and service calls'],
  ['Size of the repair', 'A minor, isolated part', 'A major component on an older system'],
  ['Comfort', 'The home stays comfortable when the system runs', 'Rooms are too hot or too cold; humidity is hard to control'],
  ['Energy bills', 'Steady from year to year', 'Rising without a change in how you use the system'],
  ['Refrigerant', 'Uses a currently produced refrigerant', 'Uses R-22, which is no longer produced in the U.S.'],
  ['Your plans', 'You expect to move soon', 'You plan to stay in the home for years'],
];

export default {
  path: PATH,
  title: 'HVAC Replacement in Kearny, NJ | Mountain Weather',
  description:
    'Thinking about replacing an aging heating or cooling system in Kearny, NJ? See the warning signs, the benefits and how HVAC replacement works. Text (862) 270-8862.',
  render() {
    const faqBlock = faq({
      title: 'HVAC replacement questions',
      intro: 'Honest answers before you make a big decision.',
      items: FAQ_ITEMS.map((q) =>
        q.q.startsWith('My system just broke down')
          ? { ...q, a: q.a.replace('start with our emergency HVAC services.', 'start with our <a href="/emergency-hvac-services">emergency heating and cooling service</a>.') }
          : q
      ),
    });

    const body = `
${pageHero({
  trail: TRAIL,
  tone: 'cool',
  eyebrow: `${icon('sparkles', { size: 16 })} Heating &amp; cooling system replacement`,
  title: 'HVAC Replacement in Kearny, NJ',
  lead: 'An aging system that keeps breaking down costs you comfort, time and money. Mountain Weather helps you understand when replacement makes sense — and what to expect from the first conversation to the final walkthrough.',
  actions: `${btnText('Ask About a Replacement', MESSAGES.replacement, { variant: 'cool', cls: 'btn--lg' })}${btnCall('Call Now', { variant: 'navy', cls: 'btn--lg' })}`,
  image: pic('pipe-fitting-detail', {
    alt: 'Gloved hands tightening a pipe fitting during a heating system installation',
    sizes: HERO_SIZES,
    eager: true,
  }),
})}

${definition(
  'HVAC replacement is the removal of an aging or failing furnace, boiler, air conditioner or heat pump and the installation of new equipment matched to the home, restoring reliable comfort and typically improving energy efficiency.'
)}

<section class="section" aria-labelledby="signs-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow">Warning signs</p>
      <h2 id="signs-title">Six signs your system may be ready for replacement</h2>
      <p>One sign on its own doesn’t mean you need a new system. Several together usually mean it’s time for a closer look.</p>
    </header>
    <ul class="sign-grid">
      <li class="sign reveal">${icon('calendar-check', { size: 26 })}<h3>It’s getting older</h3><p><a href="${ENERGY_STAR}" target="_blank" rel="noopener noreferrer">ENERGY STAR<span class="sr-only"> (opens in a new tab)</span></a> suggests calling a professional when a heat pump or AC is more than 10 years old, or a furnace or boiler is more than 15.</p></li>
      <li class="sign reveal" style="--d:1">${icon('wrench', { size: 26 })}<h3>Repairs keep piling up</h3><p>Frequent service calls — and repair bills that add up season after season — are a classic signal.</p></li>
      <li class="sign reveal" style="--d:2">${icon('gauge', { size: 26 })}<h3>Energy bills are climbing</h3><p>Rising costs without a change in how you use the system can mean the equipment is losing efficiency.</p></li>
      <li class="sign reveal">${icon('thermometer', { size: 26 })}<h3>Some rooms never feel right</h3><p>Rooms that stay too hot or too cold, or humidity you can’t control, can point to a system that no longer fits the home.</p></li>
      <li class="sign reveal" style="--d:1">${icon('snowflake', { size: 26 })}<h3>It runs on R-22</h3><p>Production and import of R-22 refrigerant ended in the U.S. on January 1, 2020, which can make servicing older systems costly.</p></li>
      <li class="sign reveal" style="--d:2">${icon('wind', { size: 26 })}<h3>New noises, dust or odors</h3><p>Louder operation, more dust than usual or lingering odors can be signs of equipment that’s struggling.</p></li>
    </ul>
  </div>
</section>

<section class="section section--tint" aria-labelledby="compare-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow">Repair or replace?</p>
      <h2 id="compare-title">How to weigh repair against replacement</h2>
      <p>No single rule fits every home. Use this as a starting point — then we’ll look at your actual equipment together.</p>
    </header>
    <div class="table-wrap reveal" role="region" aria-labelledby="compare-title" tabindex="0">
      <table class="compare">
        <thead><tr><th scope="col">Factor</th><th scope="col">Repair usually makes sense</th><th scope="col">Replacement is worth considering</th></tr></thead>
        <tbody>
          ${COMPARE.map(([f, r, p]) => `<tr><th scope="row">${f}</th><td data-label="Repair usually makes sense">${r}</td><td data-label="Replacement is worth considering">${p}</td></tr>`).join('\n          ')}
        </tbody>
      </table>
    </div>
    <p class="section-note">Age guidelines from <a href="${ENERGY_STAR}" target="_blank" rel="noopener noreferrer">ENERGY STAR<span class="sr-only"> (opens in a new tab)</span></a>. If your system has failed and you need help now, see our <a href="/emergency-hvac-services">urgent heating and cooling repair</a> page.</p>
  </div>
</section>

<section class="section" aria-labelledby="benefits-title">
  <div class="container benefits-grid">
    <div class="benefits-media reveal">
      ${pic('smart-thermostat', {
        alt: 'Smart thermostat mounted on a textured wall displaying 63 degrees',
        sizes: '(min-width: 1000px) 520px, 92vw',
        position: '60% 50%',
      })}
    </div>
    <div>
      <p class="eyebrow">Benefits of new equipment</p>
      <h2 id="benefits-title">What a new system can do for your home</h2>
      <ul class="why-list why-list--compact">
        <li>${icon('gauge', { size: 22 })}<div><h3>Higher efficiency</h3><p>Federal minimum efficiency standards for new central air conditioners and heat pumps (measured as SEER2 and HSPF2) took effect January 1, 2023. ENERGY STAR notes that certified equipment, installed correctly, can save up to 20% on heating and cooling costs.</p></div></li>
        <li>${icon('shield-check', { size: 22 })}<div><h3>Reliability you can count on</h3><p>New equipment means fewer surprise breakdowns, and it typically comes with a manufacturer’s warranty — just be sure it’s registered.</p></div></li>
        <li>${icon('thermometer', { size: 22 })}<div><h3>Better comfort</h3><p>Correctly sized modern systems can deliver more even temperatures and better humidity control, and many run more quietly than older units.</p></div></li>
        <li>${icon('sparkles', { size: 22 })}<div><h3>Modern controls</h3><p>New systems pair well with programmable and smart thermostats, making it easier to manage comfort and energy use.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section how" aria-labelledby="process-title">
  <div class="container">
    <header class="section-head section-head--center">
      <p class="eyebrow">The process</p>
      <h2 id="process-title">How an HVAC replacement works</h2>
    </header>
    ${steps([
      { title: 'Reach out', text: 'Tell us about your current system — its age, the problems you’ve noticed and photos of the equipment labels.' },
      { title: 'Assessment', text: 'We evaluate the existing equipment, your home and your comfort concerns.' },
      { title: 'Options explained', text: 'You get a clear recommendation and your options in plain language, so you can decide with confidence.' },
      { title: 'Installation', text: 'The old equipment is removed and the new system is installed, connected and tested.' },
      { title: 'Walkthrough', text: 'We show you how to operate the new system and what it needs to keep running well.' },
    ])}
  </div>
</section>

<section class="section" aria-labelledby="criteria-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow">Hire with confidence</p>
      <h2 id="criteria-title">Six questions to ask any HVAC contractor before a replacement</h2>
      <p>A replacement is a major investment. Whoever you hire, these questions help you compare contractors and avoid surprises.</p>
    </header>
    <div class="table-wrap reveal" role="region" aria-labelledby="criteria-title" tabindex="0">
      <table class="compare compare--criteria">
        <thead><tr><th scope="col">Question to ask</th><th scope="col">Why it matters</th></tr></thead>
        <tbody>
          ${CRITERIA.map(([q, w]) => `<tr><th scope="row">${q}</th><td data-label="Why it matters">${w}</td></tr>`).join('\n          ')}
        </tbody>
      </table>
    </div>
    <p class="section-note">Want to know more about who you’d be working with? <a href="/about">Meet the family business behind Mountain Weather</a>.</p>
  </div>
</section>

${faqBlock.html}

${finalCta({
  title: 'Ready to talk about a new system?',
  text: 'Text us your system’s age and what’s been going on — photos of the equipment labels help. We’ll take it from there.',
  message: MESSAGES.replacement,
})}
`;

    const schema = [
      {
        '@type': 'WebPage',
        '@id': `${SITE.url}${PATH}#webpage`,
        url: `${SITE.url}${PATH}`,
        name: this.title,
        description: this.description,
        breadcrumb: { '@id': `${SITE.url}${PATH}#breadcrumb` },
        about: { '@id': `${SITE.url}${PATH}#service` },
        dateModified: SITE.updated,
        inLanguage: 'en-US',
      },
      {
        '@type': 'Service',
        '@id': `${SITE.url}${PATH}#service`,
        name: 'HVAC Replacement',
        serviceType: 'Heating and air conditioning system replacement',
        description:
          'Replacement of aging or failing heating and cooling equipment with new equipment matched to the home.',
        provider: { '@id': ORG_ID() },
        areaServed: { '@type': 'City', name: 'Kearny', containedInPlace: { '@type': 'State', name: 'New Jersey' } },
        url: `${SITE.url}${PATH}`,
      },
      breadcrumbNode(TRAIL),
      faqBlock.schema,
    ];
    return { body, schema, preload: imagePreload('pipe-fitting-detail', HERO_SIZES) };
  },
};
