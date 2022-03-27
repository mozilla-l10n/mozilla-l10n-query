<?php
namespace tests\units\QueryL10n;

use atoum\atoum;
use QueryL10n\Utils as _Utils;

require_once __DIR__ . '/../bootstrap.php';

class Utils extends atoum\test
{
    public function colorizeOutputDP()
    {
        return [
            ['test pass message', 'green', "\033[1;37m\033[42mtest pass message\033[0m\n"],
            ['test error message', 'red', "\033[1;37m\033[41mtest error message\033[0m\n"],
            ['test unknown color', 'blue', "test unknown color\033[0m\n"],
        ];
    }

    /**
     * @dataProvider colorizeOutputDP
     */
    public function testColorizeOutput($a, $b, $c)
    {
        $obj = new _Utils();
        $this
            ->string($obj->colorizeOutput($a, $b))
                ->isEqualTo($c);
    }

    public function secureTextDP()
    {
        return [
            ['test%0D', false, 'test'],
            ['%0Atest', false, 'test'],
            ['%0Ate%0Dst', false, 'test'],
            ['%0Ate%0Dst', true, 'test'],
            ['&test', false, '&amp;test'],
            [['test%0D', '%0Atest'], false, 'test'],
        ];
    }

    /**
     * @dataProvider secureTextDP
     */
    public function testsecureText($a, $b, $c)
    {
        $obj = new _Utils();
        $this
            ->string($obj->secureText($a, $b))
                ->isEqualTo($c);
    }
}
