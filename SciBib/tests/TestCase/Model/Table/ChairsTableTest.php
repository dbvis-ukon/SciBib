<?php
namespace App\Test\TestCase\Model\Table;

use App\Model\Table\ChairsTable;
use Cake\ORM\TableRegistry;
use Cake\TestSuite\TestCase;

/**
 * App\Model\Table\ChairsTable Test Case
 */
class ChairsTableTest extends TestCase
{

    /**
     * Test subject
     *
     * @var \App\Model\Table\ChairsTable
     */
    public $Chairs;

    /**
     * Fixtures
     *
     * @var array
     */
    public $fixtures = [
        'app.chairs',
        'app.publications',
        'app.copyrights',
        'app.documents',
        'app.keywords',
        'app.authors',
        'app.authors_publications',
        'app.chairs_publications',
        'app.chair_pub',
        'app.categories',
        'app.categories_publications'
    ];

    /**
     * setUp method
     *
     * @return void
     */
    public function setUp()
    {
        parent::setUp();
        $config = TableRegistry::exists('Chairs') ? [] : ['className' => 'App\Model\Table\ChairsTable'];
        $this->Chairs = TableRegistry::get('Chairs', $config);
    }

    /**
     * tearDown method
     *
     * @return void
     */
    public function tearDown()
    {
        unset($this->Chairs);

        parent::tearDown();
    }

    /**
     * Test initialize method
     *
     * @return void
     */
    public function testInitialize()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }

    /**
     * Test validationDefault method
     *
     * @return void
     */
    public function testValidationDefault()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }
}
