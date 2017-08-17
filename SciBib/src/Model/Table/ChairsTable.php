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

namespace App\Model\Table;

/* Copyright {2017} {University Konstanz -  Data Analysis and Visualization Group}

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

use Cake\ORM\Table;
use Cake\Validation\Validator;

/**
 * Chairs Model.
 *
 * @property \Cake\ORM\Association\BelongsToMany $Publications
 *
 * @method \App\Model\Entity\Chair get($primaryKey, $options = [])
 * @method \App\Model\Entity\Chair newEntity($data = null, array $options = [])
 * @method \App\Model\Entity\Chair[] newEntities(array $data, array $options = [])
 * @method \App\Model\Entity\Chair|bool save(\Cake\Datasource\EntityInterface $entity, $options = [])
 * @method \App\Model\Entity\Chair patchEntity(\Cake\Datasource\EntityInterface $entity, array $data, array $options = [])
 * @method \App\Model\Entity\Chair[] patchEntities($entities, array $data, array $options = [])
 * @method \App\Model\Entity\Chair findOrCreate($search, callable $callback = null, $options = [])
 */
class ChairsTable extends Table
{
    /**
     * Initialize method.
     *
     * @param array $config the configuration for the Table
     */
    public function initialize(array $config)
    {
        parent::initialize($config);

        $this->table('chairs');
        $this->displayField('name');
        $this->primaryKey('id');

        $this->belongsToMany('Publications', [
            'foreignKey' => 'chair_id',
            'targetForeignKey' => 'publication_id',
            'joinTable' => 'chairs_publications',
        ]);
    }

    /**
     * Default validation rules.
     *
     * @param \Cake\Validation\Validator $validator validator instance
     *
     * @return \Cake\Validation\Validator
     */
    public function validationDefault(Validator $validator)
    {
        $validator
            ->integer('id')
            ->allowEmpty('id', 'create');

        $validator
            ->allowEmpty('name');

        return $validator;
    }
}
