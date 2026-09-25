<?php $estimateHeading = $estimateHeading ?? 'Tell us about your project'; ?>
<section class="section estimate" id="estimate" aria-labelledby="estimate-title">
  <div class="container estimate__grid">
    <div class="estimate__intro reveal">
      <p class="eyebrow">Free in-home estimate</p>
      <h2 class="h2" id="estimate-title"><?= e($estimateHeading) ?></h2>
      <p class="lead">Send the form or reach out directly. We schedule a visit, measure the space and, in most cases, give you the price right there.</p>
      <ul class="estimate__points">
        <li><?= icon('check') ?>No cost and no obligation</li>
        <li><?= icon('check') ?>Flexible visit times, including busy weeks</li>
        <li><?= icon('check') ?>Clear price and timeline before any work starts</li>
      </ul>
      <div class="estimate__direct">
        <a class="contact-card" href="<?= e(tel_link()) ?>" data-track="call">
          <?= icon('phone') ?><span><small>Call</small><?= e(PHONE_DISPLAY) ?></span>
        </a>
        <a class="contact-card" href="<?= e(sms_link()) ?>" data-track="sms">
          <?= icon('sms') ?><span><small>Text</small><?= e(PHONE_DISPLAY) ?></span>
        </a>
        <a class="contact-card contact-card--wide" href="mailto:<?= e(EMAIL) ?>" data-track="email">
          <?= icon('mail') ?><span><small>Email</small><span class="break"><?= e(EMAIL) ?></span></span>
        </a>
      </div>
    </div>
    <div class="estimate__card">
      <h3 class="estimate__card-title">Request your free estimate</h3>
      <?php include __DIR__ . '/estimate-form.php'; ?>
    </div>
  </div>
</section>
