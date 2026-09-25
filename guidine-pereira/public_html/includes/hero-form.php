<?php /* Estimate form card shown inside the hero. Optional: $preselect. */ ?>
<div class="hero-form" id="quote">
  <div class="hero-form__head">
    <p class="hero-form__kicker">Free in-home estimate</p>
    <h2 class="hero-form__title">Get your price, fast</h2>
    <p class="hero-form__sub">Takes less than a minute. We call or text you back to schedule a visit.</p>
  </div>
  <?php
  $formId = 'quote-form';
  $compact = true;
  include __DIR__ . '/estimate-form.php';
  ?>
</div>
