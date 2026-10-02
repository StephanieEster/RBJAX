<?php
/*
 * OPTIONAL SMTP settings for send-form.php (recommended for reliable delivery to Gmail).
 *
 * 1. Create a mailbox in Hostinger hPanel (Emails), e.g. website@yourdomain.com.
 * 2. Copy this file as "guardian-mail-config.php" ONE LEVEL ABOVE public_html
 *    (e.g. domains/yourdomain.com/guardian-mail-config.php), so it can never be downloaded.
 * 3. Fill in the values below. Never put this password in HTML or JavaScript.
 *
 * Hostinger: smtp.hostinger.com, port 465 + 'ssl' (or 587 + 'tls').
 */
return [
    'smtp_host'   => 'smtp.hostinger.com',
    'smtp_port'   => 465,
    'smtp_secure' => 'ssl',
    'smtp_user'   => 'website@yourdomain.com',
    'smtp_pass'   => 'MAILBOX-PASSWORD-HERE',
    // Optional. Defaults to smtp_user. Must be a mailbox of your own domain.
    'from_email'  => '',
    // Optional. Real domain without https:// or www (e.g. 'guardianhomes.com').
    'site_domain' => '',
];
