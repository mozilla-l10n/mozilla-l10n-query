<?php
namespace QueryL10n;

/**
 * Bugzilla class
 *
 * This class is used to extract information about Bugzilla l10n components
 *
 * @package QueryL10n
 */
class Bugzilla
{
    /**
     * @var array $component_list  List of Bugzilla l10n components
     */
    private $component_list;

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
        $this->component_list = $this->getBugzillaComponentsJson();
    }

    /**
     * Return array with data for all Bugzilla l10n components
     *
     * @return array Data repositories
     */
    public function getBugzillaComponentsJson()
    {
        $json_data = new Json($this->source_path . 'bugzilla_components.json');

        return $json_data->fetchContent();
    }

    /**
     * Return list of Bugzilla component names based on product.
     * For Mozilla Localization (default) we need its component names.
     * For www.mozilla.org::L10N we need values of cf_locale (locale selector).
     *
     * @param string $product Bugzilla product
     *
     * @return array List of locales and their Bugzilla references
     */
    public function getBugzillaComponents($product)
    {
        $result = [];
        if ($product == 'www') {
            $locale_list = 'cf_locale';
        } else {
            $locale_list = 'mozilla_localizations';
        }

        foreach ($this->component_list[$locale_list] as $locale => $data) {
            $result[$locale] = $data['full_name'];
        }

        return $result;
    }
}
