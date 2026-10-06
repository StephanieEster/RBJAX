<?php
declare(strict_types=1);

// The recipient is fixed here on the server. The HTML _to value is never used.
const NEAT_RECIPIENT = 'Neatcleaningservicesusa@gmail.com';
const NEAT_COMPANY = 'Neat Cleaning';

// Optional: set the final HTTPS domain to force one canonical host.
// Example: 'https://your-actual-domain.com' (no trailing slash).
// Empty means the site's validated current host is used automatically.
const NEAT_SITE_URL = '';

function neat_site_origin(): string
{
    if (NEAT_SITE_URL !== '') {
        $configured = rtrim(NEAT_SITE_URL, '/');
        if (!preg_match('~^https://[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$~i', $configured)) {
            throw new RuntimeException('Invalid site URL configuration.');
        }
        return $configured;
    }
    $host = strtolower((string) ($_SERVER['HTTP_HOST'] ?? ''));
    if (!preg_match('/\A(?:[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?)(?::[0-9]{1,5})?\z/i', $host)) {
        throw new RuntimeException('Invalid host.');
    }
    $secure = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || (($_SERVER['SERVER_PORT'] ?? '') === '443');
    return ($secure ? 'https://' : 'http://') . $host;
}

function neat_pages(): array
{
    return [
        'index.html', 'services.html', 'regular-cleaning.html', 'deep-cleaning.html',
        'airbnb-cleaning.html', 'move-in-move-out-cleaning.html', 'commercial-cleaning.html',
        'about.html', 'service-areas.html', 'contact.html', 'faq.html',
        'privacy-policy.html', 'terms-of-use.html', 'thank-you.html', '404.html',
    ];
}
