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
use Cake\Core\Configure;
use Cake\Routing\Router;

$config = [
    'Users' => [
        //Table used to manage users
        'table' => 'CakeDC/Users.Users',
        //configure Auth component
        'auth' => true,
        //Public access control
        'publicAcl' => true,
        //Password Hasher
        'passwordHasher' => '\Cake\Auth\DefaultPasswordHasher',
        //token expiration, 1 hour
        'Token' => ['expiration' => 3600],
        'Email' => [
            //determines if the user should include email
            'required' => true,
            //determines if registration workflow includes email validation
            'validate' => false,
        ],
        'Registration' => [
            //determines if the register is enabled
            'active' => false,
            //determines if the reCaptcha is enabled for registration
            'reCaptcha' => false,
        ],
        'reCaptcha' => [
            //reCaptcha key goes here
            'key' => '',
            //reCaptcha secret
            'secret' => '',
            //use reCaptcha in registration
            'registration' => false,
            //use reCaptcha in login, valid values are false, true
            'login' => false,
        ],
        'Tos' => [
            //determines if the user should include tos accepted
            'required' => false,
        ],
        'Social' => [
            //enable social login
            'login' => false,
        ],
        'Profile' => [
            //Allow view other users profiles
            'viewOthers' => false,
            'route' => ['plugin' => 'CakeDC/Users', 'controller' => 'Users', 'action' => 'profile'],
        ],
        //Avatar placeholder
        //'Avatar' => ['placeholder' => 'CakeDC/Users.avatar_placeholder.png'],
        'RememberMe' => [
            //configure Remember Me component
            'active' => true,
            'Cookie' => [
                'name' => 'remember_me',
                'Config' => [
                    'expires' => '1 month',
                    'httpOnly' => true,
                ]
            ]
        ],
    ],
//default configuration used to auto-load the Auth Component, override to change the way Auth works
    'Auth' => [
        'loginAction' => [
            'plugin' => 'CakeDC/Users',
            'controller' => 'Users',
            'action' => 'login',
            'prefix' => false
        ],
        'authenticate' => [
            'all' => [
                'finder' => 'active',
            ],
            'CakeDC/Users.ApiKey',
            'CakeDC/Users.RememberMe',
            'Form',
        ],
        'authorize' => [
            'CakeDC/Users.Superuser',
            'CakeDC/Users.SimpleRbac',
        ],
    ],
];

return $config;
