<?php
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: public, max-age=3600');
$host = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
if (!preg_match('/\A[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?(?::[0-9]{1,5})?\z/D', $host)) { http_response_code(400); exit; }
$base = 'https://' . $host . rtrim(str_replace('\\', '/', dirname((string) ($_SERVER['SCRIPT_NAME'] ?? '/robots.php'))), '/');
echo "User-agent: *\nAllow: /\nDisallow: /send-form.php\nDisallow: /404.html\n\nSitemap: " . $base . "/sitemap.xml\n";
