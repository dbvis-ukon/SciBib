<!--
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
-->
<?php
echo $this->Html->css('publications_index.css');

// remove nav bar for public
if ($user['active']) {
    ?>
    <nav class="large-3 medium-4 columns" id="actions-sidebar">
        <ul class="side-nav">
            <li class="heading"><?= __('Actions') ?></li>
            <li><?= $this->Html->link($this->Html->image('/img/edit.png', ['width' => '16', 'height' => '16']) . ' ' . __('Edit Author'), ['action' => 'edit', $author->id], ['escape' => false]) ?> </li>
            <li><?= $this->Html->link($this->Html->image('/img/author.png', ['width' => '16', 'height' => '16']) . ' ' . __('List Authors'), ['action' => 'index'], ['escape' => false]) ?> </li>
        </ul>
    </nav>
<?php } ?>

<div class="authors view large-9 medium-8 columns content">
    <h3><?= h('Author') ?></h3>
    <table class="vertical-table">
        <tr>
            <th><?= __('Surname') ?></th>
            <td><?= h($author->surname) ?></td>
        </tr>
        <tr>
            <th><?= __('Forename') ?></th>
            <td><?= h($author->forename) ?></td>
        </tr>
        <tr>
            <th><?= __('Cleanname') ?></th>
            <td><?= h($author->cleanname) ?></td>
        </tr>
        <tr>
            <th><?= __('Website') ?></th>
            <td><?php
                if (!empty($author->website)) {
                    echo $this->Html->link($author->website);
                }
                ?></td>
        </tr>
        <tr>
            <th><?= __('Formatted Publications') ?></th>
            <td><?= $this->Html->link($this->Url->build('/?author='.$author->id, true), '/?author='.$author->id) ?></td>
        </tr>
    </table>
    <div class="related">
        <h4><?= __('Related Publications') ?></h4>
        <?php if (!empty($author->publications)) { ?>

        <?php
        $year = 0;
        foreach ($author->publications as $publication) {
        // check if the publication should be public
        if ($publication->public === true || $publication->published === true) {
        ?>

        <table class="publicationListEntry">
            <tbody>
            <tr>
                <td class="publicationThumbWrapper">
                    <?php
                    //Use the standard thumbnail if no thumb is available
                    if ($publication->thumb == null
                        || !file_exists(WWW_ROOT . 'uploadedFiles' . DS . 'thumbs' . DS . $publication->thumb)
                    ) {
                        echo $this->Html->image('/uploadedFiles/thumbs/default.png', ['width' => '100px', 'height' => '100px']);
                    } else {
                        echo $this->Html->image('/uploadedFiles/thumbs/' . $publication->thumb, ['width' => '100px', 'height' => '100px']);
                    }
                    ?>
                </td>
                <td>
                    <!--authors listed-->
                                                    <span class="publicationAuthors">
                                                        <?php
                                                        //print the authors with ',' - 'and'
                                                        $numAuthors = count($publication->authors);
                                                        $i = 0;
                                                        foreach ($publication->authors as $author):
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
                    <?= $this->Html->link(__($publication->title), ['controller' => 'Publications', 'action' => 'view', $publication->id]) . '  <br>' ?>
                    <span class="publicationBookTitle">
                                                        <?php
                                                        //publication type stuff 
                                                        echo $this->element('publicationText', ['publication' => $publication, 'renderCopyable' => true]);
                                                        ?>
                                                    </span></td>
                <?php
                }
                if ($year !== $publication->year) {
                    $year = $publication->year;
                    echo '<h4>' . $publication->year . '</h4>';
                }
                }
                } ?>
    </div>
