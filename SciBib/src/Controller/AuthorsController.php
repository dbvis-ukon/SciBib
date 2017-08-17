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
 * Authors Controller.
 *
 * @property \App\Model\Table\AuthorsTable $Authors
 */
class AuthorsController extends AppController
{
    //paginator definition
    public $paginate = [
        'limit' => 50,
        'order' => [
            'Authors.surname' => 'asc',
        ],
    ];

    /**
     * The Search.Prg component will allow your filtering
     * forms to be populated using the data in the query params.
     */
    public function initialize()
    {
        parent::initialize();
        $this->loadComponent('Search.Prg', [
            'actions' => ['index'],
        ]);
    }

    /**
     * Index method
     * Show all authors in a list.
     */
    public function index()
    {
        $authors = $this->Authors
                // Use the plugins 'search' custom finder and pass in the
                // processed query params
                ->find('search', $this->Authors->filterParams($this->request->query))
                ->contain(['Publications']);
        //  ->where(['Authors.surname  IS NOT' => null]);
        $this->paginate($authors);

        //setting view variables
        $this->set('authors', $authors);
        $this->set('_serialize', ['authors'], 'title');
    }

    /**
     * View method
     * Show author information with id.
     *
     * @param string|null $id author id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function view($id = null)
    {
        $author = $this->Authors->get($id, [
            'contain' => ['Publications' => [
                    //sort the publications
                    'sort' => ['Publications.year' => 'DESC'],
                ], 'Publications.Authors' => [
                    // this is needed to show the sequence of the authors correctly
                    'sort' => ['AuthorsPublications.position' => 'ASC'],
                ]],
        ]);
        //setting view variables
        $this->set('author', $author);
        $this->set('_serialize', ['author']);
    }

    /**
     * Add method
     * Add a new author to the system.
     */
    public function add()
    {
        $author = $this->Authors->newEntity();
        if ($this->request->is('post')) {
            $author = $this->Authors->patchEntity($author, $this->request->data);
            //generate cleanname
            $cleanname = $this->createCleanname($author->forename, $author->surname);
            //set cleanname
            $author->cleanname = $cleanname;
            if ($this->Authors->save($author)) {
                $this->Flash->success(__('The author has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The author could not be saved. Please, try again.'));
        }
        $this->set(compact('author'));
        $this->set('_serialize', ['author']);
    }

    /**
     * Edit method
     * Edit author information with id.
     *
     * @param string|null $id author id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function edit($id = null)
    {
        $author = $this->Authors->get($id, [
            'contain' => ['Publications'],
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            $author = $this->Authors->patchEntity($author, $this->request->data);
            if ($this->Authors->save($author)) {
                $this->Flash->success(__('The author has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The author could not be saved. Please, try again.'));
        }
        $this->set(compact('author'));
        $this->set('_serialize', ['author']);
    }

    /**
     * Delete method
     * Delete author with id.
     *
     * @param string|null $id author id
     *
     * @return \Cake\Network\Response|null redirects to index
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $author = $this->Authors->get($id);
        if ($this->Authors->delete($author)) {
            $this->Flash->success(__('The author has been deleted.'));
        } else {
            $this->Flash->error(__('The author could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'index']);
    }

    /**
     * Create Cleanname
     * Creates a clean name to show stems forename
     * (from the old bib system).
     *
     *
     * @param string forename
     * @param string surname
     * @param mixed $forename
     * @param mixed $surname
     *
     * @return cleanname of the author
     */
    public function createCleanname($forename, $surname)
    {
        if (!isset($forename) || !isset($surname)) {
            return '';
        }
        if (!is_string($forename) || !is_string($surname)) {
            return '';
        }

        $result = '';

        $hasBlanks = !mb_strpos($forename, ' ') ? false : true;
        $hasDashes = !mb_strpos($forename, '-') ? false : true;

        if (!$hasBlanks && !$hasDashes) {
            $result = $this->shortenToken($forename);
        } else {
            $tokens = explode(' ', $forename);

            for ($i = 0; $i < count($tokens); ++$i) {
                $result .= mb_strpos($tokens[$i], '-') === false ? $this->shortenToken($tokens[$i]) : $this->shortenTokenWithDash($tokens[$i]);
                if ($i < count($tokens) - 1) {
                    $result .= ' ';
                }
            }
        }

        return $result.' '.$surname;
    }

    /**
     * Shortens a token with a dash
     * (from the old bib system).
     *
     * @param string t
     * @param mixed $t
     *
     * @return shortened t
     */
    public function shortenTokenWithDash($t)
    {
        if (!$t || !is_string($t) || mb_strlen($t) <= 1) {
            return $t;
        }
        $result = '';
        $tokens = explode('-', $t);

        for ($i = 0; $i < count($tokens); ++$i) {
            $result .= $this->shortenToken($tokens[$i]);

            if ($i < count($tokens) - 1) {
                $result .= '-';
            }
        }

        return $result;
    }

    /**
     * Shortens a token without a dash
     * (from the old bib system).
     *
     * @param string t
     * @param mixed $t
     *
     * @return shortened t
     */
    public function shortenToken($t)
    {
        if (!$t || !is_string($t) || mb_strlen($t) <= 1) {
            return $t;
        }

        return mb_strtoupper(mb_substr($t, 0, 1)).'.';
    }

    /**
     * Ajax create new author.
     *
     * @return json encoded author
     */
    public function ajaxCreate()
    {
        // create a new author entity
        $author = $this->Authors->newEntity();
        // check if the request is a post
        if ($this->request->is('post')) {
            //stop the view from rendering
            $this->autoRender = false;
            //get forename from query parameters
            $author->forename = $this->request->query('forename');
            //get surname from query parameters
            $author->surname = $this->request->query('surname');
            //generate Cleanname
            $cleanname = $this->createCleanname($author->forename, $author->surname);
            $author->cleanname = $cleanname;
            if ($this->Authors->save($author)) {
                //if authors could be saved return the author as a json object
                echo json_encode($this->jsonSerialize($author));
            } else {
                // return the json error
                echo json_encode(['error' => $this->Author->validationErrors]);
            }
        }
    }

    /**
     * Create json object for author.
     *
     * @param object author
     * @param mixed $author
     *
     * @return json object of author
     */
    public function jsonSerialize($author)
    {
        return [
            'id' => $author->id,
            'forename' => $author->forename,
            'surname' => $author->surname,
            'cleanname' => $author->cleanname,
        ];
    }
}
