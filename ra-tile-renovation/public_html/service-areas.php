<?php
require __DIR__ . '/includes/bootstrap.php';

$page = [
    'title'       => 'Service Areas | Tile Installer Manchester, Nashua & Concord NH',
    'description' => 'Tile installation in Manchester, Nashua, Concord, Bedford, Londonderry, Derry, Merrimack, Salem, Hudson and towns within ~50 miles in NH. Free estimates.',
    'path'        => 'service-areas',
    'body_class'  => 'page-areas',
    'schema'      => [breadcrumb_schema(['Home' => '', 'Service Areas' => 'service-areas'])],
];
require __DIR__ . '/includes/header.php';
$sorted = $CITIES;
sort($sorted);
?>

<section class="page-hero page-hero--short" aria-labelledby="page-title">
  <div class="page-hero__bg"><?= img('floor-2', '16:9', '100vw', ['eager' => true, 'widths' => [800, 1200, 1600], 'base' => 1600]) ?></div>
  <div class="container page-hero__inner">
    <?= breadcrumbs_html(['Home' => '', 'Service Areas' => 'service-areas']) ?>
    <p class="eyebrow eyebrow--light"><?= icon('pin', 'icon icon--xs') ?> New Hampshire</p>
    <h1 id="page-title" class="page-hero__title">Tile Services Across <span class="text-gold">Southern New Hampshire</span></h1>
    <p class="page-hero__lead">Based in Manchester, NH, we install tile for homeowners within about 50 miles — and the estimate is always free.</p>
  </div>
</section>

<section class="section" aria-labelledby="areas-title">
  <div class="container split split--top">
    <div class="split__content prose">
      <h2 id="areas-title" class="section-title">Cities &amp; Towns We Serve</h2>
      <p>We work throughout Hillsborough, Rockingham and Merrimack counties, including the cities below. Don't see your town? If you're in New Hampshire within about an hour of Manchester, just send us a text — we'll let you know right away.</p>
      <ul class="chips chips--light">
        <?php foreach ($sorted as $c): ?>
        <li class="chip"><?= e($c) ?>, NH</li>
        <?php endforeach; ?>
      </ul>
      <p class="note"><?= icon('pin') ?> We currently serve New Hampshire only (no Massachusetts or Maine projects).</p>
      <h3 class="h4">Services available in every area</h3>
      <ul class="checklist checklist--cols">
        <?php foreach ($SERVICES as $slug => $s): ?>
        <li><?= icon('check') ?> <a href="<?= e(link_to($slug)) ?>"><?= e($s['nav']) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <aside class="split__media sticky-aside">
      <div class="map-card">
        <iframe title="Service area map — Manchester, NH" src="https://maps.google.com/maps?q=Manchester,+NH&amp;z=9&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" width="600" height="600"></iframe>
      </div>
      <div class="promise">
        <p class="promise__title">Free estimate, anywhere we serve</p>
        <p>Many contractors charge to quote a job. With R.A Tile Renovation, your estimate is always free — no matter the distance within our service area.</p>
        <a class="btn btn--gold btn--block" href="/contact#estimate">Book My Free Estimate</a>
      </div>
    </aside>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
