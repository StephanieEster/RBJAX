<?php
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'footer.php') {
    http_response_code(403);
    exit;
}
?>
</main>

<footer class="site-footer">
  <div class="tile-divider" aria-hidden="true"></div>
  <div class="container site-footer__grid">
    <div class="site-footer__brand">
      <img src="<?= e(asset('img/logo-stacked-gold.png')) ?>" alt="<?= e(SITE_NAME) ?>" width="263" height="160" loading="lazy">
      <p>Tile installation and bathroom remodeling for homeowners in Manchester and Southern New Hampshire. <?= e(YEARS_EXPERIENCE) ?> years of tile experience, free estimates and a 1-year warranty on every job.</p>
      <div class="social">
        <a href="<?= e(INSTAGRAM_URL) ?>" target="_blank" rel="noopener" aria-label="Instagram"><?= icon('instagram') ?></a>
        <?php if (FACEBOOK_URL): ?><a href="<?= e(FACEBOOK_URL) ?>" target="_blank" rel="noopener" aria-label="Facebook"><?= icon('facebook') ?></a><?php endif; ?>
      </div>
    </div>

    <div>
      <h2 class="site-footer__title">Services</h2>
      <ul class="site-footer__links">
        <?php foreach ($SERVICES as $svcSlug => $svc): ?>
        <li><a href="<?= e(link_to($svcSlug)) ?>"><?= e($svc['nav']) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>

    <div>
      <h2 class="site-footer__title">Company</h2>
      <ul class="site-footer__links">
        <li><a href="/about">About Us</a></li>
        <li><a href="/service-areas">Service Areas</a></li>
        <li><a href="/contact">Free Estimate</a></li>
        <li><a href="/privacy-policy">Privacy Policy</a></li>
      </ul>
    </div>

    <div>
      <h2 class="site-footer__title">Contact</h2>
      <ul class="site-footer__contact">
        <li><a href="<?= e(sms_link()) ?>" data-track="sms_footer"><?= icon('sms') ?> Text <?= e(PHONE_DISPLAY) ?></a></li>
        <li><a href="<?= e(tel_link()) ?>" data-track="call_footer"><?= icon('phone') ?> Call <?= e(PHONE_DISPLAY) ?></a></li>
        <li><a href="mailto:<?= e(EMAIL_PUBLIC) ?>"><?= icon('mail') ?> <?= e(EMAIL_PUBLIC) ?></a></li>
        <li><span><?= icon('pin') ?> <?= e(BASE_CITY) ?>, <?= e(BASE_STATE) ?> &amp; surrounding NH towns</span></li>
        <li><span><?= icon('wallet') ?> Zelle · Cash · Check · Venmo</span></li>
      </ul>
    </div>
  </div>
  <div class="site-footer__bottom">
    <div class="container">
      <p>&copy; <?= date('Y') ?> <?= e(SITE_NAME) ?>. All rights reserved. Serving New Hampshire since <?= e(FOUNDED_YEAR) ?>.</p>
    </div>
  </div>
</footer>

<!-- Sticky mobile action bar -->
<div class="action-bar" role="region" aria-label="Quick contact">
  <a class="action-bar__btn action-bar__btn--sms" href="<?= e(sms_link()) ?>" data-track="sms_sticky"><?= icon('sms') ?> Text Us</a>
  <a class="action-bar__btn action-bar__btn--cta" href="/contact#estimate" data-track="cta_sticky"><?= icon('calendar') ?> Free Estimate</a>
</div>

<script src="<?= e(asset('js/main.js')) ?>" defer></script>
</body>
</html>
