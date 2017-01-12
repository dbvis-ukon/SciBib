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
        <li><?php echo $this->Html->image('/img/add.png', ['width' => '16', 'height' => '16']) . ' ' . 'Add Keywords by creating them on the publication edit page' ?></li>
    </ul>
</nav>
<div class="keywords index large-9 medium-8 columns content">
    <h3><?= __('Keywords') ?></h3>
    <table cellpadding="0" cellspacing="0">
        <tbody>
            <?php foreach ($keywords as $keyword): ?>
                <tr>
                    <td>
                        <?php
                        $tmp = $keyword->name;
                        echo $this->Html->link(__($tmp), ['action' => 'edit', $keyword->id])
                        ?>
                    </td>
                </tr>
            <?php endforeach; ?>
        </tbody>
    </table>
</div>
