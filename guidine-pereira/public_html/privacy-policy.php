<?php
require __DIR__ . '/includes/functions.php';

$page = [
    'slug' => 'privacy-policy',
    'title' => 'Privacy Policy | Guidine Pereira Construction',
    'description' => 'How Guidine Pereira Construction LLC collects and uses the information you share through this website.',
    'body' => 'page-legal',
];
include __DIR__ . '/includes/header.php';
?>

<section class="page-hero">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__narrow">
    <?php breadcrumbs([['Home', ''], ['Privacy Policy', 'privacy-policy']]); ?>
    <h1 class="page-hero__title">Privacy Policy</h1>
    <p class="hero__lead">Last updated: <?= date('F Y', filemtime(__FILE__)) ?></p>
  </div>
</section>

<section class="section">
  <div class="container prose">
    <p><?= e(BUSINESS_NAME) ?> ("we", "us") respects your privacy. This policy explains what information we collect through this website and how we use it.</p>
    <h2>Information you give us</h2>
    <p>When you request an estimate, we collect the details you enter in the form: your name, phone number, email address, city or ZIP code, the service you are interested in and any project details you choose to share.</p>
    <h2>How we use it</h2>
    <p>We use this information only to respond to your request, schedule an estimate, prepare a quote and communicate with you about your project. We may contact you by phone, text message or email, based on the preference you select. Message and data rates may apply to text messages.</p>
    <h2>What we don't do</h2>
    <p>We do not sell, rent or trade your personal information. We do not share it with third parties except service providers that help us operate this website and deliver messages, and only as needed for that purpose.</p>
    <h2>Cookies and analytics</h2>
    <p>This website may use cookies and similar technologies from Google and Meta to measure visits and the performance of our advertising. You can block or delete cookies in your browser settings at any time.</p>
    <h2>Data retention and your choices</h2>
    <p>We keep your information only as long as needed to serve you and meet legal obligations. You can ask us to update or delete your information, or to stop contacting you, at any time.</p>
    <h2>Contact</h2>
    <p>Questions about this policy? Email <a href="mailto:<?= e(EMAIL) ?>"><?= e(EMAIL) ?></a> or call <a href="<?= e(tel_link()) ?>"><?= e(PHONE_DISPLAY) ?></a>.</p>
  </div>
</section>

<?php include __DIR__ . '/includes/footer.php';
