<?php
require __DIR__ . '/includes/functions.php';

$page = [
    'slug' => 'service-areas',
    'title' => 'Service Areas | Tile Contractor Myrtle Beach & Grand Strand',
    'description' => 'Guidine Pereira Construction serves homeowners within about two hours of Myrtle Beach, SC: North Myrtle Beach, Conway, Murrells Inlet, Pawleys Island, Georgetown, Florence, Wilmington NC and more.',
    'schema' => [breadcrumb_schema([['Home', ''], ['Service Areas', 'service-areas']])],
    'body' => 'page-areas',
];
include __DIR__ . '/includes/header.php';
?>

<section class="page-hero">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__narrow">
    <?php breadcrumbs([['Home', ''], ['Service Areas', 'service-areas']]); ?>
    <p class="eyebrow eyebrow--light">Service areas</p>
    <h1 class="page-hero__title">Tile and remodeling across the Grand Strand and beyond</h1>
    <p class="hero__lead">We are based in Myrtle Beach and travel up to about two hours for showers, bathrooms, floors, walls and backsplashes.</p>
  </div>
</section>

<section class="section">
  <div class="container areas__grid">
    <div class="reveal">
      <p class="eyebrow">Where we work</p>
      <h2 class="h2">Communities we serve</h2>
      <p>Most of our projects are along the coast, from Little River and North Myrtle Beach down through Surfside Beach, Murrells Inlet and Pawleys Island to Georgetown. We also work inland in Conway, Carolina Forest, Loris and Aynor, in the Pee Dee region around Florence, Marion and Dillon, and across the state line in Brunswick and New Hanover counties, North Carolina.</p>
      <p>Don't see your town? If you are within about two hours of Myrtle Beach, reach out. We will let you know right away if we can take the job.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="#estimate">Check my area <?= icon('arrow') ?></a>
        <a class="btn btn--dark" href="<?= e(tel_link()) ?>" data-track="call"><?= icon('phone') ?><?= e(PHONE_DISPLAY) ?></a>
      </div>
    </div>
    <div class="areas__lists reveal">
      <div>
        <h3 class="areas__state">South Carolina</h3>
        <ul class="chips"><?php foreach ($AREAS_SC as $c): ?><li><?= e($c) ?>, SC</li><?php endforeach; ?></ul>
      </div>
      <div>
        <h3 class="areas__state">North Carolina</h3>
        <ul class="chips"><?php foreach ($AREAS_NC as $c): ?><li><?= e($c) ?>, NC</li><?php endforeach; ?></ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft" aria-labelledby="svc-title">
  <div class="container">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">Services in your area</p>
        <h2 class="h2" id="svc-title">What we can do for your home</h2>
      </div>
    </div>
    <div class="services">
      <?php $n = 1; foreach ($SERVICES as $slug => $s): ?>
      <article class="service-card reveal">
        <a href="<?= e(url($slug)) ?>" class="service-card__link">
          <div class="service-card__media"><?= picture($s['image'], '(max-width: 600px) 100vw, (max-width: 1100px) 50vw, 25vw') ?></div>
          <div class="service-card__body">
            <span class="service-card__num">0<?= $n++ ?></span>
            <h3 class="service-card__title"><?= e($s['name']) ?></h3>
            <p><?= e($s['card']) ?></p>
            <span class="more">Learn more <?= icon('arrow') ?></span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?php
include __DIR__ . '/includes/estimate-section.php';
include __DIR__ . '/includes/footer.php';
