<?php
require __DIR__ . '/includes/bootstrap.php';

$page = [
    'title'       => 'Tile Installer & Bathroom Remodeling Manchester, NH | R.A Tile',
    'description' => 'Tile showers, bathroom remodels, floor tile, backsplashes & fireplaces in Manchester & Southern NH. 20+ years of experience. Free estimates + 1-year warranty.',
    'path'        => '',
    'schema'      => [faq_schema($FAQS)],
    'body_class'  => 'page-home',
];
require __DIR__ . '/includes/header.php';
?>

<!-- HERO -->
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__bg">
    <?= img('hero', '16:9', '100vw', ['eager' => true, 'widths' => [800, 1200, 1600, 2000], 'base' => 1600]) ?>
  </div>
  <div class="container hero__inner">
    <div class="hero__content">
      <p class="eyebrow eyebrow--light"><?= icon('diamond', 'icon icon--xs') ?> Manchester, NH · Since <?= e(FOUNDED_YEAR) ?></p>
      <h1 id="hero-title" class="hero__title">Tile Installation &amp; <span class="text-gold">Bathroom Remodeling</span> in Manchester, NH</h1>
      <p class="hero__lead">Custom tile showers, floors, backsplashes and fireplaces with a fine, precise finish — installed fast by a team with <?= e(YEARS_EXPERIENCE) ?> years of tile experience.</p>
      <div class="hero__actions">
        <a class="btn btn--gold btn--lg" href="#estimate" data-track="cta_hero">Get My Free Estimate <?= icon('arrow') ?></a>
        <a class="btn btn--outline-light btn--lg" href="<?= e(sms_link()) ?>" data-track="sms_hero"><?= icon('sms') ?> Text Us Now</a>
      </div>
      <ul class="hero__badges">
        <li><?= icon('tag') ?> <span><strong>Free</strong> Estimates</span></li>
        <li><?= icon('shield') ?> <span><strong>1-Year</strong> Warranty</span></li>
        <li><?= icon('award') ?> <span><strong><?= e(YEARS_EXPERIENCE) ?></strong> Years Exp.</span></li>
      </ul>
    </div>
    <div class="hero__form" id="estimate">
      <?php $formId = 'hero-form'; $formTitle = 'Get Your Free Estimate'; $formCompact = true; include __DIR__ . '/includes/estimate-form.php'; ?>
    </div>
  </div>
</section>

<!-- FREE ESTIMATE STRIP -->
<section class="strip" aria-label="Free estimates">
  <div class="container strip__inner">
    <p class="strip__text"><strong>Other contractors charge just to quote your job. We don't.</strong> Your estimate is 100% free — no matter where you are in our service area.</p>
    <a class="btn btn--navy" href="<?= e(sms_link()) ?>" data-track="sms_strip"><?= icon('sms') ?> Text for a Free Estimate</a>
  </div>
</section>

<!-- SERVICES -->
<section class="section" id="services" aria-labelledby="services-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> What we do</p>
      <h2 id="services-title" class="section-title">Tile Services for Every Room</h2>
      <p class="section-lead">Tile is all we do — and we do it with care, precision and attention to every detail, from prep to the final grout line.</p>
    </header>
    <div class="cards">
      <?php foreach ($SERVICES as $slug => $s): ?>
      <article class="card">
        <a class="card__link" href="<?= e(link_to($slug)) ?>">
          <?= figure($s['image'], '4:3', '(min-width: 1100px) 25vw, (min-width: 640px) 50vw, 100vw', ['widths' => [480, 800, 1200], 'base' => 800]) ?>
          <div class="card__body">
            <span class="card__icon"><?= icon($s['icon']) ?></span>
            <h3 class="card__title"><?= e($s['nav']) ?></h3>
            <p><?= e($s['short']) ?></p>
            <span class="card__more">Learn more <?= icon('arrow') ?></span>
          </div>
        </a>
      </article>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<!-- FEATURE: SHOWERS -->
