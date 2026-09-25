<?php
require __DIR__ . '/includes/functions.php';

$page = [
    'slug' => 'projects',
    'title' => 'Tile & Bathroom Remodeling Projects | Guidine Pereira',
    'description' => 'Photos of real tile showers, bathroom remodels, tile floors, feature walls and backsplashes completed by Guidine Pereira Construction in the Myrtle Beach, SC area.',
    'schema' => [breadcrumb_schema([['Home', ''], ['Projects', 'projects']])],
    'body' => 'page-projects',
];
include __DIR__ . '/includes/header.php';

$counts = [];
foreach (gallery() as $p) {
    $counts[$p[1]] = ($counts[$p[1]] ?? 0) + 1;
}
?>

<section class="page-hero">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__narrow">
    <?php breadcrumbs([['Home', ''], ['Projects', 'projects']]); ?>
    <p class="eyebrow eyebrow--light">Portfolio</p>
    <h1 class="page-hero__title">Our tile and remodeling projects</h1>
    <p class="hero__lead">Real photos from homes we have worked on across the Myrtle Beach area. Showers, bathrooms, floors, walls and backsplashes, plus a look at the prep work that happens before the tile goes on.</p>
  </div>
</section>

<section class="section" aria-label="Project gallery">
  <div class="container">
    <div class="filters" role="toolbar" aria-label="Filter projects">
      <button type="button" class="filter is-active" data-filter="all" aria-pressed="true">All <span><?= count(gallery()) ?></span></button>
      <?php foreach ($CATEGORIES as $key => $label): if (empty($counts[$key])) continue; ?>
      <button type="button" class="filter" data-filter="<?= e($key) ?>" aria-pressed="false"><?= e($label) ?> <span><?= (int) $counts[$key] ?></span></button>
      <?php endforeach; ?>
    </div>
    <div class="masonry masonry--full" data-gallery>
      <?php foreach (gallery() as $p): ?>
      <a class="masonry__item" href="<?= e(work_img($p[0])) ?>" data-lightbox data-cat="<?= e($p[1]) ?>" data-caption="<?= e($p[2]) ?>">
        <?= picture($p[0], '(max-width: 600px) 50vw, (max-width: 1100px) 33vw, 25vw') ?>
        <span class="masonry__cap"><?= e($CATEGORIES[$p[1]]) ?></span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?php
$estimateHeading = 'Like what you see? Let\'s plan yours';
include __DIR__ . '/includes/estimate-section.php';
include __DIR__ . '/includes/footer.php';
