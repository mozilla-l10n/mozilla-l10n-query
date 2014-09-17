<?php
namespace QueryL10n;

// Autoloading of composer dependencies
require_once __DIR__ . '/vendor/autoload.php';

$source_path = __DIR__ . '/sources/';

$list = Utils::getQueryParam('list');
$repo = Utils::getQueryParam('repo');
$repos = new Repositories($source_path);

if ($repo != '') {
    $locales = $repos->getSingleRepository($repo);
    if ($locales) {
        die(Json::output($locales));
    } else {
        http_response_code(400);
        die('ERROR: unknown repository.');
    }
}

if ($list == '' || $list == 'all') {
    die(Json::output($repos->getRepositories()));
}

if ($list == 'gaia') {
    die(Json::output($repos->getGaiaRepositories()));
}

// In case of unknown request
http_response_code(400);
die('ERROR: unknown request.');

