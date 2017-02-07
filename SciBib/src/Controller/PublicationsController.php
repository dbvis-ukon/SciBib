<?php

namespace App\Controller;

use Cake\View\Helper;
use App\Controller\AppController;
use Cake\Core\Configure;

/**
 * Publications Controller
 *
 * @property \App\Model\Table\PublicationsTable $Publications
 */
class PublicationsController extends AppController {

    public function initialize() {
        parent::initialize();
        //add the search to the index of the publications
        $this->loadComponent('Search.Prg', [
            'actions' => ['index', 'privateIndex']
        ]);
    }

    // Paginator for the publications
    public $paginate = [
        'limit' => 100000,
        'order' => [
            'Publications.year' => 'desc',
            'Publications.created' => 'desc'
        ]
    ];

    /**
     * Private index method
     * To show all publications with title only and options to edit or delete
     *
     * @return void
     */
    public function privateIndex() {
        //the result of the search
        $result = [];
        //resulting authors
        $resultAuthors = [];
        //check if there is a request
        if ($this->request->query('q')) {
            //check  the input string against every forename and surname
            $queryAuthor = $this->Publications->Authors
                    ->find('search', $this->Publications->filterParams($this->request->query))
                    ->contain(['Publications']);
            // if the query for the authors is not empty and there are authors
            // with that name
            if (0 !== $queryAuthor->count()) {
                // for every author found
                foreach ($queryAuthor as $author) {
                    $resultAuthors = array_merge($resultAuthors, [$author]);
                }
            }
            //check the input string agains every publication title and year
            $query = $this->Publications
                    ->find('search', $this->Publications->filterParams($this->request->query));
            $result = $this->paginate($query);
        } else {
            //no search input - just show the regular Publications
            $result = $this->paginate($this->Publications->find('all', [
                        'fields' => ['id', 'title', 'year', 'kops']
            ]));
        }
        //setting view variables
        $this->set('authors', $resultAuthors);
        $this->set('publications', $result);
        $this->set('_serialize', ['publications']);
    }

    /**
     * View method
     *
     * @param string|null $id Publication id.
     * @return void
     * @throws \Cake\Network\Exception\NotFoundException When record not found.
     */
    public function view($id = null) {
        $publication = $this->Publications->get($id, [
            'contain' => ['Authors' => [
                    'sort' => ['AuthorsPublications.position' => 'ASC']
                ], 'Categories', 'Documents', 'Keywords']
        ]);
        //show related publications of the first and second author
        $firstAuthor = $publication->authors[0];
        $secondAuthor = $publication->authors[0];
        //related publications
        $relatedPublications = $this->Publications->find('all', [
                    'contain' => ['Authors' => [
                            'sort' => ['AuthorsPublications.position' => 'ASC']
                        ], 'AuthorsPublications'],
                    'order' => [
                        'Publications.year' => 'desc',
                        'Publications.created' => 'desc'
                    ]
                ])
                //load only authors with the specify id
                ->matching('AuthorsPublications')
                ->where([
                    'AuthorsPublications.author_id ' => $firstAuthor['id']
                ])
                ->where([
                    'AuthorsPublications.author_id ' => $secondAuthor['id']
                ])
                //show only 5 pubications
                ->limit(5);
        //setting view variables
        $this->set('publication', $publication);
        $this->set('relatedPublications', $relatedPublications);
        $this->set('_serialize', ['publication', 'relatedPublications']);
    }

