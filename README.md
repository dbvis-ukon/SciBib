# SciBib

SciBib is an online **Sci**entific **Bib**liography System. The aim of SciBib is to provide a system to organizes and distribute publications online. 

### Features

- Website to publish publications 
- Admin center - Add and edit publication, authors, keywords, categories 
- User management
- Filter publications by year, publication type, user 
- Publish publications as PDF files 
- Export bibtex functionality 

### Prerequisites

 What things you need to install the system

 - PHP 5.5.9 or greater 
 - Composer
 - MySQL 
 - Apache HTTP Server


### Installation

 - Install PHP and extensions
 ```
sudo apt install php7.0 php7.0-cli php7.0-intl php7.0-xsl php7.0-mbstring
```
 
 - Install [Composer](https://getcomposer.org/download/)
 ```
 curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer
```

 - Install MySQL database and PHP extension
 ```
 sudo apt install mysql-server php-mysql
 ```
 
 - Install Apache HTTP Server
  ```
 sudo apt install apache2 apache2-doc 
  ```
  
----------
 Use for this the ```scibib_db.sql``` sql file
 - Clone the git repository
```
git clone https://github.com/UKN-DBVIS/SciBib.git
```

 - Create the scibib mysql database. 


 - Use composer to get the required packages and plugins.
 Move to ```~/SciBib/``` and use the update composer command
```
composer update
```

 - Edit the ````~/SciBib/config/app.php `` 
 Create a custom salt security string
 ```
 echo -e "import uuid\nprint(uuid.uuid4().hex)" | python3
 ```
 
 Add your salt to the config (minimum length: 256 bits / 32 bytes)
```
...
'Security' => [
        'salt' => 'WIuOujq1mi7i40ZJMySHAMw1Q8z6Htdj',
    ],
...
```
Add the MySQL credentials
```
...        /**
             * CakePHP will use the default DB port based on the driver selected
             * MySQL on MAMP uses port 8889, MAMP users will want to uncomment
             * the following line and set the port accordingly
             */
            //'port' => 'nonstandard_port_number',
            
            'username' => 'username',
            'password' => 'secret',
            'database' => 'scibib',
            'encoding' => 'utf8',
            'timezone' => 'UTC',
            'cacheMetadata' => true,
            'log' => false,
...
```
 - Add the admin user. Move to ``` ~/SciBib/ ``` 
First create some tables in the database
```
 bin/cake migrations migrate -p CakeDC/Users
```
Add the superuser
```
bin/cake users addSuperuser
```
- Change the DocumentRoot in the Apache httpd.conf to use ```~/SciBib/``` directory 


## Deployment

***ToDo*** how to deploy live system

## Built With

* [CakePHP](https://github.com/cakephp/cakephp)


## License

This project is licensed under the Apache 2.0 - see the [LICENSE](LICENSE) file for details

Copyright 2017 [University Konstanz -  Data Analysis and Visualization Group](https://www.vis.uni-konstanz.de/)
