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

class AdminCenterController extends AppController {

    /**
     * Index method
     * Show statistics and nav bar for the admin center start page
     *
     * @return void
     */
    function index() {

        // load and calculate statistics
        $this->loadModel('Publications');
        //get all publications
        $publications = $this->Publications->find('all', [
            'contain' => ['Authors' => [
                    'sort' => ['AuthorsPublications.position' => 'ASC']
                ], 'Chairs']
                ]
        );
        // keim pub
        $pubs_keim = $publications->filter(function ($publication) {
            foreach ($publication->authors as $author) {
                if ($author->id === 1) {
                    return true;
                }
            }
            return false;
        });
        // schreck pub
        $pubs_schreck = $publications->filter(function ($publication) {
            foreach ($publication->authors as $author) {
                if ($author->id === 37) {
                    return true;
                }
            }
            return false;
        });
        // pubs  external 
        $pubs_external = $publications->filter(function ($publication) {
            foreach ($publication->authors as $author) {
                if ($author->id === 1 || $author->id === 37) {
                    return false;
                }
            }
            return true;
        });
        //pubs ls keim 
        $pubs_ls_keim = $publications->filter(function ($publication) {
            foreach ($publication->chairs as $chair) {
                if ($chair->id === 1) {
                    return true;
                }
            }
            return false;
        });
        //pubs ls schreck
        $pubs_ls_schreck = $publications->filter(function ($publication) {
            foreach ($publication->chairs as $chair) {
                if ($chair->id === 2) {
                    return true;
                }
            }
            return false;
        });
        //pubs external marked
        $pubs_ls_external = $publications->filter(function ($publication) {
            foreach ($publication->chairs as $chair) {
                if ($chair->id === 3) {
                    return true;
                }
            }
            return false;
        });
        //set the result
        $this->set('result', [count($publications->toArray()),
            count($pubs_keim->toArray()),
            count($pubs_schreck->toArray()),
            count($pubs_external->toArray()),
            count($pubs_ls_keim->toArray()),
            count($pubs_ls_schreck->toArray()),
            count($pubs_ls_external->toArray())
        ]);
    }

}

?>