<section class="section section--navy feature" aria-labelledby="feature-title">
  <div class="container feature__grid">
    <div class="feature__media">
      <?= figure('shower-1', '4:5', '(min-width: 900px) 45vw, 100vw', ['widths' => [480, 800, 1200], 'base' => 800]) ?>
      <div class="feature__badge"><strong><?= e(YEARS_EXPERIENCE) ?></strong><span>years of tile<br>experience</span></div>
    </div>
    <div class="feature__content">
      <p class="eyebrow eyebrow--light"><?= icon('diamond', 'icon icon--xs') ?> Our specialty</p>
      <h2 id="feature-title" class="section-title">Showers &amp; Bathrooms Built to Last</h2>
      <p>Bathrooms are our most requested project. We build every shower on a proper foundation — solid prep, reliable waterproofing and correct drain slopes — then finish it with the clean lines and precise cuts that make a bathroom feel custom.</p>
      <ul class="checklist checklist--light">
        <li><?= icon('check') ?> Walk-in &amp; curbless tile showers</li>
        <li><?= icon('check') ?> Tub-to-shower conversions</li>
        <li><?= icon('check') ?> Niches, benches &amp; ledges</li>
        <li><?= icon('check') ?> Bathroom floors &amp; tub surrounds</li>
        <li><?= icon('check') ?> Waterproofing done right</li>
        <li><?= icon('check') ?> Large-format, mosaic &amp; marble-look tile</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn--gold" href="/bathroom-shower-remodeling">Explore Bathroom Remodeling</a>
        <a class="btn btn--outline-light" href="<?= e(sms_link("Hi Renato! I'd like a free estimate for a shower/bathroom. My name is ")) ?>" data-track="sms_feature"><?= icon('sms') ?> Text Us</a>
      </div>
    </div>
  </div>
</section>

<!-- WHY US -->
<section class="section" aria-labelledby="why-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> Why homeowners choose us</p>
      <h2 id="why-title" class="section-title">Quality You Can See. Service You Can Trust.</h2>
    </header>
    <div class="features">
      <div class="feature-item">
        <span class="feature-item__icon"><?= icon('tag') ?></span>
        <h3>Free Estimates</h3>
        <p>No charge to come out, measure and quote your project — anywhere in our New Hampshire service area.</p>
      </div>
      <div class="feature-item">
        <span class="feature-item__icon"><?= icon('shield') ?></span>
        <h3>1-Year Warranty</h3>
        <p>Every job is covered for one year on workmanship and product. If something isn't right, we come back and fix it.</p>
      </div>
      <div class="feature-item">
        <span class="feature-item__icon"><?= icon('sparkle') ?></span>
        <h3>Fine Finish</h3>
        <p>Straight lines, even grout joints and clean cuts around every fixture. The details are what our clients notice first.</p>
      </div>
      <div class="feature-item">
        <span class="feature-item__icon"><?= icon('clock') ?></span>
        <h3>Fast, Organized Work</h3>
        <p>We show up, work efficiently and keep your home clean — so your project is done on schedule without cutting corners.</p>
      </div>
      <div class="feature-item">
        <span class="feature-item__icon"><?= icon('award') ?></span>
        <h3><?= e(YEARS_EXPERIENCE) ?> Years of Experience</h3>
        <p>A lifetime working with tile. You get experienced installers on your job — the owners themselves.</p>
      </div>
      <div class="feature-item">
        <span class="feature-item__icon"><?= icon('wallet') ?></span>
        <h3>Fair, Clear Pricing</h3>
        <p>A detailed written estimate with no surprises. Pay easily with Zelle, cash, check or Venmo.</p>
      </div>
    </div>
  </div>
</section>

<!-- PROCESS -->
<section class="section section--light" aria-labelledby="process-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> How it works</p>
      <h2 id="process-title" class="section-title">From First Text to Finished Tile</h2>
    </header>
    <ol class="steps">
      <li class="step">
        <span class="step__num">1</span>
        <h3>Text or send the form</h3>
        <p>Tell us about your project. Photos of the space help us prepare.</p>
      </li>
      <li class="step">
        <span class="step__num">2</span>
        <h3>Free in-home estimate</h3>
        <p>We visit, measure, talk through tile options and give you a clear quote.</p>
      </li>
      <li class="step">
        <span class="step__num">3</span>
        <h3>Expert installation</h3>
        <p>Careful prep, precise installation and a clean jobsite every day.</p>
      </li>
      <li class="step">
        <span class="step__num">4</span>
        <h3>Final walkthrough</h3>
        <p>We review every detail with you — backed by our 1-year warranty.</p>
      </li>
    </ol>
  </div>
</section>

