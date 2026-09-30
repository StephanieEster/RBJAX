<?php
/**
 * Lead form handler — works with AJAX (JSON response) and plain POST (redirect).
 */
require __DIR__ . '/includes/bootstrap.php';
require __DIR__ . '/includes/mailer.php';

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false
    || ($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') === 'XMLHttpRequest';

function respond(bool $ok, string $message = '', array $errors = [], int $code = 200): void
{
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($ok ? 200 : $code);
        header('Content-Type: application/json; charset=UTF-8');
        header('Cache-Control: no-store');
        echo json_encode([
            'ok'       => $ok,
            'message'  => $message,
            'errors'   => (object) $errors,
            'redirect' => $ok ? '/thank-you' : null,
        ]);
        exit;
    }
    if ($ok) {
        header('Location: /thank-you', true, 303);
    } else {
        $back = '/contact';
        $ref = $_SERVER['HTTP_REFERER'] ?? '';
        $host = parse_url(SITE_URL, PHP_URL_HOST);
        if ($ref && (parse_url($ref, PHP_URL_HOST) === $host || parse_url($ref, PHP_URL_HOST) === ($_SERVER['HTTP_HOST'] ?? ''))) {
            $back = strtok($ref, '?#');
        }
        header('Location: ' . $back . '?form_error=1#estimate', true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contact', true, 303);
    exit;
}

$smsHtml = '<a href="' . e(sms_link()) . '">' . e(PHONE_DISPLAY) . '</a>';

// ---------------------------------------------------------------------------
// Anti-spam
// ---------------------------------------------------------------------------
// 1) Honeypot: silently accept (bots think it worked)
if (!empty($_POST['website'])) {
    respond(true);
}
// 2) Signed time token (blocks direct posts and instant bot submits)
if (!form_token_valid((string) ($_POST['token'] ?? ''))) {
    respond(false, 'Please wait a few seconds and try again (or refresh the page). You can also text us at ' . $smsHtml . '.', [], 400);
}
// 3) Simple per-IP rate limit: max 5 submissions / 10 minutes
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$rlDir = ROOT_DIR . '/data/ratelimit';
if (!is_dir($rlDir)) {
    @mkdir($rlDir, 0755, true);
}
$rlFile = $rlDir . '/' . hash('sha256', $ip . form_secret()) . '.json';
$now = time();
$hits = [];
if (is_file($rlFile)) {
    $hits = json_decode((string) @file_get_contents($rlFile), true) ?: [];
}
$hits = array_values(array_filter($hits, fn($t) => $t > $now - 600));
if (count($hits) >= 5) {
    respond(false, 'Too many requests. Please text us at ' . $smsHtml . '.', [], 429);
}

// ---------------------------------------------------------------------------
// Validation
// ---------------------------------------------------------------------------
$in = function (string $k, int $max = 200): string {
    $v = trim((string) ($_POST[$k] ?? ''));
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr($v, 0, $max);
};

$data = [
    'name'         => $in('name', 80),
    'phone'        => $in('phone', 25),
    'email'        => $in('email', 120),
    'city'         => $in('city', 60),
    'service'      => $in('service', 60),
    'message'      => $in('message', 2000),
    'contact_pref' => $in('contact_pref', 20) ?: 'Text',
    'page_url'     => $in('page_url', 300),
    'form_id'      => $in('form_id', 40),
    'utm'          => $in('utm', 900),
];

$errors = [];
if (mb_strlen($data['name']) < 2) {
    $errors['name'] = 'Please enter your name.';
}
$digits = preg_replace('/\D/', '', $data['phone']);
if (strlen($digits) === 11 && $digits[0] === '1') {
    $digits = substr($digits, 1);
}
if (strlen($digits) !== 10) {
    $errors['phone'] = 'Please enter a valid 10-digit US phone number.';
} else {
    $data['phone'] = sprintf('(%s) %s-%s', substr($digits, 0, 3), substr($digits, 3, 3), substr($digits, 6));
}
if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Please enter a valid e-mail address.';
}
if ($data['city'] === '') {
    $errors['city'] = 'Please tell us where the project is.';
}
$allowedServices = array_merge(array_column($SERVICES, 'nav'), ['Other tile project']);
if (!in_array($data['service'], $allowedServices, true)) {
    $errors['service'] = 'Please choose a service.';
}
if (!in_array($data['contact_pref'], ['Text', 'Call', 'E-mail'], true)) {
    $data['contact_pref'] = 'Text';
}
// Link spam in message
if (preg_match_all('~https?://|www\.~i', $data['message']) > 2) {
    $errors['message'] = 'Please remove links from your message.';
}
if ($errors) {
    respond(false, 'Please fix the highlighted fields.', $errors, 422);
}

// Count only valid submissions toward the rate limit
$hits[] = $now;
@file_put_contents($rlFile, json_encode($hits), LOCK_EX);

$utm = json_decode($data['utm'], true);
$utm = is_array($utm) ? $utm : [];
$source = $utm['utm_source'] ?? (isset($utm['gclid']) ? 'google-ads' : (isset($utm['fbclid']) ? 'facebook' : ($utm['ref'] ?? 'direct')));

// ---------------------------------------------------------------------------
// Save backup (CSV)
// ---------------------------------------------------------------------------
$saved = false;
if (SAVE_LEADS_CSV) {
    $csv = ROOT_DIR . '/data/leads.csv';
    $isNew = !is_file($csv);
    $fh = @fopen($csv, 'ab');
    if ($fh) {
        flock($fh, LOCK_EX);
        $safe = function ($v) {
            $v = (string) $v;
            return preg_match('/^[=+\-@\t\r]/', $v) ? "'" . $v : $v; // CSV-injection guard
        };
        if ($isNew) {
            fputcsv($fh, ['date', 'name', 'phone', 'email', 'city', 'service', 'contact_pref', 'message', 'source', 'page', 'utm', 'ip']);
        }
        fputcsv($fh, array_map($safe, [
            date('Y-m-d H:i:s'), $data['name'], $data['phone'], $data['email'], $data['city'],
            $data['service'], $data['contact_pref'], $data['message'], $source, $data['page_url'], $data['utm'], $ip,
        ]));
        flock($fh, LOCK_UN);
        fclose($fh);
        $saved = true;
    }
}

// ---------------------------------------------------------------------------
// E-mail to the business
// ---------------------------------------------------------------------------
$rows = [
    'Name'          => $data['name'],
    'Phone'         => $data['phone'],
    'E-mail'        => $data['email'] ?: '—',
    'City / ZIP'    => $data['city'],
    'Service'       => $data['service'],
    'Prefers'       => $data['contact_pref'],
    'Project'       => $data['message'] ?: '—',
    'Lead source'   => $source,
    'Page'          => $data['page_url'],
];
$tableRows = '';
$text = "NEW ESTIMATE REQUEST — " . SITE_NAME . "\n\n";
foreach ($rows as $k => $v) {
    $tableRows .= '<tr><td style="padding:8px 12px;background:#f3f6fa;font-weight:600;white-space:nowrap;vertical-align:top">' . e($k)
        . '</td><td style="padding:8px 12px;vertical-align:top">' . nl2br(e($v)) . '</td></tr>';
    $text .= $k . ': ' . $v . "\n";
}
$smsTo = 'sms:+1' . $digits;
$html = '<!doctype html><html><body style="margin:0;background:#eef2f7;font-family:Arial,Helvetica,sans-serif;color:#0e1a2e">'
    . '<div style="max-width:600px;margin:0 auto;background:#fff">'
    . '<div style="background:#01183A;padding:20px 24px;color:#fbe88a;font-size:20px;font-weight:bold">New Free Estimate Request</div>'
    . '<div style="height:5px;background:#d4a23a"></div>'
    . '<div style="padding:20px 24px">'
    . '<p style="margin:0 0 16px">You received a new lead from the website. Reply fast — speed wins jobs!</p>'
    . '<table cellspacing="0" cellpadding="0" style="width:100%;border-collapse:collapse;font-size:15px">' . $tableRows . '</table>'
    . '<p style="margin:24px 0 8px"><a href="' . e($smsTo) . '" style="display:inline-block;background:#d4a23a;color:#01183A;padding:12px 20px;border-radius:24px;text-decoration:none;font-weight:bold">Text ' . e($data['name']) . '</a> &nbsp; '
    . '<a href="tel:+1' . e($digits) . '" style="display:inline-block;background:#01183A;color:#fff;padding:12px 20px;border-radius:24px;text-decoration:none;font-weight:bold">Call</a></p>'
    . '</div></div></body></html>';

$subject = 'New estimate request: ' . $data['service'] . ' — ' . $data['name'] . ' (' . $data['city'] . ')';
$sent = send_mail(LEAD_TO, $subject, $html, $text, $data['email'], $data['name']);

// ---------------------------------------------------------------------------
// Optional: webhook (CRM / Zapier / Make)
// ---------------------------------------------------------------------------
if (LEAD_WEBHOOK_URL !== '') {
    $payload = json_encode(array_merge($data, ['source' => $source, 'date' => date('c')]));
    if (function_exists('curl_init')) {
        $ch = curl_init(LEAD_WEBHOOK_URL);
        curl_setopt_array($ch, [
            CURLOPT_POST           => true,
            CURLOPT_POSTFIELDS     => $payload,
            CURLOPT_HTTPHEADER     => ['Content-Type: application/json'],
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => 6,
        ]);
        $hookOk = curl_exec($ch) !== false && curl_getinfo($ch, CURLINFO_HTTP_CODE) < 400;
        curl_close($ch);
        $sent = $sent || $hookOk;
    }
}

// ---------------------------------------------------------------------------
// Auto-reply to the visitor
// ---------------------------------------------------------------------------
if ($sent && SEND_AUTOREPLY && $data['email'] !== '') {
    $first = e(explode(' ', $data['name'])[0]);
    $arHtml = '<!doctype html><html><body style="margin:0;background:#eef2f7;font-family:Arial,Helvetica,sans-serif;color:#0e1a2e">'
        . '<div style="max-width:600px;margin:0 auto;background:#fff">'
        . '<div style="background:#01183A;padding:24px;text-align:center"><img src="' . e(url('assets/img/logo-stacked-gold.png')) . '" alt="' . e(SITE_NAME) . '" width="180" style="max-width:180px;height:auto"></div>'
        . '<div style="height:5px;background:#d4a23a"></div>'
        . '<div style="padding:24px;font-size:15px;line-height:1.6">'
        . '<p>Hi ' . $first . ',</p>'
        . '<p>Thank you for contacting <strong>' . e(SITE_NAME) . '</strong>! We received your request for a <strong>free estimate</strong> (' . e($data['service']) . ') and will reach out shortly to schedule a visit.</p>'
        . '<p>Want to speed things up? Text a few photos of your space to <a href="' . e(sms_link()) . '">' . e(PHONE_DISPLAY) . '</a>.</p>'
        . '<p style="margin-top:24px">— Renato &amp; Anderson<br>' . e(SITE_NAME) . '</p>'
        . '</div></div></body></html>';
    $arText = "Hi {$first},\n\nThank you for contacting " . SITE_NAME . "! We received your request for a free estimate ({$data['service']}) and will reach out shortly.\n\nText photos of your space to " . PHONE_DISPLAY . ".\n\n— Renato & Anderson\n" . SITE_NAME;
    send_mail($data['email'], 'We received your free estimate request — ' . SITE_NAME, $arHtml, $arText, EMAIL_PUBLIC, SITE_NAME);
}

if ($sent || $saved) {
    if (!$sent) {
        error_log('[RA send] Lead saved to CSV but e-mail delivery failed. Check MAIL_FROM / SMTP settings in includes/config.php');
    }
    respond(true, 'Thank you!');
}

respond(false, 'Sorry, we could not send your request right now. Please text us at ' . $smsHtml . '.', [], 500);
