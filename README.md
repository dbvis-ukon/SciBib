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

 - Install some tools (in most cases these will already be installed)
 ``` 
 sudo apt install unzip
 ```

 - Install PHP and extensions
 ```
sudo apt install php7.0 php7.0-cli php7.0-intl php7.0-xsl php7.0-mbstring php7.0-zip php7.0-sqlite php7.0-gd
```
 
 - Install [Composer](https://getcomposer.org/download/)
 ```
 curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer
```

 - Install MySQL database and PHP extension
 ```
 sudo apt install mysql-server php-mysql
 ```
 
 - Install Apache HTTP Server and enable the rewrite mod
  ```
 sudo apt install apache2 apache2-doc libapache2-mod-php7.0
 sudo a2enmod rewrite
  ```
  
  - Change the settings to let Apache use rewrite on SciBib
  ```
 /etc/apache2/sites-available/default
 <Directory /your/path/to/SciBib>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride All
                Order allow,deny
                allow from all
 </Directory>
 ```
  
----------

 - Clone the git repository
 ```
 git clone https://github.com/UKN-DBVIS/SciBib.git
 ```

 - Create the scibib mysql database. Use for this the ```scibib_db.sql``` sql file.
 ```
 mysql -u root -p < scibib_db.sql 
 ```

 - Use composer to get the required packages and plugins.
 Move to ```~/SciBib/``` and use the update composer command
 ```
 cd SciBib
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
            
            'username' => 'CHANGEME',
            'password' => 'CHANGEME',
            'database' => 'scibib',
            'encoding' => 'utf8',
            'timezone' => 'UTC',
            'cacheMetadata' => true,
            'log' => false,
 ...
 ```
 - Add the admin user. Move to ``` ~/SciBib/ ``` 
First create some tables in the database. In case an error `1050 Table 'users' already exists [...]` is shown, you can ignore it.
```
 chmod +x bin/cake
 bin/cake migrations migrate -p CakeDC/Users
```


Add the superuser
```
bin/cake users addSuperuser
```

- Create a symlink to make SciBib accessible to Apache2
``` 
ln -s /home/ubuntu/litmgmt/SciBib/SciBib /var/www/html/SciBib
```

- Change permissions so that Apache2 can access the files
```
chown -R www-data /home/ubuntu/litmgmt/SciBib/*
```

- Patch users directory
``` 
sudo rm -rf /home/ubuntu/litmgmt/SciBib/SciBib/vendor/cakedc/users/
wget https://github.com/UKN-DBVIS/SciBib/archive/master.zip
unzip master.zip
sudo cp -r SciBib-master/SciBib/vendor/cakedc/users litmgmt/SciBib/SciBib/vendor/cakedc/
sudo chown -R www-data litmgmt/SciBib/SciBib/vendor/cakedc/*
sudo chgrp -R www-data litmgmt/SciBib/SciBib/vendor/cakedc/*
sudo services apache2 restart
```

- For productive usage, run the command `mysql_secure_installation` to secure the MYSQL db.

## Deployment

Steps as seen as in the Installation process above.

## Troubleshooting

- If ```composer update``` fails, be sure to have installed all required PHP extensions. 
  Especially the php-intl and MYSQL extensions. 


## Built With

* [CakePHP](https://github.com/cakephp/cakephp)


## License

This project is licensed under the Apache 2.0 - see the [LICENSE](LICENSE) file for details

Copyright 2017 [University Konstanz -  Data Analysis and Visualization Group](https://www.vis.uni-konstanz.de/)
