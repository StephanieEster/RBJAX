<?php
/**
 * Builds a static HTML version of the site for hosts without PHP (e.g. Vercel).
 *
 * Usage (from the ra-tile-renovation folder):
 *   php tools/build-static.php [site-url] [output-dir]
 *   php tools/build-static.php https://ra-tile-renovation.vercel.app vercel
 *
 * The form posts to STATIC_FORM_ENDPOINT (FormSubmit) instead of send.php.
 */
if (PHP_SAPI !== 'cli') {
    exit("Run from the command line.\n");
}

$root    = dirname(__DIR__);
$src     = $root . '/public_html';
$siteUrl = rtrim($argv[1] ?? 'https://ra-tile-renovation.vercel.app', '/');
$out     = $root . '/' . trim($argv[2] ?? 'vercel', '/');

$pages = [
    'index.html'                      => 'index.php',
    'bathroom-shower-remodeling.html' => 'bathroom-shower-remodeling.php',
    'tile-flooring.html'              => 'tile-flooring.php',
    'kitchen-backsplash.html'         => 'kitchen-backsplash.php',
    'fireplace-tile.html'             => 'fireplace-tile.php',
    'about.html'                      => 'about.php',
    'service-areas.html'              => 'service-areas.php',
    'contact.html'                    => 'contact.php',
    'thank-you.html'                  => 'thank-you.php',
    'privacy-policy.html'             => 'privacy-policy.php',
    '404.html'                        => '404.php',
    'sitemap.xml'                     => 'sitemap.php',
    'robots.txt'                      => 'robots.php',
];

function rrmdir(string $dir): void
{
    if (!is_dir($dir)) {
        return;
    }
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::CHILD_FIRST);
    foreach ($it as $f) {
        $f->isDir() ? rmdir($f->getPathname()) : unlink($f->getPathname());
    }
    rmdir($dir);
}

function rcopy(string $from, string $to): void
{
    @mkdir($to, 0755, true);
    $it = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($from, FilesystemIterator::SKIP_DOTS), RecursiveIteratorIterator::SELF_FIRST);
    foreach ($it as $f) {
        $dest = $to . '/' . substr($f->getPathname(), strlen($from) + 1);
        $f->isDir() ? @mkdir($dest, 0755, true) : copy($f->getPathname(), $dest);
    }
}

rrmdir($out);
mkdir($out, 0755, true);

$php = escapeshellarg(PHP_BINARY);
$env = 'STATIC_BUILD=1 SITE_URL=' . escapeshellarg($siteUrl);
foreach ($pages as $file => $script) {
    $cmd = "cd " . escapeshellarg($src) . " && $env $php -d display_errors=stderr " . escapeshellarg($script) . ' 2>&1 1>' . escapeshellarg("$out/$file");
    $errors = shell_exec($cmd);
    if ($errors) {
        fwrite(STDERR, "Error building $file:\n$errors\n");
        exit(1);
    }
    // Static hosts don't need ".php" references
    $html = file_get_contents("$out/$file");
    file_put_contents("$out/$file", ltrim($html));
    echo "  ✓ $file\n";
}

rcopy("$src/assets", "$out/assets");
copy("$src/favicon.ico", "$out/favicon.ico");
copy("$src/site.webmanifest", "$out/site.webmanifest");
@unlink("$out/assets/img/projects/README.txt");

$vercel = [
    'cleanUrls'     => true,
    'trailingSlash' => false,
    'redirects'     => [
        ['source' => '/index', 'destination' => '/', 'permanent' => true],
        ['source' => '/send.php', 'destination' => '/contact', 'permanent' => false],
    ],
    'headers'       => [
        [
            'source'  => '/assets/(.*)',
            'headers' => [['key' => 'Cache-Control', 'value' => 'public, max-age=31536000, immutable']],
        ],
        [
            'source'  => '/(.*)',
            'headers' => [
                ['key' => 'X-Content-Type-Options', 'value' => 'nosniff'],
                ['key' => 'X-Frame-Options', 'value' => 'SAMEORIGIN'],
                ['key' => 'Referrer-Policy', 'value' => 'strict-origin-when-cross-origin'],
            ],
        ],
        [
            'source'  => '/thank-you',
            'headers' => [['key' => 'X-Robots-Tag', 'value' => 'noindex']],
        ],
    ],
];
file_put_contents("$out/vercel.json", json_encode($vercel, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n");

echo "\nStatic site ready in: $out\nSite URL: $siteUrl\n";
