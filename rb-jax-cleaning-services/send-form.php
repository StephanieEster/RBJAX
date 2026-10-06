<?php
declare(strict_types=1);

header('Content-Type: application/json; charset=UTF-8');
header('X-Content-Type-Options: nosniff');

function respond(bool $success, string $message, int $status = 200): void
{
    http_response_code($status);
    echo json_encode([
        'success' => $success,
        'data' => ['message' => $message],
    ], JSON_UNESCAPED_SLASHES);
    exit;
}

function clean_text(string $value, int $maxLength = 200): string
{
    $value = trim(strip_tags($value));
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value) ?? '';
    return mb_substr($value, 0, $maxLength);
}

function has_header_break(string $value): bool
{
    return preg_match('/[\r\n]/', $value) === 1;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    respond(false, 'Method not allowed.', 405);
}

$contentLength = (int) ($_SERVER['CONTENT_LENGTH'] ?? 0);
if ($contentLength <= 0 || $contentLength > 1048576) {
    respond(false, 'Invalid request size.', 413);
}

if (($_POST['action'] ?? '') !== 'cw_form_submit') {
    respond(false, 'Invalid form request.', 400);
}

$host = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
$host = preg_replace('/:\d+$/', '', $host) ?? '';
$origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? '');
$referer = (string) ($_SERVER['HTTP_REFERER'] ?? '');
$sourceUrl = $origin !== '' ? $origin : $referer;

if ($host === '' || $sourceUrl === '') {
    respond(false, 'We could not verify this request.', 403);
}

$sourceHost = strtolower((string) parse_url($sourceUrl, PHP_URL_HOST));
$validLocalhost = in_array($host, ['localhost', '127.0.0.1'], true)
    && in_array($sourceHost, ['localhost', '127.0.0.1'], true);

if (!$validLocalhost && !hash_equals($host, $sourceHost)) {
    respond(false, 'We could not verify this request.', 403);
}

if (!empty($_POST['botcheck'])) {
    respond(true, 'Thank you! Your request has been sent successfully.');
}

session_name('rbjax_form_session');
session_start();
$now = time();
$lastSubmission = (int) ($_SESSION['last_submission'] ?? 0);
if ($lastSubmission > 0 && ($now - $lastSubmission) < 20) {
    respond(false, 'Please wait a moment before sending another request.', 429);
}

$name = clean_text((string) ($_POST['name'] ?? ''), 100);
$phone = clean_text((string) ($_POST['phone'] ?? ''), 40);
$emailRaw = trim((string) ($_POST['email'] ?? ''));
$email = filter_var($emailRaw, FILTER_VALIDATE_EMAIL) ? $emailRaw : '';
$service = clean_text((string) ($_POST['service'] ?? ''), 80);
$propertyType = clean_text((string) ($_POST['property_type'] ?? ''), 80);
$preferredContact = clean_text((string) ($_POST['preferred_contact'] ?? ''), 40);
$message = clean_text((string) ($_POST['message'] ?? ''), 2000);
$consentCare = (string) ($_POST['consent_care'] ?? '');
$consentMarketing = (string) ($_POST['consent_marketing'] ?? '');
$formContext = clean_text((string) ($_POST['form_context'] ?? 'Website estimate form'), 100);

$allowedServices = [
    'Regular cleaning',
    'Deep cleaning',
    'Commercial cleaning',
    'Recurring cleaning',
    'Exterior window cleaning',
    'Not sure yet',
];
$allowedContact = ['Call', 'Text message', 'Email'];
$allowedProperty = ['House', 'Vacation home', 'Office', 'Daycare', 'Store', 'Supermarket', 'Other commercial property', 'Other'];

if (mb_strlen($name) < 2 || mb_strlen($name) > 100) {
    respond(false, 'Please enter your full name.', 422);
}
if (!preg_match('/^[0-9+()\-\s.]{7,40}$/', $phone)) {
    respond(false, 'Please enter a valid phone number.', 422);
}
if ($email === '' || has_header_break($emailRaw)) {
    respond(false, 'Please enter a valid email address.', 422);
}
if (!in_array($service, $allowedServices, true)) {
    respond(false, 'Please select a service.', 422);
}
if ($propertyType !== '' && !in_array($propertyType, $allowedProperty, true)) {
    respond(false, 'Please select a valid property type.', 422);
}
if ($preferredContact !== '' && !in_array($preferredContact, $allowedContact, true)) {
    respond(false, 'Please select a valid contact preference.', 422);
}
if (has_header_break($name) || has_header_break($phone) || has_header_break($formContext)) {
    respond(false, 'Invalid form data.', 422);
}

$recipient = 'rbcleaningfl@gmail.com';
$subject = 'New cleaning estimate request - RB Jax Cleaning Services';
$safeHost = preg_replace('/^www\./', '', $host) ?? $host;
$safeHost = preg_replace('/[^a-z0-9.-]/', '', $safeHost) ?? '';
if ($safeHost === '' || in_array($safeHost, ['localhost', '127.0.0.1'], true)) {
    $safeHost = 'jaxcleaningservices.com';
}
$fromEmail = 'website@' . $safeHost;

$bodyLines = [
    'New estimate request received from the website.',
    '',
    'Form: ' . $formContext,
    'Name: ' . $name,
    'Phone: ' . $phone,
    'Email: ' . $email,
    'Preferred contact: ' . ($preferredContact !== '' ? $preferredContact : 'Not provided'),
    'Service: ' . $service,
    'Property type: ' . ($propertyType !== '' ? $propertyType : 'Not provided'),
    '',
    'Message:',
    $message !== '' ? $message : 'No additional message provided.',
    '',
    'Customer care SMS consent: ' . ($consentCare === 'agreed' ? 'Agreed' : 'Not agreed'),
    'Marketing SMS consent: ' . ($consentMarketing === 'agreed' ? 'Agreed' : 'Not agreed'),
    'Submitted at: ' . gmdate('Y-m-d H:i:s') . ' UTC',
];
$body = implode("\r\n", $bodyLines);

$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'From: RB Jax Cleaning Website <' . $fromEmail . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'X-Mailer: PHP/' . PHP_VERSION,
];

if (!mail($recipient, $subject, $body, implode("\r\n", $headers))) {
    respond(false, 'We could not send your request right now. Please call or text us instead.', 500);
}

$_SESSION['last_submission'] = $now;
respond(true, 'Thank you! Your request has been sent successfully. We will contact you to arrange an in-person estimate.');
