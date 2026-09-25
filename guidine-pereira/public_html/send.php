<?php
/**
 * Estimate form handler.
 * Validates the request, emails it to LEAD_TO and keeps a CSV backup in /leads.
 * Answers JSON to the JavaScript form and redirects when JavaScript is off.
 */
require __DIR__ . '/includes/functions.php';

$wantsJson = (($_SERVER['HTTP_X_REQUESTED_WITH'] ?? '') === 'XMLHttpRequest')
    || strpos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;

function respond($ok, $message, $errors = [])
{
    global $wantsJson;
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        http_response_code($ok ? 200 : 422);
        echo json_encode(['ok' => $ok, 'message' => $message, 'errors' => $errors, 'redirect' => $ok ? url('thank-you') : null]);
    } else {
        header('Location: ' . ($ok ? url('thank-you') : url('contact') . '?form=error#estimate'), true, 303);
    }
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Location: ' . url('contact'), true, 303);
    exit;
}

function field($key, $max = 200)
{
    $v = isset($_POST[$key]) && is_string($_POST[$key]) ? $_POST[$key] : '';
    $v = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $v));
    return function_exists('mb_substr') ? mb_substr($v, 0, $max) : substr($v, 0, $max);
}

$data = [
    'name'         => field('name', 80),
    'phone'        => field('phone', 20),
    'email'        => field('email', 120),
    'city'         => field('city', 60),
    'service'      => field('service', 80),
    'timeline'     => field('timeline', 40),
    'contact_pref' => field('contact_pref', 10),
    'message'      => field('message', 2000),
    'page'         => field('page', 60),
    'utm_source'   => field('utm_source', 100),
    'utm_medium'   => field('utm_medium', 100),
    'utm_campaign' => field('utm_campaign', 150),
    'utm_term'     => field('utm_term', 150),
    'gclid'        => field('gclid', 200),
    'fbclid'       => field('fbclid', 200),
];

/* Spam checks: hidden field must stay empty and the form must not be sent instantly. */
$ts = (int) field('ts', 12);
if (field('website') !== '' || ($ts && time() - $ts < 3)) {
    respond(true, 'Thank you.');
}

/* Simple rate limit: 5 requests per IP every 10 minutes. */
$ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
$rlDir = __DIR__ . '/leads/.ratelimit';
if (!is_dir($rlDir)) {
    @mkdir($rlDir, 0750, true);
}
$rlFile = $rlDir . '/' . md5($ip);
$hits = array_filter(array_map('intval', is_file($rlFile) ? file($rlFile, FILE_IGNORE_NEW_LINES) : []), function ($t) {
    return $t > time() - 600;
});
if (count($hits) >= 5) {
    respond(false, 'Too many requests. Please call or text us at ' . PHONE_DISPLAY . '.');
}
$hits[] = time();
@file_put_contents($rlFile, implode("\n", $hits));

/* Validation */
$errors = [];
if (strlen($data['name']) < 2) {
    $errors['name'] = 'Please enter your name.';
}
$digits = preg_replace('/\D/', '', $data['phone']);
if (strlen($digits) < 10 || strlen($digits) > 15) {
    $errors['phone'] = 'Please enter a valid phone number.';
}
if ($data['email'] !== '' && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    $errors['email'] = 'Please enter a valid email address.';
}
if (strlen($data['city']) < 2) {
    $errors['city'] = 'Tell us where the project is.';
}
if ($data['service'] === '') {
    $errors['service'] = 'Please choose a service.';
}
if ($errors) {
    respond(false, 'Please check the highlighted fields.', $errors);
}

