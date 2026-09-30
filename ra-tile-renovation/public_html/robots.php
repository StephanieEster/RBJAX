<?php
require __DIR__ . '/includes/bootstrap.php';
header('Content-Type: text/plain; charset=UTF-8');
?>
User-agent: *
Allow: /
Disallow: /includes/
Disallow: /data/
Disallow: /send.php
Disallow: /thank-you

Sitemap: <?= url('sitemap.xml') ?>

