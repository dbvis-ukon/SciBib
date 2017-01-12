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

use App\Model\Entity\AuthorPub;
use Cake\ORM\Query;
use Cake\ORM\Table;

/**
 * Authors Model
 *
 * @property \Cake\ORM\Association\BelongsToMany $Publications
 */
class AuthorPubTable extends Table {

    /**
     * Initialize method
     *
     * @param array $config The configuration for the Table.
     * @return void
     */
    public function initialize(array $config) {
        parent::initialize($config);

        $this->table('authors_publications');
        $this->displayField('publication_id');

    }

}
