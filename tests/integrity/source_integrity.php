<?php
namespace QueryL10n;

// Autoloading of composer dependencies
require_once __DIR__ . '/../../vendor/autoload.php';

$source_path = __DIR__ . '/../../sources/';

$repos = new Repositories($source_path);
$available_repositories = $repos->getRepositories();

$errors = [];

// Check if there are duplicated display_order values
$order = [];
foreach ($available_repositories as $repo_data) {
    $repo_order = $repo_data['display_order'];
    if ($repo_order == 0) {
        continue;
    }
    if (! in_array($repo_order, $order)) {
        $order[] = $repo_order;
    } else {
        $errors[] = "Repository *{$repo_data['id']}* has a duplicated display_order ({$repo_order})";
    }
}

// Check if display_order values are not sequential
sort($order);
for ($i = 0; $i < count($order) - 1; $i++) {
    if ($order[$i] + 1 != $order[$i + 1]) {
        $errors[] = "display_order value is not sequential ({$order[$i + 1]})";
    }
}

// Check files
$repositories_json = $repos->getRepositoriesJson();
foreach ($repositories_json as $repo_data) {
    $file_name = $source_path . $repo_data['locales'];
    if (! file_exists($file_name)) {
        $errors[] = "Repository *{$repo_data['id']}* references a missing file ({$repo_data['locales']})";
    }
}

if (! empty($errors)) {
    echo "Detected errors during source integrity checks:\n";
    echo implode("\n", $errors);
    echo "\n";
    exit(1);
} else {
    echo "All sources seem to be OK.\n";
}
