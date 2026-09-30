<?php
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'bootstrap.php') {
    http_response_code(403);
    exit;
}

define('ROOT_DIR', dirname(__DIR__));

require __DIR__ . '/config.php';
require __DIR__ . '/data.php';
require __DIR__ . '/functions.php';

if (!headers_sent()) {
    header('Content-Type: text/html; charset=UTF-8');
}
