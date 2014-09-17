<?php
namespace QueryL10n;

/**
 * Repositories class
 *
 * This class is used to extract all the data we need about repositories
 *
 * @package QueryL10n
 */
Class Repositories
{
    private $repo_list;
    private $source_path;

    /**
     * The constructor sets shared variables
     *
     * @param string $path Path to folder with source files
     */
    public function __construct($path)
    {
        $this->source_path = $path;
        $this->repo_list = self::getRepositoriesJson($path);
    }

    /**
     * Return array with data for all repositories
     *
     * @param string $path Path to folder with source files
     * @return array       Data repositories
     */
    public function getRepositoriesJson($path)
    {
        return Json::fetch($path . 'repositories.json');
    }

    /**
     * Return a full list of repositories with ID, pretty name and
     * supported locales
     *
     * @return array List of supported repositories
     */
    public function getRepositories()
    {
        $result = [];
        foreach ($this->repo_list as $repo) {
            $result[] = [
                'id' => $repo['id'],
                'name' => $repo['name'],
                'locales' => self::getSupportedLocales($repo['id'])
            ];
        }

        return $result;
    }

    /**
     * Return list of Gaia repositories with ID, pretty name and
     * supported locales
     *
     * @return array List of supported repositories
     */
    public function getGaiaRepositories()
    {
        $result = [];
        foreach ($this->repo_list as $repo) {
            if (strpos($repo['id'], 'gaia') !== false) {
                $result[] = [
                    'id' => $repo['id'],
                    'name' => $repo['name'],
                    'locales' => self::getSupportedLocales($repo['id'])
                ];
            }
        }

        return $result;
    }

    /**
     * Return data about a single repository
     *
     * @param  string        $repo_id Repository ID
     * @return array/boolean          Data about the requested repository, false if unknown repo
     */
    public function getSingleRepository($repo_id)
    {
        if (isset($this->repo_list[$repo_id])) {
            $repo = $this->repo_list[$repo_id];

            return [
                'id' => $repo['id'],
                'name' => $repo['name'],
                'locales' => self::getSupportedLocales($repo['id'])
            ];
        }

        return false;
    }

    /**
     * Return a list of locales supported for a specific repo ID
     *
     * @param  string $repo_id  Repository ID
     * @return array            List of supported locales
     */
    public function getSupportedLocales($repo_id)
    {
        $locales = [];
        if (isset($this->repo_list[$repo_id])) {
            $file_name = $this->source_path . $this->repo_list[$repo_id]['locales'];
            $locales = file($file_name, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        }

        return $locales;
    }
}
