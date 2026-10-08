import { SITE, MESSAGES } from '../config.mjs';
import { icon, pic, imagePreload, btnText, btnCall } from '../lib/html.mjs';
import { pageHero, definition, faq, steps, finalCta } from '../lib/sections.mjs';
import { ORG_ID, breadcrumbNode } from '../lib/layout.mjs';

const PATH = '/emergency-hvac-services';
const TRAIL = [
  { href: '/', label: 'Home' },
  { href: PATH, label: 'Emergency HVAC Services' },
];
const HERO_SIZES = '(min-width: 1000px) 460px, 92vw';

const FAQ_ITEMS = [
  {
    q: 'Do you offer 24/7 emergency HVAC service?',
    a: 'Our availability depends on our current schedule, so we don’t advertise round-the-clock service. The best move is to text or call (862) 270-8862 as soon as you notice a problem. We’ll tell you honestly when we can help, so you can plan around it.',
  },
  {
    q: 'What counts as an HVAC emergency?',
    a: 'No heat in cold weather, no cooling during a heat wave — especially with infants, older adults or anyone with health concerns at home — water leaking from equipment, burning smells, or a system that keeps tripping its breaker. A gas smell or a carbon monoxide alarm is a safety emergency: leave the building and call 911 or your gas utility first.',
  },
  {
    q: 'What should I do while I wait for help?',
    a: 'Turn the system off if it’s making unusual noises, leaking or tripping the breaker. In winter, keep doors closed, dress in layers and use space heaters only as directed, away from anything flammable. In summer, close blinds, run fans and stay hydrated. Never use an oven, stove or grill to heat your home.',
  },
  {
    q: 'Can I fix my HVAC system myself?',
    a: 'Simple checks — thermostat settings and batteries, the breaker and the air filter — are safe for most homeowners. Past that, HVAC equipment involves high voltage, gas connections and pressurized refrigerant, and federal rules require EPA certification to handle refrigerants. For anything beyond the basics, it’s safer to let a trained technician diagnose the problem.',
  },
  {
    q: 'Do you handle both heating and cooling emergencies?',
    a: 'Yes. Mountain Weather is a cooling and heating company — it’s right there in our name. Whether your heat stopped working on a cold night or your air conditioning quit during a hot spell, text or call (862) 270-8862 and describe what’s happening.',
  },
  {
    q: 'What information should I share when I reach out?',
    a: 'Tell us whether it’s heating or cooling, what the system is doing, when it started and whether anything changed recently, like a power outage or a new thermostat. Photos of the equipment, its model label and any error codes on the thermostat or unit are very helpful.',
  },
  {
    q: 'Will you tell me whether repair or replacement makes more sense?',
    a: 'Yes. After diagnosing the problem, we’ll explain what failed and your realistic options. If the system is older and the repair is significant, we’ll walk you through what a replacement would involve so you can compare. The decision is always yours.',
  },
  {
    q: 'Is emergency service available outside Kearny?',
    a: 'We’re based in Kearny, New Jersey. If you’re nearby, text us your town or ZIP code along with a description of the problem, and we’ll let you know right away whether we’re able to help.',
  },
];

