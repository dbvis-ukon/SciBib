<script>
    var baseURL = "<?php echo $this->request->webroot ?>/";
    var imageBaseURL = baseURL + "img";
</script>

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


//Javascirpt libs
echo $this->Html->script('/js/jquery-1.12.0.js');
echo $this->Html->script('/js/jquery-ui.js');
echo $this->Html->script('/js/select2.full.js');
echo $this->Html->script('/js/publications_add.js');
echo $this->Html->script('/js/Sortable.js');
?>

<script>
    var selectedAuthors = <?php
//pass the authors that are already selected to javascript
echo json_encode($publication->authors);
?>;
</script>

<?php
//CSS files
echo $this->Html->css('jquery-ui.css');
echo $this->Html->css('select2.css');
echo $this->Html->css('publications-add.css');
?>
<!-- Navigations -->
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/publication.png', ['width' => '16', 'height' => '16']) . ' ' . __('List Publications'), ['action' => 'privateIndex'], ['escape' => false]) ?></li>
    </ul>
</nav>
<div class="publications form large-9 medium-8 columns content">

    <?= $this->Form->create($publication, ['type' => 'file', 'onsubmit' => 'return valid(event);']) ?>

    <h4>General Information</h4>

    <!--    Type of the Publication and the title-->
    <table>
        <tbody style="vertical-align: top;">
            <tr>
                <td>
                    <?=
                    $this->Form->input('title', ['label' => ['class' => 'labelField'],
                        'class' => 'inputFieldTitle',
                        'id' => 'title',
                        'placeholder' => 'Good research paper title']);
                    ?>
                </td>
                <td>
                    Type &nbsp
                    <?=
                    $this->Form->select('type', $optionsType, ['empty' => false,
                        'id' => 'typebox'])
                    ?>
                </td>
            </tr>
        </tbody>
    </table>

    <table>
        <tbody style="vertical-align: top;">
            <tr>
                <td id="institution">
                    <?php $selectedChairs = array();
                    for ($i = 0; $i < count($publication->chairs); $i++) {
                        array_push($selectedChairs, $publication->chairs[$i]['id']);
                    }
                    echo $this->Form->input('chairs._ids', ['options' => $chairs,
                        'multiple' => 'checkbox',
                        'type' => 'select'
                    ]);

                    ?>
                </td>
                <!--Submitted, Published Checkbox with the Publication data option-->
                <td>
                    <?= $this->Form->checkbox('submitted', ['id' => 'PublicationSubmitted']) ?>
                    Submitted &nbsp
                </td>
                <td>
                    <?= $this->Form->checkbox('published', ['id' => 'PublicationPublished']) ?>
                    Published &nbsp
                </td>
                <td>
                    <!-- Checkboxes not public, public, made ... -->
                    <?=
                    $this->Form->checkbox('public', [
                        'id' => 'PublicationPublic'
                    ]);
                    ?>
                    Public &nbsp  <br>
                    <input type="checkbox" id="PublicationDate" >
                    Made public on  &nbsp<br>
                    <?php
                    //Publication data text field
                    echo $this->Form->input('publicationdate', ['id' => 'PublicationPublicationdate',
                        'type' => 'text', 'label' => false, 'div' => false,
                        'disabled' => true, 'readonly' => true,
                        'error' => ['class' => 'error']]);
                    ?>
                </td>
            </tr>
        </tbody>
    </table>
    <!--Warning and Status of the publication these are used in the publications_index.js-->
    <div id="publicationStatusMessage" class="fakeLabel" style="display: none;"></div>
    <div id="publicationStatusWarning" class="fakeLabel" style="display: none;"></div>
    <br>

    <table>
        <tbody style="vertical-align: top;">
            <tr>
                <td style="width: 30%;">
                    Year &nbsp
                    <?php
                    $years = array_combine(range(date('Y') + 1, date('Y') - 20), range(date('Y') + 1, date('Y') - 20));
                    echo $this->Form->select('year', $years, ['label' => ['class' => 'labelField'],
                        'class' => 'inputFieldTitle']);
                    ?>
                </td>
                <td>
                    <?=
                    $this->Form->input('kops', ['label' => ['class' => 'labelField'],
                        'class' => 'inputFieldTitle',
                        'placeholder' => 'Example: http://kops.uni-konstanz.de/handle/1234567/1235']);
                    ?>
                    <p class="kopsLabel">
                        Please search <a href='http://kops.uni-konstanz.de/discover?query=' target='_blank'>KOPS</a> for the full URL!
                    </p>
                </td>
            </tr>
        </tbody>
    </table>
    <?=
    $this->Form->input('doi', ['label' => ['class' => 'labelField'],
        'class' => 'inputFieldTitle',
        'placeholder' => 'Without the URL part of the DOI! (Example: 10.123/Conf/123-456)']);
    ?>
    <!-- Categories-->
    <script type="text/javascript">
        var categories = <?php echo json_encode($categories) . ';'; ?>
    </script>
    <?php
