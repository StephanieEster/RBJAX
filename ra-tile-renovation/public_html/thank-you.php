<?php
require __DIR__ . '/includes/bootstrap.php';

$page = [
    'title'       => 'Thank You | R.A Tile Renovation',
    'description' => 'Thank you for requesting a free estimate from R.A Tile Renovation.',
    'path'        => 'thank-you',
    'noindex'     => true,
    'body_class'  => 'page-thanks',
];
require __DIR__ . '/includes/header.php';
?>

<section class="section thanks">
  <div class="container container--narrow center">
    <span class="thanks__icon"><?= icon('check') ?></span>
    <h1 class="section-title">Thank You! We Got Your Request.</h1>
    <p class="section-lead">We'll reach out shortly to schedule your free estimate. Want to speed things up? Send us a text with a few photos of your space.</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--gold btn--lg" href="<?= e(sms_link("Hi Renato! I just sent the estimate form on your website. Here are some photos of my space: ")) ?>" data-track="sms_thankyou"><?= icon('sms') ?> Text Photos to <?= e(PHONE_DISPLAY) ?></a>
      <a class="btn btn--outline btn--lg" href="/">Back to Home</a>
    </div>
  </div>
</section>

<script>
  // Conversion tracking (fires only if IDs are configured in includes/config.php)
  window.addEventListener('load', function () {
    try {
      if (window.gtag && window.RA && RA.adsId && RA.adsLabel) {
        gtag('event', 'conversion', { send_to: RA.adsId + '/' + RA.adsLabel });
      }
      if (window.gtag) { gtag('event', 'generate_lead', { method: 'website_form' }); }
      if (window.fbq) { fbq('track', 'Lead'); }
    } catch (e) {}
  });
</script>

<?php require __DIR__ . '/includes/footer.php'; ?>
