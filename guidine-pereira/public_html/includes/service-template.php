<?php
/* Shared layout for the service pages. Expects $slug to be set before including. */
require_once __DIR__ . '/functions.php';
$s = $SERVICES[$slug];

$ABOUT = [
    'shower-bathroom-remodeling' => [
        'A bathroom is the room where water, tile and daily use meet, so the work behind the walls matters as much as the finish. Every shower we build starts with demolition down to a sound structure, a continuous waterproofing system and a pan sloped properly to the drain.',
        'From there we plan the layout with you: where the niche sits, how the bench is framed, which wall gets the accent tile and how the floor tile lines up with the shower. The result is a bathroom that looks clean and intentional, and holds up to everyday use along the coast.',
    ],
    'tile-flooring-installation' => [
        'A tile floor is only as good as what is underneath it. We check the subfloor, correct high and low spots and plan the layout so cuts land at the edges of the room, not in the middle of your doorway.',
        'On large-format and plank tile we use leveling systems to keep every edge flush. Whether it is a wood-look plank through the living area, a classic checkerboard or a decorative patterned porcelain, the floor is laid out to look balanced from every entrance.',
    ],
    'wall-tile-installation' => [
        'Walls are where layout mistakes are easiest to see. Before setting a single tile we mark reference lines, center the design on the focal point and plan cuts around windows, niches and fixtures so both sides of the wall match.',
        'We install full-height bathroom walls, wainscots, accent bands and patterned feature walls, and finish every exposed edge with trim or bullnose pieces for a clean, built-in look.',
    ],
    'backsplash-installation' => [
        'A new backsplash changes the look of a kitchen in a day or two, without a full remodel. We cover your countertops and cabinets, remove outlet covers and set the tile with consistent spacing from counter to cabinet.',
        'Subway, mosaic, stone-look and porcelain tile all have their own details. We plan where the pattern starts, how it ends at the cabinets and windows, and seal the joints where tile meets the counter so it is easy to keep clean.',
    ],
];

$photos = array_values(array_filter(gallery(), function ($p) use ($s) {
    return in_array($p[1], $s['cats'], true);
}));
$photos = array_slice($photos, 0, 12);
$heroSide = $photos[1][0] ?? $s['image'];

$faqs = array_merge($s['faq'], [$FAQ_GENERAL[3], $FAQ_GENERAL[4], $FAQ_GENERAL[5]]);

$page = [
    'slug' => $slug,
    'title' => $s['title'] . ' | Guidine Pereira',
    'description' => $s['meta'],
    'preload' => $s['image'],
    'schema' => [
        breadcrumb_schema([['Home', ''], [$s['name'], $slug]]),
        [
            '@context' => 'https://schema.org',
            '@type' => 'Service',
            'name' => $s['name'],
            'serviceType' => $s['name'],
            'description' => $s['meta'],
            'url' => abs_url($slug),
            'image' => site_url() . work_img($s['image']),
            'provider' => ['@id' => abs_url() . '#business'],
            'areaServed' => ['@type' => 'GeoCircle', 'geoMidpoint' => ['@type' => 'GeoCoordinates', 'latitude' => 33.6891, 'longitude' => -78.8867], 'geoRadius' => 160000],
        ],
        faq_schema($faqs),
    ],
    'body' => 'page-service',
];
include __DIR__ . '/header.php';
?>

<section class="page-hero page-hero--media">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__grid">
    <div class="page-hero__copy">
      <?php breadcrumbs([['Home', ''], [$s['name'], $slug]]); ?>
      <p class="eyebrow eyebrow--light">Myrtle Beach, SC &amp; surrounding areas</p>
      <h1 class="page-hero__title"><?= e($s['h1']) ?></h1>
      <p class="hero__lead"><?= e($s['lead']) ?></p>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="#estimate">Get a Free Estimate <?= icon('arrow') ?></a>
        <a class="btn btn--outline-light btn--lg" href="<?= e(sms_link()) ?>" data-track="sms"><?= icon('sms') ?>Text us</a>
      </div>
    </div>
    <div class="page-hero__media">
      <figure class="page-hero__img"><?= picture($s['image'], '(max-width: 900px) 60vw, 28vw', false) ?></figure>
      <figure class="page-hero__img page-hero__img--offset"><?= picture($heroSide, '(max-width: 900px) 40vw, 18vw') ?></figure>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="included-title">
  <div class="container split">
    <div class="split__copy">
      <p class="eyebrow reveal"><?= e($s['short']) ?></p>
      <h2 class="h2 reveal" id="included-title">What's included</h2>
      <?php foreach ($ABOUT[$slug] as $para): ?>
      <p class="reveal"><?= e($para) ?></p>
      <?php endforeach; ?>
      <a class="btn btn--dark reveal" href="#estimate">Schedule my free estimate <?= icon('arrow') ?></a>
    </div>
    <div class="included">
      <?php foreach ($s['includes'] as $item): ?>
      <div class="included__item reveal">
        <?= icon('check') ?>
        <div><h3><?= e($item[0]) ?></h3><p><?= e($item[1]) ?></p></div>
      </div>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?php if ($photos): ?>
