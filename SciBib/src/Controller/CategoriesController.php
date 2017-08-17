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
 * Categories Controller.
 *
 * @property \App\Model\Table\CategoriesTable $Categories
 */
class CategoriesController extends AppController
{
    /**
     * Index method.
     */
    public function index()
    {
        $this->paginate = [
            'contain' => ['ParentCategories', 'Publications'],
        ];
        $list = $this->Categories->find('treelist', [
            'spacer' => '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', ]);
        // an extra query for the number of publications per category
        $query = $this->Categories->find('all', [
            'contain' => ['Publications'],
            'fields' => ['Categories.id', 'Categories.name', 'Categories.lft'],
            'order' => ['Categories.lft'], ]);
        $list = $list->toArray();
        //add the number of publication per category to the title
        foreach ($query as $tmp) {
            $list[$tmp->id] = $list[$tmp->id].' - '.count($tmp->publications);
        }
        //setting view variables
        $this->set('list', $list);
    }

    /**
     * View method.
     *
     * @param string|null $id category id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function view($id = null)
    {
        //get the category
        $category = $this->Categories->get($id, [
            'contain' => ['ParentCategories', 'Publications' => [
                    'sort' => ['Publications.year' => 'DESC'],
                ], 'ChildCategories', 'Publications.Authors' => [
                    'sort' => ['AuthorsPublications.position' => 'ASC'],
                ]],
        ]);
        //setting view variables
        $this->set('category', $category);
        $this->set('_serialize', ['category']);
    }

    /**
     * Add method.
     */
    public function add()
    {
        $category = $this->Categories->newEntity();
        if ($this->request->is('post')) {
            $category = $this->Categories->patchEntity($category, $this->request->data);
            if ($this->Categories->save($category)) {
                $this->Flash->success(__('The category has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The category could not be saved. Please, try again.'));
        }
        $list = $this->Categories->find('treeList', [
            'spacer' => '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', ]);
        //setting view variables
        $this->set(compact('category', 'list'));
        $this->set('_serialize', ['category']);
    }

    /**
     * Edit method.
     *
     * @param string|null $id category id
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function edit($id = null)
    {
        $category = $this->Categories->get($id, [
            'contain' => ['Publications'],
        ]);
        if ($this->request->is(['patch', 'post', 'put'])) {
            $category = $this->Categories->patchEntity($category, $this->request->data);
            if ($this->Categories->save($category)) {
                $this->Flash->success(__('The category has been saved.'));

                return $this->redirect(['action' => 'index']);
            }
            $this->Flash->error(__('The category could not be saved. Please, try again.'));
        }
        $list = $this->Categories->find('treeList', [
            'spacer' => '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', ]);
        //setting view variables
        $this->set(compact('category', 'list'));
        $this->set('_serialize', ['category']);
    }

    /**
     * Delete method.
     *
     * @param string|null $id category id
     *
     * @return \Cake\Network\Response|null redirects to index
     *
     * @throws \Cake\Network\Exception\NotFoundException when record not found
     */
    public function delete($id = null)
    {
        $this->request->allowMethod(['post', 'delete']);
        $category = $this->Categories->get($id);
        if ($this->Categories->delete($category)) {
            $this->Flash->success(__('The category has been deleted.'));
        } else {
            $this->Flash->error(__('The category could not be deleted. Please, try again.'));
        }

        return $this->redirect(['action' => 'index']);
    }
}
