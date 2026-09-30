<?php
require __DIR__ . '/includes/bootstrap.php';

$page = [
    'title'       => 'Free Estimate & Contact | R.A Tile Renovation — Manchester, NH',
    'description' => 'Request your free tile estimate in Manchester & Southern NH. Text (978) 331-6200 or fill out the form — showers, bathrooms, floors, backsplashes and fireplaces.',
    'path'        => 'contact',
    'body_class'  => 'page-contact',
    'schema'      => [breadcrumb_schema(['Home' => '', 'Contact' => 'contact'])],
];
require __DIR__ . '/includes/header.php';
?>

<section class="page-hero page-hero--short" aria-labelledby="page-title">
  <div class="page-hero__bg"><?= img('shower-3', '16:9', '100vw', ['eager' => true, 'widths' => [800, 1200, 1600], 'base' => 1600]) ?></div>
  <div class="container page-hero__inner">
    <?= breadcrumbs_html(['Home' => '', 'Contact' => 'contact']) ?>
    <p class="eyebrow eyebrow--light"><?= icon('tag', 'icon icon--xs') ?> 100% free</p>
    <h1 id="page-title" class="page-hero__title">Get Your <span class="text-gold">Free Estimate</span></h1>
    <p class="page-hero__lead">Text us or fill out the form. We'll schedule a free in-home estimate at a time that works for you.</p>
  </div>
</section>

<section class="section" aria-label="Contact options">
  <div class="container contact-grid">
    <div class="contact-info">
      <h2 class="section-title">The Fastest Way: Send Us a Text</h2>
      <p>Texting is the quickest way to reach us. Send a few photos of your space and a short description, and we'll get back to you to schedule your visit.</p>
      <div class="contact-cards">
        <a class="contact-card contact-card--primary" href="<?= e(sms_link()) ?>" data-track="sms_contact">
          <span class="contact-card__icon"><?= icon('sms') ?></span>
          <span><strong>Text us</strong><?= e(PHONE_DISPLAY) ?></span>
        </a>
        <a class="contact-card" href="<?= e(tel_link()) ?>" data-track="call_contact">
          <span class="contact-card__icon"><?= icon('phone') ?></span>
          <span><strong>Call</strong><?= e(PHONE_DISPLAY) ?></span>
        </a>
        <a class="contact-card" href="mailto:<?= e(EMAIL_PUBLIC) ?>">
          <span class="contact-card__icon"><?= icon('mail') ?></span>
          <span><strong>E-mail</strong><?= e(EMAIL_PUBLIC) ?></span>
        </a>
        <a class="contact-card" href="<?= e(INSTAGRAM_URL) ?>" target="_blank" rel="noopener">
          <span class="contact-card__icon"><?= icon('instagram') ?></span>
          <span><strong>Instagram</strong>@ra_tile_renovation_33</span>
        </a>
      </div>
      <ul class="checklist">
        <li><?= icon('check') ?> Free estimates anywhere in our NH service area</li>
        <li><?= icon('check') ?> 1-year warranty on labor &amp; product</li>
        <li><?= icon('check') ?> Payment: Zelle, cash, check or Venmo</li>
        <li><?= icon('pin') ?> <?= e(BASE_CITY) ?>, <?= e(BASE_STATE) ?> + ~50 miles (NH only)</li>
      </ul>
    </div>
    <div class="contact-form" id="estimate">
      <?php $formId = 'contact-form'; $formTitle = 'Request a Free Estimate'; $formCompact = false; include __DIR__ . '/includes/estimate-form.php'; ?>
    </div>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
