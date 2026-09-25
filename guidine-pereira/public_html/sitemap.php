<?php
require __DIR__ . '/includes/functions.php';
header('Content-Type: application/xml; charset=utf-8');

$pages = ['' => '1.0', 'shower-bathroom-remodeling' => '0.9', 'tile-flooring-installation' => '0.9', 'wall-tile-installation' => '0.9', 'backsplash-installation' => '0.9', 'projects' => '0.8', 'about' => '0.7', 'service-areas' => '0.8', 'contact' => '0.8', 'privacy-policy' => '0.2'];
echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' . "\n";
foreach ($pages as $slug => $priority) {
    $file = __DIR__ . '/' . ($slug === '' ? 'index' : $slug) . '.php';
    echo "  <url>\n    <loc>" . e(abs_url($slug)) . "</loc>\n";
    echo '    <lastmod>' . date('Y-m-d', is_file($file) ? filemtime($file) : time()) . "</lastmod>\n";
    echo "    <priority>$priority</priority>\n";
    if ($slug === 'projects') {
        foreach (gallery() as $p) {
            echo '    <image:image><image:loc>' . e(site_url() . work_img($p[0])) . '</image:loc></image:image>' . "\n";
        }
    }
    echo "  </url>\n";
}
echo "</urlset>\n";
