<?php
declare(strict_types=1);

ini_set('display_errors', '0');
require_once __DIR__ . '/site-settings.php';
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function neat_response(bool $success, string $message, int $status = 200): void
{
    http_response_code($status);
    echo json_encode(['success' => $success, 'data' => ['message' => $message]], JSON_UNESCAPED_SLASHES);
    exit;
}

function neat_field(string $key, int $max, bool $multiline = false): string
{
    $value = $_POST[$key] ?? '';
    if (!is_string($value) || strlen($value) > $max) {
        neat_response(false, 'Please check your form details and try again.', 422);
    }
    if (!$multiline && preg_match('/[\r\n\x00-\x1F\x7F]/', $value)) {
        neat_response(false, 'Please check your form details and try again.', 422);
    }
    $value = trim(strip_tags($value));
    if ($multiline) {
        $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/', '', $value) ?? '';
    }
    return $value;
}

function neat_origin_parts(string $origin): ?array
{
    $parsed = parse_url($origin);
    if (!is_array($parsed) || empty($parsed['host']) || empty($parsed['scheme'])
        || isset($parsed['user']) || isset($parsed['pass'])) {
        return null;
    }
    $scheme = strtolower($parsed['scheme']);
    if (!in_array($scheme, ['http', 'https'], true)) return null;
    return [$scheme, strtolower($parsed['host']), $parsed['port'] ?? ($scheme === 'https' ? 443 : 80)];
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    neat_response(false, 'This endpoint accepts POST requests only.', 405);
}

$size = (int) ($_SERVER['CONTENT_LENGTH'] ?? 0);
if ($size > 32768 || $size < 0) {
    neat_response(false, 'The request is too large.', 413);
}

$contentType = strtolower((string) ($_SERVER['CONTENT_TYPE'] ?? ''));
if (!str_starts_with($contentType, 'multipart/form-data')
    && !str_starts_with($contentType, 'application/x-www-form-urlencoded')) {
    neat_response(false, 'Unsupported form format.', 415);
}
if (!empty($_FILES)) neat_response(false, 'File uploads are not accepted.', 422);
// Check parsed bytes too, for requests without a declared Content-Length.
$allowedFields = ['_to', 'subject', 'from_name', 'form_id', 'botcheck', 'name', 'phone', 'email', 'service', 'location', 'details', 'consent', 'action'];
$parsedBytes = 0;
foreach ($_POST as $fieldName => $fieldValue) {
    if (!in_array($fieldName, $allowedFields, true) || !is_string($fieldValue)) {
        neat_response(false, 'Please check your form details and try again.', 422);
    }
    $parsedBytes += strlen($fieldName) + strlen($fieldValue);
}
if ($parsedBytes > 32768) neat_response(false, 'The request is too large.', 413);

try { $expectedOrigin = neat_origin_parts(neat_site_origin()); }
catch (Throwable $error) { neat_response(false, 'We could not send your request right now.', 500); }
$source = (string) ($_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? ''));
$sourceOrigin = neat_origin_parts($source);
if ($sourceOrigin === null || $sourceOrigin !== $expectedOrigin) {
    neat_response(false, 'Please submit the form from this website.', 403);
}

if (neat_field('action', 40) !== 'cw_form_submit') {
    neat_response(false, 'Invalid form request.', 400);
}
// The honeypot must not be checked. Arrays are rejected as malformed input.
if (isset($_POST['botcheck']) && (!is_string($_POST['botcheck']) || $_POST['botcheck'] !== '')) {
    neat_response(false, 'We could not process this request.', 422);
}

$name = neat_field('name', 100);
$phone = neat_field('phone', 30);
$email = neat_field('email', 254);
$service = neat_field('service', 60);
$location = neat_field('location', 100);
$details = neat_field('details', 2500, true);
$consent = neat_field('consent', 10);
$formId = neat_field('form_id', 50);

// Sanitize reference fields but never use them for the recipient or headers.
neat_field('_to', 254);
neat_field('subject', 150);
neat_field('from_name', 100);

$services = [
    'regular-cleaning' => 'Regular Cleaning',
    'deep-cleaning' => 'Deep Cleaning',
    'airbnb-cleaning' => 'Airbnb Cleaning',
    'move-in-move-out-cleaning' => 'Move-In & Move-Out Cleaning',
    'commercial-cleaning' => 'Commercial Cleaning',
];

