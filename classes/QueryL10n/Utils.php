<?php
namespace QueryL10n;

/**
 * Utils class
 *
 * Utility functions
 *
 * @package QueryL10n
 */
class Utils
{
    /*
     * Read GET parameter if set, or fallback
     *
     * @param   string  $param     GET parameter to check
     * @param   string  $fallback  Optional fallback value
     * @return  string             Parameter value, or fallback
     */
    public static function getQueryParam($param, $fallback = '')
    {
        if (isset($_GET[$param])) {
            return is_bool($fallback)
                   ? true
                   : self::secureText($_GET[$param]);
        }

        return $fallback;
    }

    /*
     * Function sanitizing a string or an array of strings.
     *
     * @param   array         $origin    String to sanitize
     * @param   boolean       $isarray   If $origin must be treated as array
     * @return  string/array             Sanitized string or array
     */
    public static function secureText($origin, $isarray = true)
    {
        if (! is_array($origin)) {
            // If $origin is a string, always return a string
            $origin  = [$origin];
            $isarray = false;
        }

        foreach ($origin as $item => $value) {
            // CRLF XSS
            $item  = str_replace('%0D', '', $item);
            $item  = str_replace('%0A', '', $item);
            $value = str_replace('%0D', '', $value);
            $value = str_replace('%0A', '', $value);

            $value = filter_var(
                $value,
                FILTER_SANITIZE_STRING,
                FILTER_FLAG_STRIP_LOW
            );

            $item  = htmlspecialchars(strip_tags($item), ENT_QUOTES);
            $value = htmlspecialchars(strip_tags($value), ENT_QUOTES);

            // Repopulate value
            $sanitized[$item] = $value;
        }

        return ($isarray == true) ? $sanitized : $sanitized[0];
    }
}
