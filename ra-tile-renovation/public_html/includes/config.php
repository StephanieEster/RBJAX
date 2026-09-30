<?php
/**
 * R.A Tile Renovation — site configuration.
 * Edit ONLY this file to change domain, contacts, e-mail delivery and tracking.
 */

if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'config.php') {
    http_response_code(403);
    exit;
}

// ---------------------------------------------------------------------------
// Site / business
// ---------------------------------------------------------------------------
define('SITE_URL', 'https://ratilerenovation.com');   // no trailing slash — change to the real domain
define('SITE_NAME', 'R.A Tile Renovation');
define('SITE_LEGAL_NAME', 'RA Tile Renovation');
define('SITE_TAGLINE', 'Tile Installation & Bathroom Remodeling in New Hampshire');

define('PHONE_E164', '+19783316200');                // used in sms: / tel: links
define('PHONE_DISPLAY', '(978) 331-6200');
define('EMAIL_PUBLIC', 'tilerenovationpro@gmail.com');
define('INSTAGRAM_URL', 'https://www.instagram.com/ra_tile_renovation_33/');
define('FACEBOOK_URL', '');                          // fill in when the page exists
define('GOOGLE_BUSINESS_URL', '');                   // fill in after GMB is verified

define('BASE_CITY', 'Manchester');
define('BASE_STATE', 'NH');
define('FOUNDED_YEAR', 2023);
define('YEARS_EXPERIENCE', '20+');

// Pre-filled SMS text (CTA is SMS-first)
define('SMS_BODY', "Hi Renato! I'd like a free tile estimate. My name is ");

// ---------------------------------------------------------------------------
// Form delivery
// ---------------------------------------------------------------------------
// Where leads are sent (comma separated for more than one address)
define('LEAD_TO', 'tilerenovationpro@gmail.com');

// Sender address — on Hostinger it MUST be a mailbox on your own domain
// (create it in hPanel > Emails), e.g. no-reply@ratilerenovation.com
define('MAIL_FROM', 'no-reply@ratilerenovation.com');
define('MAIL_FROM_NAME', 'R.A Tile Renovation Website');

// Recommended: SMTP (better delivery than PHP mail()).
// Hostinger: host smtp.hostinger.com, port 465, secure ssl, user = full mailbox, pass = mailbox password
define('SMTP_ENABLED', false);
define('SMTP_HOST', 'smtp.hostinger.com');
define('SMTP_PORT', 465);
define('SMTP_SECURE', 'ssl');                         // 'ssl' (465) or 'tls' (587)
define('SMTP_USER', 'no-reply@ratilerenovation.com');
define('SMTP_PASS', '');

// Send a confirmation e-mail to the visitor when they provide an e-mail
define('SEND_AUTOREPLY', true);

// Every lead is also saved to data/leads.csv (protected from the web) as a backup
define('SAVE_LEADS_CSV', true);

// Optional: forward each lead as JSON to a CRM / Zapier / Make webhook
define('LEAD_WEBHOOK_URL', '');

// ---------------------------------------------------------------------------
// Tracking (leave empty to disable)
// ---------------------------------------------------------------------------
define('GA4_ID', '');                 // e.g. G-XXXXXXXXXX
define('GOOGLE_ADS_ID', '');          // e.g. AW-123456789
define('GOOGLE_ADS_LEAD_LABEL', '');  // conversion label for form leads
define('META_PIXEL_ID', '');
define('GOOGLE_SITE_VERIFICATION', '');

// Secret used to sign form tokens — change to any long random string
define('FORM_SECRET', 'change-me-to-a-long-random-string-ra-tile-2026');
