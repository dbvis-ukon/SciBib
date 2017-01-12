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
?>

<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/edit.png', ['width' => '16', 'height' => '16']) . ' ' . __('Edit Category'), ['action' => 'edit', $category->id], ['escape' => false]) ?> </li>
        <li><?= $this->Html->link($this->Html->image('/img/category.png', ['width' => '16', 'height' => '16']) . ' ' . __('List Categories'), ['controller' => 'Categories', 'action' => 'index'], ['escape' => false]) ?></li>
    </ul>
</nav>
<div class="categories view large-9 medium-8 columns content">
    <h3><?= h($category->name) ?></h3>
    <table class="vertical-table">
        <tr>
            <th><?= __('Name') ?></th>
            <td><?= h($category->name) ?></td>
        </tr>
        <tr>
            <th><?= __('Parent Category') ?></th>
            <td><?= $category->has('parent_category') ? $this->Html->link($category->parent_category->name, ['controller' => 'Categories', 'action' => 'view', $category->parent_category->id]) : '' ?></td>
        </tr>
    </table>
    <div class="related">
        <h4><?= __('Related Categories') ?></h4>
        <?php if (!empty($category->child_categories)): ?>
            <table cellpadding="0" cellspacing="0">
                <tr>
                    <th><?= __('Name') ?></th>
                </tr>
                <?php foreach ($category->child_categories as $childCategories): ?>
                    <tr>
                        <td class="actions">
                            <?= $this->Html->link(($childCategories->name), ['controller' => 'Categories', 'action' => 'view', $childCategories->id]) ?>

                        </td>
                    </tr>
                <?php endforeach; ?>
            </table>
        <?php endif; ?>
    </div>
    <h3><?= __('Related Publications') ?></h3>
    <div class="related">
        <?php if (!empty($category->publications)): ?>


            <?php
            $year = 0;
            foreach ($category->publications as $publication):
                // check if the publication should be public
                if ($publication->public === true || $publication->published === true):
                    ?>

                    <table class = "publicationListEntry"> <tbody><tr>  <td class = "publicationThumbWrapper">
                                    <?php
                                    //Use the standard thumbnail if no thumb is available
                                    if ($publication->thumb == null
                                                        || !file_exists(WWW_ROOT . 'uploadedFiles' . DS . "thumbs" . DS . $publication->thumb)) {
                                        echo $this->Html->image('/uploadedFiles/thumbs/default.png', ['width' => '100px', 'height' => '100px']);
                                    } else {
                                        echo $this->Html->image('/uploadedFiles/thumbs/' . $publication->thumb, ['width' => '100px', 'height' => '100px']);
                                    }
                                    ?>
                                </td> <td>
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
                                    <?= $this->Html->link(__($publication->title), ['action' => 'view', $publication->id]) . '  <br>' ?>
                                    <span class="publicationBookTitle">
                                        <?php
                                        //publication type stuff 
                                        echo $this->element('publicationText', ['publication' => $publication, 'renderCopyable' => true]);
                                        ?>
                                    </span> </td>
                                <?php
                            endif;
                            if ($year !== $publication->year) {
                                $year = $publication->year;
                                echo '<h4>' . $publication->year . '</h4>';
                            }
                        endforeach;
                        ?>
                    <?php endif; ?>
                    </div>
                    </div>