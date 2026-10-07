<?php
/**
 * Estimate form handler. Answers AJAX requests with JSON and plain form posts with a redirect.
 * Settings live in includes/config.php.
 */
require __DIR__ . '/includes/config.php';
require __DIR__ . '/includes/mailer.php';

$wantsJson = stripos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function e(string $s): string
{
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}

function respond(bool $ok, string $message = '', array $errors = [], int $code = 200): void
{
    global $wantsJson;
    if ($wantsJson) {
        http_response_code($ok ? 200 : $code);
        header('Content-Type: application/json; charset=UTF-8');
        header('Cache-Control: no-store');
        echo json_encode(['ok' => $ok, 'message' => $message, 'errors' => (object) $errors]);
        exit;
    }
    if ($ok) {
        header('Location: /contact/?sent=1', true, 303);
        exit;
    }
    $back = '/contact/';
    $ref = (string) ($_SERVER['HTTP_REFERER'] ?? '');
    $refHost = parse_url($ref, PHP_URL_HOST);
    if ($ref !== '' && ($refHost === parse_url(SITE_URL, PHP_URL_HOST) || $refHost === ($_SERVER['HTTP_HOST'] ?? ''))) {
        $back = strtok((string) parse_url($ref, PHP_URL_PATH), '?#') ?: '/contact/';
    }
    header('Location: ' . $back . '?form_error=1#estimate', true, 303);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: /contact/', true, 303);
    exit;
}

$callHtml = '<a href="' . PHONE_TEL . '">' . PHONE_DISPLAY . '</a>';

// ------------------------------------------------------------------ anti-spam
// Honeypot: bots that fill the hidden field get a fake success.
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    respond(true);
}
// Submitted faster than a person could fill the form (field set by the page script).
$started = (int) ($_POST['started'] ?? 0);
if ($started > 0 && (int) round(microtime(true) * 1000) - $started < 2500) {
    respond(true);
}
// Per-IP rate limit.
$dataDir = __DIR__ . '/data';
if (!is_dir($dataDir)) {
    @mkdir($dataDir, 0755, true);
}
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$rlFile = $dataDir . '/rl-' . hash('sha256', $ip . __DIR__) . '.json';
$now = time();
$hits = is_file($rlFile) ? (json_decode((string) @file_get_contents($rlFile), true) ?: []) : [];
$hits = array_values(array_filter($hits, fn($t) => $t > $now - 600));
if (count($hits) >= RATE_LIMIT) {
    respond(false, 'Too many requests. Please call us at ' . $callHtml . '.', [], 429);
}

// ------------------------------------------------------------------ validation
$in = function (string $k, int $max = 200): string {
    $v = trim((string) ($_POST[$k] ?? ''));
    $v = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v) ?? '';
    return mb_substr($v, 0, $max);
};
$pick = function (string $v, array $allowed): string {
    return in_array($v, $allowed, true) ? $v : '';
};

$data = [
    'name'           => $in('name', 80),
    'phone'          => $in('phone', 25),
    'email'          => $in('email', 120),
    'zip'            => $in('zip', 10),
    'service'        => $pick($in('service', 40), ['Recurring Cleaning', 'Deep Cleaning', 'Move-In Cleaning',
                                                   'Move-Out Cleaning', 'Carpet Cleaning', 'Not Sure Yet']),
    'frequency'      => $pick($in('frequency', 20), ['Weekly', 'Biweekly', 'Monthly', 'One-Time']),
    'bedrooms'       => $pick($in('bedrooms', 12), ['1', '2', '3', '4', '5 or more']),
    'bathrooms'      => $pick($in('bathrooms', 12), ['1', '1.5', '2', '2.5', '3', '3.5', '4 or more']),
    'contact_method' => $pick($in('contact_method', 20), ['Phone call', 'Email']) ?: 'Phone call',
    'message'        => $in('message', 1500),
    'page'           => $in('page', 60),
    'page_url'       => $in('page_url', 300),
];

$errors = [];
if (mb_strlen($data['name']) < 2) {
    $errors['name'] = 'Please enter your name.';
}
$digits = preg_replace('/\D/', '', $data['phone']);
if (strlen($digits) === 11 && $digits[0] === '1') {
    $digits = substr($digits, 1);
}
if (!preg_match('/^[2-9]\d{2}[2-9]\d{6}$/', $digits)) {
    $errors['phone'] = 'Please enter a valid 10-digit U.S. phone number.';
} else {
    $data['phone'] = sprintf('(%s) %s-%s', substr($digits, 0, 3), substr($digits, 3, 3), substr($digits, 6));
}
if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Please enter a valid email address.';
} elseif ($data['email'] === '' && $data['contact_method'] === 'Email') {
    $errors['email'] = 'Please enter your email so we can reply by email.';
}
if (!preg_match('/^\d{5}$/', $data['zip'])) {
    $errors['zip'] = 'Please enter a 5-digit ZIP code.';
}
if ($data['service'] === '') {
    $errors['service'] = 'Please choose the type of cleaning.';
}
if (preg_match_all('~https?://|www\.~i', $data['message']) > 2) {
    $errors['message'] = 'Please remove links from your message.';
}
if ($errors) {
    respond(false, 'Please check the highlighted fields.', $errors, 422);
}

