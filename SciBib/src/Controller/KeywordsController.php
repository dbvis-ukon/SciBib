<?php

/** Copyright {2017} {University Konstanz -  Data Analysis and Visualization Group}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
**/

namespace App\Controller;

use App\Controller\AppController;

/**
 * Keywords Controller
 *
 * @property \App\Model\Table\KeywordsTable $Keywords
 */
class KeywordsController extends AppController {

    /**
     * Index method
     *
     * @return void
     */
    public function index() {
        $this->paginate = [
            'limit' => 100,
            'contain' => ['Publications'],
            'order' => [
                'Keywords.name' => 'asc'
            ]
        ];
        //setting view variables
        $this->set('keywords', $this->paginate($this->Keywords));
        $this->set('_serialize', ['keywords']);
    }

    /**
     * Edit method
     *
     * @param string|null $id Keyword id.
     * @return void Redirects on successful edit, renders view otherwise.
     * @throws \Cake\Network\Exception\NotFoundException When record not found.
     */
    public function edit($id = null) {
        $keyword = $this->Keywords->get($id, [
            'contain' => []
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            $keyword = $this->Keywords->patchEntity($keyword, $this->request->data);
            if ($this->Keywords->save($keyword)) {
                $this->Flash->success(__('The keyword has been saved.'));
                return $this->redirect(['action' => 'index']);
            } else {
                $this->Flash->error(__('The keyword could not be saved. Please, try again.'));
            }
        }
        //setting view variables
        $this->set(compact('keyword'));
        $this->set('_serialize', ['keyword']);
    }

    /**
     * Delete method
     *
     * @param string|null $id Keyword id.
     * @return \Cake\Network\Response|null Redirects to index.
     * @throws \Cake\Network\Exception\NotFoundException When record not found.
     */
    public function delete($id = null) {
        $this->request->allowMethod(['post', 'delete']);
        $keyword = $this->Keywords->get($id);
        if ($this->Keywords->delete($keyword)) {
            $this->Flash->success(__('The keyword has been deleted.'));
        } else {
            $this->Flash->error(__('The keyword could not be deleted. Please, try again.'));
        }
        return $this->redirect(['action' => 'index']);
    }

    /**
     * Ajax create new Keyword 
     */
    public function add() {
        //create a new entity 
        $keyword = $this->Keywords->newEntity();
        //check if the request is a http post 
        if ($this->request->is('post')) {
            //this has to be done cake magic 
            //stop the view from rendering 
            $this->autoRender = false;
            //get the keyword from the http request param
            $keyword->name = $this->request->query('keyword');
            if ($this->Keywords->save($keyword)) {
                //return the id and the keyword of the new created keyword
                echo json_encode(['id' => $keyword['id'], 'name' => $keyword['name']]);
            } else {
                //return the error
                echo json_encode(['error' => $this->Keywords->validationErrors]);
            }
        }
    }

}
