<?php
declare(strict_types=1);

/*
 * Guardians Home Health Care — inquiry endpoint. PHP 7.4+ (8.1+ recommended).
 * Recipient, subject and company name are fixed on the server.
 *
 * Delivery: if guardian-mail-config.php exists (preferably ONE LEVEL ABOVE
 * public_html), messages are sent through authenticated SMTP (recommended on
 * Hostinger). Otherwise PHP mail() is used. See INSTALLATION.md.
 */
const RECIPIENT = 'guardianshomehealthllc@gmail.com';
const COMPANY = 'Guardians Home Health Care';
const PHONE = '(321) 977-3169';
const MAX_BODY_BYTES = 32768;
const MIN_INTERVAL_SECONDS = 60;
const MIN_FILL_SECONDS = 2;
const CONSENT_VERSION = '2026-10-08';
/* Published hostname, without https://, www or a path. Set to '' to accept any host (e.g. a temporary preview domain). */
const SITE_DOMAIN = 'guardianshomehelphllc.com';

ini_set('display_errors', '0');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
header('X-Robots-Tag: noindex, nofollow');

$wantsJson = stripos((string) ($_SERVER['HTTP_ACCEPT'] ?? ''), 'application/json') !== false;

/** Absolute path prefix of this folder on the site, so the HTML fallback also works in a subfolder. */
function site_base(): string
{
    $dir = str_replace('\\', '/', dirname((string) ($_SERVER['SCRIPT_NAME'] ?? '/send-form.php')));
    return rtrim($dir, '/') . '/';
}

function reply(int $status, bool $success, string $message): void
{
    global $wantsJson;
    http_response_code($status);
    if ($wantsJson) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(['success' => $success, 'data' => ['message' => $message]], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        exit;
    }
    /* Plain HTML page for visitors whose browser did not run JavaScript. */
    header('Content-Type: text/html; charset=utf-8');
    $base = htmlspecialchars(site_base(), ENT_QUOTES, 'UTF-8');
    $title = $success ? 'Thank you' : 'We could not send your request';
    $class = $success ? 'success' : 'error';
    $text = htmlspecialchars($message, ENT_QUOTES, 'UTF-8');
    echo '<!DOCTYPE html><html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        . '<meta name="robots" content="noindex"><title>' . $title . ' | Guardians Home Health Care</title>'
        . '<link rel="icon" type="image/png" href="' . $base . 'assets/images/favicon.png">'
        . '<link rel="stylesheet" href="' . $base . 'assets/styles.css?v=20261008"></head><body>'
        . '<main id="main" class="section"><div class="container"><span class="eyebrow">Guardians Home Health Care</span>'
        . '<h1>' . $title . '</h1><p class="form-message ' . $class . ' mt-24">' . $text . '</p>'
        . '<div class="actions mt-24"><a class="btn" href="' . $base . '">Return to the website</a>'
        . '<a class="btn outline" href="tel:+13219773169">Call ' . PHONE . '</a></div></div></main></body></html>';
    exit;
}

set_exception_handler(function (Throwable $error): void {
    error_log('Guardian inquiry endpoint: ' . get_class($error));
    reply(500, false, 'We could not send your request right now. Please call ' . PHONE . '.');
});

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    reply(405, false, 'Please submit your request using the website form.');
}

$size = (int) ($_SERVER['CONTENT_LENGTH'] ?? 0);
if ($size <= 0 || $size > MAX_BODY_BYTES || !empty($_FILES)) {
    reply(413, false, 'Your request is too large or contains an attachment.');
}

/* ---------- Optional private configuration (SMTP credentials) ---------- */
$config = [];
foreach ([dirname(__DIR__) . '/guardian-mail-config.php', __DIR__ . '/guardian-mail-config.php'] as $configFile) {
    if (@is_file($configFile) && @is_readable($configFile)) {
        $loaded = include $configFile;
        if (is_array($loaded)) {
            $config = $loaded;
            break;
        }
    }
}
$siteDomain = strtolower(trim((string) ($config['site_domain'] ?? SITE_DOMAIN)));
$siteDomain = preg_replace('/^(https?:\/\/)?(www\.)?/', '', rtrim($siteDomain, '/'));

