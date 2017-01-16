<?php
/**
 * Copyright 2010 - 2015, Cake Development Corporation (http://cakedc.com)
 *
 * Licensed under The MIT License
 * Redistributions of files must retain the above copyright notice.
 *
 * @copyright Copyright 2010 - 2015, Cake Development Corporation (http://cakedc.com)
 * @license MIT License (http://www.opensource.org/licenses/mit-license.php)
 */

$activationUrl = [
    '_full' => true,
    'plugin' => 'CakeDC/Users',
    'controller' => 'Users',
    'action' => 'addPassword',
    isset($token) ? $token : ''
];
?>
<p>
    <?= __d('Users', 'Hi {0}', isset($username) ? $username : 'new User') ?>,
</p>
<p>
    <?= __d('Users', 'a new account was created for you on the Publication System.') ?>
</p>
<p>
    <strong><?= $this->Html->link(__d('Users', 'Add a new password to your account here'), $activationUrl) ?></strong>
</p>
<p>
    <?= __d('Users', "If the link is not correctly displayed, please copy the following address in your web browser {0}", $this->Url->build($activationUrl)) ?>
</p>
<p>
    <?= __d('Users', 'Thank you') ?>
</p>