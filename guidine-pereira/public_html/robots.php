<?php
require __DIR__ . '/includes/functions.php';
header('Content-Type: text/plain; charset=utf-8');
echo "User-agent: *\n";
echo "Disallow: /includes/\n";
echo "Disallow: /leads/\n";
echo "Disallow: /send.php\n";
echo "Disallow: /thank-you\n\n";
echo 'Sitemap: ' . abs_url('sitemap.xml') . "\n";
