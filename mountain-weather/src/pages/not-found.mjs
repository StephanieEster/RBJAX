import { MESSAGES } from '../config.mjs';
import { icon, btnText } from '../lib/html.mjs';
import { gauge } from '../lib/sections.mjs';

export default {
  path: '/404',
  output: '404.html',
  noindex: true,
  sitemap: false,
  title: 'Page Not Found | Mountain Weather',
  description: 'The page you were looking for could not be found.',
  render() {
    const body = `
<section class="not-found">
  <div class="container not-found-inner">
    <div class="not-found-gauge">${gauge({ id: 'nf', needle: true })}</div>
    <p class="eyebrow">Error 404</p>
    <h1>This page went off the dial.</h1>
    <p class="lead">The page you’re looking for doesn’t exist or has moved. Here’s where you can go instead:</p>
    <ul class="not-found-links">
      <li><a href="/">${icon('house', { size: 18 })} Home</a></li>
      <li><a href="/emergency-hvac-services">${icon('circle-alert', { size: 18 })} Emergency HVAC Services</a></li>
      <li><a href="/hvac-replacement">${icon('sparkles', { size: 18 })} HVAC Replacement</a></li>
      <li><a href="/contact">${icon('message-square-text', { size: 18 })} Contact</a></li>
    </ul>
    <div class="actions actions--center">${btnText('Text Mountain Weather', MESSAGES.general, { variant: 'warm' })}</div>
  </div>
</section>
`;
    return { body, schema: [], bodyClass: 'page-404' };
  },
};
