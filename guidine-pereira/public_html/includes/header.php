<?php
/**
 * Expects $page = [
 *   'slug' => '', 'title' => '', 'description' => '',
 *   'noindex' => false, 'schema' => [], 'preload' => 'image-slug', 'body' => 'css-class'
 * ]
 */
$page += ['slug' => '', 'title' => BUSINESS_SHORT, 'description' => '', 'noindex' => false, 'schema' => [], 'preload' => '', 'body' => ''];
$canonical = abs_url($page['slug']);
$ogImage = site_url() . '/assets/img/og-image.jpg';
$current = $page['slug'];
$isService = isset($SERVICES[$current]);
$estimateHref = !empty($page['hero_form']) ? '#quote' : url('contact') . '#estimate';
?>
<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>document.documentElement.className+=' js';</script>
<title><?= e($page['title']) ?></title>
<meta name="description" content="<?= e($page['description']) ?>">
<?php if ($page['noindex']): ?>
<meta name="robots" content="noindex, follow">
<?php else: ?>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta name="theme-color" content="#1e1e1e">
<meta name="format-detection" content="telephone=no">
<meta name="geo.region" content="US-SC">
<meta name="geo.placename" content="Myrtle Beach">

<meta property="og:type" content="website">
<meta property="og:site_name" content="<?= e(BUSINESS_NAME) ?>">
<meta property="og:title" content="<?= e($page['title']) ?>">
<meta property="og:description" content="<?= e($page['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($ogImage) ?>">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($page['title']) ?>">
<meta name="twitter:description" content="<?= e($page['description']) ?>">
<meta name="twitter:image" content="<?= e($ogImage) ?>">

<link rel="icon" href="<?= e(url('favicon.ico')) ?>" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="<?= e(asset('img/brand/favicon-32.png')) ?>">
<link rel="apple-touch-icon" href="<?= e(url('apple-touch-icon.png')) ?>">
<link rel="manifest" href="<?= e(url('site.webmanifest')) ?>">

<link rel="preload" href="<?= e(base_path() . '/assets/fonts/anek-devanagari-latin.woff2') ?>" as="font" type="font/woff2" crossorigin>
<?php if ($page['preload']): ?>
<link rel="preload" as="image" href="<?= e(work_img($page['preload'])) ?>" imagesrcset="<?= e(work_img($page['preload'], 'sm')) ?> 480w, <?= e(work_img($page['preload'])) ?> 900w" imagesizes="(max-width: 900px) 100vw, 45vw" fetchpriority="high">
<?php endif; ?>
<link rel="stylesheet" href="<?= e(asset('css/style.css')) ?>">

<?php
json_ld(business_schema());
foreach ($page['schema'] as $schema) {
    json_ld($schema);
}
include __DIR__ . '/tracking-head.php';
?>
</head>
<body class="<?= e($page['body']) ?>">
<?php if (GTM_ID): ?>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=<?= e(GTM_ID) ?>" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<?php endif; ?>
<a class="skip-link" href="#main">Skip to content</a>

<div class="topbar">
  <div class="container topbar__inner">
    <p class="topbar__note">Licensed &amp; insured<span class="dot" aria-hidden="true"></span>Family-owned<span class="dot" aria-hidden="true"></span>Serving the Grand Strand &amp; beyond</p>
    <div class="topbar__links">
      <a href="mailto:<?= e(EMAIL) ?>" class="topbar__mail"><?= icon('mail') ?><span><?= e(EMAIL) ?></span></a>
      <a href="<?= e(FACEBOOK_URL) ?>" target="_blank" rel="noopener" aria-label="Facebook"><?= icon('facebook') ?></a>
      <a href="<?= e(INSTAGRAM_URL) ?>" target="_blank" rel="noopener" aria-label="Instagram"><?= icon('instagram') ?></a>
    </div>
  </div>
</div>

<header class="header" id="top">
  <div class="nav-backdrop" data-nav-close></div>
  <div class="container header__inner">
    <a class="brand" href="<?= e(url()) ?>" aria-label="<?= e(BUSINESS_NAME) ?> home">
      <img src="<?= e(asset('img/brand/logo-horizontal-light.webp')) ?>" width="520" height="101" alt="<?= e(BUSINESS_NAME) ?>">
    </a>

    <nav class="nav" id="site-nav" aria-label="Main">
      <div class="nav__head">
        <span class="nav__title">Menu</span>
        <button class="nav__close" type="button" data-nav-close aria-label="Close menu"><?= icon('close') ?></button>
      </div>
      <ul class="nav__list">
        <li><a href="<?= e(url()) ?>"<?= $current === '' ? ' aria-current="page"' : '' ?>>Home</a></li>
        <li class="has-sub<?= $isService ? ' is-active' : '' ?>">
          <a href="<?= e(url('shower-bathroom-remodeling')) ?>" class="has-sub__link">Services</a>
          <button class="sub-toggle" type="button" aria-expanded="false" aria-controls="sub-services" aria-label="Show services"><?= icon('chevron') ?></button>
          <ul class="sub" id="sub-services">
            <?php foreach ($SERVICES as $svcSlug => $svc): ?>
            <li><a href="<?= e(url($svcSlug)) ?>"<?= $current === $svcSlug ? ' aria-current="page"' : '' ?>><?= e($svc['nav']) ?></a></li>
            <?php endforeach; ?>
          </ul>
        </li>
        <li><a href="<?= e(url('projects')) ?>"<?= $current === 'projects' ? ' aria-current="page"' : '' ?>>Projects</a></li>
        <li><a href="<?= e(url('about')) ?>"<?= $current === 'about' ? ' aria-current="page"' : '' ?>>About</a></li>
        <li><a href="<?= e(url('service-areas')) ?>"<?= $current === 'service-areas' ? ' aria-current="page"' : '' ?>>Service Areas</a></li>
        <li><a href="<?= e(url('contact')) ?>"<?= $current === 'contact' ? ' aria-current="page"' : '' ?>>Contact</a></li>
      </ul>
      <div class="nav__cta">
        <a class="btn btn--primary btn--block" href="<?= e($estimateHref) ?>">Get a Free Estimate</a>
        <div class="nav__contact">
          <a class="btn btn--ghost-light" href="<?= e(tel_link()) ?>" data-track="call"><?= icon('phone') ?>Call</a>
          <a class="btn btn--ghost-light" href="<?= e(sms_link()) ?>" data-track="sms"><?= icon('sms') ?>Text</a>
        </div>
        <p class="nav__meta"><?= e(PHONE_DISPLAY) ?><br><?= e(EMAIL) ?></p>
      </div>
    </nav>

    <div class="header__actions">
      <a class="header__phone" href="<?= e(tel_link()) ?>" data-track="call">
        <?= icon('phone') ?>
        <span><small>Call or text</small><?= e(PHONE_DISPLAY) ?></span>
      </a>
      <a class="btn btn--primary header__cta" href="<?= e($estimateHref) ?>">Free Estimate</a>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="site-nav" data-nav-open>
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<main id="main">
