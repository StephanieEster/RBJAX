<?php
require __DIR__ . '/includes/bootstrap.php';

$page = [
    'title'       => 'Privacy Policy | R.A Tile Renovation',
    'description' => 'How R.A Tile Renovation collects, uses and protects the information you share through our website.',
    'path'        => 'privacy-policy',
    'body_class'  => 'page-legal',
];
require __DIR__ . '/includes/header.php';
?>

<section class="section">
  <div class="container container--narrow prose">
    <?= breadcrumbs_html(['Home' => '', 'Privacy Policy' => 'privacy-policy']) ?>
    <h1 class="section-title">Privacy Policy</h1>
    <p><em>Last updated: <?= date('F j, Y', filemtime(__FILE__)) ?></em></p>

    <h2 class="h4">Information we collect</h2>
    <p>When you request an estimate or contact us, we collect the information you provide, such as your name, phone number, e-mail address, city or ZIP code and details about your project. We may also collect basic technical data (such as pages visited and the ad or link that brought you to our site) to understand how visitors find us.</p>

    <h2 class="h4">How we use your information</h2>
    <p>We use your information only to respond to your request, schedule and provide your estimate, perform the services you hire us for and follow up about your project. By submitting a form, you agree that we may contact you by text message, phone call or e-mail. Message and data rates may apply. You can reply STOP to any text message to opt out.</p>

    <h2 class="h4">Sharing</h2>
    <p>We do not sell or rent your personal information. We may use trusted service providers (for example, e-mail, CRM, website hosting and advertising platforms such as Google and Meta) that process data on our behalf.</p>

    <h2 class="h4">Cookies and analytics</h2>
    <p>Our website may use cookies and similar technologies from analytics and advertising partners to measure site performance and the effectiveness of our ads. You can disable cookies in your browser settings.</p>

    <h2 class="h4">Data security</h2>
    <p>We take reasonable measures to protect the information you share with us. No method of transmission over the internet is 100% secure, but we work to keep your data safe.</p>

    <h2 class="h4">Contact</h2>
    <p>Questions about this policy? E-mail us at <a href="mailto:<?= e(EMAIL_PUBLIC) ?>"><?= e(EMAIL_PUBLIC) ?></a> or text <?= e(PHONE_DISPLAY) ?>.</p>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
