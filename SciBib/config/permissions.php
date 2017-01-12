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
/*
 * IMPORTANT:
 * This is an example configuration file. Copy this file into your config directory and edit to
 * setup your app permissions.
 *
 * This is a quick roles-permissions implementation
 * Rules are evaluated top-down, first matching rule will apply
 * Each line define
 *      [
 *          'role' => 'role' | ['roles'] | '*'
 *          'prefix' => 'Prefix' | , (default = null)
 *          'plugin' => 'Plugin' | , (default = null)
 *          'controller' => 'Controller' | ['Controllers'] | '*',
 *          'action' => 'action' | ['actions'] | '*',
 *          'allowed' => true | false | callback (default = true)
 *      ]
 * You could use '*' to match anything
 * 'allowed' will be considered true if not defined. It allows a callable to manage complex
 * permissions, like this
 * 'allowed' => function (array $user, $role, Request $request) {}
 *
 * Example, using allowed callable to define permissions only for the owner of the Posts to edit/delete
 *
 * (remember to add the 'uses' at the top of the permissions.php file for Hash, TableRegistry and Request
  [
  'role' => ['user'],
  'controller' => ['Posts'],
  'action' => ['edit', 'delete'],
  'allowed' => function(array $user, $role, Request $request) {
  $postId = Hash::get($request->params, 'pass.0');
  $post = TableRegistry::get('Posts')->get($postId);
  $userId = Hash::get($user, 'id');
  if (!empty($post->user_id) && !empty($userId)) {
  return $post->user_id === $userId;
  }
  return false;
  }
  ],
 */

return [
    'Users.SimpleRbac.permissions' => [
        [
            // public user for viewing the publications index and the view 
            'role' => '*',
            'controller' => ['Publications', 'Authors'],
            'action' => ['Index', 'view'],
            'allowed' => true,
        ],
        [
            // normal user for viewing change password and logout 
            'role' => 'user',
            'plugin' => 'CakeDC/Users',
            'controller' => 'Users',
            'action' => ['change_password', 'new_password', 'add_password', 'logout'],
            'allowed' => true,
        ],
        [
            // normal users are not allowed to create new users
            'role' => 'user',
            'plugin' => 'CakeDC/Users',
            'controller' => 'Users',
            'action' => ['*'],
            'allowed' => false,
        ],
        [
            // normal users can access everything else
            'role' => 'user',
            'controller' => '*',
            'action' => '*',
        ],
        ]];
