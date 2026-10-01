<?php
declare(strict_types=1);

// FG Professional Services inquiry endpoint. The recipient and sender are fixed here.
header('Content-Type: application/json; charset=UTF-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

function respond(int $status, bool $success, string $message): void
{
    http_response_code($status);
    echo json_encode(['success' => $success, 'data' => ['message' => $message]], JSON_UNESCAPED_SLASHES);
    exit;
}

function field(string $key, int $max): string
{
    $value = $_POST[$key] ?? '';
    if (!is_string($value)) {
        return '';
    }
    $value = trim(strip_tags($value));
    if (strlen($value) > $max * 4) {
        return '';
    }
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value);
    return is_string($value) ? trim($value) : '';
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(405, false, 'This request could not be processed.');
}

if ((int)($_SERVER['CONTENT_LENGTH'] ?? 0) > 16000 || strlen(http_build_query($_POST)) > 16000) {
    respond(413, false, 'The request is too large.');
}

if (($_POST['action'] ?? null) !== 'cw_form_submit') {
    respond(400, false, 'Invalid form request.');
}

// Browser submissions must come from this same site. This also works on a staging host.
$host = strtolower((string)($_SERVER['HTTP_HOST'] ?? ''));
$host = preg_replace('/:\d+$/', '', $host);
$source = (string)($_SERVER['HTTP_ORIGIN'] ?? ($_SERVER['HTTP_REFERER'] ?? ''));
$sourceHost = strtolower((string)parse_url($source, PHP_URL_HOST));
$sourceScheme = strtolower((string)parse_url($source, PHP_URL_SCHEME));
if (!$host || !$sourceHost || !hash_equals($host, $sourceHost) || !in_array($sourceScheme, ['http', 'https'], true)) {
    respond(403, false, 'This request could not be processed.');
}

if (isset($_POST['botcheck']) && (!is_string($_POST['botcheck']) || trim($_POST['botcheck']) !== '')) {
    respond(400, false, 'This request could not be processed.');
}

$name = field('name', 100);
$phone = field('phone', 30);
$email = field('email', 180);
$service = field('service', 100);
$message = field('message', 1500);
$allowedServices = ['Interior Painting', 'Cabinet Painting', 'Drywall Repair', 'Exterior Painting', 'Other Painting Project'];

if (strlen($name) < 2 || strlen($name) > 100 || preg_match('/[\r\n]/', $name)
    || !filter_var($email, FILTER_VALIDATE_EMAIL) || strlen($email) > 180
    || preg_match('/[\r\n]/', $email)
    || strlen($phone) > 30 || preg_match('/[\r\n]/', $phone)
    || !preg_match('/^[0-9+().\s-]+$/', $phone)
    || strlen(preg_replace('/\D/', '', $phone)) < 7
    || strlen(preg_replace('/\D/', '', $phone)) > 18
    || !in_array($service, $allowedServices, true)
    || strlen($message) > 1500
    || ($_POST['consent'] ?? '') !== 'yes') {
    respond(422, false, 'Please check the form fields and try again.');
}

// Short IP-based interval between submissions; no client supplied recipient is used.
$limitPath = sys_get_temp_dir() . '/fg_form_' . hash('sha256', (string)($_SERVER['REMOTE_ADDR'] ?? 'unknown'));
$limitFile = @fopen($limitPath, 'c+');
if ($limitFile === false || !flock($limitFile, LOCK_EX)) {
    if (is_resource($limitFile)) { fclose($limitFile); }
    respond(503, false, 'We could not send your request right now.');
}
$last = (int)trim((string)stream_get_contents($limitFile));
if ($last > 0 && time() - $last < 30) {
    flock($limitFile, LOCK_UN);
    fclose($limitFile);
    respond(429, false, 'Please wait a moment before sending another request.');
}
rewind($limitFile);
ftruncate($limitFile, 0);
fwrite($limitFile, (string)time());
fflush($limitFile);
flock($limitFile, LOCK_UN);
fclose($limitFile);

$to = 'fgprofessionalservice@gmail.com';
$subject = 'FG Professional Services | New project request';
$body = "New project inquiry from the website\n\n"
    . "Name: {$name}\nPhone: {$phone}\nEmail: {$email}\nService: {$service}\n\n"
    . "Project details:\n" . ($message === '' ? 'Not provided' : $message) . "\n\n"
    . "Calls and SMS consent: Yes, submitted through the required checkbox.\n"
    . "Received (UTC): " . gmdate('Y-m-d H:i:s') . "\n";
$headers = [
    'From: FG Professional Services Website <website@fgproservices.com>',
    'Reply-To: ' . $email,
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: FG Website'
];

if (!@mail($to, $subject, $body, implode("\r\n", $headers))) {
    respond(503, false, 'We could not send your request right now.');
}
respond(200, true, 'Thank you! Your request has been sent successfully.');