/* Build the email */
$labels = [
    'name' => 'Name', 'phone' => 'Phone', 'email' => 'Email', 'city' => 'City / ZIP',
    'service' => 'Service', 'timeline' => 'Start', 'contact_pref' => 'Preferred contact', 'message' => 'Project details',
];
$tracking = array_filter([
    'Page' => $data['page'], 'utm_source' => $data['utm_source'], 'utm_medium' => $data['utm_medium'],
    'utm_campaign' => $data['utm_campaign'], 'utm_term' => $data['utm_term'], 'gclid' => $data['gclid'], 'fbclid' => $data['fbclid'],
]);

$subject = 'New estimate request: ' . $data['service'] . ' - ' . $data['name'];
$text = "New estimate request from the website\n\n";
$rows = '';
foreach ($labels as $k => $label) {
    $v = $data[$k] !== '' ? $data[$k] : '-';
    $text .= $label . ': ' . $v . "\n";
    $rows .= '<tr><td style="padding:8px 12px;border-bottom:1px solid #e5e5e5;color:#575757;width:150px;vertical-align:top">' . e($label)
        . '</td><td style="padding:8px 12px;border-bottom:1px solid #e5e5e5;color:#1e1e1e">' . nl2br(e($v)) . '</td></tr>';
}
$trackRows = '';
if ($tracking) {
    $text .= "\nSource\n";
    foreach ($tracking as $k => $v) {
        $text .= $k . ': ' . $v . "\n";
        $trackRows .= e($k) . ': ' . e($v) . '<br>';
    }
}
$text .= "\nSent " . date('Y-m-d H:i') . ' from ' . site_url();

$telDigits = preg_replace('/[^\d+]/', '', $data['phone']);
$html = '<!doctype html><html><body style="margin:0;background:#f3f4f3;font-family:Segoe UI,Arial,sans-serif">'
    . '<table width="100%" cellpadding="0" cellspacing="0" style="background:#f3f4f3;padding:24px 0"><tr><td align="center">'
    . '<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff;border-top:4px solid #2a8255">'
    . '<tr><td style="background:#1e1e1e;padding:20px 24px;color:#fdfffe;font-size:18px;font-weight:bold">New estimate request</td></tr>'
    . '<tr><td style="padding:16px 12px"><table width="100%" cellpadding="0" cellspacing="0" style="font-size:15px">' . $rows . '</table></td></tr>'
    . '<tr><td style="padding:0 24px 20px"><a href="tel:' . e($telDigits) . '" style="display:inline-block;background:#2a8255;color:#ffffff;padding:12px 20px;text-decoration:none;font-weight:bold">Call ' . e($data['name']) . '</a></td></tr>'
    . ($trackRows ? '<tr><td style="padding:12px 24px;font-size:12px;color:#575757;border-top:1px solid #e5e5e5">' . $trackRows . '</td></tr>' : '')
    . '</table></td></tr></table></body></html>';

/* Save a backup copy first, so a lead is never lost if email delivery fails. */
$saved = false;
if (SAVE_LEADS_CSV) {
    $csv = __DIR__ . '/leads/leads.csv';
    $new = !is_file($csv);
    if ($fh = @fopen($csv, 'a')) {
        if (flock($fh, LOCK_EX)) {
            if ($new) {
                fputcsv($fh, array_merge(['date'], array_keys($data), ['ip']));
            }
            $row = array_map(function ($v) {
                return preg_match('/^[=+\-@]/', $v) ? "'" . $v : $v; // keep spreadsheet formulas out
            }, array_values($data));
            $saved = fputcsv($fh, array_merge([date('Y-m-d H:i:s')], $row, [$ip])) !== false;
            flock($fh, LOCK_UN);
        }
        fclose($fh);
    }
}

$host = preg_replace('/^www\./', '', parse_url(site_url(), PHP_URL_HOST) ?: 'localhost');
$from = MAIL_FROM !== '' ? MAIL_FROM : 'no-reply@' . $host;
$sent = send_mail(LEAD_TO, $subject, $html, $text, $from, BUSINESS_SHORT . ' Website', $data['email'] ?: null, $data['name']);

