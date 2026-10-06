<?php
declare(strict_types=1);
require_once __DIR__ . '/site-settings.php';
try { $origin = neat_site_origin(); }
catch (Throwable $error) { http_response_code(400); exit; }
header('Content-Type: text/plain; charset=utf-8');
echo "User-agent: *\nAllow: /\nDisallow: /send-form.php\nDisallow: /site-settings.php\nDisallow: /thank-you.html\nSitemap: " . $origin . "/sitemap.xml\n";
