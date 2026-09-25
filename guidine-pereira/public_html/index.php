<?php
require __DIR__ . '/includes/functions.php';

$page = [
    'slug' => '',
    'title' => 'Tile & Bathroom Remodeling in Myrtle Beach, SC | Guidine Pereira',
    'description' => 'Family-owned tile contractor in Myrtle Beach, SC. Shower and bathroom remodeling, tile flooring, wall tile and backsplash installation. Licensed and insured. Free estimate: (843) 492-8374.',
    'preload' => 'wood-look-tile-walk-in-shower-bench-window',
    'schema' => [faq_schema($FAQ_GENERAL)],
    'body' => 'page-home',
];
include __DIR__ . '/includes/header.php';

$featured = [
    'white-subway-tile-shower-mosaic-feature',
    'star-pattern-decorative-floor-tile',
    'marble-look-shower-bench-mosaic-niche',
    'kitchen-backsplash-grey-subway-tile',
    'black-white-checkerboard-floor-tile',
    'botanical-feature-wall-tile-bathroom',
    'marble-shower-vertical-mosaic-accent',
    'curbless-shower-marble-hex-floor',
    'marble-hexagon-floor-tile',
    'blue-subway-tile-shower',
    'beige-porcelain-shower-niche',
    'marble-wall-tile-mosaic-band',
];
?>

<section class="hero">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container hero__grid">
    <div class="hero__copy">
      <p class="eyebrow eyebrow--light">Tile &amp; remodeling contractor in Myrtle Beach, SC</p>
      <h1 class="hero__title">Showers, floors and walls finished with <em>precision</em></h1>
      <p class="hero__lead">Guidine Pereira Construction is a family-owned team that remodels bathrooms and installs tile for homeowners across the Grand Strand. Straight lines, level floors and a clean job from the first day to the final walkthrough.</p>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="#estimate">Get a Free Estimate <?= icon('arrow') ?></a>
        <a class="btn btn--outline-light btn--lg" href="<?= e(tel_link()) ?>" data-track="call"><?= icon('phone') ?><?= e(PHONE_DISPLAY) ?></a>
      </div>
      <ul class="hero__trust">
        <li><?= icon('shield') ?>Licensed &amp; insured</li>
        <li><?= icon('home') ?>Family-owned</li>
        <li><?= icon('ruler') ?>Price at the estimate</li>
      </ul>
    </div>
    <div class="hero__media">
      <figure class="hero__img hero__img--main">
        <?= picture('wood-look-tile-walk-in-shower-bench-window', '(max-width: 900px) 62vw, 30vw', false) ?>
      </figure>
      <figure class="hero__img hero__img--top">
        <?= picture('white-subway-tile-shower-mosaic-feature', '(max-width: 900px) 36vw, 18vw') ?>
      </figure>
      <figure class="hero__img hero__img--bottom">
        <?= picture('star-pattern-decorative-floor-tile', '(max-width: 900px) 36vw, 18vw') ?>
      </figure>
      <div class="hero__badge">
        <strong><span data-count="800">800</span>+</strong>
        <span>projects completed</span>
      </div>
    </div>
  </div>
</section>

<section class="stats" aria-label="Company in numbers">
  <div class="container stats__grid">
    <div class="stat"><strong><span data-count="10">10</span>+</strong><span>Years of experience in the trade</span></div>
    <div class="stat"><strong><span data-count="7">7</span></strong><span>Years serving U.S. homeowners</span></div>
    <div class="stat"><strong><span data-count="500">500</span>+</strong><span>Clients served</span></div>
    <div class="stat"><strong><span data-count="800">800</span>+</strong><span>Projects completed</span></div>
  </div>
</section>

<section class="section" id="services" aria-labelledby="services-title">
  <div class="container">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">What we do</p>
        <h2 class="h2" id="services-title">Tile and remodeling services</h2>
      </div>
      <p class="section-head__text">Four specialties, one standard. Every project gets the same careful prep, layout planning and finish work, whether it is a single backsplash or a complete bathroom.</p>
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

