<?php
declare(strict_types=1);
require_once __DIR__ . '/site-settings.php';
try { $origin = neat_site_origin(); }
catch (Throwable $error) { http_response_code(400); exit; }
header('Content-Type: application/xml; charset=utf-8');
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
foreach (neat_pages() as $page) {
    if (in_array($page, ['404.html', 'thank-you.html'], true)) continue;
    $url = $origin . ($page === 'index.html' ? '/' : '/' . $page);
    echo '<url><loc>' . htmlspecialchars($url, ENT_XML1, 'UTF-8') . '</loc><lastmod>'
        . gmdate('Y-m-d', (int) filemtime(__DIR__ . '/' . $page)) . '</lastmod></url>' . "\n";
}
echo '</urlset>';
