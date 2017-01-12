<?php
namespace App\Test\Fixture;

use Cake\TestSuite\Fixture\TestFixture;

/**
 * RightsprofilerightlinkFixture
 *
 */
class RightsprofilerightlinkFixture extends TestFixture
{

    /**
     * Table name
     *
     * @var string
     */
    public $table = 'rightsprofilerightlink';

    /**
     * Fields
     *
     * @var array
     */
    // @codingStandardsIgnoreStart
    public $fields = [
        'rightsprofile_id' => ['type' => 'integer', 'length' => 10, 'unsigned' => false, 'null' => false, 'default' => null, 'comment' => '', 'precision' => null, 'autoIncrement' => null],
        'right_name' => ['type' => 'string', 'length' => 20, 'null' => false, 'default' => null, 'comment' => '', 'precision' => null, 'fixed' => null],
        '_constraints' => [
            'primary' => ['type' => 'primary', 'columns' => ['rightsprofile_id', 'right_name'], 'length' => []],
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
            'rightsprofile_id' => 1,
            'right_name' => 'c2338890-6018-42dc-adb6-aaaabc463fc4'
        ],
    ];
}