// Make a tmpArray for the categories
// this array will be used for the view to select and unselect things
    $tmpArray = [];
    foreach ($categories as $categorie) {
        $tmpArray[$categorie->id] = $categorie->longName;
    }
    echo $this->Form->input('categories._ids', ['options' => $tmpArray,
        'multiple' => 'multiple',
        'type' => 'select',
        'escape' => false]);
    ?>
    <br>
    <!-- KEYWORDS -->
    <?=
    $this->Form->input('keywords._ids', ['options' => $keywords,
        'multiple' => 'multiple',
        'type' => 'select',
        'escape' => false]);
    ?>
    <br>
    <!-- ajax request -->
    <p id="addKeywordButton">
        Add new keyword
        <?php echo $this->Html->image('/img/add.png', ['width' => '16', 'height' => '16']); ?>
    </p>
    <br>
    <table id="addKeywordTable" style="display: none;">
        <tbody style="vertical-align: top;">
            <tr>
                <td>
                    Keyword &nbsp;
                    <input type="text" id="AddKeyword" value="" />
                </td>
                <td>
                    <input type="button" value="Add"  id="SubmitKeyword" />
                </td>
            </tr>
        </tbody>
    </table>
    <div id="CreateKeywordSuccess"></div>
    <div id="CreateKeywordError"></div>
    <br>
    <?=
    /* COPYRIGHT */
    //Existing copyright selection or input fields to create a new copyright.
    $this->Form->input('copyright_id', ['label' =>
        ['text' => 'Copyright &copy;',
            'class' => 'labelCopyrightField',
            'escape' => false],
        'class' => 'inputFieldTitle']);
    ?>
    <table>
        <tbody style="vertical-align: top;">
            <tr>
                <td style="width: 30%;">
                    <br> Thumbnail
                    <?=
                    $this->Form->input('thumb', ['type' => 'file',
                        'options' => ['accept' => 'image/*'],
                        'label' => false]);
                    ?>
                </td>
                <td>
                    <div id="imagePreview">

                    </div>
                </td>
                <td>
                    <div id="currentThumb">
                        Current Thumbnail:
                           <?php if ($publication->thumb == null ||
                                       !file_exists(WWW_ROOT . 'uploadedFiles' . DS . 'thumbs' . DS . $publication->thumb)) {
                                    echo $this->Html->image('/uploadedFiles/thumbs/default.png'
                            , ['width' => '100px', 'height' => '100px',]);
                                } else {
                                    echo $this->Html->image('/uploadedFiles/thumbs/'
                            . $publication->thumb, ['width' => '100px', 'height' => '100px ;']);
                            }
                        ?>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>

    <!-- AUTHOR -->
    <h4>Authors</h4>
    <table id="authors">
        <tbody style="vertical-align: top;">
            <tr>
                <td style="width: 70%;">
                    <?=
                    $this->Form->input('authors._ids', ['options' => $authors,
                        'multiple' => 'multiple',
                        'type' => 'select',
                        'escape' => false,
                    ]);
                    ?>
                </td>
                <td>
                    <div id="authorsSort">
                        Sequence of Authors
                        <?=
                        //needed to link the two tables authors and publications -> authors position
                        $this->Form->text('authorsPosition', ['type' => 'hidden', 'id' => 'authorsPos']);
                        ?>
                        <!--The sortable authors list -->
                        <ul id="authorsSortable">
                        </ul>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
    <!-- ajax request -->
    <p id="addAuthorButton">
        Add new author <?php echo $this->Html->image('/img/add.png', ['width' => '16', 'height' => '16']); ?>
    </p>
    <br>
    <table id="addAuthorTable" style="display: none;">
        <tbody style="vertical-align: top;">
            <tr>
                <td>
                    Forename &nbsp;
                    <input type="text" id="AddForename" value="" />
                </td>
                <td>
                    Surname &nbsp;
                    <input type="text" id="AddSurname" value="" />
                </td>
                <td>
                    <input type="button" value="Add"  name="SubmitAuthor" id="SubmitAuthor" />
                </td>
            </tr>
        </tbody>
    </table>
    <div id="CreateAuthorSuccess"></div>
    <div id="CreateAuthorError"></div>
    <br>

    <h4>BibTex Information</h4>
    <span id="BibtexFields"> <!-- needed so we can disable certain fields for certain types -->
        <?php
        echo '<div id="address">' . $this->Form->input('address', ['type' => 'text']) . '</div>';
        echo '<div id="booktitle">' . $this->Form->input('booktitle') . '</div>';
        echo '<div id="chapter">' . $this->Form->input('chapter') . '</div>';
        echo '<div id="edition">' . $this->Form->input('edition') . '</div>';
        echo '<div id="editor">' . $this->Form->input('editor') . '</div>';
        echo '<div id="howpublished">' . $this->Form->input('howpublished', ['type' => 'text']) . '</div>';
        echo '<div id="institution">' . $this->Form->input('institution') . '</div>';
        echo '<div id="journal">' . $this->Form->input('journal') . '</div>';
        echo '<div id="month">' . $this->Form->input('month') . '</div>';
        echo '<div id="note">' . $this->Form->input('note', ['type' => 'text']) . '</div>';
        echo '<div id="number">' . $this->Form->input('number') . '</div>';
        echo '<div id="organization">' . $this->Form->input('organization') . '</div>';
        echo '<div id="pages">' . $this->Form->input('pages') . '</div>';
        echo '<div id="school">' . $this->Form->input('school') . '</div>';
        echo '<div id="series">' . $this->Form->input('series') . '</div>';
        echo '<div id="volume">' . $this->Form->input('volume') . '</div>';
        echo '<div id="publisher">' . $this->Form->input('publisher') . '</div>';
        ?>

    </span>

    <h4>Documents </h4>

    <table id="documents">
        <tr>
            <th>
                Mainfile
            </th>
            <th>
                URL/Filepath
            </th>
            <th>
            </th>
        </tr>
        <tr>
          <td>
              <input type="radio" name="file" value="files[0]" checked>
          </td>
          <td>
            <?php
            if (!empty(trim($publication->mainfile)) &&
               file_exists(WWW_ROOT . 'uploadedFiles' . DS . $publication->mainfile)
                ) {
                    echo '<a href="' . $this->request->webroot . './uploadedFiles/' . $publication->mainfile .
                    '">' . $publication->mainfile . '</a>';
            } else {
                echo $this->Form->input('files[0]', ['type' => 'file', 'label' => false]);
            }
            ?>
          </td>
          <td>
          </td>
        </tr>
        <?php
            $p = 1; $r = 0;
            foreach ($publication->documents as $document) {
                if ($document->remote) {
                    echo '<tr>
                        <td></td>
                        <td><a href="' . $document->filename . '">' . $document->filename . '</a><input type="hidden" name="external[' . $r . ']" value="' . $document->filename . '"></td>
                        <td><img onclick="$(this).parent().parent().remove();" src="/img/remove.png" width="16" height="16"></td>
                    </tr>';
                    $r++;
                } else {
                    echo '<tr>
                        <td><input type="radio" name="file" value="files[' . $p . ']"></td>
                        <td><a href="' . $this->request->webroot . './uploadedFiles/' . $document->filename . '"><input type="hidden" name="files[' . $p . ']" value="' . $document . '"></a></td>
                        <td><img onclick="$(this).parent().parent().remove();" src="/img/remove.png" width="16" height="16"></td>
                    </tr>';
                    $p++;
                }
            }
        ?>
    </table>

    <p onclick='javascript:addDocument(true, "/img/remove.png", <?=$r ?>, <?=$p ?>); return false;' class="addButton">
      Add external document
      <?php echo $this->Html->image('/img/add.png', ['width' => '16', 'height' => '16']); ?>
    </p>

    <p onclick='javascript:addDocument(false, "/img/remove.png", <?=$r ?>, <?=$p ?>); return false;' class="addButton">
      Upload PDF document
      <?php echo $this->Html->image('/img/add.png', ['width' => '16', 'height' => '16']); ?>
    </p>

    <div class="divider">
    </div>

    <h4>
        Paper Abstract
        <?php echo $this->Html->image('/img/info_icon.png', ['width' => '32', 'height' => '32', 'id' => 'info_icon']); ?>
    </h4>
    <div id="abstractInfoText">
        This additional information is optional.
        It is shown in the detailed view of the paper. The image is resized to 400x400.
    </div>
    <?=
    /* FILES */
    $this->Form->input('abstract');
    ?>

    <table>
        <tbody style="vertical-align: top;">
            <tr>
                <td style="width: 20%;">
                    Image which represents the paper
                </td>
                <td>
                    <?=
                    $this->Form->input('abstractphoto', ['type' => 'file', 'label' => false]);
                    ?>
                </td>
            </tr>
        </tbody>
    </table>
    <div id="imagePreview2"></div>
    <div id="currentThumb">

        <?php
            if ($publication->abstractphoto) {
                 echo  'Current paper image:' ;
                 echo $this->Html->link(
                        $this->Html->image('/uploadedFiles/abstractphotos/'
                        . $publication->abstractphoto), ('/uploadedFiles/abstractphotos/original-' . $publication->abstractphoto), ['escape' => false, 'class' => 'abstractPhoto']);
            }
        ?>
    </div>

    <div id="paperPreview">

    </div>
    <?= $this->Form->button(__('Submit')) ?>
    <?= $this->Form->end() ?>
</div>
