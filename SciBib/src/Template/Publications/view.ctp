<?php
$typeColors['inproceedings'] = '#7f7fff';
$typeColors['article'] = '#ff7f7f';
$typeColors['techreport'] = '#7fbf7f';
$typeColors['inbook'] = '#c5b4a1';
$typeColors['book'] = '#b5a1c5';
$typeColors['other'] = '#888888';
?>

<div class="col-lg-12">
    <?php
    // show login if user is not logged in
    if (!$user['active']) {
        ?><div id="login">
            <ul class="right">
                <?= $this->Html->link('Login', ['controller' => '', 'action' => 'login']) ?>
            </ul>
        </div>
    <?php } ?>


    <div class="paperInfo">
        <h1><?= h($publication->title) ?>  </h1>
        <div class="authors">
            <?php
            $last = end($publication->authors);
            foreach ($publication->authors as $authors) {
                echo $this->Html->link(($authors->cleanname), ['controller' => 'Authors', 'action' => 'view', $authors->id], ['escape' => false]);
                if ($last !== $authors)
                    echo ', ';
            }
            ?>
        </div>
        <?php
        if ($publication->abstractphoto) {
            echo $this->Html->link(
                    $this->Html->image('/uploadedFiles/abstractphotos/'
                            . $publication->abstractphoto), ('/uploadedFiles/abstractphotos/original-' . $publication->abstractphoto), ['escape' => false, 'class' => 'abstractPhoto']);
        }
        ?>
        <br>
        <div class="buzzwords">
            <?php
            if ($publication->keywords) {
                echo 'Keywords: ';
            }
            $last = end($publication->keywords);
            foreach ($publication->keywords as $keywords) {
                echo h($keywords->name);
                if ($last !== $keywords)
                    echo ', ';
            }
            ?>
        </div>
        <div class="information">
            <?=
            $this->element('publicationText', ['publication' => $publication, 'renderCopyable' => true]);
            ?>
            <br>
            Type:
            <?= $publication->type ?>
        </div>
        <div class="abstract">
            <?php
            if ($publication->abstract) {
                echo '<b>Abstract</b> <br>';
                echo $publication->abstract;
            }
            ?>
        </div>
        <br>
        <b>Materials</b> <br>
        <ul class="button-group">
            <?php
            if (!empty(trim($publication->mainfile)) &&
                    file_exists(WWW_ROOT . 'uploadedFiles' . DS . $publication->mainfile && $publication->published)
            ) {
                echo '<li><a href="' . $this->request->webroot . './uploadedFiles/' . $publication->mainfile .
                '"><button class="large button">Get PDF</button></a> </li>';
            }
            ?>
            <li>
                <a href="<?php echo $this->Url->build(['action' => 'bibtex', $publication->id], true) ?>" target="_blank" title="Download BibTeX file">
                    <button class="large button">Get Bibtex</button>
                </a>
            </li>
            <?php
            foreach ($publication->documents as $document) {
                if ($document->remote) {
                    echo '<li><a href="' . $document->filename .
                '"><button class="large button">External Resource</button></a></li>';
                } else {
                    echo '<li><a href="' . $this->request->webroot . './uploadedFiles/' . $document->filename .
                '"><button class="large button">Get PDF</button></a></li>';
                }
            }
            ?>
        </ul>
    </div>
    <br>

    <b>Related Publications</b>

    <br>
    <?php
    foreach ($relatedPublications as $relatedPublication):
        //check if the publication is the one which is viewed
        if ($relatedPublication->id != $publication->id):

            // check if the publication should be public
            if ($relatedPublication->public === true || $relatedPublication->published === true):

                $typeColor = $typeColors['other'];
                $loweredType = strtolower($relatedPublication->type);
                if (array_key_exists($loweredType, $typeColors))
                    $typeColor = $typeColors[$loweredType];
                ?>
                <table class="publicationListEntry">
                    <tbody>
                        <tr>
                            <td class="publicationThumbWrapper">
                                <?php
                                //Use the standard thumbnail if no thumb is available
                                if ($relatedPublication->thumb == null || !file_exists(WWW_ROOT . 'uploadedFiles' . DS . 'thumbs' . DS . $relatedPublication->thumb)) {
                                    echo $this->Html->image('/uploadedFiles/thumbs/default.png'
                                            , ['width' => '100px', 'height' => '100px', 'style' => 'border: 2px solid ' . $typeColor . ';']);
                                } else {
                                    echo $this->Html->image('/uploadedFiles/thumbs/'
                                            . $relatedPublication->thumb, ['width' => '100px', 'height' => '100px', 'style' => 'border: 2px solid ' . $typeColor . ';']);
                                }
                                ?>
                            </td>
                            <td style="width: 70%">
                                <!--authors listed-->
                                <span class="publicationAuthors">
                                    <?php
                                    //print the authors with ',' - 'and'
                                    $numAuthors = count($relatedPublication->authors);
                                    $i = 0;
                                    foreach ($relatedPublication->authors as $author):
                                        if (++$i === $numAuthors && $i !== 1) {
                                            echo ' and ';
                                        } else {
                                            if ($i !== 1) {
                                                echo ', ';
                                            }
                                        }
                                        echo $author->cleanname;
                                    endforeach;
                                    echo '.'
                                    ?>
                                </span> <br>
                                <span class="publicationTitle">
                                    <?=
                                    $this->Html->link(__($relatedPublication->title)
                                            , ['action' => 'view', $relatedPublication->id]) . '  <br>'
                                    ?>
                                </span>
                                <span class="publicationBookTitle">
                                    <?php
                                    //publication type stuff
                                    echo $this->element('publicationText', ['publication' => $relatedPublication, 'renderCopyable' => true]);
                                    ?>
                                </span></td>
                            <td class="publicationDownloadIcons">
                                <a href="<?php echo $this->Url->build(['action' => 'bibtex', $relatedPublication->id], true) ?>"
                                   target="_blank" title="Download BibTeX file">
                                    <img src="<?php echo $this->request->webroot ?>img/document_bibtex.png" alt="Bibtex Download"
                                         style="width:50px;height:50px;">
                                </a>
                                <?php
                                if ($relatedPublication->public) {
                                    if ($relatedPublication->doi) {
                                        echo '<a href="http://dx.doi.org/' . $relatedPublication->doi . '" target="_blank">'
                                        . '<img src="' . $this->request->webroot . 'img/document_url.png" alt="DOI" style="width:50px;height:50px;"></a>';
                                    }
                                    if (!empty(trim($relatedPublication->mainfile)) &&
                                            file_exists(WWW_ROOT . 'uploadedFiles' . DS . $relatedPublication->mainfile)
                                    ) {
                                        echo '<a href="' . $this->request->webroot . './uploadedFiles/' . $relatedPublication->mainfile .
                                        '"><img src="' . $this->request->webroot . 'img/document_pdf.png" alt="PDF" style="width:50px;height:50px;"></a>';
                                    }
                                }
                                ?>
                            </td>
                        </tr>
                    </tbody>
                </table>
                            <?php
                        endif;
                    endif;
                endforeach;
                ?>
</div>
<!-- Placed at the end of the document so the pages load faster -->
<?php
echo $this->Html->script('jquery-3.2.1.min.js');
echo $this->Html->script('bootstrap.min.js');
?>
