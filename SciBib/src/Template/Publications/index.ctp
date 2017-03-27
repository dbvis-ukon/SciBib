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

$typeColors['inproceedings'] = '#7f7fff';
$typeColors['article'] = '#ff7f7f';
$typeColors['techreport'] = '#7fbf7f';
$typeColors['inbook'] = '#c5b4a1';
$typeColors['book'] = '#b5a1c5';
$typeColors['other'] = '#888888';

echo $this->Html->css('publications_index.css');

?>
<div class="publications index large-9 medium-8 columns content">
<?php

if (!$user['active'] && !$hideFilterHeader && !$isEmbedded['isEmbedded']) {
    ?>
        <div id="login">
            <ul class="right">
                <?= $this->Html->link('Login', ['controller' => '', 'action' => 'login']) ?>
            </ul>
        </div>
        <?php } ?>

        <?php if (!$hideFilterHeader) { ?>
            <div class="filterSection">
                <span class="filterTitle">Show only</span>
                <span class="oneLineListEntry">
                    <?php
                    echo '<span class="smallColorBlock" style="background-color: ' . $typeColors['inproceedings'] . ';"></span>';
                    echo $this->Html->link('Inproceedings', ['type' => 'inproceedings',
                        'year' => $this->request->query('year'),
                        'author' => $this->request->query('author')], ['style' => 'color: ' . $typeColors['inproceedings']]);
                    ?>
                </span>
                <span class="oneLineListEntry">
                    <?php
                    echo '<span class="smallColorBlock" style="background-color: ' . $typeColors['article'] . ';"></span>';
                    echo $this->Html->link('Articles', ['type' => 'article',
                        'year' => $this->request->query('year'),
                        'author' => $this->request->query('author')], ['style' => 'color: ' . $typeColors['article']]);
                    ?>
                </span>
                <span class="oneLineListEntry">
                    <?php
                    echo '<span class="smallColorBlock" style="background-color: ' . $typeColors['techreport'] . ';"></span>';
                    echo $this->Html->link('Tech Reports', ['type' => 'techreport',
                        'year' => $this->request->query('year'),
                        'author' => $this->request->query('author')], ['style' => 'color: ' . $typeColors['techreport']]);
                    ?>
                </span>
                <span class="oneLineListEntry">
                    <?php
                    echo '<span class="smallColorBlock" style="background-color: ' . $typeColors['inbook'] . ';"></span>';
                    echo $this->Html->link('Inbooks', ['type' => 'inbook',
                        'year' => $this->request->query('year'),
                        'author' => $this->request->query('author')], ['style' => 'color: ' . $typeColors['inbook']]);
                    ?>
                </span>
                <span class="oneLineListEntry">
                    <?php
                    echo '<span class="smallColorBlock" style="background-color: ' . $typeColors['book'] . ';"></span>';
                    echo $this->Html->link('Books', ['type' => 'book',
                        'year' => $this->request->query('year'),
                        'author' => $this->request->query('author')], ['style' => 'color: ' . $typeColors['book']]);
                    ?>
                </span>
                <span class="oneLineListEntry">
                    <?php
                    echo '<span class="smallColorBlock" style="background-color: ' . $typeColors['other'] . ';"></span>';
                    echo $this->Html->link('Others', ['type' => 'other',
                        'year' => $this->request->query('year'),
                        'author' => $this->request->query('author')], ['style' => 'color: ' . $typeColors['other']]);
                    ?>
                </span>
                <?php
                if ($this->request->query('type')) {
                    echo '<span class="additionalFilterInfo">Only showing ' .
                        $this->request->query('type') . ' (' . $this->Html->link('Remove Filter', ['action' => 'index', 'year' => $this->request->query('year')]) . ')</span>';
                }
                ?>
            </div>
            <div class="filterSection">
                <span class="filterTitle">Show only publications from</span>
                <?php
                foreach (range(1991, date("Y")) as $number) {
                    echo "<span class=\"oneLineListEntry\">" . $this->Html->link($number, ['year' => $number, 'type' => $this->request->query('type'),
                            'author' => $this->request->query('author')]) . "</span> ";
                }
                if ($this->request->query('year')) {
                    echo '<span class="additionalFilterInfo">Only showing publications from  '
                        . $this->request->query('year') . ' (' . $this->Html->link('Remove Filter', ['action' => 'index', 'type' => $this->request->query('type'),
                            'author' => $this->request->query('author')]) . ')</span>';
                }
                ?>
            </div>


            <?php
        }
        ?>


        <?php
        $year = 0;
        foreach ($publications as $publication) {
        // check if the publication should be public
        if ($publication->public === true || $publication->published === true) {

        $typeColor = $typeColors['other'];
        $loweredType = strtolower($publication->type);
        if (array_key_exists($loweredType, $typeColors))
            $typeColor = $typeColors[$loweredType];
        ?>

        <table class="publicationListEntry">
            <tbody>
            <tr>
                <td class="publicationThumbWrapper">
                    <?php
                    //Use the standard thumbnail if no thumb is available
                    if ($publication->thumb == null || !file_exists(WWW_ROOT . 'uploadedFiles' . DS . 'thumbs' . DS . $publication->thumb)) {
                        echo $this->Html->image('/uploadedFiles/thumbs/default.png'
                            , ['width' => '100px', 'height' => '100px', 'style' => 'border: 2px solid ' . $typeColor . ';']);
                    } else {
                        echo $this->Html->image('/uploadedFiles/thumbs/'
                            . $publication->thumb, ['width' => '100px', 'height' => '100px', 'style' => 'border: 2px solid ' . $typeColor . ';']);
                    }
                    ?>
                </td>
                <td style="width: 70%">
                    <!--authors listed-->
                    <span class="publicationAuthors">
                    <?php
                    //print the authors with ',' - 'and'
                    $numAuthors = count($publication->authors);
                    $i = 0;
                    foreach ($publication->authors as $author) {
                        if (++$i === $numAuthors && $i !== 1) {
                            echo ' and ';
                        } else {
                            if ($i !== 1) {
                                echo ', ';
                            }
                        }
                        echo $author->cleanname;
                    }
                    ?>
                    </span> <br>
                    <span class="publicationTitle">
                    <?php
                    echo $this->Html->link(__($publication->title), ['action' => 'view', $publication->id]) . '  <br>';
                    ?>
                    </span>
                    <span class="publicationBookTitle">
                        <?php
                        //publication type stuff
                        echo $this->element('publicationText', ['publication' => $publication, 'renderCopyable' => true]);
                        ?>
                    </span>
                </td>
                <td class="publicationDownloadIcons">
                    <a href="<?php echo $this->Url->build(['action' => 'bibtex', $publication->id], true) ?>"
                       target="_blank" title="Download BibTeX file">
                        <img src="<?php echo $this->request->webroot ?>img/document_bibtex.png" alt="Bibtex Download"
                             style="width:50px;height:50px;">
                    </a>
                    <?php
                        if ($publication->doi) {
                            echo '<a href="http://dx.doi.org/' . $publication->doi . '" target="_blank">'
                                . '<img src="' . $this->request->webroot . 'img/document_doi.png" alt="DOI" style="width:50px;height:50px;"></a>';
                        }
                        if (!empty(trim($publication->mainfile)) &&
                            file_exists(WWW_ROOT . 'uploadedFiles' . DS . $publication->mainfile) &&
                            $publication->published
                        ) {
                            echo '<a href="' . $this->request->webroot . './uploadedFiles/' . $publication->mainfile .
                                '"><img src="' . $this->request->webroot . 'img/document_pdf.png" alt="PDF" style="width:50px;height:50px;"></a>';
                        }
                        if ($publication->documents) {
                          foreach ($publication->documents as $document) {
                            if ($document->remote) {
                              echo '<a href="' . $document->filename .
                                  '"><img src="' . $this->request->webroot . 'img/document_url.png" alt="PDF" style="width:50px;height:50px;"></a>';
                            }
                          }
                        }
                    ?>
                </td>
                <?php
                if ($year !== $publication->year) {
                    $year = $publication->year;
                    echo '<h4>' . $publication->year . '</h4>';
                }
                }
                }
                ?>
    </div>
