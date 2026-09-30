<?php
/**
 * Shared helpers. Every page starts with: require __DIR__ . '/includes/bootstrap.php';
 */

if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'functions.php') {
    http_response_code(403);
    exit;
}

function e($value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

/** Absolute URL for a site path ('' = home). */
function url(string $path = ''): string
{
    $path = ltrim($path, '/');
    return SITE_URL . '/' . $path;
}

/** Root-relative link used in navigation. */
function link_to(string $path = ''): string
{
    return '/' . ltrim($path, '/');
}

/** Cache-busted asset URL. */
function asset(string $path): string
{
    $file = ROOT_DIR . '/assets/' . ltrim($path, '/');
    $v = is_file($file) ? filemtime($file) : '1';
    return '/assets/' . ltrim($path, '/') . '?v=' . $v;
}

function sms_link(string $body = SMS_BODY): string
{
    // "?&body=" works on both iOS and Android
    return 'sms:' . PHONE_E164 . '?&body=' . rawurlencode($body);
}

function tel_link(): string
{
    return 'tel:' . PHONE_E164;
}

// ---------------------------------------------------------------------------
// Images (stock library or local files) — always rendered with a fixed ratio,
// width/height attributes and a responsive srcset to avoid layout shift.
// ---------------------------------------------------------------------------
function image_src(array $img, int $w, int $h): string
{
    if (!empty($img['pexels'])) {
        $id = (int) $img['pexels'];
        return "https://images.pexels.com/photos/{$id}/pexels-photo-{$id}.jpeg?auto=compress&cs=tinysrgb&fit=crop&w={$w}&h={$h}";
    }
    return '/' . ltrim($img['src'], '/');
}

/**
 * @param string $key    key from $IMAGES
 * @param string $ratio  "16:9", "4:3", "1:1", "3:4"...
 * @param string $sizes  sizes attribute
 * @param array  $opt    class, eager (bool), alt override
 */
function img(string $key, string $ratio = '4:3', string $sizes = '100vw', array $opt = []): string
{
    global $IMAGES;
    if (!isset($IMAGES[$key])) {
        return '';
    }
    $img = $IMAGES[$key];
    [$rw, $rh] = array_map('intval', explode(':', $ratio));
    $widths = $opt['widths'] ?? [480, 800, 1200, 1600];
    $srcset = [];
    foreach ($widths as $w) {
        $h = (int) round($w * $rh / $rw);
        $srcset[] = image_src($img, $w, $h) . " {$w}w";
    }
    $baseW = $opt['base'] ?? 1200;
    $baseH = (int) round($baseW * $rh / $rw);
    $eager = !empty($opt['eager']);
    $attrs = [
        'src'      => image_src($img, $baseW, $baseH),
        'alt'      => $opt['alt'] ?? $img['alt'],
        'width'    => $baseW,
        'height'   => $baseH,
        'loading'  => $eager ? 'eager' : 'lazy',
        'decoding' => $eager ? 'sync' : 'async',
        'class'    => $opt['class'] ?? '',
    ];
    if (!empty($img['pexels'])) {
        $attrs['srcset'] = implode(', ', $srcset);
        $attrs['sizes'] = $sizes;
    }
    if ($eager) {
        $attrs['fetchpriority'] = 'high';
    }
    $html = '<img';
    foreach ($attrs as $k => $v) {
        if ($v === '' && $k !== 'alt') {
            continue;
        }
        $html .= ' ' . $k . '="' . e($v) . '"';
    }
    return $html . '>';
}

/** Ratio-locked figure wrapper (keeps every photo proportional). */
function figure(string $key, string $ratio = '4:3', string $sizes = '100vw', array $opt = []): string
{
    $r = str_replace(':', ' / ', $ratio);
    $cls = 'media' . (!empty($opt['figclass']) ? ' ' . $opt['figclass'] : '');
    return '<figure class="' . e($cls) . '" style="aspect-ratio:' . e($r) . '">' . img($key, $ratio, $sizes, $opt) . '</figure>';
}

// ---------------------------------------------------------------------------
// Icons (inline SVG, no external requests)
// ---------------------------------------------------------------------------
function icon(string $name, string $class = 'icon'): string
{
    $p = [
        'sms'        => '<path d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H8l-4 4V6a2 2 0 0 1 2-2z"/><path d="M8 10h.01M12 10h.01M16 10h.01"/>',
        'phone'      => '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
        'mail'       => '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
        'instagram'  => '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
        'facebook'   => '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
        'check'      => '<path d="M20 6 9 17l-5-5"/>',
        'shield'     => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
        'tag'        => '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><path d="M7 7h.01"/>',
        'award'      => '<circle cx="12" cy="8" r="6"/><path d="M15.5 13 17 22l-5-3-5 3 1.5-9"/>',
        'clock'      => '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        'pin'        => '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
        'star'       => '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
        'sparkle'    => '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/>',
        'ruler'      => '<path d="M21.3 8.7 8.7 21.3a1 1 0 0 1-1.4 0l-4.6-4.6a1 1 0 0 1 0-1.4L15.3 2.7a1 1 0 0 1 1.4 0l4.6 4.6a1 1 0 0 1 0 1.4z"/><path d="m7.5 10.5 2 2M10.5 7.5l2 2M4.5 13.5l2 2M13.5 4.5l2 2"/>',
        'calendar'   => '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
        'wallet'     => '<path d="M21 12V7H5a2 2 0 0 1 0-4h14v4"/><path d="M3 5v14a2 2 0 0 0 2 2h16v-5"/><path d="M18 12a2 2 0 0 0 0 4h4v-4z"/>',
        'arrow'      => '<path d="M5 12h14M13 5l7 7-7 7"/>',
        'chevron'    => '<path d="m6 9 6 6 6-6"/>',
        'menu'       => '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'close'      => '<path d="M18 6 6 18M6 6l12 12"/>',
        'shower'     => '<path d="M4 20V8a5 5 0 0 1 10 0"/><path d="M10 8h8"/><path d="M12 12v1M16 12v1M20 12v1M14 16v1M18 16v1M12 20v1M16 20v1M20 20v1"/>',
        'floor'      => '<path d="M3 3h8v8H3zM13 3h8v8h-8zM3 13h8v8H3zM13 13h8v8h-8z"/>',
        'backsplash' => '<path d="M3 4h18v10H3z"/><path d="M3 9h18M9 4v5M15 9v5M6 9v0M12 4v0"/><path d="M2 18h20"/>',
        'fireplace'  => '<path d="M3 21V5h18v16"/><path d="M1 5h22"/><path d="M7 21v-8h10v8"/><path d="M12 19c-1.5 0-2-1-2-2 0-1.5 2-2.5 2-4 1 1 2 2.2 2 3.7 0 1.3-.7 2.3-2 2.3z"/>',
        'diamond'    => '<path d="M12 2 22 12 12 22 2 12z"/>',
    ];
    $d = $p[$name] ?? $p['diamond'];
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $d . '</svg>';
}

// ---------------------------------------------------------------------------
// Form security helpers
// ---------------------------------------------------------------------------
function form_secret(): string
{
    if (FORM_SECRET !== '' && strpos(FORM_SECRET, 'change-me') !== 0) {
        return FORM_SECRET;
    }
    // Auto-generate and persist a secret the first time
    $file = ROOT_DIR . '/data/.secret';
    if (is_file($file)) {
        $s = trim((string) file_get_contents($file));
        if ($s !== '') {
            return $s;
        }
    }
    $s = bin2hex(random_bytes(32));
    @file_put_contents($file, $s, LOCK_EX);
    return is_file($file) ? $s : FORM_SECRET;
}

/** Signed, time-stamped token: stateless (works with page caching, no cookies needed). */
function form_token(): string
{
    $t = (string) time();
    return $t . '.' . hash_hmac('sha256', $t, form_secret());
}

function form_token_valid(string $token, int $minSeconds = 3, int $maxSeconds = 86400): bool
{
    $parts = explode('.', $token, 2);
    if (count($parts) !== 2 || !ctype_digit($parts[0])) {
        return false;
    }
    [$t, $sig] = $parts;
    if (!hash_equals(hash_hmac('sha256', $t, form_secret()), $sig)) {
        return false;
    }
    $age = time() - (int) $t;
    return $age >= $minSeconds && $age <= $maxSeconds;
}

// ---------------------------------------------------------------------------
// SEO / structured data
// ---------------------------------------------------------------------------
function business_schema(): array
{
    global $CITIES, $SERVICES;
    $areas = [];
    foreach ($CITIES as $c) {
        $areas[] = ['@type' => 'City', 'name' => $c . ', NH'];
    }
    $offers = [];
    foreach ($SERVICES as $slug => $s) {
        $offers[] = [
            '@type'       => 'Offer',
            'itemOffered' => ['@type' => 'Service', 'name' => $s['nav'], 'url' => url($slug)],
        ];
    }
    $same = array_values(array_filter([INSTAGRAM_URL, FACEBOOK_URL, GOOGLE_BUSINESS_URL]));
    return [
        '@context'      => 'https://schema.org',
        '@type'         => ['HomeAndConstructionBusiness', 'GeneralContractor'],
        '@id'           => url() . '#business',
        'name'          => SITE_NAME,
        'legalName'     => SITE_LEGAL_NAME,
        'description'   => 'Tile installation and bathroom remodeling company serving Manchester and Southern New Hampshire: tile showers, bathrooms, floor tile, kitchen backsplashes and fireplace tile. Free estimates and a 1-year warranty.',
        'url'           => url(),
        'logo'          => url('assets/img/logo-stacked-gold.png'),
        'image'         => url('assets/img/og-image.jpg'),
        'telephone'     => PHONE_E164,
        'email'         => EMAIL_PUBLIC,
        'foundingDate'  => (string) FOUNDED_YEAR,
        'founders'      => [
            ['@type' => 'Person', 'name' => 'Renato De Almeida'],
            ['@type' => 'Person', 'name' => 'Anderson Soares'],
        ],
        'address'       => [
            '@type'           => 'PostalAddress',
            'addressLocality' => BASE_CITY,
            'addressRegion'   => BASE_STATE,
            'addressCountry'  => 'US',
        ],
        'areaServed'    => $areas,
        'priceRange'    => '$$',
        'paymentAccepted' => 'Cash, Check, Zelle, Venmo',
        'hasOfferCatalog' => [
            '@type'           => 'OfferCatalog',
            'name'            => 'Tile Services',
            'itemListElement' => $offers,
        ],
        'sameAs'        => $same,
    ];
}

function faq_schema(array $faqs): array
{
    $items = [];
    foreach ($faqs as [$q, $a]) {
        $items[] = [
            '@type'          => 'Question',
            'name'           => $q,
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $a],
        ];
    }
    return ['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => $items];
}

function breadcrumb_schema(array $crumbs): array
{
    $list = [];
    $i = 1;
    foreach ($crumbs as $name => $path) {
        $list[] = ['@type' => 'ListItem', 'position' => $i++, 'name' => $name, 'item' => url($path)];
    }
    return ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $list];
}

function json_ld(array $data): string
{
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . '</script>' . "\n";
}

function breadcrumbs_html(array $crumbs): string
{
    $html = '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>';
    $n = count($crumbs);
    $i = 0;
    foreach ($crumbs as $name => $path) {
        $i++;
        if ($i === $n) {
            $html .= '<li aria-current="page">' . e($name) . '</li>';
        } else {
            $html .= '<li><a href="' . e(link_to($path)) . '">' . e($name) . '</a></li>';
        }
    }
    return $html . '</ol></nav>';
}
