<?php
require __DIR__ . '/includes/bootstrap.php';
http_response_code(404);

$page = [
    'title'       => 'Page Not Found | R.A Tile Renovation',
    'description' => 'The page you are looking for could not be found.',
    'path'        => '404',
    'noindex'     => true,
    'body_class'  => 'page-404',
];
require __DIR__ . '/includes/header.php';
?>

<section class="section thanks">
  <div class="container container--narrow center">
    <span class="thanks__icon thanks__icon--muted"><?= icon('diamond') ?></span>
    <h1 class="section-title">Page Not Found</h1>
    <p class="section-lead">Sorry, we couldn't find that page. Try one of our services below or request your free estimate.</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn--gold btn--lg" href="/contact#estimate">Get a Free Estimate</a>
      <a class="btn btn--outline btn--lg" href="/">Back to Home</a>
    </div>
    <ul class="chips chips--light chips--center mt-2">
      <?php foreach ($SERVICES as $slug => $s): ?>
      <li><a class="chip chip--link" href="<?= e(link_to($slug)) ?>"><?= e($s['nav']) ?></a></li>
      <?php endforeach; ?>
    </ul>
  </div>
</section>

<?php require __DIR__ . '/includes/footer.php'; ?>
