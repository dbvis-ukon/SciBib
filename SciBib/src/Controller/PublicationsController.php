<?php

/*
 *
 *     Copyright {2017} {University Konstanz -  Data Analysis and Visualization Group}
 *
 *     Licensed under the Apache License, Version 2.0 (the "License");
 *     you may not use this file except in compliance with the License.
 *     You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0
 *
 *     Unless required by applicable law or agreed to in writing, software
 *     distributed under the License is distributed on an "AS IS" BASIS,
 *     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *     See the License for the specific language governing permissions and
 *     limitations under the License.
 *
 */

namespace App\Controller;


/**
 * Publications Controller.
 *
 * @property \App\Model\Table\PublicationsTable $Publications
 */
class PublicationsController extends AppController
{
    // Paginator for the publications
    public $paginate = [
        'limit' => 100000,
        'order' => [
            'Publications.year' => 'desc',
            'Publications.created' => 'desc',
        ],
    ];

    public function initialize()
    {
        parent::initialize();
        //add the search to the index of the publications
        $this->loadComponent('Search.Prg', [
            'actions' => ['index', 'privateIndex'],
        ]);
    }

    /**
     * Private index method
     * To show all publications with title only and options to edit or delete.
     */
    public function privateIndex()
    {
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
                        'fields' => ['id', 'title', 'year', 'kops'],
            ]));
        }
        //setting view variables
        $this->set('authors', $resultAuthors);
        $this->set('publications', $result);
        $this->set('_serialize', ['publications']);
    }

    /**
     * View method.
     *
     * @param string|null $id publication id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function view($id = null)
    {
        $this->viewBuilder()->layout('view');

        $publication = $this->Publications->get($id, [
            'contain' => ['Authors' => [
                    'sort' => ['AuthorsPublications.position' => 'ASC'],
                ], 'Categories', 'Documents', 'Keywords'],
        ]);

        //show related publications of the first and second author
        $firstAuthor = $publication->authors[0];
        $secondAuthor = isset($publication->authors[1]) ? $publication->authors[1] : null;

        //related publications
        if (isset($secondAuthor)) {
            $relatedPublications = $this->Publications->find('all', [
                        'contain' => ['Authors' => [
                                'sort' => ['AuthorsPublications.position' => 'ASC'],
                            ], 'AuthorsPublications'],
                        'order' => [
                            'Publications.year' => 'desc',
                            'Publications.created' => 'desc',
                        ],
                    ])
                    //load only authors with the specify id
                ->matching('AuthorsPublications')
                ->where([
                    'AuthorsPublications.author_id ' => $firstAuthor['id'],
                ])
                ->where([
                    'AuthorsPublications.author_id ' => $secondAuthor['id'],
                ])
                ->limit(5);
        } else {
            $relatedPublications = $this->Publications->find('all', [
                        'contain' => ['Authors' => [
                                'sort' => ['AuthorsPublications.position' => 'ASC'],
                            ], 'AuthorsPublications'],
                        'order' => [
                            'Publications.year' => 'desc',
                            'Publications.created' => 'desc',
                        ],
                    ])
                    //load only authors with the specify id
                ->matching('AuthorsPublications')
                ->where([
                    'AuthorsPublications.author_id ' => $firstAuthor['id'],
                ])
                ->limit(5);
        }

        //setting view variables
        $this->set('publication', $publication);
        $this->set('relatedPublications', $relatedPublications);
        $this->set('_serialize', ['publication', 'relatedPublications']);
    }

    private function _removeType($data, $delete = false) {
        foreach ($data as $key => $value) {
            if (is_array($value)) {
                $data[$key] = $this->_removeType($data[$key], true);
            }
            if ($delete && $key === 'type') {
                unset($data[$key]);
            }
        }
        return $data;
    }

    /**
     * Add method.
     */
    public function add()
    {
        $publication = $this->Publications->newEntity();

        //the user submitted a form with data
        if ($this->request->is('post')) {
            // get the data
            $data = $this->request->data;
            // set documents and mainfile
            $data['documents'] = [];

            $name = substr($data['file'], 0, strpos($data['file'], '['));
            $pos = substr($data['file'], strpos($data['file'], '[') + 1, 1);
            if (isset($data[$name][(int) $pos]['name']) && $data[$name][(int) $pos]['name'] !== '') {
                $data['mainfile'] = $data[$name][(int) $pos];
            } else {
                $data['mainfile'] = '';
            }

            foreach ($data[$name] as $tmp) {
                if (isset($tmp['name']) && $tmp['name'] !== '') {
                    $document = [];
                    $document['filename'] = $tmp;
                    $document['visible'] = true;
                    $document['public'] = true;
                    $document['remote'] = false;
                    array_push($data['documents'], $document);
                }
            }

            foreach ($data['external'] as $tmp) {
                $document = [];
                $document['filename'] = $tmp;
                $document['visible'] = true;
                $document['public'] = true;
                $document['remote'] = true;
                array_push($data['documents'], $document);
            }

            // delete the authors input
            $data['authors'] = [];
            // get the authorsPosition hidden input
            // split the string, this results in an array
            // e.g. [[id,position],[id,position],....]
            $authorsPositions = explode(';', $data['authorsPosition']);
            // transform it to the form CakePHP needs it to be
            foreach ($authorsPositions as $tmp) {
                $author = [];
                if ($tmp) {
                    //split the string id,position
                    $tmp = explode(',', $tmp);
                    $author['id'] = $tmp[0];
                    $author['_joinData'] = ['position' => $tmp[1]];
                    //add the stuff to the authors array
                    array_push($data['authors'], $author);
                }
            }

            $data = $this->_removeType($data);
            $publication = $this->Publications->patchEntity($publication, $data);

            if ($this->Publications->save($publication)) {
                $this->Flash->success(__('The publication has been saved.'));

                return $this->redirect(['action' => 'private-index']);
            }
            $this->Flash->error(__('The publication could not be saved. Please, try again.'));
        }

        // a new publication will be created
        $copyrights = $this->Publications->Copyrights->find('list', ['limit' => 200]);
        $authors = $this->Publications->Authors->find('list', ['keyField' => 'id',
            'valueField' => 'cleanname', ]);
        // Categories are prepared for the later tree multiselect view
        $tmp = $this->Publications->Categories->find(
            'treelist',
            [
                    'valuePath' => 'name',
                    'spacer' => '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', ]
                )->toArray();
        $categories = $this->Publications->Categories->find('all', [
            'order' => ['Categories.lft'], ]);
        // get the long name for the categories
        foreach ($categories as $value) {
            $value->longName = $tmp[$value->id];
        }
        // Types of publications
        $optionsType = ['Article' => 'Article', 'Book' => 'Book', 'Booklet' => 'Booklet',
            'Conference' => 'Conference', 'Inbook' => 'Inbook', 'Incollection' => 'Incollection',
            'Inproceedings' => 'Inproceedings', 'Manual' => 'Manual', 'Masterthesis' => 'Masterthesis', 'Misc' => 'Misc',
            'PhDThesis' => 'PhDThesis', 'Proceedings' => 'Proceedings', 'Techreport' => 'Techreport',
            'Unpublished' => 'Unpublished', ];
        // get chairs
        $chair = $this->Publications->Chairs->find('list', ['keyField' => 'id',
            'valueField' => 'name', ]);
        // get keywords
        $keywords = $this->Publications->Keywords->find('list', ['keyField' => 'id',
            'valueField' => 'name', ]);
        // setting view variables
        $this->set(compact('publication', 'copyrights', 'authors', 'categories', 'chair', 'optionsType', 'keywords'));
        $this->set('_serialize', ['publication']);
    }

    /**
     * Edit method.
     *
     * @param string|null $id publication id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function edit($id = null)
    {
        $publication = $this->Publications->get($id, [
            'contain' => ['Authors' => [
                    //needed so that the authros are in the right ordering
                    'sort' => ['AuthorsPublications.position' => 'ASC'],
                ], 'Categories', 'Chairs', 'Documents'],
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            // get the data
            $data = $this->request->data;

            // set documents and mainfile
            $data['documents'] = [];
            $name = substr($data['file'], 0, strpos($data['file'], '['));
            $pos = substr($data['file'], strpos($data['file'], '[') + 1, 1);
            if (isset($data[$name][(int) $pos]['name']) && $data[$name][(int) $pos]['name'] !== '') {
                $data['mainfile'] = $data[$name][(int) $pos];
            }

            foreach ($data[$name] as $tmp) {
                if (isset($tmp['name']) && $tmp['name'] !== '') {
                    $document = [];
                    $document['filename'] = $tmp;
                    $document['visible'] = true;
                    $document['public'] = true;
                    $document['remote'] = false;
                    array_push($data['documents'], $document);
                }
            }

            if (isset($data['external'])) {
                foreach ($data['external'] as $tmp) {
                    if (isset($tmp) && $tmp !== '') {

                        $skip = true;
                        foreach ($publication['documents'] as $doc) {
                            if ($doc['filename'] === $tmp) {
                                break;
                            }
                        }
                        if ($skip) {
                            continue;
                        }

                        $document = [];
                        $document['filename'] = $tmp;
                        $document['visible'] = true;
                        $document['public'] = true;
                        $document['remote'] = true;
                        array_push($data['documents'], $document);
                    }
                }
            }

            // delete the authors input
            $data['authors'] = [];
            // get the authorsPosition hidden input
            // split the string, this results in an array
            // e.g. [[id,position],[id,position],....]
            $authorsPositions = explode(';', $data['authorsPosition']);
            // transform it to the form CakePHP needs it to be
            foreach ($authorsPositions as $tmp) {
                $author = [];
                if ($tmp) {
                    //split the string id,position
                    $tmp = explode(',', $tmp);
                    $author['id'] = $tmp[0];
                    $author['_joinData'] = ['position' => $tmp[1]];
                    //add the stuff to the authors array
                    array_push($data['authors'], $author);
                }
            }

            $data = $this->_removeType($data);
            $publication = $this->Publications->patchEntity($publication, $data);
            if ($this->Publications->save($publication)) {
                $this->Flash->success(__('The publication has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The publication could not be saved. Please, try again.'));
        }
        //a new publication will be created
        $copyrights = $this->Publications->Copyrights->find('list', ['limit' => 200]);
        // get authors
        $authors = $this->Publications->Authors->find('list', ['keyField' => 'id',
            'valueField' => 'cleanname', ]);
        // Categories are prepared for the later tree multiselect view
        $tmp = $this->Publications->Categories->find(
            'treelist',
            [
                    'valuePath' => 'name',
                    'spacer' => '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', ]
                )->toArray();
        $categories = $this->Publications->Categories->find('all', [
            'order' => ['Categories.lft'], ]);
        // get the long name for the categories
        foreach ($categories as $value) {
            $value->longName = $tmp[$value->id];
        }
        // Types of publications
        $optionsType = ['Article' => 'Article', 'Book' => 'Book', 'Booklet' => 'Booklet',
            'Conference' => 'Conference', 'Inbook' => 'Inbook', 'Incollection' => 'Incollection',
            'Inproceedings' => 'Inproceedings', 'Manual' => 'Manual', 'Masterthesis' => 'Masterthesis', 'Misc' => 'Misc',
            'PhDThesis' => 'PhDThesis', 'Proceedings' => 'Proceedings', 'Techreport' => 'Techreport',
            'Unpublished' => 'Unpublished', ];
        // get chairs
        $chairs = $this->Publications->Chairs->find('list', ['keyField' => 'id',
            'valueField' => 'name', ]);
        // get keywords
        $keywords = $this->Publications->Keywords->find('list', ['keyField' => 'id',
            'valueField' => 'name', ]);
        //setting view variables
        $this->set(compact('publication', 'copyrights', 'authors', 'categories', 'chairs', 'optionsType', 'keywords'));
        $this->set('_serialize', ['publication']);
    }

    /**
     * Delete method.
     *
     * @param string|null $id publication id
     *
     * @return \Cake\Network\Response|null redirects to index
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $publication = $this->Publications->get($id);
        if ($this->Publications->delete($publication)) {
            $this->Flash->success(__('The publication has been deleted.'));
        } else {
            $this->Flash->error(__('The publication could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'private-index']);
    }

    /**
     * Public index method.
     */
    public function Index()
    {
        $this->viewBuilder()->layout('index');

        $information = $this->getInformation();

        //setting view variables
        $this->set('hideFilterHeader', $information[1]);
        $this->set('publications', $information[0]);
        $this->set('isEmbedded', $this->isEmbedded());
    }

    /**
     * Public tojson method.
     */
    public function tojson()
    {
        $this->viewBuilder()->layout('ajax');

        $information = $this->getInformation();

        //setting view variables
        $this->set(['publications' => $information[0],
            '_serialize' => ['publications'], ]);
    }

    /**
     * Public tobibtex method.
     */
    public function tobibtex()
    {
        $this->viewBuilder()->layout('ajax');

        $information = $this->getInformation();

        //setting view variables
        $this->set('publications', $information[0]);
    }

    /**
     * Public bibtex method.
     */
    public function bibtex($id = null)
    {
        $this->viewBuilder()->layout('ajax');

        $publication = $this->Publications->get($id, [
            'contain' => ['Copyrights', 'Authors' => [
                    'sort' => ['AuthorsPublications.position' => 'ASC'],
                ], 'Categories', 'Documents', 'Keywords'],
        ]);
        //setting view variables
        $this->set('publication', $publication);
    }

    /**
     * Private getInformation method
     * sub method to filter publications and hide header.
     *
     * @return array containing 0: results for query 1: hide header
     */
    private function getInformation()
    {
        // get all publications
        $result = $this->paginate($this->Publications->find(
            'all',
            [
                'contain' => [
                    'Authors' => [
                          'sort' => ['AuthorsPublications.position' => 'ASC'],
                      ],
                    'Categories',
                    'Documents',
                    'Chairs',
                ],
            ]
        ));

        // remove non public
        $result = $result->filter(function ($publication) {
            return $publication->public;
        });

        // filter year
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

        // filter header
        $hideHeader = false;
        if ($this->request->query('hide')) {
            $hideHeader = true;
        }

        // filter type
        if ($this->request->query('type')) {
            // Other option
            if ($this->request->query('type') === 'other') {
                $result = $result->filter(function ($publication) {
                    return $publication->type === 'Booklet' ||
                          $publication->type === 'Conference' ||
                          $publication->type === 'Incollection' ||
                          $publication->type === 'Manual' ||
                          $publication->type === 'Masterthesis' ||
                          $publication->type === 'Misc' ||
                          $publication->type === 'PhDThesis' ||
                          $publication->type === 'Proceedings' ||
                          $publication->type === 'Techreport' ||
                          $publication->type === 'Unpublished';
                });
            } else {
                $result = $result->filter(function ($publication) {
                    return strcasecmp($publication->type, $this->request->query('type')) === 0;
                });
            }
        }

        // filter author
        if ($this->request->query('author')) {
            $result = $result->filter(function ($publication) {
                if (strpos($this->request->query('author'), ",") >= 0) {
                    $authors_query = explode(",", $this->request->query('author'));
                } else {
                    $authors_query = array($this->request->query('author'));
                }

                foreach ($publication->authors as $author) {
                    foreach ($authors_query as $author_query) {
                        if ($author->id === (int) $author_query) {
                            return true;
                        }
                    }
                }

                return false;
            });
        }

        // filter category
        if ($this->request->query('category')) {
            $result = $result->filter(function ($publication) {
                if (strpos($this->request->query('category'), ",") >= 0) {
                    $categories_query = explode(",", $this->request->query('category'));
                } else {
                    $categories_query = array($this->request->query('category'));
                }

                foreach ($publication->categories as $category) {
                    foreach ($categories_query as $category_query) {
                        if ($category->id === (int) $category_query) {
                            return true;
                        }
                    }
                }

                return false;
            });
        }

        // filter chairs
        if ($this->request->query('chairs')) {
            $result = $result->filter(function ($publication) {
                if (strpos($this->request->query('chairs'), ",") >= 0) {
                    $chairs_query = explode(",", $this->request->query('chairs'));
                } else {
                    $chairs_query = array($this->request->query('chairs'));
                }

                foreach ($publication->chairs as $chair) {
                    foreach ($chairs_query as $chair_query) {
                        if ($chair->id === (int) $chair_query) {
                            return true;
                        }
                    }
                }

                return false;
            });
        }

        // filter by kops
        if ($this->request->query('filterByKops')) {
            $result = $result->filter(function ($publication) {
                return $publication->kops;
            });
        }

        return [$result, $hideHeader];
    }

    private function isEmbedded()
    {
        //global $_SERVER, $embeddedHosts;

        $result = [];

        /* Add an entry for each remote host here. Each array has to have the following entries:
          baseurl: A full, non-relative URL that is used as the base for links
          linkstyle: Determines how filter links work. 'embedded' tries to embed filters in the remote host. If that is not working, use 'phonehome'
          cssfile: The CSS file to be used specifically for this host
          utf8compatible: Should be set to true if the host webpage is UTF8, otherwise to false

          Add an array under a given host ip to support more than one clients per host ip. The keys of the ips
          are used to identify the embedded settings. In the request, the User-Agent header is used as the embedded
          tag.
         */
        $embeddedHosts = [
            '134.34.240.76' => [
                'baseurl' => 'https://www.vis.uni-konstanz.de/publikationen/',
                'linkstyle' => 'embedded',
                'cssfile' => '',
                'utf8compatible' => true,
            ],
            '10.0.0.11' => [
                'TextVisualization' => [
                    'baseurl' => 'http://research.dbvis.de/',
                    'linkstyle' => 'embedded',
                    'cssfile' => '',
                    'utf8compatible' => true,
                ],
            ],
        ];

        $curClient = false;

        $result['isEmbedded'] = false;

        // search for the ip (proxied or direct request)
        if (array_key_exists('HTTP_X_FORWARDED_FOR', $_SERVER)) {
            $curClient = $_SERVER['HTTP_X_FORWARDED_FOR'];
            $result['isEmbedded'] = array_key_exists($curClient, $embeddedHosts);
        } elseif (array_key_exists('REMOTE_ADDR', $_SERVER)) {
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
