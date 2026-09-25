<?php
require __DIR__ . '/includes/functions.php';

$page = [
    'slug' => 'contact',
    'title' => 'Contact & Free Estimate | Guidine Pereira, Myrtle Beach SC',
    'description' => 'Request a free in-home estimate for tile, shower, bathroom, flooring or backsplash work in the Myrtle Beach area. Call or text (843) 492-8374.',
    'schema' => [breadcrumb_schema([['Home', ''], ['Contact', 'contact']])],
    'body' => 'page-contact',
];
include __DIR__ . '/includes/header.php';
?>

<section class="page-hero">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__narrow">
    <?php breadcrumbs([['Home', ''], ['Contact', 'contact']]); ?>
    <p class="eyebrow eyebrow--light">Contact</p>
    <h1 class="page-hero__title">Let's talk about your project</h1>
    <p class="hero__lead">Call, text or send the form below. We will set up a free in-home estimate at a time that works for you.</p>
    <div class="hero__actions">
      <a class="btn btn--primary btn--lg" href="<?= e(tel_link()) ?>" data-track="call"><?= icon('phone') ?>Call <?= e(PHONE_DISPLAY) ?></a>
      <a class="btn btn--outline-light btn--lg" href="<?= e(sms_link()) ?>" data-track="sms"><?= icon('sms') ?>Send a text</a>
    </div>
  </div>
</section>

<?php
$estimateHeading = 'Request your free estimate';
include __DIR__ . '/includes/estimate-section.php';
?>

<section class="section section--soft" aria-labelledby="faq-title">
  <div class="container faq-wrap">
    <div class="faq-wrap__head reveal">
      <p class="eyebrow">Before you reach out</p>
      <h2 class="h2" id="faq-title">Common questions</h2>
    </div>
    <div class="reveal"><?php render_faq($FAQ_GENERAL); ?></div>
  </div>
</section>

<?php include __DIR__ . '/includes/footer.php';
