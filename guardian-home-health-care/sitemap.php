<?php
declare(strict_types=1);
header('Content-Type: application/xml; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: public, max-age=3600');
$host = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
if (!preg_match('/\A[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?(?::[0-9]{1,5})?\z/D', $host)) { http_response_code(400); exit; }
$base = 'https://' . $host . rtrim(str_replace('\\', '/', dirname((string) ($_SERVER['SCRIPT_NAME'] ?? '/sitemap.php'))), '/');
/* file => [canonical path, priority] — the home page canonical is "/". */
$pages = [
    'index.html' => ['/', '1.0'],
    'services.html' => ['/services.html', '0.9'],
    'senior-home-care.html' => ['/senior-home-care.html', '0.9'],
    'companion-care.html' => ['/companion-care.html', '0.9'],
    'respite-care.html' => ['/respite-care.html', '0.9'],
    'day-overnight-care.html' => ['/day-overnight-care.html', '0.9'],
    'service-areas.html' => ['/service-areas.html', '0.8'],
    'about.html' => ['/about.html', '0.7'],
    'contact.html' => ['/contact.html', '0.8'],
    'privacy.html' => ['/privacy.html', '0.3'],
    'terms.html' => ['/terms.html', '0.3'],
];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach ($pages as $file => [$path, $priority]) {
    $mtime = @filemtime(__DIR__ . '/' . $file);
    if ($mtime === false) { continue; }
    echo '  <url><loc>' . htmlspecialchars($base . $path, ENT_XML1 | ENT_QUOTES, 'UTF-8') . '</loc><lastmod>' . gmdate('Y-m-d', $mtime) . '</lastmod><priority>' . $priority . "</priority></url>\n";
}
echo '</urlset>' . "\n";
