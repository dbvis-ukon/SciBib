<?php
namespace App\Test\Fixture;

use Cake\TestSuite\Fixture\TestFixture;

/**
 * AigaiongeneralFixture
 *
 */
class AigaiongeneralFixture extends TestFixture
{

    /**
     * Table name
     *
     * @var string
     */
    public $table = 'aigaiongeneral';

    /**
     * Fields
     *
     * @var array
     */
    // @codingStandardsIgnoreStart
    public $fields = [
        'version' => ['type' => 'string', 'length' => 10, 'null' => false, 'default' => '', 'comment' => '', 'precision' => null, 'fixed' => null],
        'releaseversion' => ['type' => 'string', 'length' => 10, 'null' => false, 'default' => null, 'comment' => '', 'precision' => null, 'fixed' => null],
        '_constraints' => [
            'primary' => ['type' => 'primary', 'columns' => ['version'], 'length' => []],
        ],
        '_options' => [
            'engine' => 'MyISAM',
            'collation' => 'utf8_general_ci'
        ],
    ];
    // @codingStandardsIgnoreEnd

    /**
     * Records
     *
     * @var array
     */
    public $records = [
        [
            'version' => '3eb4c40a-dc91-42ad-a196-70ce9443ed29',
            'releaseversion' => 'Lorem ip'
        ],
    ];
}
