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

namespace App\Model\Entity;

use Cake\ORM\Entity;

/**
 * Publication Entity.
 *
 * @property int $id
 * @property string $address
 * @property string $booktitle
 * @property int $chapter
 * @property string $edition
 * @property string $editor
 * @property string $howpublished
 * @property string $institution
 * @property string $journal
 * @property string $month
 * @property string $note
 * @property string $number
 * @property string $organization
 * @property string $pages
 * @property string $school
 * @property string $series
 * @property string $title
 * @property string $volume
 * @property string $url
 * @property string $doi
 * @property string $year
 * @property string $citename
 * @property string $publisher
 * @property bool $published
 * @property bool $submitted
 * @property bool $public
 * @property \Cake\I18n\Time $created
 * @property \Cake\I18n\Time $modified
 * @property int $copyright_id
 * @property \App\Model\Entity\Copyright $copyright
 * @property string $type
 * @property string $thumb
 * @property string $mainfile
 * @property \App\Model\Entity\Document[] $documents
 * @property \App\Model\Entity\Keyword[] $keywords
 * @property \App\Model\Entity\Author[] $authors
 * @property \App\Model\Entity\Category[] $categories
 */
class Publication extends Entity {

    /**
     * Fields that can be mass assigned using newEntity() or patchEntity().
     *
     * Note that when '*' is set to true, this allows all unspecified fields to
     * be mass assigned. For security purposes, it is advised to set '*' to false
     * (or remove it), and explicitly make individual fields accessible as needed.
     *
     * @var array
     */
    protected $_accessible = [
        '*' => true,
        'id' => false,
    ];

}
