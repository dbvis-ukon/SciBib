<?php
/**
 * CakePHP(tm) : Rapid Development Framework (http://cakephp.org)
 * Copyright (c) Cake Software Foundation, Inc. (http://cakefoundation.org)
 *
 * Licensed under The MIT License
 * For full copyright and license information, please see the LICENSE.txt
 * Redistributions of files must retain the above copyright notice.
 *
 * @copyright     Copyright (c) Cake Software Foundation, Inc. (http://cakefoundation.org)
 * @link          http://cakephp.org CakePHP(tm) Project
 * @since         0.10.0
 * @license       http://www.opensource.org/licenses/mit-license.php MIT License
 */
$title = 'BIB Vis LS Keim';
?>
<!DOCTYPE html>
<html>
    <head>
        <?= $this->Html->charset() ?>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>
            <?= $title ?>:
            <?= $this->fetch('title') ?>
        </title>
        <?= $this->Html->meta('icon') ?>

        <?= $this->Html->css('bootstrap.min.css') ?>

        <?= $this->Html->css('base.css') ?>
        <?= $this->Html->css('cake.css') ?>

        <?= $this->Html->css('publications_view.css') ?>

        <?= $this->fetch('meta') ?>
        <?= $this->fetch('css') ?>
        <?= $this->fetch('script') ?>
    </head>
    <body>
        <?php
        //show header if the user is logged in and the site is not embedded
        if ($user['active'] && (!isset($isEmbedded) || !$isEmbedded['isEmbedded'])) {
            ?>
            <nav class = "top-bar expanded" data-topbar role = "navigation">
                <section class="top-bar-section">
                    <ul class="left">
                        <li class="name" >
                            <h1 style="color: #FFF !important; margin-left: 5px;">
                                Welcome, <?= $user['username'] ?>
                            </h1>
                        </li>
                    </ul>
                    <ul class="right">
                        <li><?= $this->Html->link($this->Html->image('/img/list.png', ['width' => '16', 'height' => '16']) . ' ' . __('Publications'), ['controller' => 'Publications', 'action' => 'index'], ['escape' => false]) ?></li>
                        <li><?= $this->Html->link($this->Html->image('/img/admin_icon.png', ['width' => '16', 'height' => '16']) . ' ' . __('Admincenter'), ['controller' => 'Admincenter', 'action' => 'index'], ['escape' => false]) ?></li>
                        <li><?= $this->Html->link($this->Html->image('/img/Logout.png', ['width' => '16', 'height' => '16']) . ' ' . __('Logout'), ['controller' => '', 'action' => 'logout'], ['escape' => false]) ?></li>
                    </ul>
                </section>
            </nav>
        <?php } ?>
        <?= $this->Flash->render() ?>
        <section class="container-fluid">
            <?= $this->fetch('content') ?>
        </section>
    </body>
</html>
