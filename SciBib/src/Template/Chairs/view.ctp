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
        <li><?= $this->Html->link($this->Html->image('/img/edit.png', ['width' => '16', 'height' => '16']) . ' ' .__('Edit Chair'), ['action' => 'edit', $chair->id], ['escape' => false]) ?> </li>
        <li><?= $this->Html->link($this->Html->image('/img/university.png', ['width' => '16', 'height' => '16']) . ' ' . __('List Chairs'), ['action' => 'index'], ['escape' => false]) ?> </li>
    </ul>
</nav>
<div class="chairs view large-9 medium-8 columns content">
    <h3><?= h($chair->name) ?></h3>
    <table class="vertical-table">
        <tr>
            <th scope="row"><?= __('Name') ?></th>
            <td><?= h($chair->name) ?></td>
        </tr>
        <tr>
            <th scope="row"><?= __('Id') ?></th>
            <td><?= $this->Number->format($chair->id) ?></td>
        </tr>
    </table>
    
</div>
