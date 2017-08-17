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
 * Copyrights Controller.
 *
 * @property \App\Model\Table\CopyrightsTable $Copyrights
 */
class CopyrightsController extends AppController
{
    /**
     * Index method.
     */
    public function index()
    {
        $this->set('copyrights', $this->paginate($this->Copyrights));
        $this->set('_serialize', ['copyrights']);
    }

    /**
     * View method.
     *
     * @param string|null $id copyright id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function view($id = null)
    {
        $copyright = $this->Copyrights->get($id, [
            'contain' => ['Publications'],
        ]);
        //setting view variables
        $this->set('copyright', $copyright);
        $this->set('_serialize', ['copyright']);
    }

    /**
     * Add method.
     */
    public function add()
    {
        $copyright = $this->Copyrights->newEntity();
        if ($this->request->is('post')) {
            $copyright = $this->Copyrights->patchEntity($copyright, $this->request->data);
            if ($this->Copyrights->save($copyright)) {
                $this->Flash->success(__('The copyright has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The copyright could not be saved. Please, try again.'));
        }
        //setting view variables
        $this->set(compact('copyright'));
        $this->set('_serialize', ['copyright']);
    }

    /**
     * Edit method.
     *
     * @param string|null $id copyright id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function edit($id = null)
    {
        $copyright = $this->Copyrights->get($id, [
            'contain' => [],
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            $copyright = $this->Copyrights->patchEntity($copyright, $this->request->data);
            if ($this->Copyrights->save($copyright)) {
                $this->Flash->success(__('The copyright has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The copyright could not be saved. Please, try again.'));
        }
        //setting view variables
        $this->set(compact('copyright'));
        $this->set('_serialize', ['copyright']);
    }

    /**
     * Delete method.
     *
     * @param string|null $id copyright id
     *
     * @return \Cake\Network\Response|null redirects to index
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $copyright = $this->Copyrights->get($id);
        if ($this->Copyrights->delete($copyright)) {
            $this->Flash->success(__('The copyright has been deleted.'));
        } else {
            $this->Flash->error(__('The copyright could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'index']);
    }
}
