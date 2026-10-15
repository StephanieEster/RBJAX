<?php
/**
 * Rio Cleaning Services — form delivery settings.
 * Edit ONLY this file to change where estimate requests go and how e-mail is sent.
 */
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'config.php') {
    http_response_code(403);
    exit;
}

define('SITE_URL', 'https://riocleaningservice.com');      // no trailing slash
define('SITE_NAME', 'Rio Cleaning Services');
define('PHONE_DISPLAY', '(267) 694-4609');
define('PHONE_TEL', 'tel:+12676944609');

// Where estimate requests are delivered (comma separated for more than one address)
define('LEAD_TO', 'riocleaningservices.m@gmail.com');

// How e-mail is sent: out of the box the site uses PHP mail() on Hostinger, nothing to configure.
// The sender shown is an address on the site's own domain (it does not need to exist as a mailbox);
// replies go straight to the customer.
define('MAIL_FROM', 'no-reply@riocleaningservice.com');
define('MAIL_FROM_NAME', 'Rio Cleaning Website');

// OPTIONAL upgrade: authenticated SMTP lands in the inbox more reliably than mail().
// To use it, create the mailbox above in hPanel > Emails, set SMTP_ENABLED to true and
// paste the mailbox password in SMTP_PASS. If SMTP ever fails, the site falls back to mail().
define('SMTP_ENABLED', false);
define('SMTP_HOST', 'smtp.hostinger.com');
define('SMTP_PORT', 465);
define('SMTP_SECURE', 'ssl');                         // 'ssl' (465) or 'tls' (587)
define('SMTP_USER', 'no-reply@riocleaningservice.com');
define('SMTP_PASS', '');

// Send a short confirmation e-mail to the visitor when they leave an e-mail address
define('SEND_AUTOREPLY', true);

// Every request is also saved to data/leads.csv (blocked from the web) as a backup
define('SAVE_LEADS_CSV', true);

// Optional: also forward each request as JSON to a CRM / Zapier / Make webhook
define('LEAD_WEBHOOK_URL', '');

// Anti-spam: at most this many requests per visitor IP every 10 minutes
define('RATE_LIMIT', 5);
