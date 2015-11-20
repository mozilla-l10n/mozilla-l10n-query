<?php

use Json\Json;

define('INSTALL_ROOT',  realpath(__DIR__ . '/../../') . '/');

// We always work with UTF8 encoding
mb_internal_encoding('UTF-8');

// Make sure we have a timezone set
date_default_timezone_set('Europe/Paris');

require __DIR__ . '/../../vendor/autoload.php';

// Set an environment variable so that the instance will use content from test files
putenv("AUTOMATED_TESTS=true");

// Launch PHP dev server in the background
chdir(INSTALL_ROOT);
exec('php -S 0.0.0.0:8083 > /dev/null 2>&1 & echo $!', $output);

// We will need the pid to kill it, beware, this is the pid of the php server started above
$pid = $output[0];

// Pause to let time for the dev server to launch in the background
sleep(3);

$failures = [];
$base_url = 'http://localhost:8083/';
$json_data = new Json;

// Base URL
$headers = get_headers($base_url, 1);
if (strpos($headers[0], '200 OK') === false) {
    $failures[] = "HTTP status for base URL is: {$headers[0]}. Expected: 200.";
}
$response = $json_data
    ->setURI($base_url)
    ->fetchContent();
if (! isset($response[0])) {
    $failures[] = "Product 0 is missing.";
} else {
    if ($response[0]['id'] !== 'beta') {
        $failures[] = "Product 0 is not 'beta'.";
    }
    if (! in_array('de', $response[0]['locales'])) {
        $failures[] = "'de' is missing from product 0.";
    }
}

// /?type=gaia
$url = $base_url . '?type=gaia';
$headers = get_headers($url, 1);
if (strpos($headers[0], '200 OK') === false) {
    $failures[] = "HTTP status for /?type=gaia is: {$headers[0]}. Expected: 200.";
}
$response = $json_data
    ->setURI($url)
    ->fetchContent();
$tmp_element = array_pop($response);
if ($tmp_element['id'] !== 'gaia_1_3') {
    $failures[] = "Last product for /?type=gaia is not 'gaia_1_3'.";
}
if (! in_array('ca', $tmp_element['locales'])) {
    $failures[] = "'ca' is missing from product 'gaia_1_3'.";
}

// /?repo=unknown
$url = $base_url . '?repo=unknown';
$headers = get_headers($url, 1);
if (strpos($headers[0], '400 Bad Request') === false) {
    $failures[] = "HTTP status for /?repo=unknown is: {$headers[0]}. Expected: 400.";
}

// /?repo=beta
$url = $base_url . '?repo=beta';
$headers = get_headers($url, 1);
if (strpos($headers[0], '200 OK') === false) {
    $failures[] = "HTTP status for /?repo=beta is: {$headers[0]}. Expected: 200.";
}
$response = $json_data
    ->setURI($url)
    ->fetchContent();
if ($response['id'] !== 'beta') {
    $failures[] = "Product ID for /?repo=beta is not 'beta'.";
}
if (! in_array('de', $response['locales'])) {
    $failures[] = "'de' is missing from product 'beta'.";
}

// /?bugzilla=www
$url = $base_url . '?bugzilla=www';
$headers = get_headers($url, 1);
if (strpos($headers[0], '200 OK') === false) {
    $failures[] = "HTTP status for /?bugzilla=www is: {$headers[0]}. Expected: 200.";
}
$response = $json_data
    ->setURI($url)
    ->fetchContent();
if (! isset($response['it'])) {
    $failures[] = "'it' is missing from response for /?bugzilla=www.";
}
if ($response['es-ES'] !== 'es-ES / Spanish (Spain)') {
    $failures[] = "Description for es-ES in /?bugzilla=www is wrong.\nExpected: es-ES / Spanish (Spain)\nReceived: {$response['es-ES']}\n";
}

// /?bugzilla=product
$url = $base_url . '?bugzilla=product';
$headers = get_headers($url, 1);
if (strpos($headers[0], '200 OK') === false) {
    $failures[] = "HTTP status for /?bugzilla=product is: {$headers[0]}. Expected: 200.";
}
$response = $json_data
    ->setURI($url)
    ->fetchContent();
if (! isset($response['it'])) {
    $failures[] = "'it' is missing from response for /?bugzilla=product.";
}
if ($response['es-ES'] !== 'es-ES / Spanish') {
    $failures[] = "Description for es-ES in /?bugzilla=product is wrong.\nExpected: es-ES / Spanish\nReceived: {$response['es-ES']}\n";
}

// Kill PHP dev server we launched in the background
exec('kill -9 ' . $pid);

// Display results
if ($failures) {
    echo chr(27) . "[41m" . 'There are functional test failures: ' . count($failures) . chr(27) . "[0m\n";
    echo implode("\n", $failures);
    echo "\n";
    exit(1);
} else {
    echo chr(27) . "[42m" . 'All functional tests PASSED.' . chr(27) . "[0m\n";
}
