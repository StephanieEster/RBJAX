<?php
require __DIR__ . '/includes/bootstrap.php';

$page = [
    'title'       => 'About Us | R.A Tile Renovation — Tile Experts in Manchester, NH',
    'description' => 'Meet Renato De Almeida and Anderson Soares, the tile installers behind R.A Tile Renovation. 20+ years of tile experience serving Manchester and Southern New Hampshire.',
    'path'        => 'about',
    'body_class'  => 'page-about',
    'schema'      => [breadcrumb_schema(['Home' => '', 'About' => 'about'])],
];
require __DIR__ . '/includes/header.php';
?>

<section class="page-hero page-hero--short" aria-labelledby="page-title">
  <div class="page-hero__bg"><?= img('bath-3', '16:9', '100vw', ['eager' => true, 'widths' => [800, 1200, 1600], 'base' => 1600]) ?></div>
  <div class="container page-hero__inner">
    <?= breadcrumbs_html(['Home' => '', 'About' => 'about']) ?>
    <p class="eyebrow eyebrow--light"><?= icon('diamond', 'icon icon--xs') ?> Our story</p>
    <h1 id="page-title" class="page-hero__title">About <span class="text-gold">R.A Tile Renovation</span></h1>
    <p class="page-hero__lead">A lifetime of tile experience, a company built on care, precision and trust.</p>
  </div>
</section>

<section class="section" aria-labelledby="story-title">
  <div class="container split split--top">
    <div class="split__content prose">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> How we started</p>
      <h2 id="story-title" class="section-title">From Tile Installers to Business Owners</h2>
      <p>Renato De Almeida has worked with tile his entire life. After years of installing tile in Brazil, he moved to the United States in 2022 and kept doing what he does best — first for a Brazilian company, then for an American contractor.</p>
      <p>It was there that he brought in Anderson Soares as an installer. Working side by side for about two years, the two built a strong partnership and a reputation for clean, precise work. On the side, they started taking extra jobs of their own — and homeowners kept asking for them again.</p>
      <p>Seeing that potential, Renato and Anderson decided to take the leap and launched <strong>R.A Tile Renovation</strong>, registered in New Hampshire in <?= e(FOUNDED_YEAR) ?>. Today, every project is run by the owners themselves.</p>
      <h3 class="h4">What guides our work</h3>
      <p>We transform spaces through tile work executed with care, precision and attention to detail. Each project combines quality workmanship, functionality and a finish that adds value to your home — from the preparation to the very last grout line.</p>
    </div>
    <aside class="split__media sticky-aside">
      <?= figure('about-story', '4:5', '(min-width: 900px) 40vw, 100vw', ['base' => 800]) ?>
      <div class="stats">
        <div class="stat"><strong><?= e(YEARS_EXPERIENCE) ?></strong><span>Years of tile experience</span></div>
        <div class="stat"><strong><?= e(FOUNDED_YEAR) ?></strong><span>Company founded</span></div>
        <div class="stat"><strong>1-Year</strong><span>Warranty on every job</span></div>
        <div class="stat"><strong>$0</strong><span>Cost for your estimate</span></div>
      </div>
    </aside>
  </div>
</section>

<section class="section section--light" aria-labelledby="values-title">
  <div class="container">
    <header class="section-head">
      <p class="eyebrow"><?= icon('diamond', 'icon icon--xs') ?> Our values</p>
      <h2 id="values-title" class="section-title">What You Can Expect From Us</h2>
    </header>
    <div class="features">
      <div class="feature-item"><span class="feature-item__icon"><?= icon('ruler') ?></span><h3>Precision</h3><p>Level surfaces, straight lines, even joints and careful cuts. We measure twice and set once.</p></div>
      <div class="feature-item"><span class="feature-item__icon"><?= icon('shield') ?></span><h3>Responsibility</h3><p>Proper prep and waterproofing on every job, backed by a 1-year warranty on workmanship and product.</p></div>
      <div class="feature-item"><span class="feature-item__icon"><?= icon('clock') ?></span><h3>Efficiency</h3><p>Organized, fast execution that respects your time and your home.</p></div>
      <div class="feature-item"><span class="feature-item__icon"><?= icon('star') ?></span><h3>Commitment</h3><p>We build trust through our work. Your satisfaction is how we grow — one project at a time.</p></div>
    </div>
  </div>
</section>

<section class="section cta-band" aria-labelledby="cta-title">
  <div class="container cta-band__inner">
    <div>
      <h2 id="cta-title" class="section-title">Ready to Work With Us?</h2>
      <p>Get a free, no-obligation estimate for your tile project.</p>
    </div>
    <div class="btn-row">
      <a class="btn btn--gold btn--lg" href="/contact#estimate">Get a Free Estimate</a>
      <a class="btn btn--outline-light btn--lg" href="<?= e(sms_link()) ?>" data-track="sms_about"><?= icon('sms') ?> Text Us</a>
    </div>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
