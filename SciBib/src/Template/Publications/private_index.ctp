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
<nav class="large-3 medium-4 columns" id="actions-sidebar">
    <ul class="side-nav">
        <li class="heading"><?= __('Actions') ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/add.png', ['width' => '16', 'height' => '16']) . ' ' . __('New Publication'), ['action' => 'add'], ['escape' => false]) ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/publication.png', ['width' => '16', 'height' => '16']) . ' ' . __('Public Publications'), ['action' => 'index', 'year' => 'lastTwoYears'], ['escape' => false]) ?></li>
    </ul>
</nav>
<div class="publications index large-9 medium-8 columns content">
    <!-- Search Form -->
    <?php echo $this->Form->create(); ?>
    <fieldset>
        <legend><?php echo __('Publication Search', true); ?></legend>
        <table cellpadding="0" cellspacing="0">
            <tr>
                <th><?php
                    echo $this->Form->input('q', [
                        'label' => false
                    ]);
                    ?>
                </th> 
                <th><?= $this->Form->submit('search.png', ['type' => 'submit']); ?>
                    <?= $this->Html->link('Reset', ['action' => 'privateIndex']); ?>
                </th>
            </tr>
            <tr> <p  style="font-size: 0.8rem"> Search the publication list for authors, titles,  years, etc.</p> </tr>
        </table>

    </fieldset>
    <?php echo $this->Form->end(); ?>

    <?php
    //Show the found authors 
    if ($authors) {
        echo ' <h3> Authors </h3>';
        foreach ($authors as $author) {
            echo $this->Html->link(($author->forename . ', ' . $author->surname), ['controller' => 'authors', 'action' => 'view', $author->id]) . '<br>';
        }
        echo '<br>';
    }
    ?>

    <h3><?= __('Publications') ?></h3>
    <?php
    $year = 0;
    foreach ($publications as $publication) {
        if ($year != $publication->year) {
            $year = $publication->year;
            echo '<h4>' . $publication->year . '</h4>';
        }
        //KOPS 
        if ($publication['kops'] == true) {
            echo ' <a href="' . $publication['kops'] . '" title="Archived in KOPS" target="_blank"><font color="green">&#9632;</font></a> - ';
        }
        //title
        echo $this->Html->link(__($publication->title), ['action' => 'view', $publication->id]) . '&nbsp&nbsp';
        //edit 
        echo $this->Html->link($this->Html->image('/img/edit.png', ['width' => '16', 'height' => '16']), ['action' => 'edit', $publication->id], ['escape' => false]) . '&nbsp&nbsp';
        //delete
        echo $this->Form->postLink($this->Html->image('/img/remove.png', ['width' => '16', 'height' => '16']) . ' '
                . __(''), ['action' => 'delete', $publication->id], ['escape' => false,
            'confirm' => __('Are you sure you want to delete {0}?', $publication->title)]) . '<br>';
    }
    ?>
</div>
