<?php
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('Cache-Control: public, max-age=3600');
/* Canonical site URL — must match the canonical links in the HTML pages. */
$base = 'https://guardianshomehelphllc.com';
echo "User-agent: *\nAllow: /\nDisallow: /send-form.php\nDisallow: /404.html\n\nSitemap: " . $base . "/sitemap.xml\n";
