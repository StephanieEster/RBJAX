import { SITE } from '../config.mjs';
import { breadcrumbs } from '../lib/sections.mjs';
import { breadcrumbNode } from '../lib/layout.mjs';

const PATH = '/privacy-policy';
const TRAIL = [
  { href: '/', label: 'Home' },
  { href: PATH, label: 'Privacy Policy' },
];

export default {
  path: PATH,
  title: 'Privacy Policy | Mountain Weather',
  description:
    'How Mountain Weather Cooling & Heating handles information on this website and when you contact us by text, phone, WhatsApp or email.',
  render() {
    const body = `
<section class="legal">
  <div class="container legal-inner">
    ${breadcrumbs(TRAIL)}
    <h1>Privacy Policy</h1>
    <p class="legal-meta">Effective date: October 8, 2026</p>

    <p>This Privacy Policy explains how ${SITE.legalishName} (“Mountain Weather,” “we,” “us”) handles information related to this website and to the messages you send us. We’ve kept it short because this website collects very little.</p>

    <h2>Information this website collects</h2>
    <p>This website does not have user accounts, does not use analytics or advertising trackers, and does not set cookies. Our fonts and images are served from this website itself, so loading a page does not send requests to third-party services.</p>

    <h2>The message form on our Contact page</h2>
    <p>The form on our Contact page runs entirely in your browser. When you choose “Open in Text Messages,” “Open in WhatsApp” or “Open in Email,” it opens that app on your device with your message filled in. Nothing you type is sent to or stored by this website. Your message reaches us only if you choose to send it from your app.</p>

    <h2>Information you send us</h2>
    <p>When you text, call, message us on WhatsApp or email us, we receive the information you choose to share — such as your name, phone number, email address, town or ZIP code, a description of your heating or cooling issue, and any photos. We use it to respond to you, to provide and follow up on our services, and to keep records of the work we perform.</p>
    <p>We do not sell your personal information, and we do not share it with third parties for their own marketing.</p>

    <h2>Third-party services</h2>
    <p>Messages and calls travel through the services you choose to use — your mobile carrier, WhatsApp, or your email provider — and are handled under those providers’ own privacy policies. This website links to our Instagram and Facebook pages; if you visit them, Instagram’s and Facebook’s policies apply.</p>

    <h2>Website hosting</h2>
    <p>Like any website, this site is delivered by a hosting provider that may automatically process technical information, such as your IP address, browser type and the pages requested, in order to deliver the site and keep it secure.</p>

    <h2>How long we keep information</h2>
    <p>We keep the information you send us for as long as needed to respond to you, provide our services and maintain reasonable business records, and then delete it when it’s no longer needed.</p>

    <h2>Your choices</h2>
    <p>You can ask us what information we have from you, or ask us to correct or delete it, by emailing <a href="mailto:${SITE.email}">${SITE.email}</a>. If you’d rather not receive follow-up messages from us, just tell us.</p>

    <h2>Children’s privacy</h2>
    <p>This website is intended for adults and is not directed to children under 13. We do not knowingly collect information from children.</p>

    <h2>Changes to this policy</h2>
    <p>If we change how we handle information — for example, by adding a new tool to the website — we will update this page and its effective date.</p>

    <h2>Contact</h2>
    <p>Questions about this policy? Email <a href="mailto:${SITE.email}">${SITE.email}</a> or text <a href="sms:${SITE.phoneE164}">${SITE.phoneDisplay}</a>.</p>
  </div>
</section>
`;
    const schema = [
      {
        '@type': 'WebPage',
        '@id': `${SITE.url}${PATH}#webpage`,
        url: `${SITE.url}${PATH}`,
        name: this.title,
        breadcrumb: { '@id': `${SITE.url}${PATH}#breadcrumb` },
        inLanguage: 'en-US',
      },
      breadcrumbNode(TRAIL),
    ];
    return { body, schema };
  },
};
