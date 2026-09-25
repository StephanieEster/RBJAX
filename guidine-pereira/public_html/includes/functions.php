<?php
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/data.php';

function e($s)
{
    return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
}

function site_url()
{
    if (SITE_URL !== '') {
        return rtrim(SITE_URL, '/');
    }
    $https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'https')
        || (($_SERVER['SERVER_PORT'] ?? '') == 443);
    $host = preg_replace('/[^a-z0-9.\-:]/i', '', $_SERVER['HTTP_HOST'] ?? 'localhost');
    return ($https ? 'https' : 'http') . '://' . $host . base_path();
}

/** Sub-folder the site lives in ('' when installed in public_html root). */
function base_path()
{
    static $base = null;
    if ($base === null) {
        $docRoot = realpath($_SERVER['DOCUMENT_ROOT'] ?? '') ?: '';
        $appRoot = realpath(__DIR__ . '/..') ?: '';
        $base = ($docRoot && strpos($appRoot, $docRoot) === 0) ? substr($appRoot, strlen($docRoot)) : '';
        $base = rtrim(str_replace('\\', '/', $base), '/');
    }
    return $base;
}

/** Root-relative link to a page slug ('' = home). */
function url($slug = '')
{
    return base_path() . '/' . ltrim($slug, '/');
}

function abs_url($slug = '')
{
    return site_url() . '/' . ltrim($slug, '/');
}

/** Asset URL with a version string so browsers pick up changes. */
function asset($path)
{
    $file = __DIR__ . '/../assets/' . $path;
    $v = is_file($file) ? filemtime($file) : '1';
    return base_path() . '/assets/' . $path . '?v=' . $v;
}

function work_img($slug, $size = '')
{
    return base_path() . '/assets/img/work/' . $slug . ($size ? '-' . $size : '') . '.webp';
}

function gallery()
{
    static $g = null;
    if ($g === null) {
        $g = require __DIR__ . '/gallery-data.php';
    }
    return $g;
}

function photo($slug)
{
    foreach (gallery() as $p) {
        if ($p[0] === $slug) {
            return $p;
        }
    }
    return [$slug, '', '', 900, 1200];
}

/**
 * Responsive project image. $sizes is the CSS sizes hint.
 */
function picture($slug, $sizes = '(max-width: 700px) 100vw, 50vw', $lazy = true, $class = '', $alt = null)
{
    $p = photo($slug);
    $alt = $alt ?? $p[2];
    $h480 = (int) round($p[4] * 480 / $p[3]);
    return '<img class="' . e($class) . '" src="' . e(work_img($slug)) . '" srcset="'
        . e(work_img($slug, 'sm')) . ' 480w, ' . e(work_img($slug)) . ' 900w" sizes="' . e($sizes) . '" width="'
        . (int) $p[3] . '" height="' . (int) $p[4] . '" alt="' . e($alt) . '"'
        . ($lazy ? ' loading="lazy" decoding="async"' : ' fetchpriority="high" decoding="async"') . '>';
}

function tel_link()
{
    return 'tel:' . PHONE_E164;
}

function sms_link()
{
    return 'sms:' . PHONE_E164;
}

