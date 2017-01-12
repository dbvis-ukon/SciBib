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
        <h5 style="color:#004d40"><?= __('Menu') ?></h5>

        <li><?= $this->Html->link($this->Html->image('/img/publication.png', ['width' => '16', 'height' => '16']) . ' ' . __('Add, edit or delete a publication'), ['controller' => 'Publications', 'action' => 'privateIndex'], ['escape' => false]); ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/author.png', ['width' => '16', 'height' => '16']) . ' ' . __('Add, edit or delete an author'), ['controller' => 'Authors', 'action' => 'index'], ['escape' => false]) ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/keyword.png', ['width' => '16', 'height' => '16']) . ' ' . __('Edit or delete a keyword'), ['controller' => 'Keywords', 'action' => 'index'], ['escape' => false]) ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/category.png', ['width' => '16', 'height' => '16']) . ' ' . __('Add, edit or delete a category'), ['controller' => 'Categories', 'action' => 'index'], ['escape' => false]) ?></li>
        <li><?= $this->Html->link($this->Html->image('/img/change_password.png', ['width' => '16', 'height' => '16']) . ' ' . __('Change your user password'), ['controller' => 'users', 'action' => 'users/changePassword'], ['escape' => false]) ?></li>
        <?php
        // check if user is superuser and if show the add users menu point 
        if ($user['is_superuser']) {
            echo '<li>' . $this->Html->link($this->Html->image('/img/new_user.png', ['width' => '16', 'height' => '16']) . ' '
                    . __('Add, edit or delete a user'), ['controller' => 'Users', 'action' => 'users'], ['escape' => false]) . '</li>';
        }
        ?>
    </ul>
</nav>
<div class="Admincenter index large-9 medium-8 columns content">
    <h3><?= __('Latest changes:') ?></h3>



    <h3><?= __('Statistics:') ?></h3>

    <table>
        <tr>
            <th><?= __('Publications') ?></th>
            <th><?= __('Cite Keim') ?></th>
            <th><?= __('Cite Schreck') ?></th>
            <th><?= __('External cites') ?></th>
            <th><?= __('LS Keim') ?></th>
            <th><?= __('LS Schreck') ?></th>
            <th><?= __('External') ?></th>
        </tr>
        <tr>
            <td><?php echo $result[0]; ?></td>
            <td><?php echo $result[1]; ?></td>
            <td><?php echo $result[2]; ?></td>
            <td><?php echo $result[3]; ?></td>
            <td><?php echo $result[4]; ?></td>
            <td><?php echo $result[5]; ?></td>
            <td><?php echo $result[6]; ?></td>
        </tr>
    </table>

</div>
