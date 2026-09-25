<?php
require __DIR__ . '/includes/functions.php';

$page = [
    'slug' => 'thank-you',
    'title' => 'Thank You | Guidine Pereira Construction',
    'description' => 'Your estimate request was received.',
    'noindex' => true,
    'body' => 'page-thanks',
];
include __DIR__ . '/includes/header.php';
?>

<section class="page-hero page-hero--center">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__narrow">
    <div class="thanks__icon"><?= icon('check') ?></div>
    <p class="eyebrow eyebrow--light">Request received</p>
    <h1 class="page-hero__title">Thank you. We'll be in touch soon.</h1>
    <p class="hero__lead">Your estimate request is on its way to our team. We will contact you to schedule a visit. If your project is urgent, call or text us now.</p>
    <div class="hero__actions">
      <a class="btn btn--primary btn--lg" href="<?= e(tel_link()) ?>" data-track="call"><?= icon('phone') ?><?= e(PHONE_DISPLAY) ?></a>
      <a class="btn btn--outline-light btn--lg" href="<?= e(url('projects')) ?>">See our projects</a>
    </div>
  </div>
</section>

<?php if (GOOGLE_ADS_ID && GOOGLE_ADS_LEAD_LABEL): ?>
<script>if(typeof gtag==='function'){gtag('event','conversion',{send_to:'<?= e(GOOGLE_ADS_ID . '/' . GOOGLE_ADS_LEAD_LABEL) ?>'});}</script>
<?php endif; ?>
<?php if (GA4_ID): ?>
<script>if(typeof gtag==='function'){gtag('event','generate_lead',{form:'estimate'});}</script>
<?php endif; ?>
<?php if (META_PIXEL_ID): ?>
<script>if(typeof fbq==='function'){fbq('track','Lead');}</script>
<?php endif; ?>
<script>window.dataLayer=window.dataLayer||[];window.dataLayer.push({event:'estimate_form_submit'});</script>

<?php include __DIR__ . '/includes/footer.php';