/* ---------- Same-site request checks ---------- */
$requestHost = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
if (!preg_match('/\A[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?(?::[0-9]{1,5})?\z/D', $requestHost)) {
    reply(403, false, 'Please submit your request from this website.');
}
$requestDomain = preg_replace('/:[0-9]+$/', '', $requestHost);
if ($siteDomain !== '' && $requestDomain !== $siteDomain && $requestDomain !== 'www.' . $siteDomain) {
    reply(403, false, 'Please submit your request from this website.');
}

/*
 * Require a same-host browser Origin; Referer is a fallback only if absent.
 * Only the host is compared: behind Hostinger CDN/Cloudflare the PHP side may
 * see plain HTTP while the visitor uses HTTPS, so the scheme is not reliable.
 */
$origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? '');
$source = ($origin !== '' && $origin !== 'null') ? $origin : (string) ($_SERVER['HTTP_REFERER'] ?? '');
$parsed = $source !== '' ? parse_url($source) : false;
if (!$parsed || empty($parsed['host']) || !in_array(strtolower($parsed['scheme'] ?? ''), ['http', 'https'], true)) {
    reply(403, false, 'Please submit your request from this website.');
}
$originDomain = strtolower($parsed['host']);
if ($originDomain !== $requestDomain || (($_SERVER['HTTP_SEC_FETCH_SITE'] ?? '') === 'cross-site')) {
    reply(403, false, 'Please submit your request from this website.');
}

if (!is_string($_POST['action'] ?? null) || $_POST['action'] !== 'cw_form_submit') {
    /* Browsers without JavaScript post the form directly and do not add "action". */
    if (isset($_POST['action'])) {
        reply(400, false, 'Invalid form request.');
    }
}
if (isset($_POST['botcheck']) && $_POST['botcheck'] !== '') {
    reply(400, false, 'We could not process this request.');
}
$elapsed = $_POST['elapsed'] ?? '';
if (is_string($elapsed) && $elapsed !== '' && ctype_digit($elapsed) && (int) $elapsed < MIN_FILL_SECONDS) {
    reply(422, false, 'Please take a moment to review your information and try again.');
}

/* ---------- Field validation ---------- */
function field(string $key, int $max, bool $multiline = false): string
{
    $value = $_POST[$key] ?? '';
    if (!is_string($value) || strlen($value) > $max || !preg_match('//u', $value)) {
        reply(422, false, 'Please check the information in your form.');
    }
    if (!$multiline && preg_match('/[\r\n]/', $value)) {
        reply(422, false, 'Please check the information in your form.');
    }
    $value = trim(strip_tags($value));
    $value = preg_replace($multiline ? '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/' : '/[\x00-\x1F\x7F]/', '', $value);
    return $value ?? '';
}

function char_count(string $value): int
{
    return (int) preg_match_all('/./us', $value);
}

$name = field('name', 240);
$phone = field('phone', 30);
$email = field('email', 254);
$service = field('service', 60);
$consent = field('consent', 8);
$city = field('city', 240);
$message = field('message', 4800, true);
$sourceForm = field('source', 40);
$labels = [
    'senior-home-care' => 'Senior home care',
    'companion-care' => 'Companion care',
    'respite-care' => 'Family & respite support',
    'day-overnight-care' => 'Day & overnight support',
    'not-sure' => 'Not sure — conversation requested',
];
if (char_count($name) < 2 || char_count($name) > 80 || !preg_match('/\p{L}/u', $name)) {
    reply(422, false, 'Please enter your full name.');
}
$digits = preg_replace('/\D/', '', $phone);
if (!preg_match('/\A[+0-9().\s-]{8,30}\z/D', $phone) || strlen($digits) < 8 || strlen($digits) > 15) {
    reply(422, false, 'Please enter a valid phone number.');
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    reply(422, false, 'Please enter a valid email address.');
}
if (!isset($labels[$service])) {
    reply(422, false, 'Please select a care interest.');
}
if ($consent !== 'yes') {
    reply(422, false, 'Please review and accept the communication consent to submit this form.');
}
if (char_count($city) > 80 || char_count($message) > 1200) {
    reply(422, false, 'Please shorten your city or message.');
}
if (!in_array($sourceForm, ['hero-care', 'contact-care', 'popup-care'], true)) {
    reply(422, false, 'Invalid form source.');
}