    /**
     * Add method
     *
     * @return void Redirects on successful add, renders view otherwise.
     */
    public function add() {

        $publication = $this->Publications->newEntity();

        //the user submitted a form with data
        if ($this->request->is('post')) {
            // get the data
            $data = $this->request->data;
            // delete the authors input
            $data['authors'] = [];
            // get the authorsPosition hidden input
            // split the string, this results in an array
            // e.g. [[id,position],[id,position],....]
            $authorsPositions = explode(";", $data['authorsPosition']);
            // transform it to the form CakePHP needs it to be
            foreach ($authorsPositions as $tmp) {
                $author = [];
                if ($tmp) {
                    //split the string id,position
                    $tmp = explode(",", $tmp);
                    $author['id'] = $tmp[0];
                    $author['_joinData'] = ['position' => $tmp[1]];
                    //add the stuff to the authors array
                    array_push($data['authors'], $author);
                }
            }
            $publication = $this->Publications->patchEntity($publication, $data);
            if ($this->Publications->save($publication)) {
                $this->Flash->success(__('The publication has been saved.'));
                return $this->redirect(['action' => 'index']);
            } else {
                $this->Flash->error(__('The publication could not be saved. Please, try again.'));
            }
        }

        // a new publication will be created
        $copyrights = $this->Publications->Copyrights->find('list', ['limit' => 200]);
        $authors = $this->Publications->Authors->find('list', ['keyField' => 'id',
            'valueField' => 'cleanname']);
        // Categories are prepared for the later tree multiselect view
        $tmp = $this->Publications->Categories->find('treelist', [
                    'valuePath' => 'name',
                    'spacer' => '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;']
                )->toArray();
        $categories = $this->Publications->Categories->find('all', [
            'order' => ['Categories.lft']]);
        // get the long name for the categories
        foreach ($categories as $value) {
            $value->longName = $tmp[$value->id];
        }
        // Types of publications
        $optionsType = ['Article' => 'Article', 'Book' => 'Book', 'Booklet' => 'Booklet',
            'Conference' => 'Conference', 'Inbook' => 'Inbook', 'Incollection' => 'Incollection',
            'Inproceedings' => 'Inproceedings', 'Manual' => 'Manual', 'Masterthesis' => 'Masterthesis', 'Misc' => 'Misc',
            'PhDThesis' => 'PhDThesis', 'Proceedings' => 'Proceedings', 'Techreport' => 'Techreport',
            'Unpublished' => 'Unpublished'];
        // get chairs
        $chair = $this->Publications->Chairs->find('list', ['keyField' => 'id',
            'valueField' => 'name']);
        // get keywords
        $keywords = $this->Publications->Keywords->find('list', ['keyField' => 'id',
            'valueField' => 'name']);
        // setting view variables
        $this->set(compact('publication', 'copyrights', 'authors', 'categories', 'chair', 'optionsType', 'keywords'));
        $this->set('_serialize', ['publication']);
    }

