# SciBib

[![Foo](scibib.png)](https://bib.dbvis.de)

An implementation for an online Scientific Bibliography System to organize and distribute publications online while having 
full control over the publication system.

See https://bib.dbvis.de for a running instance of SciBib.

See https://webdev.dbvis.de for a website using the JSON API.

#### Features

 * Website to publish publications
 * User-Management
 * Admin-Center (Add/edit/delete publications, authors, keywords, categories)
 * Filter Functionality 
 * Export bibtex support
 * JSON API
 * Responsive Design
 

## Deploy SciBib
Start by executing these first 6 steps and then continue either with deployment *A)* or deployment *B)* depending on your setup.

0. Clone repository:

    `git clone scibib`

1. Add your own `favicon.png` to `app/frontend/static/images/favicon.ico`.

2. Add your own `logo.png` to `app/frontend/static/images/logo.png`.

3. Edit the default welcome message at `app/frontend/templates/includes/welcome_msg.html`

4. Generate a password salt: 

    `echo -n "value" | openssl dgst -sha1 -hmac "key"` 

5. Update the environment variables in `.env` (Use the password salt generated in the last step for `SECURITY_PASSWORD_SALT`):

   ```shell script
    ...
   
   SCIBIB_EMAIL_SENDER=mail.user@mail.server.com
   SCIBIB_BIND_ADDRESS=0.0.0.0
   SCIBIB_BIND_PORT=8080

   MAIL_SERVER=mail.server.com
   MAIL_PORT=465
   MAIL_USE_SSL=true
   MAIL_USERNAME=user

   SECURITY_PASSWORD_SALT=57443a4c052350a44638835d64fd66822f813319
   ```

### A) Deploy all Docker
Deploy SciBib with both, a docker container for a MariaDB database and a docker container for SciBib.

0. Update the MYSQL passwords and db name in `.env`:
    ```
    MYSQL_ROOT_PASSWORD=very_strong_password
    # SCIBIB_MYSQL_HOST=db
    SCIBIB_MYSQL_DATABASE=scibib
    SCIBIB_MYSQL_USER=scibib_user
    SCIBIB_MYSQL_PASSWORD=very_strong_password2
    ...
   ```

1. Add executable permissions to init script: 

    `chmod +x db/init_script/init_db.sh`

2. Start the system via docker-compose: 

    `docker-compose -f docker-compose-db.yml up -d`

3. Initialize database:

    `docker exec scibib bash -c "python3 /srv/scibib/init.py"`

4. Update permissions of the static folder to `www-data`:

    `sudo chown -R www-data:www-data frontend/static`

5. Visit SciBib at `$SCIBIB_BIND_ADDRESS:$SCIBIB_BIND_PORT`

6. The default login credentials are user `admin` and password `superuser`. **Log in and navigate to Admincenter->User-Management 
   to edit the password of the admin user**.

### B) Deploy with an external database
Deploy SciBib with an external MariaDB database and a docker container for SciBib.

0. Create a MariaDB database and user if no database is already existing:

    a) `CREATE DATABASE scibib;`
    
    b) `CREATE USER 'scibib_user'@'host' IDENTIFIED BY 'very_strong_password2';`
    
    c) `GRANT ALL PRIVILEGES ON scibib.* TO 'scibib_user'@'host';`
    
    d) `FLUSH PRIVILEGES`
    
1. Update the MYSQL credentials in `.env`:
    ```
    # MYSQL_ROOT_PASSWORD=very_strong_password
    SCIBIB_MYSQL_HOST=host
    SCIBIB_MYSQL_DATABASE=scibib
    SCIBIB_MYSQL_USER=scibib_user
    SCIBIB_MYSQL_PASSWORD=very_strong_password2
    ...
   ```    

2. Start the system via docker-compose (Make sure the database server is reachable when executing this command):

    `docker-compose up -d`

4. Update permissions of the static folder to `www-data`:

    `sudo chown -R www-data:www-data app/frontend/static`

5. The default login credentials are user `admin` and password `superuser`. **Log in and navigate to Admincenter->User-Management 
   to edit the password of the admin user**.

# Credits

The system was developed with the aid of the following OpenSource libraries and frameworks:

#### Frontend

* [jQuery](https://github.com/jquery/jquery)
* [Bootstrap](https://github.com/twbs/bootstrap)
* [DataTables-Responsive-Bootstrap4](https://github.com/DataTables/Dist-DataTables-Responsive-Bootstrap4)
* [Select2](https://github.com/select2/select2)
* [select2-bootstrap4-theme](https://github.com/ttskch/select2-bootstrap4-theme)
* [SortableJS](https://github.com/SortableJS/Sortable)
* [Font Awesome](https://github.com/onface/font-awesome)
* [Animate.css](https://github.com/animate-css/animate.css)
* [Bibtex](https://github.com/digitalheir/bibtex-js)

#### Backend Python Libs

* [Flask](https://github.com/pallets/flask)
* [Flask-SQLAlchemy](https://github.com/pallets/flask-sqlalchemy)
* [Flask-Security-Too](https://github.com/Flask-Middleware/flask-security)
* [SQLAlchemy-serializer](https://github.com/n0nSmoker/SQLAlchemy-serializer)
* [mysqlclient](https://github.com/PyMySQL/mysqlclient-python)
* [bibtexparser](https://github.com/sciunto-org/python-bibtexparser)
* [Pillow](https://github.com/python-pillow/Pillow)
* [gunicorn](https://github.com/benoitc/gunicorn)

# License

This project is licensed under GNU GPLv3. See the [LICENSE](LICENSE) file for details.

Copyright 2020 [University of Konstanz - Data Analysis and Visualization Group](https://vis.uni-konstanz.de).