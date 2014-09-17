<?php
namespace QueryL10n;

// Autoloading of composer dependencies
require_once __DIR__ . '/vendor/autoload.php';

$source_path = __DIR__ . '/sources/';

// Query request
$type = Utils::getQueryParam('type');
$repo = Utils::getQueryParam('repo');

$repos = new Repositories($source_path);

// Only one repo requested
if ($repo != '') {
    $locales = $repos->getSingleRepository($repo);
    if ($locales) {
        die(Json::output($locales));
    } else {
        http_response_code(400);
        die('ERROR: unknown repository.');
    }
}

// Only one type of repo requested
if ($type != '') {
    die(Json::output($repos->getTypeRepositories($type)));
}

// Display a list of all repositories
die(Json::output($repos->getRepositories()));

