<?php
namespace QueryL10n;

use Json\Json;

// Autoloading of composer dependencies
require_once __DIR__ . '/vendor/autoload.php';

// Override sources for functional tests both locally and on Travis
if (getenv('TRAVIS') || getenv('AUTOMATED_TESTS')) {
    $source_path = __DIR__ . '/tests/testfiles/';
} else {
    $source_path = __DIR__ . '/sources/';
}

// Query request
$type = Utils::getQueryParam('type');
$repo = Utils::getQueryParam('repo');
$bugzilla = Utils::getQueryParam('bugzilla');

$repos = new Repositories($source_path);

$json_data = new Json;

// Only one repo requested
if ($repo != '') {
    $locales = $repos->getSingleRepository($repo);
    if ($locales) {
        die($json_data->outputContent($locales));
    } else {
        http_response_code(400);
        die('ERROR: unknown repository.');
    }
}

// Only one type of repo requested
if ($type != '') {
    die($json_data->outputContent($repos->getTypeRepositories($type)));
}

// Bugzilla components
if ($bugzilla != '') {
    $bugzilla_query = new Bugzilla($source_path);
    die($json_data->outputContent($bugzilla_query->getBugzillaComponents($bugzilla)));
}

// Display a list of all repositories
die($json_data->outputContent($repos->getRepositories()));