if (!$sent) {
    @file_put_contents(__DIR__ . '/leads/mail-errors.log', date('c') . ' mail failed for ' . $data['name'] . ' ' . $data['phone'] . "\n", FILE_APPEND);
}

if ($sent || $saved) {
    respond(true, 'Thank you. We received your request.');
}
respond(false, 'We could not send your request. Please call or text us at ' . PHONE_DISPLAY . '.');


/* ------------------------------------------------------------------ */

function encode_header($s)
{
    return preg_match('/[^\x20-\x7E]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
}

function send_mail($to, $subject, $html, $text, $from, $fromName, $replyTo = null, $replyName = '')
{
    $boundary = 'b' . bin2hex(random_bytes(12));
    $headers = [
        'From: ' . encode_header($fromName) . ' <' . $from . '>',
        'MIME-Version: 1.0',
        'Content-Type: multipart/alternative; boundary="' . $boundary . '"',
        'X-Mailer: PHP',
    ];
    if ($replyTo) {
        $headers[] = 'Reply-To: ' . encode_header(str_replace(['"', "\r", "\n"], '', $replyName)) . ' <' . $replyTo . '>';
    }
    $body = "--$boundary\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($text))
        . "--$boundary\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($html))
        . "--$boundary--\r\n";
    $subjectEnc = encode_header($subject);

    if (SMTP_HOST !== '') {
        return smtp_send($to, $subjectEnc, $body, $headers, $from);
    }
    if (!function_exists('mail')) {
        return false;
    }
    return @mail($to, $subjectEnc, $body, implode("\r\n", $headers), '-f' . $from);
}

/** Minimal authenticated SMTP client (SSL on 465 or STARTTLS on 587). */
function smtp_send($to, $subject, $body, array $headers, $from)
{
    $secure = strtolower(SMTP_SECURE);
    $remote = ($secure === 'ssl' ? 'ssl://' : 'tcp://') . SMTP_HOST . ':' . SMTP_PORT;
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'SNI_enabled' => true]]);
    $fp = @stream_socket_client($remote, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) {
        return false;
    }
    stream_set_timeout($fp, 15);
    $read = function () use ($fp) {
        $out = '';
        while (($line = fgets($fp, 515)) !== false) {
            $out .= $line;
            if (isset($line[3]) && $line[3] === ' ') {
                break;
            }
        }
        return $out;
    };
    $cmd = function ($c, $expect) use ($fp, $read) {
        if ($c !== null) {
            fwrite($fp, $c . "\r\n");
        }
        $r = $read();
        return in_array(substr($r, 0, 3), (array) $expect, true);
    };
    $ehlo = 'EHLO ' . (gethostname() ?: 'localhost');
    $ok = $cmd(null, '220') && $cmd($ehlo, '250');
    if ($ok && $secure === 'tls') {
        $ok = $cmd('STARTTLS', '220')
            && stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)
            && $cmd($ehlo, '250');
    }
    $ok = $ok && $cmd('AUTH LOGIN', '334') && $cmd(base64_encode(SMTP_USER), '334') && $cmd(base64_encode(SMTP_PASS), '235');
    $ok = $ok && $cmd('MAIL FROM:<' . $from . '>', '250');
    foreach (array_map('trim', explode(',', $to)) as $rcpt) {
        $ok = $ok && $cmd('RCPT TO:<' . $rcpt . '>', ['250', '251']);
    }
    if ($ok && $cmd('DATA', '354')) {
        $msg = 'To: ' . $to . "\r\nSubject: " . $subject . "\r\nDate: " . date('r') . "\r\nMessage-ID: <" . bin2hex(random_bytes(8)) . '@' . SMTP_HOST . ">\r\n"
            . implode("\r\n", $headers) . "\r\n\r\n" . $body;
        $msg = preg_replace('/^\./m', '..', $msg);
        $ok = $cmd($msg . "\r\n.", '250');
    } else {
        $ok = false;
    }
    fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}
