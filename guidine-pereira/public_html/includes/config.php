<?php
/**
 * Site settings. This is the only file you normally need to edit.
 */

// Final domain, no trailing slash. Leave empty to detect it automatically from the request.
define('SITE_URL', '');

define('BUSINESS_NAME', 'Guidine Pereira Construction LLC');
define('BUSINESS_SHORT', 'Guidine Pereira Construction');
define('TAGLINE', 'Precision. Quality. Trust.');

define('PHONE_DISPLAY', '(843) 492-8374');
define('PHONE_E164', '+18434928374');
define('EMAIL', 'guidinepereiraconstructionusa@gmail.com');

define('FACEBOOK_URL', 'https://www.facebook.com/guidinepereiraconstruction/');
define('INSTAGRAM_URL', 'https://www.instagram.com/guidinepereiraconstruction/');
define('GOOGLE_BUSINESS_URL', ''); // Paste the Google Business Profile link once it is verified.

/* ---------------------------------------------------------------
 * Estimate form delivery
 * ------------------------------------------------------------- */

// Who receives the estimate requests (comma separated for more than one).
define('LEAD_TO', 'guidinepereiraconstructionusa@gmail.com');

// Sender address. On Hostinger it must be a mailbox on the site's own domain
// (e.g. contact@yourdomain.com). Empty = no-reply@<current domain>.
define('MAIL_FROM', '');

// Optional SMTP (recommended for best delivery). Hostinger: smtp.hostinger.com, port 465, ssl.
// Leave SMTP_HOST empty to use PHP mail().
define('SMTP_HOST', '');
define('SMTP_PORT', 465);
define('SMTP_SECURE', 'ssl'); // 'ssl' (465) or 'tls' (587)
define('SMTP_USER', '');
define('SMTP_PASS', '');

// Every request is also saved to /leads/leads.csv (blocked from public access) as a backup.
define('SAVE_LEADS_CSV', true);

/* ---------------------------------------------------------------
 * Tracking (leave empty to disable)
 * ------------------------------------------------------------- */
define('GTM_ID', '');            // GTM-XXXXXXX
define('GA4_ID', '');            // G-XXXXXXXXXX
define('GOOGLE_ADS_ID', '');     // AW-XXXXXXXXX
define('GOOGLE_ADS_LEAD_LABEL', ''); // conversion label for the form lead (fires on /thank-you)
define('META_PIXEL_ID', '');     // 15-16 digit pixel id
