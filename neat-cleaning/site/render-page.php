<?php
declare(strict_types=1);
require_once __DIR__ . '/site-settings.php';

$requestPath = (string) parse_url((string) ($_SERVER['REQUEST_URI'] ?? '/'), PHP_URL_PATH);
$file = basename($requestPath);
if ($requestPath === '/' || $file === '') $file = 'index.html';
if (!in_array($file, neat_pages(), true)) {
    $file = '404.html';
    http_response_code(404);
}
try { $origin = neat_site_origin(); }
catch (Throwable $error) { http_response_code(400); exit('Invalid request host.'); }

$canonicalPath = $file === 'index.html' ? '/' : '/' . $file;
$canonical = htmlspecialchars($origin . $canonicalPath, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
// 1200x630 JPG share images, one per page that has its own photo.
$ogImages = [
    'index.html' => 'home-hero', 'services.html' => 'regular-hero', 'regular-cleaning.html' => 'regular-hero',
    'deep-cleaning.html' => 'deep-hero', 'airbnb-cleaning.html' => 'airbnb-hero',
    'move-in-move-out-cleaning.html' => 'move-hero', 'commercial-cleaning.html' => 'commercial-hero',
    'about.html' => 'about-hero', 'service-areas.html' => 'area-hero', 'contact.html' => 'contact-hero',
    'faq.html' => 'contact-hero',
];
$image = '/assets/images/og-' . ($ogImages[$file] ?? 'home-hero') . '.jpg';
$seo = '<link rel="canonical" href="' . $canonical . '">'
    . '<meta property="og:url" content="' . $canonical . '">'
    . '<meta property="og:image" content="' . htmlspecialchars($origin . $image, ENT_QUOTES, 'UTF-8') . '">'
    . '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
    . '<meta property="og:site_name" content="Neat Cleaning">';
if ($file === '404.html') $seo .= '<meta name="robots" content="noindex,follow">';

$markup = file_get_contents(__DIR__ . '/' . $file);
if ($markup === false) { http_response_code(500); exit('Unable to load this page.'); }
// JSON-LD in the HTML uses {{ORIGIN}} so schema URLs always match the live domain.
$jsonOrigin = substr(json_encode($origin, JSON_UNESCAPED_SLASHES | JSON_HEX_TAG), 1, -1);
$markup = str_replace(['<!--AUTO_SEO-->', '{{ORIGIN}}'], [$seo, $jsonOrigin], $markup);
header('Content-Type: text/html; charset=utf-8');
header('X-Content-Type-Options: nosniff');
echo $markup;
