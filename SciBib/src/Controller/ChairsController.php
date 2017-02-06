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
 * Chairs Controller
 *
 * @property \App\Model\Table\ChairsTable $Chairs
 */
class ChairsController extends AppController
{

    /**
     * Index method
     *
     * @return \Cake\Network\Response|null
     */
    public function index()
    {
        $chairs = $this->paginate($this->Chairs);

        $this->set(compact('chairs'));
        $this->set('_serialize', ['chairs']);
    }

    /**
     * View method
     *
     * @param string|null $id Chair id.
     * @return \Cake\Network\Response|null
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function view($id = null)
    {
        $chair = $this->Chairs->get($id, [
            'contain' => []
        ]);

        $this->set('chair', $chair);
        $this->set('_serialize', ['chair']);
    }

    /**
     * Add method
     *
     * @return \Cake\Network\Response|void Redirects on successful add, renders view otherwise.
     */
    public function add()
    {
        $chair = $this->Chairs->newEntity();
        if ($this->request->is('post')) {
            $chair = $this->Chairs->patchEntity($chair, $this->request->data);
            if ($this->Chairs->save($chair)) {
                $this->Flash->success(__('The chair has been saved.'));

                return $this->redirect(['action' => 'index']);
            } else {
                $this->Flash->error(__('The chair could not be saved. Please, try again.'));
            }
        }
        $this->set(compact('chair'));
        $this->set('_serialize', ['chair']);
    }

    /**
     * Edit method
     *
     * @param string|null $id Chair id.
     * @return \Cake\Network\Response|void Redirects on successful edit, renders view otherwise.
     * @throws \Cake\Network\Exception\NotFoundException When record not found.
     */
    public function edit($id = null)
    {
        $chair = $this->Chairs->get($id, [
            'contain' => []
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            $chair = $this->Chairs->patchEntity($chair, $this->request->data);
            if ($this->Chairs->save($chair)) {
                $this->Flash->success(__('The chair has been saved.'));

                return $this->redirect(['action' => 'index']);
            } else {
                $this->Flash->error(__('The chair could not be saved. Please, try again.'));
            }
        }
        $this->set(compact('chair'));
        $this->set('_serialize', ['chair']);
    }

    /**
     * Delete method
     *
     * @param string|null $id Chair id.
     * @return \Cake\Network\Response|null Redirects to index.
     * @throws \Cake\Datasource\Exception\RecordNotFoundException When record not found.
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $chair = $this->Chairs->get($id);
        if ($this->Chairs->delete($chair)) {
            $this->Flash->success(__('The chair has been deleted.'));
        } else {
            $this->Flash->error(__('The chair could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'index']);
    }
}
