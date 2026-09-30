<?php
require __DIR__ . '/includes/bootstrap.php';
header('Content-Type: application/xml; charset=UTF-8');

$pages = [
    ''              => ['1.0', 'weekly', 'index.php', ['hero', 'shower-2', 'kitchen-1', 'fireplace-1', 'floor-2']],
    'about'         => ['0.7', 'monthly', 'about.php', ['bath-3', 'install']],
    'service-areas' => ['0.8', 'monthly', 'service-areas.php', ['floor-2']],
    'contact'       => ['0.8', 'monthly', 'contact.php', ['shower-3']],
    'privacy-policy'=> ['0.2', 'yearly', 'privacy-policy.php', []],
];
foreach ($SERVICES as $slug => $s) {
    $pages[$slug] = ['0.9', 'monthly', $slug . '.php', array_merge([$s['image']], $s['gallery'])];
}

echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
<?php foreach ($pages as $path => [$prio, $freq, $file, $imgs]): ?>
  <url>
    <loc><?= e(url($path)) ?></loc>
    <lastmod><?= date('Y-m-d', max(filemtime(__DIR__ . '/' . $file), filemtime(__DIR__ . '/includes/data.php'))) ?></lastmod>
    <changefreq><?= $freq ?></changefreq>
    <priority><?= $prio ?></priority>
<?php foreach (array_unique($imgs) as $k): if (!isset($IMAGES[$k])) continue; ?>
    <image:image><image:loc><?= e(image_src($IMAGES[$k], 1200, 900)) ?></image:loc></image:image>
<?php endforeach; ?>
  </url>
<?php endforeach; ?>
</urlset>
