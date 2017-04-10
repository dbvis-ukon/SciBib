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

namespace App\Model\Table;

use App\Model\Entity\Document;
use Cake\ORM\Query;
use Cake\ORM\RulesChecker;
use Cake\ORM\Table;
use Cake\Validation\Validator;

/**
 * Documents Model
 *
 * @property \Cake\ORM\Association\BelongsTo $Publications
 */
class DocumentsTable extends Table {

    /**
     * Initialize method
     *
     * @param array $config The configuration for the Table.
     * @return void
     */
    public function initialize(array $config) {
        parent::initialize($config);

        $this->table('documents');
        $this->displayField('id');
        $this->primaryKey('id');

        $this->belongsTo('Publications', [
            'foreignKey' => 'publication_id',
            'dependent' => true
        ]);

        $this->addBehavior('Josegonzalez/Upload.Upload', [
            'filename' => [
                'path' => 'webroot{DS}uploadedFiles{DS}',
                // rename PDF
                'nameCallback' => function (array $data, array $options) {
                    return date('Y-m-d') . 'doc' . $data['name'];
                }
            ]
          ]
        );

    }

    /**
     * Default validation rules.
     *
     * @param \Cake\Validation\Validator $validator Validator instance.
     * @return \Cake\Validation\Validator
     */
    public function validationDefault(Validator $validator) {
        $validator
                ->add('id', 'valid', ['rule' => 'numeric'])
                ->allowEmpty('id', 'create');

        $validator
                ->add('visible', 'valid', ['rule' => 'boolean'])
                ->allowEmpty('visible');

        $validator
                ->allowEmpty('filename');

        $validator
                ->allowEmpty('description');

        return $validator;
    }

    /**
     * Returns a rules checker object that will be used for validating
     * application integrity.
     *
     * @param \Cake\ORM\RulesChecker $rules The rules object to be modified.
     * @return \Cake\ORM\RulesChecker
     */
    public function buildRules(RulesChecker $rules) {
        $rules->add($rules->existsIn(['publication_id'], 'Publications'));
        return $rules;
    }

}
