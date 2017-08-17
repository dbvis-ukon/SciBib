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

use Cake\ORM\Table;

/**
 * Authors Model.
 *
 * @property \Cake\ORM\Association\BelongsToMany $Publications
 */
class ChairPubTable extends Table
{
    /**
     * Initialize method.
     *
     * @param array $config the configuration for the Table
     */
    public function initialize(array $config)
    {
        parent::initialize($config);

        $this->table('chairs_publications');
        $this->displayField('chair_id');
        $this->primaryKey('id');

        $this->belongsTo('Publications', [
            'foreignKey' => 'publication_id',
        ]);

        $this->belongsTo('Chairs', [
            'foreignKey' => 'id',
        ]);
    }
}
