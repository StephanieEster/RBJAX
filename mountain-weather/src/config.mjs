// Single source of truth for business facts used across every page and in structured data.
// Only facts confirmed in the client brief belong here.

function resolveSiteUrl() {
  if (process.env.SITE_URL) return process.env.SITE_URL;
  // Set automatically by Vercel at build time (custom domain if configured, else *.vercel.app).
  if (process.env.VERCEL_PROJECT_PRODUCTION_URL) return `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`;
  return 'https://mountain-weather.vercel.app';
}

export const SITE = {
  url: resolveSiteUrl().replace(/\/+$/, ''),
  name: 'Mountain Weather',
  legalishName: 'Mountain Weather Cooling & Heating',
  tagline: 'Cooling & Heating',
  locale: 'en_US',
  founded: '2017-07-19',
  foundedLabel: 'July 19, 2017',
  customersServed: '2,000+',
  city: 'Kearny',
  state: 'NJ',
  stateFull: 'New Jersey',
  county: 'Hudson County',
  phoneDisplay: '(862) 270-8862',
  phoneE164: '+18622708862',
  phoneSchema: '+1-862-270-8862',
  email: 'mountainweather63@gmail.com',
  whatsapp: 'https://wa.me/18622708862',
  instagram: 'https://www.instagram.com/mountainweather63',
  facebook: 'https://www.facebook.com/mountainweather63',
  updated: '2026-10-08',
  // New Jersey (N.J.A.C. 13:32A-5.1) requires HVACR advertising to show the master HVACR contractor's
  // name and license number. Fill both in before going live; the footer prints them automatically.
  license: { masterName: '', number: '' },
};

export const NAV = [
  { href: '/emergency-hvac-services', label: 'Emergency Service' },
  { href: '/hvac-replacement', label: 'Replacement' },
  { href: '/about', label: 'Our Story' },
  { href: '/service-areas', label: 'Service Area' },
  { href: '/contact', label: 'Contact' },
];

// Pre-filled message bodies for SMS / WhatsApp links.
export const MESSAGES = {
  general: 'Hi Mountain Weather, I have a question about my heating/cooling system.',
  emergency: 'Hi Mountain Weather, I need emergency HVAC help. My heating/cooling system is:',
  replacement: "Hi Mountain Weather, I'd like to talk about replacing my HVAC system.",
  cooling: "Hi Mountain Weather, my AC isn't working right. Here's what's happening:",
  heating: "Hi Mountain Weather, my heat isn't working right. Here's what's happening:",
};

export const smsHref = (body) => `sms:${SITE.phoneE164}${body ? `?&body=${encodeURIComponent(body)}` : ''}`;
export const telHref = () => `tel:${SITE.phoneE164}`;
export const waHref = (text) => `${SITE.whatsapp}${text ? `?text=${encodeURIComponent(text)}` : ''}`;
export const mailHref = (subject) => `mailto:${SITE.email}${subject ? `?subject=${encodeURIComponent(subject)}` : ''}`;