$hits[] = $now;
@file_put_contents($rlFile, json_encode($hits), LOCK_EX);

// ------------------------------------------------------------------ backup copy
if (SAVE_LEADS_CSV) {
    $csv = $dataDir . '/leads.csv';
    $isNew = !is_file($csv);
    if ($fh = @fopen($csv, 'ab')) {
        flock($fh, LOCK_EX);
        // Prefix values that spreadsheets would read as formulas.
        $safe = fn($v) => preg_match('/^[=+\-@]/', (string) $v) ? "'" . $v : (string) $v;
        if ($isNew) {
            fputcsv($fh, ['Date', 'Name', 'Phone', 'Email', 'ZIP', 'Service', 'Frequency', 'Bedrooms', 'Bathrooms',
                          'Contact method', 'Message', 'Page']);
        }
        fputcsv($fh, array_map($safe, [date('Y-m-d H:i'), $data['name'], $data['phone'], $data['email'], $data['zip'],
                                        $data['service'], $data['frequency'], $data['bedrooms'], $data['bathrooms'],
                                        $data['contact_method'], $data['message'], $data['page']]));
        flock($fh, LOCK_UN);
        fclose($fh);
    }
}

// ------------------------------------------------------------------ e-mail to the business
$rows = [
    'Name' => $data['name'], 'Phone' => $data['phone'], 'Email' => $data['email'] ?: '—', 'ZIP code' => $data['zip'],
    'Type of cleaning' => $data['service'], 'Frequency' => $data['frequency'] ?: '—',
    'Bedrooms' => $data['bedrooms'] ?: '—', 'Bathrooms' => $data['bathrooms'] ?: '—',
    'Preferred contact' => $data['contact_method'], 'Details' => $data['message'] ?: '—',
    'Sent from' => trim($data['page'] . ' ' . $data['page_url']),
];
$tel = 'tel:+1' . $digits;
$html = '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#16212c">'
    . '<h2 style="margin:0 0 6px;font-size:20px">New estimate request</h2>'
    . '<p style="margin:0 0 16px">Call back: <a href="' . e($tel) . '" style="font-weight:bold">' . e($data['phone']) . '</a></p>'
    . '<table cellpadding="8" cellspacing="0" style="border-collapse:collapse;max-width:640px">';
$text = "New estimate request\n\n";
foreach ($rows as $label => $value) {
    $html .= '<tr><td style="border-bottom:1px solid #e2d9ca;font-weight:bold;vertical-align:top;white-space:nowrap">'
        . e($label) . '</td><td style="border-bottom:1px solid #e2d9ca">' . nl2br(e($value)) . '</td></tr>';
    $text .= $label . ': ' . $value . "\n";
}
$html .= '</table><p style="color:#66707a;font-size:12px;margin-top:16px">Sent ' . e(date('M j, Y g:i A'))
    . ' from riocleanings.com</p></div>';

$subject = 'New estimate request: ' . $data['service'] . ' - ' . $data['name'];
$sent = send_mail(LEAD_TO, $subject, $html, $text, $data['email'], $data['name']);

if (LEAD_WEBHOOK_URL !== '') {
    $ctx = stream_context_create(['http' => ['method' => 'POST', 'timeout' => 6,
        'header' => "Content-Type: application/json\r\n", 'content' => json_encode($data)]]);
    @file_get_contents(LEAD_WEBHOOK_URL, false, $ctx);
}

if (!$sent) {
    error_log('[Rio form] mail delivery failed' . (SAVE_LEADS_CSV ? '; request kept in data/leads.csv' : ''));
    respond(false, 'Sorry, your request could not be sent right now. Please call us at ' . $callHtml . '.', [], 500);
}

// ------------------------------------------------------------------ confirmation to the visitor
if (SEND_AUTOREPLY && $data['email'] !== '') {
    $first = explode(' ', $data['name'])[0];
    $reply = "Hi {$first},\n\nThank you for contacting Rio Cleaning Services. We received your request for "
        . strtolower($data['service']) . " and will get back to you soon to confirm the details and prepare your estimate.\n\n"
        . 'If you need us sooner, call ' . PHONE_DISPLAY . ".\n\nRio Cleaning Services\n" . SITE_URL . "\n";
    $replyHtml = '<div style="font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#16212c">'
        . nl2br(e($reply)) . '</div>';
    send_mail($data['email'], 'We received your estimate request - Rio Cleaning Services', $replyHtml, $reply,
              LEAD_TO, SITE_NAME);
}

respond(true, 'Thank you! Your estimate request was sent.');
