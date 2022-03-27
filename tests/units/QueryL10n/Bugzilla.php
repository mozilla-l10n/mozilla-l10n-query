<?php
namespace tests\units\QueryL10n;

use atoum\atoum;
use QueryL10n\Bugzilla as _Bugzilla;

require_once __DIR__ . '/../bootstrap.php';

class Bugzilla extends atoum\test
{
    public function getBugzillaComponentsDP()
    {
        return [
            ['', 'it', 'it / Italian'],
            ['product', 'es-ES', 'es-ES / Spanish'],
            ['www',  'es-ES', 'es-ES / Spanish (Spain)'],
        ];
    }

    /**
     * @dataProvider getBugzillaComponentsDP
     */
    public function testGetBugzillaComponents($a, $b, $c)
    {
        $obj = new _Bugzilla(TEST_FILES);

        $this
            ->string($obj->getBugzillaComponents($a)[$b])
                ->isEqualTo($c);
    }
}