function icon($name)
{
    $paths = [
        'phone'   => '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
        'sms'     => '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 12h.01M12 12h.01M15.5 12h.01"/>',
        'mail'    => '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
        'pin'     => '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
        'arrow'   => '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'check'   => '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        'shield'  => '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3z"/><path d="m9 12 2 2 4-4"/>',
        'clock'   => '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        'chat'    => '<path d="M4 5h16v11H9l-5 4V5z"/><path d="M8 9.5h8M8 12.5h5"/>',
        'ruler'   => '<path d="m3 16.5 13.5-13.5 4.5 4.5L7.5 21 3 16.5z"/><path d="m7 12.5 1.8 1.8M10 9.5l1.8 1.8M13 6.5l1.8 1.8"/>',
        'layers'  => '<path d="m12 3 9 4.5-9 4.5-9-4.5L12 3z"/><path d="m3 12 9 4.5 9-4.5"/><path d="m3 16.5 9 4.5 9-4.5"/>',
        'home'    => '<path d="M4 11 12 4l8 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
        'wallet'  => '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M16 12.5h2M3 9.5h18"/>',
        'star'    => '<path d="m12 4 2.4 5 5.4.6-4 3.7 1.1 5.4L12 16l-4.9 2.7 1.1-5.4-4-3.7 5.4-.6z"/>',
        'facebook'  => '<path d="M14 8.5h2.5V5H14a4 4 0 0 0-4 4v2H8v3.5h2V21h3.5v-6.5H16l.5-3.5h-3V9.5a1 1 0 0 1 1-1z"/>',
        'instagram' => '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.2 6.8h.01"/>',
        'close'   => '<path d="M6 6l12 12M18 6 6 18"/>',
        'chevron' => '<path d="m6 9 6 6 6-6"/>',
        'google'  => '<path d="M20.5 12.2c0-.6-.1-1.2-.2-1.7H12v3.3h4.8a4.1 4.1 0 0 1-1.8 2.7v2.2h2.9c1.7-1.6 2.6-3.9 2.6-6.5z"/><path d="M12 21c2.4 0 4.5-.8 5.9-2.2L15 16.5c-.8.5-1.8.9-3 .9-2.3 0-4.3-1.6-5-3.7H4v2.3A9 9 0 0 0 12 21z"/><path d="M7 13.7a5.4 5.4 0 0 1 0-3.4V8H4a9 9 0 0 0 0 8l3-2.3z"/><path d="M12 6.6c1.3 0 2.5.5 3.4 1.3l2.6-2.6A9 9 0 0 0 4 8l3 2.3c.7-2.1 2.7-3.7 5-3.7z"/>',
    ];
    return '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' . ($paths[$name] ?? '') . '</svg>';
}

function json_ld($data)
{
    echo '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . "</script>\n";
}

function business_schema()
{
    global $AREAS_SC, $AREAS_NC;
    $areas = [];
    foreach ($AREAS_SC as $c) {
        $areas[] = ['@type' => 'City', 'name' => $c . ', SC'];
    }
    foreach ($AREAS_NC as $c) {
        $areas[] = ['@type' => 'City', 'name' => $c . ', NC'];
    }
    $same = array_values(array_filter([FACEBOOK_URL, INSTAGRAM_URL, GOOGLE_BUSINESS_URL]));
    return [
        '@context' => 'https://schema.org',
        '@type' => 'HomeAndConstructionBusiness',
        '@id' => abs_url() . '#business',
        'name' => BUSINESS_NAME,
        'alternateName' => BUSINESS_SHORT,
        'slogan' => TAGLINE,
        'description' => 'Family-owned tile and remodeling contractor serving Myrtle Beach, SC and the surrounding area: shower and bathroom remodeling, tile flooring, wall tile and backsplash installation.',
        'url' => abs_url(),
        'telephone' => PHONE_E164,
        'email' => EMAIL,
        'logo' => site_url() . '/assets/img/brand/icon-512.png',
        'image' => site_url() . '/assets/img/og-image.jpg',
        'foundingDate' => '2022-01-20',
        'paymentAccepted' => 'Cash, Check, Zelle',
        'address' => [
            '@type' => 'PostalAddress',
            'addressLocality' => 'Myrtle Beach',
            'addressRegion' => 'SC',
            'addressCountry' => 'US',
        ],
        'areaServed' => $areas,
        'knowsAbout' => ['Bathroom remodeling', 'Shower remodeling', 'Tile installation', 'Tile flooring', 'Wall tile', 'Backsplash installation'],
        'sameAs' => $same,
    ];
}

function breadcrumb_schema(array $items)
{
    $list = [];
    foreach ($items as $i => $item) {
        $list[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $item[0], 'item' => abs_url($item[1])];
    }
    return ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $list];
}

function faq_schema(array $faqs)
{
    $q = [];
    foreach ($faqs as $f) {
        $q[] = ['@type' => 'Question', 'name' => $f[0], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f[1]]];
    }
    return ['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $q];
}

function render_faq(array $faqs)
{
    echo '<div class="faq">';
    foreach ($faqs as $i => $f) {
        echo '<details class="faq__item"' . ($i === 0 ? ' open' : '') . '><summary><span>' . e($f[0]) . '</span>'
            . icon('chevron') . '</summary><div class="faq__a"><p>' . e($f[1]) . '</p></div></details>';
    }
    echo '</div>';
}

function breadcrumbs(array $items)
{
    echo '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $last = count($items) - 1;
    foreach ($items as $i => $item) {
        echo $i === $last
            ? '<li aria-current="page">' . e($item[0]) . '</li>'
            : '<li><a href="' . e(url($item[1])) . '">' . e($item[0]) . '</a></li>';
    }
    echo '</ol></nav>';
}
