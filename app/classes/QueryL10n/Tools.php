<?php
namespace QueryL10n;

/**
 * Tools class
 *
 * This class is used to return the list of locales working in a specific tool
 *
 * @package QueryL10n
 */
class Tools
{
    /**
     * @var string $source_path  Path for sources
     */
    private $source_path;

    /**
     * The constructor sets shared variables
     *
     * @param string $path Path to folder with source files
     */
    public function __construct($path)
    {
        $this->source_path = $path;
    }

    /**
     * Return a list of locales supported for a specific tool
     *
     * @param  string $tool Tool ID
     * @return array  List of supported locales
     */
    public function getLocales($tool)
    {
        $locales = [];
        $supported_tools = ['locamotion', 'pontoon'];
        if (in_array($tool, $supported_tools)) {
            $file_name = $this->source_path . $tool . '.txt';
            if (file_exists($file_name)) {
                $locales = file($file_name, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
                sort($locales);
            }
        }

        return $locales;
    }
}
