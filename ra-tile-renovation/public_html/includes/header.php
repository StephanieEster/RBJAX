<?php
/**
 * Expects $page = [
 *   'title' => '', 'description' => '', 'path' => '', 'image' => '(optional absolute url)',
 *   'noindex' => false, 'schema' => [ ...arrays... ], 'body_class' => ''
 * ];
 */
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'header.php') {
    http_response_code(403);
    exit;
}

$page = array_merge([
    'title'       => SITE_NAME . ' | ' . SITE_TAGLINE,
    'description' => '',
    'path'        => '',
    'image'       => url('assets/img/og-image.jpg'),
    'noindex'     => false,
    'schema'      => [],
    'body_class'  => '',
], $page ?? []);

$canonical = url($page['path']);
$current = trim($page['path'], '/');
$isActive = function (string $path) use ($current): string {
    return trim($path, '/') === $current ? ' aria-current="page"' : '';
};
$servicesActive = isset($SERVICES[$current]);
?><!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title><?= e($page['title']) ?></title>
<meta name="description" content="<?= e($page['description']) ?>">
<?php if ($page['noindex']): ?>
<meta name="robots" content="noindex, follow">
<?php else: ?>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta name="theme-color" content="#01183A">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="US-NH">
<meta name="geo.placename" content="<?= e(BASE_CITY) ?>">
<?php if (GOOGLE_SITE_VERIFICATION): ?>
<meta name="google-site-verification" content="<?= e(GOOGLE_SITE_VERIFICATION) ?>">
<?php endif; ?>

<!-- Open Graph / Social -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="<?= e($page['title']) ?>">
<meta property="og:description" content="<?= e($page['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($page['image']) ?>">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($page['title']) ?>">
<meta name="twitter:description" content="<?= e($page['description']) ?>">
<meta name="twitter:image" content="<?= e($page['image']) ?>">

<!-- Icons -->
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="<?= e(asset('img/favicon-32.png')) ?>">
<link rel="apple-touch-icon" href="<?= e(asset('img/apple-touch-icon.png')) ?>">
<link rel="manifest" href="/site.webmanifest">

<!-- Performance -->
<link rel="preconnect" href="https://images.pexels.com" crossorigin>
<link rel="dns-prefetch" href="https://images.pexels.com">
<link rel="preload" href="/assets/fonts/ArchivoBlack-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Poppins-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="<?= e(asset('css/style.css')) ?>">

<?= json_ld(business_schema()) ?>
<?php foreach ($page['schema'] as $schema): ?>
<?= json_ld($schema) ?>
<?php endforeach; ?>

<?php if (GA4_ID || GOOGLE_ADS_ID): ?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= e(GA4_ID ?: GOOGLE_ADS_ID) ?>"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
<?php if (GA4_ID): ?>gtag('config', '<?= e(GA4_ID) ?>');<?php endif; ?>
<?php if (GOOGLE_ADS_ID): ?>gtag('config', '<?= e(GOOGLE_ADS_ID) ?>');<?php endif; ?>
</script>
<?php endif; ?>
<?php if (META_PIXEL_ID): ?>
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '<?= e(META_PIXEL_ID) ?>');
fbq('track', 'PageView');
</script>
<?php endif; ?>
<script>
window.RA = {
  adsId: <?= json_encode(GOOGLE_ADS_ID) ?>,
  adsLabel: <?= json_encode(GOOGLE_ADS_LEAD_LABEL) ?>
};
document.documentElement.classList.add('js');
</script>
</head>
<body class="<?= e($page['body_class']) ?>">
<a class="skip-link" href="#main">Skip to content</a>

<div class="topbar" role="region" aria-label="Highlights">
  <div class="container topbar__inner">
    <p class="topbar__msg">
      <span><?= icon('tag') ?> <strong>Free estimates</strong> — no charge, anywhere we serve</span>
      <span class="topbar__sep" aria-hidden="true">◆</span>
      <span><?= icon('shield') ?> 1-Year Warranty</span>
      <span class="topbar__sep" aria-hidden="true">◆</span>
      <span><?= icon('pin') ?> Serving Manchester &amp; Southern NH</span>
    </p>
    <a class="topbar__phone" href="<?= e(sms_link()) ?>" data-track="sms_topbar"><?= icon('sms') ?> Text <?= e(PHONE_DISPLAY) ?></a>
  </div>
