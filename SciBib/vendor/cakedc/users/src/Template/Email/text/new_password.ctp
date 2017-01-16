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
<?= __d('Users', "Hi {0}", isset($username) ? $username : 'new User') ?>,

<?= __d('Users', 'a new account was created for you on the Publication System.') ?>

<?= __d('Users', "Please copy the following address in your web browser {0}", $this->Url->build($activationUrl)) ?>

<?= __d('Users', 'Thank you') ?>,