if (strlen($name) < 2 || !preg_match('/[\p{L}]/u', $name)) {
    neat_response(false, 'Please enter your full name.', 422);
}
$phoneDigits = preg_replace('/\D/', '', $phone) ?? '';
if (!preg_match('/\A[0-9+().\-\s]+\z/', $phone) || strlen($phoneDigits) < 10 || strlen($phoneDigits) > 15) {
    neat_response(false, 'Please enter a valid phone number, including the area code.', 422);
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    neat_response(false, 'Please enter a valid email address.', 422);
}
if (!isset($services[$service])) neat_response(false, 'Please select a cleaning service.', 422);
if (strlen($location) < 2) neat_response(false, 'Please enter your town or ZIP code.', 422);
if ($consent !== '1') neat_response(false, 'Please confirm the contact consent checkbox.', 422);
$formIds = ['home-quote', 'contact-quote', 'area-quote', 'regular-cleaning-quote', 'deep-cleaning-quote',
    'airbnb-cleaning-quote', 'move-in-move-out-cleaning-quote', 'commercial-cleaning-quote'];
if (!in_array($formId, $formIds, true)) {
    neat_response(false, 'Invalid form source.', 422);
}

// Short, server-side per-IP interval. Locking prevents concurrent bypass.
// Only a hashed identifier and a timestamp are stored, not the form contents.
$remoteIp = (string) ($_SERVER['REMOTE_ADDR'] ?? 'unknown');
$key = hash('sha256', __DIR__ . '|' . $remoteIp);
$rateFile = rtrim(sys_get_temp_dir(), DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'neat-form-' . $key;
$rateHandle = @fopen($rateFile, 'c+');
if (!$rateHandle || !flock($rateHandle, LOCK_EX)) {
    if (is_resource($rateHandle)) fclose($rateHandle);
    neat_response(false, 'We could not send your request right now. Please text (508) 202-8132.', 503);
}
@chmod($rateFile, 0600);
$lastSent = (int) trim((string) stream_get_contents($rateHandle));
$now = time();
if ($lastSent > 0 && $now - $lastSent < 60) {
    flock($rateHandle, LOCK_UN); fclose($rateHandle);
    header('Retry-After: 60');
    neat_response(false, 'Please wait one minute before sending another request.', 429);
}
rewind($rateHandle); ftruncate($rateHandle, 0); fwrite($rateHandle, (string) $now); fflush($rateHandle);
flock($rateHandle, LOCK_UN); fclose($rateHandle);

$host = (string) parse_url(neat_site_origin(), PHP_URL_HOST);
$mailDomain = preg_replace('/^www\./i', '', $host) ?? '';
if (!preg_match('/\A[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?\.[a-z]{2,}\z/i', $mailDomain)) {
    neat_response(false, 'The website email domain is not configured. Please text (508) 202-8132.', 503);
}
$fromEmail = 'website@' . $mailDomain;
$consentText = 'By submitting, you agree to receive calls and text messages from Neat Cleaning about your request. Consent is not a condition of purchase. Message frequency varies. Message and data rates may apply. Reply STOP to opt out or HELP for help. See our Terms and Privacy Policy.';
$body = "NEW CLEANING QUOTE REQUEST\n\n"
    . "Name: {$name}\nPhone: {$phone}\nEmail: {$email}\nService: {$services[$service]}\nTown / ZIP: {$location}\n\n"
    . "Details:\n" . ($details !== '' ? $details : 'No additional details provided.') . "\n\n"
    . "Contact consent: Yes (explicit checkbox)\nConsent text: {$consentText}\n"
    . "Marketing consent: Not requested or granted by this form\n"
    . "Form source: {$formId}\nSubmitted at (UTC): " . gmdate('Y-m-d H:i:s') . "\n"
    . "Website: " . neat_site_origin() . "\n";
$headers = [
    'From' => NEAT_COMPANY . ' Website <' . $fromEmail . '>',
    'Reply-To' => $email,
    'MIME-Version' => '1.0',
    'Content-Type' => 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding' => '8bit',
];

try {
    $sent = @mail(NEAT_RECIPIENT, 'New cleaning quote request - Neat Cleaning', $body, $headers);
} catch (Throwable $error) { $sent = false; }

if (!$sent) {
    error_log('Neat Cleaning: mail() did not accept the quote request.');
    neat_response(false, 'We could not send your request right now. Please text (508) 202-8132.', 500);
}
neat_response(true, 'Thank you! Your request has been sent successfully.');
