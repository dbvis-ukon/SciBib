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
 * Documents Controller.
 *
 * @property \App\Model\Table\DocumentsTable $Documents
 */
class DocumentsController extends AppController
{
    /**
     * Index method.
     */
    public function index()
    {
        $this->paginate = [
            'contain' => ['Publications'],
        ];
        $this->set('documents', $this->paginate($this->Documents));
        $this->set('_serialize', ['documents']);
    }

    /**
     * View method.
     *
     * @param string|null $id document id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function view($id = null)
    {
        $document = $this->Documents->get($id, [
            'contain' => ['Publications'],
        ]);
        //setting view variables
        $this->set('document', $document);
        $this->set('_serialize', ['document']);
    }

    /**
     * Add method.
     */
    public function add()
    {
        $document = $this->Documents->newEntity();
        if ($this->request->is('post')) {
            $document = $this->Documents->patchEntity($document, $this->request->data);
            if ($this->Documents->save($document)) {
                $this->Flash->success(__('The document has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The document could not be saved. Please, try again.'));
        }
        $publications = $this->Documents->Publications->find('list', ['limit' => 200]);
        //setting view variables
        $this->set(compact('document', 'publications'));
        $this->set('_serialize', ['document']);
    }

    /**
     * Edit method.
     *
     * @param string|null $id document id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function edit($id = null)
    {
        $document = $this->Documents->get($id, [
            'contain' => [],
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            $document = $this->Documents->patchEntity($document, $this->request->data);
            if ($this->Documents->save($document)) {
                $this->Flash->success(__('The document has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The document could not be saved. Please, try again.'));
        }
        $publications = $this->Documents->Publications->find('list', ['limit' => 200]);
        //setting view variables
        $this->set(compact('document', 'publications'));
        $this->set('_serialize', ['document']);
    }

    /**
     * Delete method.
     *
     * @param string|null $id document id
     *
     * @return \Cake\Network\Response|null redirects to index
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $document = $this->Documents->get($id);
        if ($this->Documents->delete($document)) {
            $this->Flash->success(__('The document has been deleted.'));
        } else {
            $this->Flash->error(__('The document could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'index']);
    }
}
