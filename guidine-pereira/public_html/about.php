<?php
require __DIR__ . '/includes/functions.php';

$page = [
    'slug' => 'about',
    'title' => 'About Us | Family-Owned Tile Contractor in Myrtle Beach, SC',
    'description' => 'Guidine Pereira Construction is a family-owned tile and remodeling company in Myrtle Beach, SC with more than 10 years of experience, 500+ clients and 800+ projects completed.',
    'schema' => [breadcrumb_schema([['Home', ''], ['About', 'about']])],
    'body' => 'page-about',
];
include __DIR__ . '/includes/header.php';
?>

<section class="page-hero">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__narrow">
    <?php breadcrumbs([['Home', ''], ['About', 'about']]); ?>
    <p class="eyebrow eyebrow--light">About us</p>
    <h1 class="page-hero__title">A family business built one tile at a time</h1>
    <p class="hero__lead">More than ten years in the trade, seven of them serving homeowners in the United States, and a simple way of working: show up, communicate clearly and finish every detail.</p>
  </div>
</section>

<section class="section">
  <div class="container split split--media">
    <div class="about__media reveal">
      <figure class="about__img about__img--a"><?= picture('walk-in-shower-wood-look-tile-bench', '(max-width: 900px) 70vw, 30vw') ?></figure>
      <figure class="about__img about__img--b"><?= picture('marble-look-shower-bench-mosaic-niche', '(max-width: 900px) 45vw, 18vw') ?></figure>
    </div>
    <div class="split__copy">
      <p class="eyebrow reveal">Our story</p>
      <h2 class="h2 reveal">Guidine Pereira Construction LLC</h2>
      <p class="reveal">Our work began in the tile trade more than a decade ago, learning the craft on real jobsites where every cut and every line had to be right. After years of installing showers, floors and walls for homeowners and for other contractors and stores, we founded Guidine Pereira Construction LLC in January 2022 in Myrtle Beach, South Carolina.</p>
      <p class="reveal">Today we are a family-owned company led by Adeildo, who meets clients in person at the estimate and stays involved until the final walkthrough. Our core crew works together on every project and brings in additional hands when a job calls for it, so your schedule stays on track.</p>
      <p class="reveal">We have served more than 500 clients and completed more than 800 projects, from single backsplashes to complete bathroom remodels. Much of our work comes from referrals, which is the best measure we know of a job done right.</p>
    </div>
  </div>
</section>

<section class="stats stats--light" aria-label="Company in numbers">
  <div class="container stats__grid">
    <div class="stat"><strong><span data-count="10">10</span>+</strong><span>Years of experience in the trade</span></div>
    <div class="stat"><strong><span data-count="7">7</span></strong><span>Years serving U.S. homeowners</span></div>
    <div class="stat"><strong><span data-count="500">500</span>+</strong><span>Clients served</span></div>
    <div class="stat"><strong><span data-count="800">800</span>+</strong><span>Projects completed</span></div>
  </div>
</section>

<section class="section section--soft" aria-labelledby="values-title">
  <div class="container">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">What guides us</p>
        <h2 class="h2" id="values-title">Four values on every jobsite</h2>
      </div>
      <p class="section-head__text">Our motto is <strong><?= e(TAGLINE) ?></strong> These are the principles behind it.</p>
    </div>
    <div class="values">
      <div class="value reveal"><span class="value__n">01</span><h3>Quality</h3><p>Proper materials, proper prep and tile work that holds up long after we leave.</p></div>
      <div class="value reveal"><span class="value__n">02</span><h3>Respect</h3><p>For your home, your time and your budget. Floors protected, sites cleaned, calls returned.</p></div>
      <div class="value reveal"><span class="value__n">03</span><h3>Agility</h3><p>Flexible scheduling and quick estimates, often with the price given during the visit.</p></div>
      <div class="value reveal"><span class="value__n">04</span><h3>Excellence</h3><p>Straight lines, level floors and clean edges. The details are the job.</p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="facts-title">
  <div class="container split">
    <div class="split__copy">
      <p class="eyebrow reveal">Good to know</p>
      <h2 class="h2 reveal" id="facts-title">Working with us</h2>
      <p class="reveal">We keep things straightforward so you always know where your project stands.</p>
    </div>
    <div class="included">
      <div class="included__item reveal"><?= icon('shield') ?><div><h3>Licensed and insured</h3><p>A registered LLC with an active business license and insurance policy.</p></div></div>
      <div class="included__item reveal"><?= icon('ruler') ?><div><h3>Priced by the project</h3><p>Most work is priced by the square foot, with the quote given at the estimate.</p></div></div>
      <div class="included__item reveal"><?= icon('wallet') ?><div><h3>Simple payments</h3><p>We accept Zelle, cash and check.</p></div></div>
      <div class="included__item reveal"><?= icon('check') ?><div><h3>Workmanship guarantee</h3><p>30-day adjustments at no cost, then return visits for work-related issues for a trip fee only.</p></div></div>
    </div>
  </div>
</section>

<?php
include __DIR__ . '/includes/estimate-section.php';
include __DIR__ . '/includes/footer.php';
