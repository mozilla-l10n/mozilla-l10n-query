<?php
// Webhook to update a repo for each push on GitHub

date_default_timezone_set('Europe/Paris');

// App variables
$app_root = realpath(__DIR__ . '/../');
$composer = $app_root . '/composer.phar';

require $app_root . '/vendor/autoload.php';

// Git variables
$branch = 'master';
$header = 'HTTP_X_HUB_SIGNATURE';

$config_file = $app_root . '/app/config/config.yml';
if (!file_exists($config_file)) {
    throw new \InvalidArgumentException(sprintf('File %s is missing. Run composer install.', $config_file));
}
$config = \Symfony\Component\Yaml\Yaml::parse(file_get_contents($config_file));
$secret = $config['config']['github_key'];

// Logging function to output content to /github_log.txt
function logHookResult($message, $success = false)
{
    $log_headers = "$message\n";
    if (! $success) {
        foreach ($_SERVER as $header => $value) {
            $log_headers .= "$header: $value \n";
        }
    }
    file_put_contents(__DIR__ . '/github_log.txt', $log_headers);
}

// CHECK: Download composer in the app root if it is not already there
if (! file_exists($composer)) {
    file_put_contents(
        $composer,
        file_get_contents('https://getcomposer.org/composer.phar')
    );
}

if (isset($_SERVER[$header])) {
    $validation = hash_hmac(
        'sha1',
        file_get_contents('php://input'),
        $secret
    );

    if ($validation == explode('=', $_SERVER[$header])[1]) {
        // Pull latest changes
        $log = "Updating Git repository\n";
        exec("git checkout $branch ; git pull origin $branch");

        // Install or update dependencies
        if (file_exists($composer)) {
            chdir($app_root);

            // www-data does not have a HOME or COMPOSER_HOME, create one
            $cache_folder = "{$app_root}/.composer_cache";
            if (! is_dir($cache_folder)) {
                $log = "Creating folder {$cache_folder}\n";
                mkdir($cache_folder);
            }

            putenv("COMPOSER_HOME={$app_root}/.composer_cache");

            if (file_exists($app_root . '/vendor')) {
                $log .= "Updating Composer\n";
                exec("php {$composer} update > /dev/null 2>&1");
            } else {
                $log .= "Installing Composer\n";
                exec("php {$composer} install > /dev/null 2>&1");
            }
        }

        $log .= 'Last update: ' . date('d-m-Y H:i:s');
        logHookResult($log, true);
    } else {
        logHookResult('Invalid GitHub secret');
    }
} else {
    logHookResult("{$header} header missing, define a secret key for your project in GitHub");
}
