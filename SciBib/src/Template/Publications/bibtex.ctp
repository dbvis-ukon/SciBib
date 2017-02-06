<?php
/*
   Copyright {2017} {University Konstanz -  Data Analysis and Visualization Group}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

if (!$publication->public && !$publication->published) {
    die();
}

require_once(ROOT . DS . 'vendor' . DS . 'bibtex' . DS . 'lib_bibtex.php');

use bibtex\Bibtex;

$bibtex                         = new Bibtex();
$addarray                       = array();
$addarray['entryType']          = $publication->type;
$addarray['title']              = $publication->title;
$addarray['journal']            = $publication->journal;
$addarray['booktitle']          = $publication->booktitle;
$addarray['chapter']            = $publication->chapter;
$addarray['address']            = $publication->address;
$addarray['editor']             = $publication->editor;
$addarray['howpublished']       = $publication->howpublished;
$addarray['institution']        = $publication->institution;
$addarray['month']              = $publication->month;
$addarray['note']               = $publication->note;
$addarray['number']             = $publication->number;
$addarray['organization']       = $publication->organization;
$addarray['pages']              = $publication->pages;
$addarray['school']             = $publication->school;
$addarray['series']             = $publication->series;
$addarray['url']                = $publication->url;
$addarray['doi']                = $publication->doi;
$addarray['year']               = $publication->year;

$addarray['author'] = array();

$cite_author = "";
foreach ($publication->authors as $author) {
    $name = array();
    $name["first"] = $author->forename;
    $name["last"] = $author->surname;

    $cite_author .= $name["last"][0];

    array_push($addarray['author'], $name);
}

if (sizeof($publication->authors) > 4) {
    $cite_author = substr($cite_author, 0, 3) . "+";
}

$cite = !empty($publication->citename) ? $publication->citename : $cite_author . substr($publication->year, 2);

$addarray['cite']               = $cite;

header("Content-type: application/txt");
header("Content-Disposition: attachment; filename=publication".$cite.".bib");

$bibtex->addEntry($addarray);
echo $bibtex->toBibTex();

?>