export default {
  path: PATH,
  title: 'Emergency HVAC Services in Kearny, NJ | Mountain Weather',
  description:
    'Heat out or AC down in Kearny, NJ? Text or call Mountain Weather at (862) 270-8862 for emergency heating and cooling service from a family-owned HVAC team.',
  render() {
    const faqBlock = faq({
      title: 'Emergency HVAC questions',
      intro: 'What to expect when your heating or cooling stops working.',
      items: FAQ_ITEMS,
    });

    const body = `
${pageHero({
  trail: TRAIL,
  tone: 'heat',
  eyebrow: `${icon('circle-alert', { size: 16 })} Emergency heating &amp; cooling`,
  title: 'Emergency HVAC Services in Kearny, NJ',
  lead: 'A heating system that won’t start. An AC blowing warm air. A unit that keeps shutting itself off. When your heating or cooling fails, text or call Mountain Weather — tell us what’s happening and we’ll let you know how and when we can help.',
  actions: `${btnText('Text for Emergency Service', MESSAGES.emergency, { variant: 'warm', cls: 'btn--lg' })}${btnCall('Call Now', { variant: 'navy', cls: 'btn--lg' })}`,
  image: pic('technician-manifold-gauge', {
    alt: 'HVAC technician reading a refrigerant manifold gauge while servicing an outdoor unit',
    sizes: HERO_SIZES,
    eager: true,
    position: '50% 40%',
  }),
})}

${definition(
  'Emergency HVAC service is urgent repair work on a heating or cooling system that has stopped working or is running unsafely, focused on diagnosing the failure and restoring safe, reliable operation as soon as practical.'
)}

<section class="section" aria-labelledby="emergencies-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow">Common emergencies</p>
      <h2 id="emergencies-title">Is it time to call? Signs your system needs help now</h2>
      <p>Heating and cooling failures rarely happen at a convenient moment. These are the situations we hear about most often.</p>
    </header>
    <div class="split-cards">
      <article class="split-card split-card--heat reveal">
        <div class="split-card-media">${pic('boiler-pump-detail', {
          alt: 'Gloved hands adjusting the circulator pump of a home heating system',
          sizes: '(min-width: 900px) 560px, 92vw',
        })}</div>
        <div class="split-card-body">
          <h3>${icon('flame', { size: 22 })} No heat or poor heating</h3>
          <ul class="ticks">
            <li>${icon('check', { size: 18 })} The heating system won’t start when the thermostat calls for heat</li>
            <li>${icon('check', { size: 18 })} Vents blow cool air in heating mode</li>
            <li>${icon('check', { size: 18 })} The system turns on and off in short cycles</li>
            <li>${icon('check', { size: 18 })} Banging, grinding or squealing from the equipment</li>
            <li>${icon('check', { size: 18 })} Some rooms stay cold no matter the setting</li>
          </ul>
          ${btnText('Text us about your heat', MESSAGES.heating, { variant: 'warm' })}
        </div>
      </article>
      <article class="split-card split-card--cool reveal" style="--d:1">
        <div class="split-card-media">${pic('outdoor-ac-unit', {
          alt: 'Outdoor air conditioning unit installed against a teal exterior wall',
          sizes: '(min-width: 900px) 560px, 92vw',
          position: '70% 50%',
        })}</div>
        <div class="split-card-body">
          <h3>${icon('snowflake', { size: 22 })} No cooling or poor cooling</h3>
          <ul class="ticks">
            <li>${icon('check', { size: 18 })} The AC runs, but the air isn’t cold</li>
            <li>${icon('check', { size: 18 })} The outdoor unit won’t start, or hums without running</li>
            <li>${icon('check', { size: 18 })} Ice on the refrigerant lines or indoor coil</li>
            <li>${icon('check', { size: 18 })} Water leaking around the indoor unit</li>
            <li>${icon('check', { size: 18 })} The breaker trips when the system starts</li>
          </ul>
          ${btnText('Text us about your AC', MESSAGES.cooling, { variant: 'cool' })}
        </div>
      </article>
    </div>
  </div>
</section>

<section class="section section--tint" aria-labelledby="checks-title">
  <div class="container checks-grid">
    <div>
      <p class="eyebrow">Before you call</p>
      <h2 id="checks-title">Four quick checks that sometimes solve the problem</h2>
      <p>These are safe for most homeowners and take only a few minutes. If they don’t help, stop there and reach out — there’s no need to open up equipment.</p>
      <ol class="checks">
        <li><h3>Check the thermostat</h3><p>Confirm it’s set to the right mode (heat or cool), the setpoint is above or below room temperature as needed, and replace the batteries if the display is blank or dim.</p></li>
        <li><h3>Check the breaker and service switch</h3><p>Look for a tripped breaker in your electrical panel. Many heating systems also have a service switch nearby that looks like a regular light switch — make sure it’s on.</p></li>
        <li><h3>Check the air filter</h3><p>A badly clogged filter can choke airflow, freeze an AC coil or cause a heating system to overheat and shut down.</p></li>
        <li><h3>Note what you see and hear</h3><p>Error codes, blinking lights, unusual sounds or smells — jot them down or take a photo. It helps us understand the problem quickly.</p></li>
      </ol>
    </div>
    <aside class="danger-card" aria-labelledby="danger-title">
      <h2 id="danger-title">${icon('circle-alert', { size: 24 })} Stop and get out if:</h2>
      <ul>
        <li>You smell gas (a rotten-egg odor)</li>
        <li>Your carbon monoxide alarm is sounding</li>
        <li>You see smoke or smell something burning</li>
      </ul>
      <p>Leave the building right away and call <strong>911</strong> or your gas utility from outside. Don’t switch lights or equipment on or off. Once everyone is safe, contact us about the equipment.</p>
    </aside>
  </div>
</section>

<section class="section" aria-labelledby="pro-title">
  <div class="container pro-grid">
    <div class="pro-media reveal">${pic('ac-service-gauges', {
      alt: 'Technician measuring system pressures on an outdoor air conditioning unit',
      sizes: '(min-width: 1000px) 520px, 92vw',
    })}</div>
    <div>
      <p class="eyebrow">Why call a professional</p>
      <h2 id="pro-title">The benefits of a trained technician when it counts</h2>
      <ul class="why-list why-list--compact">
        <li>${icon('shield-check', { size: 22 })}<div><h3>Safety first</h3><p>Heating and cooling equipment involves high voltage, gas connections and pressurized refrigerant. Federal rules require EPA certification to handle refrigerants.</p></div></li>
        <li>${icon('gauge', { size: 22 })}<div><h3>An accurate diagnosis</h3><p>Testing — not guessing — finds the real cause, so you don’t pay to replace parts that weren’t the problem.</p></div></li>
        <li>${icon('wrench', { size: 22 })}<div><h3>Protect your equipment</h3><p>Running a malfunctioning system, like an AC with an iced coil, can damage expensive components. A professional knows when to shut it down.</p></div></li>
        <li>${icon('message-circle', { size: 22 })}<div><h3>A clear next step</h3><p>You’ll understand what failed and your options. If an older system is failing repeatedly, our guide to <a href="/hvac-replacement">replacing an aging HVAC system</a> explains when that makes more sense than another repair.</p></div></li>
      </ul>
    </div>
  </div>
</section>

<section class="section how" aria-labelledby="how-title">
  <div class="container">
    <header class="section-head section-head--center">
      <p class="eyebrow">How it works</p>
      <h2 id="how-title">From your first text to a working system</h2>
    </header>
    ${steps([
      { title: 'Text or call us', text: `Reach us at ${SITE.phoneDisplay}. Describe the problem and send a photo of the equipment if you can.` },
      { title: 'Talk it through', text: 'We ask a few questions, share any safety guidance and let you know when we can help based on our schedule.' },
      { title: 'Diagnosis on site', text: 'A trained technician inspects and tests the system to find the cause of the failure.' },
      { title: 'Your options, explained', text: 'We explain what we found and the realistic next steps — repair, or a plan for replacement if it makes more sense.' },
    ])}
    <p class="section-note">Mountain Weather is a family-owned company based in Kearny — read <a href="/about">how our founder built the business</a> or check <a href="/service-areas">where we provide service</a>.</p>
  </div>
</section>

${faqBlock.html}

${finalCta({
  title: 'Heating or cooling down right now?',
  text: 'Text us what’s happening — the more detail, the better. Prefer to talk? Call or send a WhatsApp message to the same number.',
  message: MESSAGES.emergency,
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
        name: 'Emergency HVAC Services',
        serviceType: 'Emergency heating and air conditioning repair',
        description:
          'Urgent diagnosis and repair of heating and cooling systems that have stopped working or are running unsafely.',
        provider: { '@id': ORG_ID() },
        areaServed: { '@type': 'City', name: 'Kearny', containedInPlace: { '@type': 'State', name: 'New Jersey' } },
        url: `${SITE.url}${PATH}`,
      },
      breadcrumbNode(TRAIL),
      faqBlock.schema,
    ];
    return { body, schema, preload: imagePreload('technician-manifold-gauge', HERO_SIZES) };
  },
};
