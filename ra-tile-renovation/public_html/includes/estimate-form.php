<?php
/**
 * Estimate form partial.
 * Optional vars before include: $formId (string), $formTitle (string), $formCompact (bool), $formService (slug)
 */
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'estimate-form.php') {
    http_response_code(403);
    exit;
}
$formId      = $formId ?? 'estimate-form';
$formTitle   = $formTitle ?? 'Get Your Free Estimate';
$formCompact = $formCompact ?? false;
$formService = $formService ?? '';
$err         = $_GET['form_error'] ?? '';
?>
<form class="lead-form<?= $formCompact ? ' lead-form--compact' : '' ?>" id="<?= e($formId) ?>" action="/send.php" method="post" novalidate data-lead-form>
  <div class="lead-form__head">
    <p class="lead-form__title"><?= e($formTitle) ?></p>
    <p class="lead-form__sub"><?= icon('check') ?> 100% free · No obligation · Fast reply</p>
  </div>

  <?php if ($err): ?>
  <div class="form-alert form-alert--error" role="alert">Something went wrong sending your request. Please check the fields and try again, or text us at <a href="<?= e(sms_link()) ?>"><?= e(PHONE_DISPLAY) ?></a>.</div>
  <?php endif; ?>
  <div class="form-alert" role="status" aria-live="polite" hidden data-form-status></div>

  <div class="form-grid">
    <div class="field">
      <label for="<?= e($formId) ?>-name">Full name <span aria-hidden="true">*</span></label>
      <input id="<?= e($formId) ?>-name" name="name" type="text" autocomplete="name" required maxlength="80" placeholder="John Smith">
      <p class="field__error" hidden>Please enter your name.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-phone">Mobile phone <span aria-hidden="true">*</span></label>
      <input id="<?= e($formId) ?>-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required maxlength="20" placeholder="(603) 555-0123" data-phone>
      <p class="field__error" hidden>Please enter a valid 10-digit US phone number.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-email">E-mail <span class="field__opt">(optional)</span></label>
      <input id="<?= e($formId) ?>-email" name="email" type="email" autocomplete="email" maxlength="120" placeholder="you@email.com">
      <p class="field__error" hidden>Please enter a valid e-mail address.</p>
    </div>
    <div class="field">
      <label for="<?= e($formId) ?>-city">City / ZIP in NH <span aria-hidden="true">*</span></label>
      <input id="<?= e($formId) ?>-city" name="city" type="text" autocomplete="address-level2" required maxlength="60" placeholder="Manchester or 03101" list="<?= e($formId) ?>-cities">
      <datalist id="<?= e($formId) ?>-cities">
        <?php foreach ($CITIES as $c): ?><option value="<?= e($c) ?>"><?php endforeach; ?>
      </datalist>
      <p class="field__error" hidden>Please tell us where the project is.</p>
    </div>
    <div class="field field--full">
      <label for="<?= e($formId) ?>-service">What do you need? <span aria-hidden="true">*</span></label>
      <select id="<?= e($formId) ?>-service" name="service" required>
        <option value="">Select a service…</option>
        <?php foreach ($SERVICES as $svcSlug => $svc): ?>
        <option value="<?= e($svc['nav']) ?>"<?= $formService === $svcSlug ? ' selected' : '' ?>><?= e($svc['nav']) ?></option>
        <?php endforeach; ?>
        <option value="Other tile project">Other tile project</option>
      </select>
      <p class="field__error" hidden>Please choose a service.</p>
    </div>
    <?php if (!$formCompact): ?>
    <div class="field field--full">
      <label for="<?= e($formId) ?>-message">Project details <span class="field__opt">(optional)</span></label>
      <textarea id="<?= e($formId) ?>-message" name="message" rows="4" maxlength="2000" placeholder="Tell us about your project: room, approximate size, tile you like, timeline…"></textarea>
    </div>
    <fieldset class="field field--full field--radios">
      <legend>Best way to reach you</legend>
      <label class="radio"><input type="radio" name="contact_pref" value="Text" checked> <span>Text message</span></label>
      <label class="radio"><input type="radio" name="contact_pref" value="Call"> <span>Phone call</span></label>
      <label class="radio"><input type="radio" name="contact_pref" value="E-mail"> <span>E-mail</span></label>
    </fieldset>
    <?php endif; ?>
  </div>

  <!-- anti-spam -->
  <div class="hp" aria-hidden="true">
    <label>Leave this field empty <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
  </div>
  <input type="hidden" name="token" value="<?= e(form_token()) ?>">
  <input type="hidden" name="form_id" value="<?= e($formId) ?>">
  <input type="hidden" name="page_url" value="">
  <input type="hidden" name="utm" value="">

  <button class="btn btn--gold btn--block btn--lg" type="submit" data-submit>
    <span data-submit-label>Request My Free Estimate</span>
    <?= icon('arrow') ?>
  </button>
  <p class="lead-form__legal">By submitting, you agree to be contacted by text message, phone or e-mail about your estimate. Msg &amp; data rates may apply. We never share your information. <a href="/privacy-policy">Privacy Policy</a>.</p>
</form>
