<?php
namespace tests\units\QueryL10n;

use atoum;
use QueryL10n\Repositories as _Repositories;

require_once __DIR__ . '/../bootstrap.php';

class Repositories extends atoum\test
{
    public function testGetRepositories()
    {
        $obj = new _Repositories(TEST_FILES);

        $result = [
            [
                'id' => 'beta',
                'name'  => 'Beta',
                'locales' => ['da', 'de', 'dsb', 'el']
            ],
            [
                'id' => 'gaia_1_3',
                'name'  => 'Gaia 1.3',
                'locales' => ['ar', 'bg', 'bn-BD', 'ca', 'cs']
            ],
        ];

        $this
            ->array($obj->getRepositories())
                ->isEqualTo($result);
    }

    public function getTypeRepositoriesDP()
    {
        return [
            [
                'gaia',
                [
                   [
                       'id' => 'gaia_1_3',
                        'name'  => 'Gaia 1.3',
                        'locales' => ['ar', 'bg', 'bn-BD', 'ca', 'cs']
                    ]
                ]
            ],
            [
                'product',
                [
                    [
                        'id' => 'beta',
                        'name'  => 'Beta',
                        'locales' => ['da', 'de', 'dsb', 'el']
                    ]
                ]
            ],
            [
                'foobar',
                []
            ]
        ];
    }

    /**
     * @dataProvider getTypeRepositoriesDP
     */
    public function testGetTypeRepositories($a, $b)
    {
        $obj = new _Repositories(TEST_FILES);

         $this
            ->array($obj->getTypeRepositories($a))
                ->isEqualTo($b);
    }

    public function testGetSingleRepository()
    {
        $obj = new _Repositories(TEST_FILES);

        $result = [
                'id' => 'gaia_1_3',
                'name'  => 'Gaia 1.3',
                'locales' => ['ar', 'bg', 'bn-BD', 'ca', 'cs']
        ];

        $this
            ->array($obj->getSingleRepository('gaia_1_3'))
                ->isEqualTo($result);

        // Non existing repository
        $this
            ->boolean($obj->getSingleRepository('foobar'))
                ->isFalse();
    }

    public function getSupportedLocalesDP()
    {
        return [
            ['gaia_1_3', ['ar', 'bg', 'bn-BD', 'ca', 'cs']],
            ['beta', ['da', 'de', 'dsb', 'el']],
            ['foobar', []]
        ];
    }

    /**
     * @dataProvider getSupportedLocalesDP
     */
    public function testGetSupportedLocales($a, $b)
    {
        $obj = new _Repositories(TEST_FILES);

        $this
            ->array($obj->getSupportedLocales($a))
                ->isEqualTo($b);
    }
}

