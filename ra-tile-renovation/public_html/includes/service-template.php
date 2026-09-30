<?php
/**
 * Service page template. Set $slug before including.
 */
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'service-template.php') {
    http_response_code(403);
    exit;
}
require __DIR__ . '/bootstrap.php';

$s = $SERVICES[$slug];
$crumbsSchema = ['Home' => '', $s['nav'] => $slug];

$page = [
    'title'       => $s['title'] . ' | R.A Tile',
    'description' => $s['meta'],
    'path'        => $slug,
    'body_class'  => 'page-service',
    'schema'      => [
        [
            '@context'    => 'https://schema.org',
            '@type'       => 'Service',
            'name'        => $s['h1'],
            'serviceType' => $s['nav'],
            'description' => $s['meta'],
            'url'         => url($slug),
            'image'       => image_src($IMAGES[$s['image']], 1200, 900),
            'provider'    => ['@id' => url() . '#business'],
            'areaServed'  => ['@type' => 'State', 'name' => 'New Hampshire'],
            'offers'      => ['@type' => 'Offer', 'description' => 'Free estimate', 'price' => '0', 'priceCurrency' => 'USD'],
        ],
        faq_schema($s['faqs']),
        breadcrumb_schema($crumbsSchema),
    ],
];
require __DIR__ . '/header.php';
?>

<section class="page-hero" aria-labelledby="page-title">
  <div class="page-hero__bg"><?= img($s['image'], '16:9', '100vw', ['eager' => true, 'widths' => [800, 1200, 1600], 'base' => 1600]) ?></div>
  <div class="container page-hero__inner">
    <?= breadcrumbs_html(['Home' => '', $s['nav'] => $slug]) ?>
    <p class="eyebrow eyebrow--light"><?= icon($s['icon'], 'icon icon--xs') ?> <?= e($s['kicker']) ?></p>
    <h1 id="page-title" class="page-hero__title"><?= e($s['h1']) ?> <span class="text-gold">in Manchester, NH</span></h1>
    <p class="page-hero__lead"><?= e($s['lead']) ?></p>
    <div class="hero__actions">
      <a class="btn btn--gold btn--lg" href="#estimate" data-track="cta_service">Get a Free Estimate <?= icon('arrow') ?></a>
      <a class="btn btn--outline-light btn--lg" href="<?= e(sms_link("Hi Renato! I'd like a free estimate for " . strtolower($s['nav']) . ". My name is ")) ?>" data-track="sms_service"><?= icon('sms') ?> Text Us</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="intro-title">
  <div class="container split split--top">
    <div class="split__content prose">
      <h2 id="intro-title" class="section-title">Professional <?= e($s['nav']) ?> Done Right</h2>
      <?php foreach ($s['intro'] as $p): ?>
      <p><?= e($p) ?></p>
      <?php endforeach; ?>
      <h3 class="h4">What we install</h3>
      <ul class="checklist checklist--cols">
        <?php foreach ($s['features'] as $f): ?>
        <li><?= icon('check') ?> <?= e($f) ?></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <aside class="split__media sticky-aside">
      <?= figure($s['gallery'][0], '4:5', '(min-width: 900px) 40vw, 100vw', ['widths' => [480, 800, 1200], 'base' => 800]) ?>
      <div class="promise">
        <p class="promise__title">Every project includes</p>
        <ul>
          <li><?= icon('tag') ?> Free in-home estimate</li>
          <li><?= icon('shield') ?> 1-year warranty (labor &amp; product)</li>
          <li><?= icon('award') ?> <?= e(YEARS_EXPERIENCE) ?> years of tile experience</li>
          <li><?= icon('sparkle') ?> Clean, detailed finish</li>
        </ul>
      </div>
    </aside>
  </div>
</section>

<section class="section section--light" aria-labelledby="looks-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> Inspiration</p>
      <h2 id="looks-title" class="section-title">Looks You Can Get</h2>
    </header>
    <div class="grid-3">
      <?php foreach (array_slice($s['gallery'], 1, 3) as $g): ?>
      <?= figure($g, '4:3', '(min-width: 900px) 33vw, 100vw', ['widths' => [480, 800, 1200], 'base' => 800, 'figclass' => 'rounded']) ?>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="process-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> Simple process</p>
      <h2 id="process-title" class="section-title">How Your Project Works</h2>
    </header>
    <ol class="steps">
      <li class="step"><span class="step__num">1</span><h3>Text or send the form</h3><p>Share a few details and photos of your space.</p></li>
      <li class="step"><span class="step__num">2</span><h3>Free estimate</h3><p>We measure, discuss options and give you a clear quote.</p></li>
      <li class="step"><span class="step__num">3</span><h3>Installation</h3><p>Careful prep and precise tile work, done efficiently.</p></li>
      <li class="step"><span class="step__num">4</span><h3>Walkthrough</h3><p>We review every detail — backed by a 1-year warranty.</p></li>
    </ol>
  </div>
</section>

<section class="section section--light" aria-labelledby="faq-title">
  <div class="container container--narrow">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> FAQ</p>
      <h2 id="faq-title" class="section-title"><?= e($s['nav']) ?> Questions</h2>
    </header>
    <div class="faq">
      <?php foreach ($s['faqs'] as $i => [$q, $a]): ?>
      <details class="faq__item"<?= $i === 0 ? ' open' : '' ?>>
        <summary><?= e($q) ?> <?= icon('chevron') ?></summary>
        <div class="faq__answer"><p><?= e($a) ?></p></div>
      </details>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="other-title">
  <div class="container">
    <header class="section-head">
      <h2 id="other-title" class="section-title">Other Tile Services</h2>
    </header>
    <div class="cards cards--3">
      <?php foreach ($SERVICES as $oslug => $o): if ($oslug === $slug) continue; ?>
      <article class="card">
        <a class="card__link" href="<?= e(link_to($oslug)) ?>">
          <?= figure($o['image'], '4:3', '(min-width: 900px) 33vw, 100vw', ['widths' => [480, 800], 'base' => 800]) ?>
          <div class="card__body">
            <span class="card__icon"><?= icon($o['icon']) ?></span>
            <h3 class="card__title"><?= e($o['nav']) ?></h3>
            <p><?= e($o['short']) ?></p>
            <span class="card__more">Learn more <?= icon('arrow') ?></span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section cta-final" id="estimate" aria-labelledby="cta-title">
  <div class="container cta-final__grid">
    <div class="cta-final__content">
      <p class="eyebrow eyebrow--light"><?= icon('diamond', 'icon icon--xs') ?> Free estimate</p>
      <h2 id="cta-title" class="section-title">Get a Free Quote for Your <?= e($s['nav']) ?> Project</h2>
      <p>Tell us about your project and we'll schedule a free in-home estimate. Prefer texting? Send us photos of your space at <?= e(PHONE_DISPLAY) ?>.</p>
      <ul class="checklist checklist--light">
        <li><?= icon('check') ?> No charge, no obligation</li>
        <li><?= icon('check') ?> 1-year warranty</li>
        <li><?= icon('check') ?> Manchester &amp; Southern NH</li>
      </ul>
    </div>
    <div class="cta-final__form">
      <?php $formId = 'service-form'; $formTitle = 'Request a Free Estimate'; $formCompact = false; $formService = $slug; include __DIR__ . '/estimate-form.php'; ?>
    </div>
  </div>
</section>

<?php require __DIR__ . '/footer.php'; ?>