</div>

<header class="site-header" id="top">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> — Home">
      <picture>
        <source srcset="<?= e(asset('img/logo-horizontal-gold.webp')) ?>" type="image/webp">
        <img src="<?= e(asset('img/logo-horizontal-gold.png')) ?>" alt="<?= e(SITE_NAME) ?> logo" width="388" height="64">
      </picture>
    </a>

    <nav class="main-nav" aria-label="Main">
      <ul class="main-nav__list">
        <li><a href="/"<?= $isActive('') ?>>Home</a></li>
        <li class="has-dropdown">
          <a href="/#services" class="<?= $servicesActive ? 'is-active' : '' ?>" aria-haspopup="true">Services <?= icon('chevron', 'icon icon--xs') ?></a>
          <ul class="dropdown">
            <?php foreach ($SERVICES as $svcSlug => $svc): ?>
            <li><a href="<?= e(link_to($svcSlug)) ?>"<?= $isActive($svcSlug) ?>><?= icon($svc['icon']) ?> <?= e($svc['nav']) ?></a></li>
            <?php endforeach; ?>
          </ul>
        </li>
        <li><a href="/about"<?= $isActive('about') ?>>About</a></li>
        <li><a href="/service-areas"<?= $isActive('service-areas') ?>>Service Areas</a></li>
        <li><a href="/contact"<?= $isActive('contact') ?>>Contact</a></li>
      </ul>
    </nav>

    <div class="header-cta">
      <a class="btn btn--ghost btn--sm" href="<?= e(sms_link()) ?>" data-track="sms_header"><?= icon('sms') ?> Text Us</a>
      <a class="btn btn--gold btn--sm" href="/contact#estimate" data-track="cta_header">Free Estimate</a>
    </div>

    <button class="nav-toggle" type="button" aria-controls="mobile-menu" aria-expanded="false" aria-label="Open menu">
      <span class="nav-toggle__bar"></span>
      <span class="nav-toggle__bar"></span>
      <span class="nav-toggle__bar"></span>
    </button>
  </div>
</header>

<!-- Mobile menu (off-canvas) -->
<div class="mobile-menu" id="mobile-menu" aria-hidden="true">
  <div class="mobile-menu__overlay" data-close-menu></div>
  <div class="mobile-menu__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="mobile-menu__head">
      <img src="<?= e(asset('img/logo-horizontal-gold.png')) ?>" alt="" width="388" height="64" class="mobile-menu__logo">
      <button class="mobile-menu__close" type="button" aria-label="Close menu" data-close-menu><?= icon('close') ?></button>
    </div>
    <nav class="mobile-menu__nav" aria-label="Mobile">
      <ul>
        <li><a href="/"<?= $isActive('') ?>>Home</a></li>
        <li>
          <button class="mobile-menu__sub-toggle" type="button" aria-expanded="<?= $servicesActive ? 'true' : 'false' ?>" aria-controls="mm-services">
            Services <?= icon('chevron', 'icon icon--xs') ?>
          </button>
          <ul class="mobile-menu__sub" id="mm-services"<?= $servicesActive ? '' : ' hidden' ?>>
            <?php foreach ($SERVICES as $svcSlug => $svc): ?>
            <li><a href="<?= e(link_to($svcSlug)) ?>"<?= $isActive($svcSlug) ?>><?= icon($svc['icon']) ?> <?= e($svc['nav']) ?></a></li>
            <?php endforeach; ?>
          </ul>
        </li>
        <li><a href="/about"<?= $isActive('about') ?>>About</a></li>
        <li><a href="/service-areas"<?= $isActive('service-areas') ?>>Service Areas</a></li>
        <li><a href="/contact"<?= $isActive('contact') ?>>Contact</a></li>
      </ul>
    </nav>
    <div class="mobile-menu__cta">
      <a class="btn btn--gold btn--block" href="/contact#estimate" data-track="cta_mobile_menu">Get a Free Estimate</a>
      <a class="btn btn--outline-light btn--block" href="<?= e(sms_link()) ?>" data-track="sms_mobile_menu"><?= icon('sms') ?> Text <?= e(PHONE_DISPLAY) ?></a>
      <p class="mobile-menu__note"><?= icon('shield') ?> Free estimates · 1-Year Warranty</p>
    </div>
  </div>
</div>

<main id="main">