/* The site domain provides the sender. The visitor email is Reply-To only. */
$mailDomain = $siteDomain !== '' ? $siteDomain : $requestDomain;
$mailDomain = preg_replace('/^www\./', '', strtolower($mailDomain));
if (!preg_match('/\A[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,63}\z/D', $mailDomain)) {
    reply(503, false, 'Please use the form on the published website or call ' . PHONE . '.');
}

/* ---------- Rate limit (hashed IP + timestamp only, never personal data) ---------- */
function rate_dir(): ?string
{
    $suffix = 'guardian-inquiry-' . substr(hash('sha256', __DIR__), 0, 16);
    $candidates = [
        rtrim(sys_get_temp_dir(), '/\\') . DIRECTORY_SEPARATOR . $suffix,
        dirname(__DIR__) . DIRECTORY_SEPARATOR . '.' . $suffix,
    ];
    foreach ($candidates as $dir) {
        if ((@is_dir($dir) || @mkdir($dir, 0700, true)) && @is_writable($dir)) {
            return $dir;
        }
    }
    return null;
}

$remote = (string) ($_SERVER['REMOTE_ADDR'] ?? 'unknown');
$rateDir = rate_dir();
$rateFile = $rateDir !== null ? $rateDir . DIRECTORY_SEPARATOR . hash('sha256', $remote . '|' . $mailDomain . '|' . RECIPIENT) . '.json' : null;
if ($rateFile !== null && @is_file($rateFile)) {
    $state = json_decode((string) @file_get_contents($rateFile), true);
    $last = is_array($state) ? (int) ($state['last'] ?? 0) : 0;
    $wait = MIN_INTERVAL_SECONDS - (time() - $last);
    if ($wait > 0) {
        header('Retry-After: ' . $wait);
        reply(429, false, 'Please wait one minute before sending another request, or call ' . PHONE . '.');
    }
}
if ($rateDir === null) {
    /* Never lose a real inquiry because temporary storage is unavailable. */
    error_log('Guardian inquiry: rate-limit storage unavailable; continuing without it.');
}

/* ---------- Message ---------- */
$timestamp = gmdate('Y-m-d\TH:i:s\Z');
$subject = 'New home care inquiry | ' . COMPANY;
$body = "New non-medical home care inquiry\n\n"
    . "Name: {$name}\nPhone: {$phone}\nEmail: {$email}\n"
    . "Care interest: {$labels[$service]}\nCity: " . ($city !== '' ? $city : 'Not provided') . "\n"
    . "Message: " . ($message !== '' ? $message : 'Not provided') . "\n\n"
    . "Form: {$sourceForm}\nSubmitted at: {$timestamp}\n"
    . "Communication consent: YES (explicit checkbox)\n"
    . "Consent text version: " . CONSENT_VERSION . "\n"
    . "Consent text: By submitting, you agree to receive calls, text messages and emails from Guardians Home Health Care about your request. Consent is not a condition of purchase. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. See our Terms and Privacy Policy.\n\n"
    . "The visitor requested a conversation; no care arrangement has been booked.\n";

function encode_header(string $value): string
{
    return preg_match('/[^\x20-\x7E]/', $value) ? '=?UTF-8?B?' . base64_encode($value) . '?=' : $value;
}

