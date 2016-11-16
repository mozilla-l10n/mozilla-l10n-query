<?php
namespace tests\units\QueryL10n;

use atoum;
use QueryL10n\Tools as _Tools;

require_once __DIR__ . '/../bootstrap.php';

class Tools extends atoum\test
{
    public function testGetLocales()
    {
        $obj = new _Tools(TEST_FILES);

        $this
            ->array($obj->getLocales('pootle'))
                ->isEqualTo([]);
        $this
            ->array($obj->getLocales('pontoon'))
                ->isEqualTo(['ast', 'bg', 'bn-IN']);
    }
}