<section class="section section--soft why" aria-labelledby="why-title">
  <div class="container why__grid">
    <div class="why__media reveal">
      <figure class="why__img why__img--a"><?= picture('white-marble-look-shower-niche-bench', '(max-width: 900px) 60vw, 28vw') ?></figure>
      <figure class="why__img why__img--b"><?= picture('double-shower-niche-detail', '(max-width: 900px) 45vw, 18vw') ?></figure>
      <div class="why__tag"><span>Detail</span> niche with mitered edges</div>
    </div>
    <div class="why__copy">
      <p class="eyebrow reveal">Why homeowners choose us</p>
      <h2 class="h2 reveal" id="why-title">The details you notice every day</h2>
      <p class="lead reveal">Tile work is judged up close. We take the time to plan the layout, prepare the surface and finish every edge, because that is what makes a remodel look right for years.</p>
      <div class="features">
        <div class="feature reveal"><?= icon('chat') ?><div><h3>Clear communication</h3><p>You talk directly with the owner, from the estimate to the final walkthrough.</p></div></div>
        <div class="feature reveal"><?= icon('ruler') ?><div><h3>Price on the spot</h3><p>We measure at the visit and, in most cases, give you the price right there.</p></div></div>
        <div class="feature reveal"><?= icon('layers') ?><div><h3>Detail-driven finish</h3><p>Balanced cuts, level joints, clean trims and sealed transitions.</p></div></div>
        <div class="feature reveal"><?= icon('clock') ?><div><h3>Flexible scheduling</h3><p>Visit and work times that fit your week, with a crew ready to start.</p></div></div>
        <div class="feature reveal"><?= icon('shield') ?><div><h3>Workmanship guarantee</h3><p>Adjustments within 30 days are on us, and we stand behind our work after that.</p></div></div>
        <div class="feature reveal"><?= icon('home') ?><div><h3>Respect for your home</h3><p>Floors protected, dust controlled and the site cleaned at the end of the day.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section" id="projects" aria-labelledby="projects-title">
  <div class="container">
    <div class="section-head reveal">
      <div>
        <p class="eyebrow">Recent work</p>
        <h2 class="h2" id="projects-title">Projects across the Grand Strand</h2>
      </div>
      <a class="btn btn--dark" href="<?= e(url('projects')) ?>">View all projects <?= icon('arrow') ?></a>
    </div>
    <div class="masonry" data-gallery>
      <?php foreach ($featured as $slug): $p = photo($slug); ?>
      <a class="masonry__item reveal" href="<?= e(work_img($slug)) ?>" data-lightbox data-caption="<?= e($p[2]) ?>">
        <?= picture($slug, '(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 25vw') ?>
        <span class="masonry__cap"><?= e($CATEGORIES[$p[1]]) ?></span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section--dark process" aria-labelledby="process-title">
  <div class="process__pattern" aria-hidden="true"></div>
  <div class="container">
    <div class="section-head section-head--light reveal">
      <div>
        <p class="eyebrow eyebrow--light">Behind the tile</p>
        <h2 class="h2" id="process-title">What you don't see matters most</h2>
      </div>
      <p class="section-head__text">A shower that looks good on day one and still performs in ten years starts long before the first tile. Here is how every project moves forward.</p>
    </div>
    <div class="process__photos">
      <figure class="reveal"><?= picture('bathroom-demolition-down-to-studs', '(max-width: 700px) 33vw, 22vw') ?><figcaption>Demolition to the studs</figcaption></figure>
      <figure class="reveal"><?= picture('shower-waterproofing-membrane', '(max-width: 700px) 33vw, 22vw') ?><figcaption>Continuous waterproofing</figcaption></figure>
      <figure class="reveal"><?= picture('waterproofed-shower-pan-drain', '(max-width: 700px) 33vw, 22vw') ?><figcaption>Sloped, sealed shower pan</figcaption></figure>
      <figure class="reveal"><?= picture('tile-leveling-system-installation', '(max-width: 700px) 33vw, 22vw') ?><figcaption>Leveling system on every floor</figcaption></figure>
    </div>
    <ol class="steps">
      <li class="step reveal"><span class="step__n">01</span><h3>Call, text or send the form</h3><p>Tell us what you have in mind. We set up a visit at a time that works for you.</p></li>
      <li class="step reveal"><span class="step__n">02</span><h3>Free in-home estimate</h3><p>We measure, talk through tile and layout options and give you a clear price and timeline.</p></li>
      <li class="step reveal"><span class="step__n">03</span><h3>Prep and protect</h3><p>Floors covered, old material removed, surfaces flattened and wet areas waterproofed.</p></li>
      <li class="step reveal"><span class="step__n">04</span><h3>Install and walkthrough</h3><p>Tile set, grouted and sealed. We walk the finished space with you before we call it done.</p></li>
    </ol>
  </div>
</section>

<section class="guarantee" aria-labelledby="guarantee-title">
  <div class="container guarantee__inner reveal">
    <div class="guarantee__icon"><?= icon('shield') ?></div>
    <div class="guarantee__copy">
      <h2 id="guarantee-title">Our workmanship guarantee</h2>
      <p>Any adjustment needed within 30 days after completion is covered at no cost. After that, if an issue related to our work shows up, we come back and make it right. You only cover a trip fee.</p>
    </div>
    <a class="btn btn--light btn--lg" href="#estimate">Start my project</a>
  </div>
</section>

<section class="section areas" aria-labelledby="areas-title">
  <div class="container areas__grid">
    <div class="reveal">
      <p class="eyebrow">Service area</p>
      <h2 class="h2" id="areas-title">Based in Myrtle Beach, working up to two hours around</h2>
      <p class="lead">We serve homeowners along the Grand Strand, inland Horry and Georgetown counties, the Pee Dee region and southeastern North Carolina.</p>
      <a class="btn btn--dark" href="<?= e(url('service-areas')) ?>">See all service areas <?= icon('arrow') ?></a>
    </div>
    <div class="areas__lists reveal">
      <div>
        <h3 class="areas__state">South Carolina</h3>
        <ul class="chips"><?php foreach ($AREAS_SC as $c): ?><li><?= e($c) ?></li><?php endforeach; ?></ul>
      </div>
      <div>
        <h3 class="areas__state">North Carolina</h3>
        <ul class="chips"><?php foreach ($AREAS_NC as $c): ?><li><?= e($c) ?></li><?php endforeach; ?></ul>
      </div>
    </div>
  </div>
</section>

<section class="section section--soft" aria-labelledby="faq-title">
  <div class="container faq-wrap">
    <div class="faq-wrap__head reveal">
      <p class="eyebrow">FAQ</p>
      <h2 class="h2" id="faq-title">Questions homeowners ask us</h2>
      <p class="lead">Don't see your question? Call or text <a href="<?= e(tel_link()) ?>" data-track="call"><?= e(PHONE_DISPLAY) ?></a> and we will walk you through it.</p>
    </div>
    <div class="reveal"><?php render_faq($FAQ_GENERAL); ?></div>
  </div>
</section>

<?php
include __DIR__ . '/includes/estimate-section.php';
include __DIR__ . '/includes/footer.php';