/** Minimal authenticated SMTP client (SSL on 465 or STARTTLS on 587). Throws on any failure. */
function smtp_send(array $c, string $from, string $to, string $message, string $heloDomain): void
{
    $host = (string) ($c['smtp_host'] ?? '');
    $secure = strtolower((string) ($c['smtp_secure'] ?? 'ssl'));
    $port = (int) ($c['smtp_port'] ?? ($secure === 'ssl' ? 465 : 587));
    if ($host === '' || !in_array($secure, ['ssl', 'tls', 'none'], true)) {
        throw new RuntimeException('SMTP configuration incomplete');
    }
    $context = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true, 'peer_name' => $host, 'SNI_enabled' => true]]);
    $socket = @stream_socket_client(($secure === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $context);
    if (!$socket) {
        throw new RuntimeException('SMTP connect failed (' . $errno . ')');
    }
    stream_set_timeout($socket, 20);
    $command = function (?string $line, array $expected) use ($socket): string {
        if ($line !== null) {
            fwrite($socket, $line . "\r\n");
        }
        $response = '';
        while (($row = fgets($socket, 1024)) !== false) {
            $response .= $row;
            if (strlen($row) < 4 || $row[3] !== '-') {
                break;
            }
        }
        $code = (int) substr($response, 0, 3);
        if (!in_array($code, $expected, true)) {
            $verb = $line === null ? 'GREETING' : strtok($line, ' :');
            throw new RuntimeException('SMTP ' . $verb . ' rejected (' . $code . ')');
        }
        return $response;
    };
    try {
        $command(null, [220]);
        $features = $command('EHLO ' . $heloDomain, [250]);
        if ($secure === 'tls') {
            $command('STARTTLS', [220]);
            $method = STREAM_CRYPTO_METHOD_TLSv1_2_CLIENT;
            if (defined('STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT')) {
                $method |= STREAM_CRYPTO_METHOD_TLSv1_3_CLIENT;
            }
            if (!@stream_socket_enable_crypto($socket, true, $method)) {
                throw new RuntimeException('SMTP STARTTLS failed');
            }
            $features = $command('EHLO ' . $heloDomain, [250]);
        }
        $user = (string) ($c['smtp_user'] ?? '');
        if ($user !== '') {
            $pass = (string) ($c['smtp_pass'] ?? '');
            if (preg_match('/AUTH[ =][^\r\n]*PLAIN/i', $features)) {
                $command('AUTH PLAIN ' . base64_encode("\0" . $user . "\0" . $pass), [235]);
            } else {
                $command('AUTH LOGIN', [334]);
                $command(base64_encode($user), [334]);
                $command(base64_encode($pass), [235]);
            }
        }
        $command('MAIL FROM:<' . $from . '>', [250]);
        $command('RCPT TO:<' . $to . '>', [250, 251]);
        $command('DATA', [354]);
        $data = preg_replace('/^\./m', '..', str_replace(["\r\n", "\r"], "\n", $message));
        $command(str_replace("\n", "\r\n", $data) . "\r\n.", [250]);
        try {
            $command('QUIT', [221]);
        } catch (RuntimeException $ignored) {
        }
    } finally {
        fclose($socket);
    }
}

$useSmtp = !empty($config['smtp_host']);
$fromEmail = (string) ($config['from_email'] ?? '');
if ($fromEmail === '') {
    $fromEmail = $useSmtp && filter_var($config['smtp_user'] ?? '', FILTER_VALIDATE_EMAIL) ? (string) $config['smtp_user'] : 'website@' . $mailDomain;
}
if (!filter_var($fromEmail, FILTER_VALIDATE_EMAIL) || preg_match('/[\r\n]/', $fromEmail)) {
    $fromEmail = 'website@' . $mailDomain;
}

$headerLines = [
    'Date: ' . date('r'),
    'From: ' . COMPANY . ' <' . $fromEmail . '>',
    'Reply-To: ' . $email,
    'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $mailDomain . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    'X-Auto-Response-Suppress: All',
];
$encodedBody = rtrim(chunk_split(base64_encode($body), 76, "\r\n"));

/* _to, subject and from_name from the browser are deliberately ignored. */
$sent = false;
if ($useSmtp) {
    try {
        $fullMessage = implode("\r\n", array_merge($headerLines, ['To: <' . RECIPIENT . '>', 'Subject: ' . encode_header($subject)]))
            . "\r\n\r\n" . $encodedBody;
        smtp_send($config, $fromEmail, RECIPIENT, $fullMessage, $mailDomain);
        $sent = true;
    } catch (Throwable $error) {
        error_log('Guardian inquiry SMTP failed: ' . $error->getMessage() . '; falling back to mail().');
    }
}
if (!$sent && function_exists('mail')) {
    $mailHeaders = implode("\r\n", array_filter($headerLines, function (string $line): bool {
        return strpos($line, 'Date:') !== 0;
    }));
    /* -f sets the envelope sender for SPF alignment; retry without it if the host refuses. */
    $sent = @mail(RECIPIENT, encode_header($subject), $encodedBody, $mailHeaders, '-f' . $fromEmail)
        || @mail(RECIPIENT, encode_header($subject), $encodedBody, $mailHeaders);
}
if (!$sent) {
    error_log('Guardian inquiry delivery failed; no visitor data logged.');
    reply(502, false, 'We could not send your request right now. Please call ' . PHONE . '.');
}

if ($rateFile !== null) {
    @file_put_contents($rateFile, json_encode(['last' => time()]), LOCK_EX);
}
reply(200, true, 'Thank you! Your request has been sent successfully. Our team will follow up with you about your care interests.');
