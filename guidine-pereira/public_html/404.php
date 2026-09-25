<?php
require __DIR__ . '/includes/functions.php';
http_response_code(404);

$page = [
    'slug' => '404',
    'title' => 'Page Not Found | Guidine Pereira Construction',
    'description' => 'The page you are looking for could not be found.',
    'noindex' => true,
    'body' => 'page-404',
];
include __DIR__ . '/includes/header.php';
?>

<section class="page-hero page-hero--center">
  <div class="hero__pattern" aria-hidden="true"></div>
  <div class="container page-hero__narrow">
    <p class="eyebrow eyebrow--light">Error 404</p>
    <h1 class="page-hero__title">This page is not here</h1>
    <p class="hero__lead">The link may be old or mistyped. Try one of these instead.</p>
    <div class="hero__actions">
      <a class="btn btn--primary btn--lg" href="<?= e(url()) ?>">Back to home</a>
      <a class="btn btn--outline-light btn--lg" href="<?= e(url('projects')) ?>">See our projects</a>
    </div>
  </div>
</section>

<?php include __DIR__ . '/includes/footer.php';
