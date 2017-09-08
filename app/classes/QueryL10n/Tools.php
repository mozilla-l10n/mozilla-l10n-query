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
     * @param string $requested_tool Tool ID
     *
     * @return array List of supported locales
     */
    public function getLocales($requested_tool)
    {
        $locales = [];
        $supported_tools = ['pontoon', 'pontoon-mozorg'];

        if ($requested_tool == 'all') {
            foreach ($supported_tools as $tool) {
                $locales[$tool] = self::readConfigTxt($tool);
            }
        } else {
            if (in_array($requested_tool, $supported_tools)) {
                $locales = self::readConfigTxt($requested_tool);
            }
        }

        return $locales;
    }

    /**
     * Read a list of locales supported for a specific tool from a .txt file
     *
     * @param string $tool Tool ID
     *
     * @return array List of supported locales
     */
    public function readConfigTxt($tool)
    {
        $locales = [];
        $file_name = $this->source_path . 'tools/' . $tool . '.txt';
        if (file_exists($file_name)) {
            $locales = file($file_name, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            sort($locales);
        }

        return $locales;
    }
}