<!-- STYLES GALLERY -->
<section class="section" aria-labelledby="styles-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> Get inspired</p>
      <h2 id="styles-title" class="section-title">Tile Styles We Install</h2>
      <p class="section-lead">Porcelain, ceramic, large-format, mosaic and marble-look tile — here are a few looks our clients love.</p>
    </header>
    <div class="gallery">
      <?= figure('shower-2', '4:5', '(min-width: 900px) 33vw, 50vw', ['figclass' => 'gallery__item gallery__item--tall', 'widths' => [480, 800, 1200], 'base' => 800]) ?>
      <?= figure('kitchen-1', '4:3', '(min-width: 900px) 33vw, 50vw', ['figclass' => 'gallery__item', 'widths' => [480, 800], 'base' => 800]) ?>
      <?= figure('bath-2', '4:3', '(min-width: 900px) 33vw, 50vw', ['figclass' => 'gallery__item', 'widths' => [480, 800], 'base' => 800]) ?>
      <?= figure('fireplace-1', '4:3', '(min-width: 900px) 33vw, 50vw', ['figclass' => 'gallery__item', 'widths' => [480, 800], 'base' => 800]) ?>
      <?= figure('floor-2', '4:3', '(min-width: 900px) 33vw, 50vw', ['figclass' => 'gallery__item', 'widths' => [480, 800], 'base' => 800]) ?>
    </div>
    <p class="center mt-2">
      <a class="btn btn--outline" href="<?= e(INSTAGRAM_URL) ?>" target="_blank" rel="noopener"><?= icon('instagram') ?> See our real jobs on Instagram</a>
    </p>
  </div>
</section>

<!-- ABOUT TEASER -->
<section class="section section--light" aria-labelledby="about-title">
  <div class="container split">
    <div class="split__content">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> Our story</p>
      <h2 id="about-title" class="section-title">A Lifetime of Tile. A Company Built on Trust.</h2>
      <p>R.A Tile Renovation was founded by Renato De Almeida and Anderson Soares — two tile installers who spent years working side by side for other companies before deciding to build their own.</p>
      <p>Renato has worked with tile his entire life. Today, every project is run by the owners themselves, with the same care, precision and commitment to the client that built our reputation.</p>
      <a class="btn btn--navy" href="/about">Meet the Team <?= icon('arrow') ?></a>
    </div>
    <div class="split__media">
      <?= figure('install', '4:3', '(min-width: 900px) 45vw, 100vw', ['widths' => [480, 800, 1200], 'base' => 800]) ?>
    </div>
  </div>
</section>

<!-- SERVICE AREAS -->
<section class="section section--navy areas" aria-labelledby="areas-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow eyebrow--light"><?= icon('pin', 'icon icon--xs') ?> Service areas</p>
      <h2 id="areas-title" class="section-title">Proudly Serving Southern New Hampshire</h2>
      <p class="section-lead">Based in Manchester, we serve homeowners within about 50 miles across New Hampshire.</p>
    </header>
    <ul class="chips">
      <?php foreach (array_slice($CITIES, 0, 18) as $c): ?>
      <li class="chip"><?= e($c) ?>, NH</li>
      <?php endforeach; ?>
    </ul>
    <p class="center mt-2"><a class="btn btn--outline-light" href="/service-areas">See all service areas <?= icon('arrow') ?></a></p>
  </div>
</section>

<!-- FAQ -->
<section class="section" aria-labelledby="faq-title">
  <div class="container container--narrow">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> FAQ</p>
      <h2 id="faq-title" class="section-title">Frequently Asked Questions</h2>
    </header>
    <div class="faq">
      <?php foreach ($FAQS as $i => [$q, $a]): ?>
      <details class="faq__item"<?= $i === 0 ? ' open' : '' ?>>
        <summary><?= e($q) ?> <?= icon('chevron') ?></summary>
        <div class="faq__answer"><p><?= e($a) ?></p></div>
      </details>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<!-- FINAL CTA -->
<section class="section cta-final" aria-labelledby="cta-title">
  <div class="container cta-final__grid">
    <div class="cta-final__content">
      <p class="eyebrow eyebrow--light"><?= icon('diamond', 'icon icon--xs') ?> Ready to start?</p>
      <h2 id="cta-title" class="section-title">Let's Talk About Your Tile Project</h2>
      <p>Send us a text with a few photos of your space or fill out the form. We'll schedule your free in-home estimate at a time that works for you.</p>
      <ul class="checklist checklist--light">
        <li><?= icon('check') ?> Free, no-obligation estimate</li>
        <li><?= icon('check') ?> 1-year warranty on labor &amp; product</li>
        <li><?= icon('check') ?> Serving Manchester &amp; Southern NH</li>
      </ul>
      <a class="btn btn--outline-light btn--lg" href="<?= e(sms_link()) ?>" data-track="sms_final"><?= icon('sms') ?> Text <?= e(PHONE_DISPLAY) ?></a>
    </div>
    <div class="cta-final__form">
      <?php $formId = 'footer-form'; $formTitle = 'Request a Free Estimate'; $formCompact = false; include __DIR__ . '/includes/estimate-form.php'; ?>
    </div>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