    /**
     * Edit method
     *
     * @param string|null $id Publication id.
     * @return void Redirects on successful edit, renders view otherwise.
     * @throws \Cake\Network\Exception\NotFoundException When record not found.
     */
    public function edit($id = null) {
        $publication = $this->Publications->get($id, [
            'contain' => ['Authors' => [
                    //needed so that the authros are in the right ordering
                    'sort' => ['AuthorsPublications.position' => 'ASC']
                ], 'Categories', 'ChairPub']
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
                        // get the data
            $data = $this->request->data;
            // delete the authors input
            $data['authors'] = [];
            // get the authorsPosition hidden input
            // split the string, this results in an array
            // e.g. [[id,position],[id,position],....]
            $authorsPositions = explode(";", $data['authorsPosition']);
            // transform it to the form CakePHP needs it to be
            foreach ($authorsPositions as $tmp) {
                $author = [];
                if ($tmp) {
                    //split the string id,position
                    $tmp = explode(",", $tmp);
                    $author['id'] = $tmp[0];
                    $author['_joinData'] = ['position' => $tmp[1]];
                    //add the stuff to the authors array
                    array_push($data['authors'], $author);
                }
            }
            $publication = $this->Publications->patchEntity($publication, $data);
            if ($this->Publications->save($publication)) {
                $this->Flash->success(__('The publication has been saved.'));
                return $this->redirect(['action' => 'index']);
            } else {
                $this->Flash->error(__('The publication could not be saved. Please, try again.'));
            }            
        }
        //a new publication will be created
        $copyrights = $this->Publications->Copyrights->find('list', ['limit' => 200]);
        // get authors
        $authors = $this->Publications->Authors->find('list', ['keyField' => 'id',
            'valueField' => 'cleanname']);
        // Categories are prepared for the later tree multiselect view
        $tmp = $this->Publications->Categories->find('treelist', [
                    'valuePath' => 'name',
                    'spacer' => '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;']
                )->toArray();
        $categories = $this->Publications->Categories->find('all', [
            'order' => ['Categories.lft']]);
        // get the long name for the categories
        foreach ($categories as $value) {
            $value->longName = $tmp[$value->id];
        }
        // Types of publications
        $optionsType = ['Article' => 'Article', 'Book' => 'Book', 'Booklet' => 'Booklet',
            'Conference' => 'Conference', 'Inbook' => 'Inbook', 'Incollection' => 'Incollection',
            'Inproceedings' => 'Inproceedings', 'Manual' => 'Manual', 'Masterthesis' => 'Masterthesis', 'Misc' => 'Misc',
            'PhDThesis' => 'PhDThesis', 'Proceedings' => 'Proceedings', 'Techreport' => 'Techreport',
            'Unpublished' => 'Unpublished'];
        // get chairs
        $chair = $this->Publications->Chairs->find('list', ['keyField' => 'id',
            'valueField' => 'name']);
        // get keywords
        $keywords = $this->Publications->Keywords->find('list', ['keyField' => 'id',
            'valueField' => 'name']);
        //setting view variables
        $this->set(compact('publication', 'copyrights', 'authors', 'categories', 'chair', 'optionsType', 'keywords'));
        $this->set('_serialize', ['publication']);
    }

    /**
     * Delete method
     *
     * @param string|null $id Publication id.
     * @return \Cake\Network\Response|null Redirects to index.
     * @throws \Cake\Network\Exception\NotFoundException When record not found.
     */
    public function delete($id = null) {
        $this->request->allowMethod(['post', 'delete']);
        $publication = $this->Publications->get($id);
        if ($this->Publications->delete($publication)) {
            $this->Flash->success(__('The publication has been deleted.'));
        } else {
            $this->Flash->error(__('The publication could not be deleted. Please, try again.'));
        }
        return $this->redirect(['action' => 'index']);
    }

    /**
     * Public index method
     *
     * @return void
     */
    public function Index() {

        // get all publications
        $result = $this->paginate($this->Publications->find('all', [
                    'contain' => ['Authors' => [
                            'sort' => ['AuthorsPublications.position' => 'ASC']
                        ], 'Categories']
                        ]
        ));
        //filter year
        if ($this->request->query('year')) {
            if ($this->request->query('year') === 'lastTwoYears') {
                $result = $result->filter(function ($publication) {
                    return $publication->year >= (date('Y') - 1);
                });
            } else {
                $result = $result->filter(function ($publication) {
                    return $publication->year === $this->request->query('year');
                });
            }
        }
        //filter header
        $hideHeader = false;
        if ($this->request->query('hide')) {
            $hideHeader = true;
        }
        //filter type 
        if ($this->request->query('type')) {
            //Other option
            if ($this->request->query('type') === 'other') {
                $result = $result->filter(function ($publication) {
                    return ($publication->type === "Booklet" ||
                            $publication->type === "Conference" ||
                            $publication->type === "Incollection" ||
                            $publication->type === "Manual" ||
                            $publication->type === "Masterthesis" ||
                            $publication->type === "Misc" ||
                            $publication->type === "PhDThesis" ||
                            $publication->type === "Proceedings" ||
                            $publication->type === "Techreport" ||
                            $publication->type === "Unpublished" );
                });
            } else {
                $result = $result->filter(function ($publication) {
                    return strcasecmp($publication->type, $this->request->query('type')) == 0;
                });
            }
        }
        //filter author
        if ($this->request->query('author')) {
            $result = $result->filter(function ($publication) {
                foreach ($publication->authors as $author) {
                    if ($author->id === (int) $this->request->query('author')) {
                        return true;
                    }
                }
                return false;
            });
        }
        //filter category
        if ($this->request->query('category')) {
            $result = $result->filter(function ($publication) {
                foreach ($publication->categories as $category) {
                    if ($category->id === (int) $this->request->query('category')) {
                        return true;
                    }
                }
                return false;
            });
        }
        //filter by kops
        if ($this->request->query('filterByKops')) {
            $result = $result->filter(function ($publication) {
                return $publication->kops;
            });
        }
        //setting view variables
        $this->set('hideFilterHeader', $hideHeader);
        $this->set('publications', $result);
        $this->set('isEmbedded', $this->isEmbedded());
    }

    public function bibtex($id = null) {

        $this->viewBuilder()->layout('ajax');

        $publication = $this->Publications->get($id, [
            'contain' => ['Copyrights', 'Authors' => [
                    'sort' => ['AuthorsPublications.position' => 'ASC']
                ], 'Categories', 'Documents', 'Keywords']
        ]);
        //setting view variables
        $this->set('publication', $publication);
        $this->set('_serialize', ['publication']);
    }

    private function isEmbedded() {
        //global $_SERVER, $embeddedHosts;

        $result = array();

        /* Add an entry for each remote host here. Each array has to have the following entries:
          baseurl: A full, non-relative URL that is used as the base for links
          linkstyle: Determines how filter links work. 'embedded' tries to embed filters in the remote host. If that is not working, use 'phonehome'
          cssfile: The CSS file to be used specifically for this host
          utf8compatible: Should be set to true if the host webpage is UTF8, otherwise to false

          Add an array under a given host ip to support more than one clients per host ip. The keys of the ips
          are used to identify the embedded settings. In the request, the User-Agent header is used as the embedded
          tag.
         */
        $embeddedHosts = array(
            '134.34.240.76' => array(
                'baseurl' => 'https://www.vis.uni-konstanz.de/publikationen/',
                'linkstyle' => 'embedded',
                'cssfile' => '',
                'utf8compatible' => true
            ),
            '10.0.0.11' => array(
                'TextVisualization' => array(
                    'baseurl' => 'http://research.dbvis.de/',
                    'linkstyle' => 'embedded',
                    'cssfile' => '',
                    'utf8compatible' => true,
                )
            )
        );

        $curClient = false;

        $result['isEmbedded'] = false;

        // search for the ip (proxied or direct request)
        if (array_key_exists('HTTP_X_FORWARDED_FOR', $_SERVER)) {
            $curClient = $_SERVER['HTTP_X_FORWARDED_FOR'];
            $result['isEmbedded'] = array_key_exists($curClient, $embeddedHosts);
        } else if (array_key_exists('REMOTE_ADDR', $_SERVER)) {
            $curClient = $_SERVER['REMOTE_ADDR'];
            $result['isEmbedded'] = array_key_exists($curClient, $embeddedHosts);
        }

        $result['hostIsUTF8Compatible'] = true;

        //search for a result with tags
        if ($result['isEmbedded']) {
            $curHost = $embeddedHosts[$curClient];
            if (is_array($curHost) && array_key_exists('baseurl', $curHost)) {
                $result['embeddedBaseURL'] = $embeddedHosts[$curClient]['baseurl'];
                $result['embeddedLinkStyle'] = $embeddedHosts[$curClient]['linkstyle'];
                $result['embeddedCSSFile'] = $embeddedHosts[$curClient]['cssfile'];
                $result['hostIsUTF8Compatible'] = $embeddedHosts[$curClient]['utf8compatible'];
            } else {
                $tag = $_SERVER['HTTP_USER_AGENT'];
                if (empty($tag) || !array_key_exists($tag, $curHost)) {
                    // failed extracting tag, fallback to non embedded mode
                    $result = null;
                } else {
                    $curHost = $curHost[$tag];
                    $result['embeddedBaseURL'] = $curHost['baseurl'];
                    $result['embeddedLinkStyle'] = $curHost['linkstyle'];
                    $result['embeddedCSSFile'] = $curHost['cssfile'];
                    $result['hostIsUTF8Compatible'] = $curHost['utf8compatible'];
                }
            }
        }

        return $result;
    }

}
