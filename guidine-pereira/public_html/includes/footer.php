</main>

<footer class="footer">
  <div class="container footer__grid">
    <div class="footer__brand">
      <a href="<?= e(url()) ?>" class="footer__logo" aria-label="<?= e(BUSINESS_NAME) ?> home">
        <img src="<?= e(asset('img/brand/logo-stacked-light.webp')) ?>" width="640" height="258" alt="<?= e(BUSINESS_NAME) ?>" loading="lazy">
      </a>
      <p class="footer__tagline"><?= e(TAGLINE) ?></p>
      <p>Family-owned tile and remodeling contractor serving homeowners within about two hours of Myrtle Beach, South Carolina.</p>
      <div class="footer__social">
        <a href="<?= e(FACEBOOK_URL) ?>" target="_blank" rel="noopener" aria-label="Facebook"><?= icon('facebook') ?></a>
        <a href="<?= e(INSTAGRAM_URL) ?>" target="_blank" rel="noopener" aria-label="Instagram"><?= icon('instagram') ?></a>
        <?php if (GOOGLE_BUSINESS_URL): ?>
        <a href="<?= e(GOOGLE_BUSINESS_URL) ?>" target="_blank" rel="noopener" aria-label="Google Business Profile"><?= icon('pin') ?></a>
        <?php endif; ?>
      </div>
    </div>
    <div>
      <h2 class="footer__title">Services</h2>
      <ul class="footer__links">
        <?php foreach ($SERVICES as $svcSlug => $svc): ?>
        <li><a href="<?= e(url($svcSlug)) ?>"><?= e($svc['nav']) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2 class="footer__title">Company</h2>
      <ul class="footer__links">
        <li><a href="<?= e(url('projects')) ?>">Projects</a></li>
        <li><a href="<?= e(url('about')) ?>">About Us</a></li>
        <li><a href="<?= e(url('service-areas')) ?>">Service Areas</a></li>
        <li><a href="<?= e(url('contact')) ?>">Contact</a></li>
        <li><a href="<?= e(url('privacy-policy')) ?>">Privacy Policy</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer__title">Get in touch</h2>
      <ul class="footer__contact">
        <li><a href="<?= e(tel_link()) ?>" data-track="call"><?= icon('phone') ?><span><?= e(PHONE_DISPLAY) ?></span></a></li>
        <li><a href="<?= e(sms_link()) ?>" data-track="sms"><?= icon('sms') ?><span>Text us</span></a></li>
        <li><a href="mailto:<?= e(EMAIL) ?>" data-track="email"><?= icon('mail') ?><span class="break"><?= e(EMAIL) ?></span></a></li>
        <li><span class="footer__area"><?= icon('pin') ?><span>Myrtle Beach, SC and up to 2 hours around</span></span></li>
      </ul>
    </div>
  </div>
  <div class="container footer__bottom">
    <p>&copy; <?= date('Y') ?> <?= e(BUSINESS_NAME) ?>. All rights reserved.</p>
    <p>Licensed &amp; insured. Payments: Zelle, cash and check.</p>
  </div>
</footer>

<div class="mobile-bar" aria-label="Quick contact">
  <a href="<?= e(tel_link()) ?>" data-track="call"><?= icon('phone') ?><span>Call</span></a>
  <a href="<?= e(sms_link()) ?>" data-track="sms"><?= icon('sms') ?><span>Text</span></a>
  <a href="<?= e(url('contact')) ?>#estimate" class="mobile-bar__primary"><?= icon('ruler') ?><span>Free Estimate</span></a>
</div>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Project photo" hidden>
  <button class="lightbox__close" type="button" aria-label="Close" data-lb-close><?= icon('close') ?></button>
  <button class="lightbox__nav lightbox__nav--prev" type="button" aria-label="Previous photo" data-lb-prev><?= icon('chevron') ?></button>
  <figure class="lightbox__figure">
    <img alt="" class="lightbox__img">
    <figcaption class="lightbox__caption"></figcaption>
  </figure>
  <button class="lightbox__nav lightbox__nav--next" type="button" aria-label="Next photo" data-lb-next><?= icon('chevron') ?></button>
</div>

<script>window.GP={thanks:<?= json_encode(url('thank-you')) ?>,ads:<?= json_encode(GOOGLE_ADS_ID) ?>};</script>
<script src="<?= e(asset('js/main.js')) ?>" defer></script>
</body>
</html>
