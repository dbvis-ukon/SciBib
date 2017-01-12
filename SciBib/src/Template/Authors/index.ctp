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
        <li><?= $this->Html->link($this->Html->image('/img/add.png', ['width' => '16', 'height' => '16']) . ' ' . __('New Author'), ['action' => 'add'], ['escape' => false])
?></li>
    </ul>
</nav>
<div class="authors index large-9 medium-8 columns content">

    <!-- Search Form -->
    <?php echo $this->Form->create(); ?>
    <fieldset>
        <legend><?php echo __('Authors Search', true); ?></legend>
        <table cellpadding="0" cellspacing="0">
            <tr>
                <th><?=
                    $this->Form->input('q', [
                        'label' => false
                    ]);
                    ?>
                </th> 
                <th><?= $this->Form->submit('search.png', ['type' => 'submit']); ?>
                    <?= $this->Html->link('Reset', ['action' => 'index']); ?>
                </th>
            </tr>
        </table>


    </fieldset>
    <?php echo $this->Form->end(); ?>

    <h3><?= __('Authors') ?></h3>
    <table cellpadding="0" cellspacing="0">
        <thead>
            <tr>
                <!-- <th><?= $this->Paginator->sort('id') ?></th> -->
                <th><?= $this->Paginator->sort('surname') ?></th>
                <th><?= $this->Paginator->sort('forename') ?></th>
                <th><?= $this->Paginator->sort('cleanname') ?></th>
                <th><?= 'Publications' ?></th>
                <th class="actions"><?= __('Actions') ?></th>
            </tr>
        </thead>
        <tbody>
            <?php foreach ($authors as $author): ?>
                <tr>
                   <!--  <td><?= $this->Number->format($author->id) ?></td> -->
                    <td><?= h($author->surname) ?></td>
                    <td><?= h($author->forename) ?></td>
                    <td><?= h($author->cleanname) ?></td>
                    <td><?= $this->Html->link(__(count($author->publications)), ['action' => 'view', $author->id]) ?></td>
                    <td class="actions">
                        <?= $this->Html->link(__('View'), ['action' => 'view', $author->id]) ?>
                    </td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
    <div class="paginator">
        <ul class="pagination">
            <?= $this->Paginator->prev('< ' . __('previous')) ?>
            <?= $this->Paginator->numbers() ?>
            <?= $this->Paginator->next(__('next') . ' >') ?>
        </ul>
        <p><?= $this->Paginator->counter() ?></p>
    </div>
</div>
