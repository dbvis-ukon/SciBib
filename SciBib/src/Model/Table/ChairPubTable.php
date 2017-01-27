<?php
/**
 * University Konstanz - udo.3.schlegel@uni-konstanz.de
 */

namespace App\Model\Table;

use App\Model\Entity\ChairPub;
use Cake\ORM\Query;
use Cake\ORM\Table;

/**
 * Authors Model
 *
 * @property \Cake\ORM\Association\BelongsToMany $Publications
 */
class ChairPubTable extends Table {

    /**
     * Initialize method
     *
     * @param array $config The configuration for the Table.
     * @return void
     */
    public function initialize(array $config) {
        parent::initialize($config);

        $this->table('chairs_publications');
        $this->displayField('chair_id');
        $this->primaryKey('id');

        $this->belongsTo('Publications', [
            'foreignKey' => 'publication_id'
        ]);

        $this->belongsTo('Chairs', [
            'foreignKey' => 'id'
        ]);

    }

}