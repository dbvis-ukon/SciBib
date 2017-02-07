<?php

namespace App\Model\Table;

use App\Model\Entity\Publication;
use Cake\ORM\Query;
use Cake\ORM\RulesChecker;
use Cake\ORM\Table;
use Cake\Validation\Validator;

/**
 * Publications Model
 *
 * @property \Cake\ORM\Association\BelongsTo $Copyrights
 * @property \Cake\ORM\Association\HasMany $Documents
 * @property \Cake\ORM\Association\HasMany $Keywords
 * @property \Cake\ORM\Association\BelongsToMany $Authors
 * @property \Cake\ORM\Association\BelongsToMany $Categories
 */
class PublicationsTable extends Table {

    /**
     * Initialize method
     *
     * @param array $config The configuration for the Table.
     * @return void
     */
    public function initialize(array $config) {
        parent::initialize($config);

        $this->table('publications');
        $this->displayField('title');
        $this->primaryKey('id');

        $this->addBehavior('Timestamp');

        $this->belongsTo('Copyrights', [
            'foreignKey' => 'copyright_id'
        ]);
        $this->hasMany('Documents', [
            'foreignKey' => 'publication_id'
        ]);
        $this->hasMany('Keywords', [
            'foreignKey' => 'publication_id'
        ]);
        $this->belongsToMany('Authors', [
            'fields' => '*',
            'foreignKey' => 'publication_id',
            'targetForeignKey' => 'author_id',
            'joinTable' => 'authors_publications',
        ]);
        $this->belongsToMany('Chairs', [
            'foreignKey' => 'publication_id',
            'targetForeignKey' => 'chair_id',
            'joinTable' => 'chairs_publications'
        ]);
        $this->belongsToMany('Categories', [
            'foreignKey' => 'publication_id',
            'targetForeignKey' => 'category_id',
            'joinTable' => 'categories_publications'
        ]);
         


        // Add the search behaviour to the table
        $this->addBehavior('Search.Search');
        $this->searchManager()
                ->add('publication_id', 'Search.Value')
                // Here we will alias the 'q' query param to search the `Articles.title`
                // field and the `Articles.content` field, using a LIKE match, with `%`
                // both before and after.
                ->add('q', 'Search.Like', [
                    'before' => true,
                    'after' => true,
                    'filterEmpty' => true,
                    'field' => [$this->aliasField('title'), $this->aliasField('year')]
                ])
                ->add('year', 'Search.Like', [
                    'filterEmpty' => true,
                    'field' => [ $this->aliasField('year')]
                ])
                ->add('type', 'Search.Like', [
                    'filterEmpty' => true,
                    'field' => [ $this->aliasField('type')]
        ]);

        // Add the Upload Plugin
        $this->addBehavior('Josegonzalez/Upload.Upload', [
            'thumb' => [
                'path' => 'webroot{DS}uploadedFiles{DS}thumbs{DS}',
                // thumb resize
                'transformer' => function (\Cake\Datasource\RepositoryInterface $table, \Cake\Datasource\EntityInterface $entity, $data, $field, $settings) {
                    // get the extension from the file
                    // there could be better ways to do this, and it will fail
                    // if the file has no extension
                    $extension = pathinfo($data['name'], PATHINFO_EXTENSION);
                    // Store the thumbnail in a temporary file
                    $tmp = tempnam(sys_get_temp_dir(), 'upload') . '.' . $extension;
                    // Use the Imagine library to DO THE THING
                    $size = new \Imagine\Image\Box(80, 80);
                    $mode = \Imagine\Image\ImageInterface::THUMBNAIL_INSET;
                    $imagine = new \Imagine\Gd\Imagine();
                    // Save that modified file to our temp file
                    $imagine->open($data['tmp_name'])
                            ->thumbnail($size, $mode)
                            ->save($tmp);
                    // Now return the original *and* the thumbnail
                    return [
                        // $data['tmp_name'] => $data['name'],
                        $tmp => $data['name'],
                    ];
                },
                        //rename thumb
                        'nameCallback' => function (array $data, array $options) {
                    return date('Y-m-d') . $data['name'];
                }
                    ],
                    'mainfile' => [
                        'path' => 'webroot{DS}uploadedFiles{DS}',
                        // rename PDF
                        'nameCallback' => function (array $data, array $options) {
                            return date('Y-m-d') . $data['name'];
                        }
                    ],
                    'abstractphoto' => [
                        'path' => 'webroot{DS}uploadedFiles{DS}abstractphotos{DS}',
                        // thumb resize
                        'transformer' => function (\Cake\Datasource\RepositoryInterface $table, \Cake\Datasource\EntityInterface $entity, $data, $field, $settings) {
                            // get the extension from the file
                            // there could be better ways to do this, and it will fail
                            // if the file has no extension
                            $extension = pathinfo($data['name'], PATHINFO_EXTENSION);
                            // Store the thumbnail in a temporary file
                            $tmp = tempnam(sys_get_temp_dir(), 'upload') . '.' . $extension;
                            // Use the Imagine library to DO THE THING
                            $size = new \Imagine\Image\Box(600, 600);
                            $mode = \Imagine\Image\ImageInterface::THUMBNAIL_INSET;
                            $imagine = new \Imagine\Gd\Imagine();
                            // Save that modified file to our temp file
                            $imagine->open($data['tmp_name'])
                                    ->thumbnail($size, $mode)
                                    ->save($tmp);
                            // Now return the original *and* the thumbnail
                            return [
                                $data['tmp_name'] => 'original-' . $data['name'],
                                $tmp => $data['name'],
                            ];
                        },
                                // rename abstract photo
                                'nameCallback' => function (array $data, array $options) {
                            return date('Y-m-d') . '-a-' . $data['name'];
                        }
                            ],
                        ]);
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
                                ->allowEmpty('address');

                        $validator
                                ->allowEmpty('booktitle');

                        $validator
                                ->add('chapter', 'valid', ['rule' => 'numeric'])
                                ->allowEmpty('chapter');

                        $validator
                                ->allowEmpty('edition');

                        $validator
                                ->allowEmpty('editor');

                        $validator
                                ->allowEmpty('howpublished');

                        $validator
                                ->allowEmpty('institution');

                        $validator
                                ->allowEmpty('journal');

                        $validator
                                ->allowEmpty('month');

                        $validator
                                ->allowEmpty('note');

                        $validator
                                ->allowEmpty('number');

                        $validator
                                ->allowEmpty('organization');

                        $validator
                                ->allowEmpty('pages');

                        $validator
                                ->allowEmpty('school');

                        $validator
                                ->allowEmpty('series');

                        $validator
                                ->notEmpty('title');

                        $validator
                                ->allowEmpty('volume');

                        $validator
                                ->allowEmpty('url');

                        $validator
                                ->allowEmpty('doi');

                        $validator
                                ->notEmpty('year');

                        $validator
                                ->allowEmpty('citename')
                                ->add('citename', 'unique', ['rule' => 'validateUnique',
                                    'provider' => 'table']);

                        $validator
                                ->allowEmpty('publisher');

                        $validator
                                ->add('published', 'valid', ['rule' => 'boolean'])
                                ->allowEmpty('published');

                        $validator
                                ->add('submitted', 'valid', ['rule' => 'boolean'])
                                ->allowEmpty('submitted');

                        $validator
                                ->add('public', 'valid', ['rule' => 'boolean'])
                                ->allowEmpty('public');

                        $validator
                                ->notEmpty('type');

                        $validator
                                ->allowEmpty('thumb');

                        $validator
                                ->allowEmpty('abstractphoto');

                        $validator
                                ->allowEmpty('abstract');

                        $validator
                                ->allowEmpty('mainfile');

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
                        $rules->add($rules->existsIn([ 'copyright_id'], 'Copyrights'));

                        return $rules;
                    }
                }
                