<section class="section section--soft" aria-labelledby="gallery-title">
  <div class="container">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">Our work</p>
        <h2 class="h2" id="gallery-title"><?= e($s['name']) ?> projects</h2>
      </div>
      <a class="btn btn--dark" href="<?= e(url('projects')) ?>">View all projects <?= icon('arrow') ?></a>
    </div>
    <div class="masonry<?= count($photos) < 4 ? ' masonry--few' : '' ?>" data-gallery>
      <?php foreach ($photos as $p): ?>
      <a class="masonry__item reveal" href="<?= e(work_img($p[0])) ?>" data-lightbox data-caption="<?= e($p[2]) ?>">
        <?= picture($p[0], '(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 25vw') ?>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>

<section class="section section--dark process" aria-labelledby="steps-title">
  <div class="process__pattern" aria-hidden="true"></div>
  <div class="container">
    <div class="section-head section-head--light reveal">
      <div>
        <p class="eyebrow eyebrow--light">How it works</p>
        <h2 class="h2" id="steps-title">From first call to final walkthrough</h2>
      </div>
      <p class="section-head__text">A simple process with one point of contact, a clear price and a clean site at the end of every day.</p>
    </div>
    <ol class="steps">
      <li class="step reveal"><span class="step__n">01</span><h3>Reach out</h3><p>Call, text or send the form with a few details about your project.</p></li>
      <li class="step reveal"><span class="step__n">02</span><h3>Free estimate</h3><p>We visit, measure and give you a clear price and timeline, often on the spot.</p></li>
      <li class="step reveal"><span class="step__n">03</span><h3>Prep and install</h3><p>Surfaces protected and prepared, then tile set with care and attention to layout.</p></li>
      <li class="step reveal"><span class="step__n">04</span><h3>Walkthrough</h3><p>We review the finished work together and leave the space clean and ready to use.</p></li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="faq-title">
  <div class="container faq-wrap">
    <div class="faq-wrap__head reveal">
      <p class="eyebrow">FAQ</p>
      <h2 class="h2" id="faq-title"><?= e($s['short']) ?> questions</h2>
      <p class="lead">Still have a question? Call or text <a href="<?= e(tel_link()) ?>" data-track="call"><?= e(PHONE_DISPLAY) ?></a>.</p>
    </div>
    <div class="reveal"><?php render_faq($faqs); ?></div>
  </div>
</section>

<section class="section section--soft" aria-labelledby="more-title">
  <div class="container">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">More services</p>
        <h2 class="h2" id="more-title">Other ways we can help</h2>
      </div>
    </div>
    <div class="services services--3">
      <?php foreach ($SERVICES as $oslug => $o): if ($oslug === $slug) continue; ?>
      <article class="service-card reveal">
        <a href="<?= e(url($oslug)) ?>" class="service-card__link">
          <div class="service-card__media"><?= picture($o['image'], '(max-width: 600px) 100vw, 33vw') ?></div>
          <div class="service-card__body">
            <h3 class="service-card__title"><?= e($o['name']) ?></h3>
            <p><?= e($o['card']) ?></p>
            <span class="more">Learn more <?= icon('arrow') ?></span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?php
$preselect = $slug;
$estimateHeading = 'Get a price for your ' . $s['name'] . ' project';
include __DIR__ . '/estimate-section.php';
include __DIR__ . '/footer.php';
