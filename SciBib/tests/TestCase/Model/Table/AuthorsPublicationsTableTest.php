<?php
namespace App\Test\TestCase\Model\Table;

use App\Model\Table\AuthorsPublicationsTable;
use Cake\ORM\TableRegistry;
use Cake\TestSuite\TestCase;

/**
 * App\Model\Table\AuthorsPublicationsTable Test Case
 */
class AuthorsPublicationsTableTest extends TestCase
{

    /**
     * Test subject
     *
     * @var \App\Model\Table\AuthorsPublicationsTable
     */
    public $AuthorsPublications;

    /**
     * Fixtures
     *
     * @var array
     */
    public $fixtures = [
        'app.authors_publications',
        'app.authors',
        'app.publications',
        'app.copyrights',
        'app.documents',
        'app.keywords',
        'app.chairs',
        'app.chairs_publications',
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
        $config = TableRegistry::exists('AuthorsPublications') ? [] : ['className' => 'App\Model\Table\AuthorsPublicationsTable'];
        $this->AuthorsPublications = TableRegistry::get('AuthorsPublications', $config);
    }

    /**
     * tearDown method
     *
     * @return void
     */
    public function tearDown()
    {
        unset($this->AuthorsPublications);

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

    /**
     * Test buildRules method
     *
     * @return void
     */
    public function testBuildRules()
    {
        $this->markTestIncomplete('Not implemented yet.');
    }
}
