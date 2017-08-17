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

use App\Model\Entity\Author;
use Cake\ORM\Query;
use Cake\ORM\RulesChecker;
use Cake\ORM\Table;
use Cake\Validation\Validator;

/**
 * Authors Model.
 *
 * @property \Cake\ORM\Association\BelongsToMany $Publications
 */
class AuthorsTable extends Table
{
    /**
     * Initialize method.
     *
     * @param array $config the configuration for the Table
     */
    public function initialize(array $config)
    {
        parent::initialize($config);

        // Add the behaviour to your table
        $this->addBehavior('Search.Search');

        $this->searchManager()
                ->add('author_id', 'Search.Value')
                // Here we will alias the 'q' query param to search the `Articles.title`
                // field and the `Articles.content` field, using a LIKE match, with `%`
                // both before and after.
                ->add('q', 'Search.Like', [
                    'before' => true,
                    'after' => true,
                    'field' => [$this->aliasField('surname'), $this->aliasField('forename'), $this->aliasField('cleanname')],
                ])
                ->add('foo', 'Search.Callback', [
                    'callback' => function ($query, $args, $manager) {
                        // Modify $query as required
                    },
        ]);

        $this->table('authors');
        $this->displayField('id', 'cleanname');
        $this->primaryKey('id');

        $this->belongsToMany('Publications', [
            'fields' => '*',
            'foreignKey' => 'author_id',
            'targetForeignKey' => 'publication_id',
            'joinTable' => 'authors_publications',
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
                ->add('id', 'valid', ['rule' => 'numeric'])
                ->allowEmpty('id', 'create');

        $validator
                ->notEmpty('surname', 'You need to provide a surname');

        $validator
                ->notEmpty('forename', 'You need to provide a surname');

        $validator
                ->allowEmpty('cleanname');
        $validator
                ->allowEmpty('website');

        return $validator;
    }

    //Rules checker classes are generally defined by the buildRules() method in your
    // table class. Behaviors and other event subscribers can use the
    // Model.buildRules event to augment the rules checker for a given Table class:
    public function buildRules(RulesChecker $rules)
    {
        // Add a rule that is applied for create and update operations
        // The combination of forename and surname is unique
        $rules->add($rules->isUnique(['forename', 'surname']), 'Author name already exists ');

        return $rules;
    }

    /*     * ******************
     * CREATE CLEANNAME *
     * ***************** */

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

    /** shortens a token with a dash */
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

    /** shortens a token without a dash */
    public function shortenToken($t)
    {
        if (!$t || !is_string($t) || mb_strlen($t) <= 1) {
            return $t;
        }

        return mb_strtoupper(mb_substr($t, 0, 1)).'.';
    }
}
