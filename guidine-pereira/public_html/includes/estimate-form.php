<?php
/* Estimate request form. Optional: $formId, $formTitle, $preselect (service slug). */
$formId = $formId ?? 'estimate-form';
$preselect = $preselect ?? '';
$status = $_GET['form'] ?? '';
?>
<form class="form" id="<?= e($formId) ?>" action="<?= e(url('send.php')) ?>" method="post" novalidate data-estimate-form>
  <div class="form__grid">
    <div class="field">
      <label for="<?= e($formId) ?>-name">Full name <span aria-hidden="true">*</span></label>
      <input id="<?= e($formId) ?>-name" name="name" type="text" autocomplete="name" required maxlength="80" placeholder="Your name">
      <p class="field__error" data-for="name">Please enter your name.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-phone">Phone <span aria-hidden="true">*</span></label>
      <input id="<?= e($formId) ?>-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required maxlength="20" placeholder="(843) 000-0000">
      <p class="field__error" data-for="phone">Please enter a valid phone number.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-email">Email</label>
      <input id="<?= e($formId) ?>-email" name="email" type="email" autocomplete="email" maxlength="120" placeholder="you@email.com">
      <p class="field__error" data-for="email">Please enter a valid email address.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-city">City or ZIP code <span aria-hidden="true">*</span></label>
      <input id="<?= e($formId) ?>-city" name="city" type="text" autocomplete="address-level2" required maxlength="60" placeholder="Myrtle Beach, 29577">
      <p class="field__error" data-for="city">Tell us where the project is.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-service">Service needed <span aria-hidden="true">*</span></label>
      <div class="select">
        <select id="<?= e($formId) ?>-service" name="service" required>
          <option value="">Select a service</option>
          <?php foreach ($SERVICES as $svcSlug => $svc): ?>
          <option value="<?= e($svc['name']) ?>"<?= $preselect === $svcSlug ? ' selected' : '' ?>><?= e($svc['name']) ?></option>
          <?php endforeach; ?>
          <option value="Other / Not sure yet">Other / Not sure yet</option>
        </select>
      </div>
      <p class="field__error" data-for="service">Please choose a service.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-timeline">When would you like to start?</label>
      <div class="select">
        <select id="<?= e($formId) ?>-timeline" name="timeline">
          <option value="As soon as possible">As soon as possible</option>
          <option value="Within 1 month">Within 1 month</option>
          <option value="1 to 3 months">1 to 3 months</option>
          <option value="Just planning">Just planning</option>
        </select>
      </div>
    </div>
    <fieldset class="field field--full field--choice">
      <legend>Best way to reach you</legend>
      <div class="choices">
        <label class="choice"><input type="radio" name="contact_pref" value="Call" checked><span>Call</span></label>
        <label class="choice"><input type="radio" name="contact_pref" value="Text"><span>Text</span></label>
        <label class="choice"><input type="radio" name="contact_pref" value="Email"><span>Email</span></label>
      </div>
    </fieldset>
    <div class="field field--full">
      <label for="<?= e($formId) ?>-message">Project details</label>
      <textarea id="<?= e($formId) ?>-message" name="message" rows="4" maxlength="2000" placeholder="Room, approximate size, tile you have in mind, anything we should know."></textarea>
    </div>
  </div>

  <div class="hp" aria-hidden="true">
    <label for="<?= e($formId) ?>-website">Leave this field empty</label>
    <input id="<?= e($formId) ?>-website" name="website" type="text" tabindex="-1" autocomplete="off">
  </div>
  <input type="hidden" name="ts" value="<?= time() ?>">
  <input type="hidden" name="page" value="<?= e($page['slug'] ?: 'home') ?>">
  <input type="hidden" name="utm_source" value="">
  <input type="hidden" name="utm_medium" value="">
  <input type="hidden" name="utm_campaign" value="">
  <input type="hidden" name="utm_term" value="">
  <input type="hidden" name="gclid" value="">
  <input type="hidden" name="fbclid" value="">

  <div class="form__foot">
    <button class="btn btn--primary btn--lg form__submit" type="submit">
      <span class="form__label">Request My Free Estimate</span>
      <span class="spinner" aria-hidden="true"></span>
    </button>
    <p class="form__legal">No cost, no obligation. By sending, you agree to be contacted about your project. See our <a href="<?= e(url('privacy-policy')) ?>">privacy policy</a>.</p>
  </div>
  <div class="form__status<?= $status === 'error' ? ' is-error' : '' ?>" role="status" aria-live="polite"><?php if ($status === 'error'): ?>Something went wrong. Please call or text us at <a href="<?= e(tel_link()) ?>"><?= e(PHONE_DISPLAY) ?></a>.<?php endif; ?></div>
</form>
