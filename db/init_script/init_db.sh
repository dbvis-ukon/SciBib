#!/bin/bash

echo "" > /var/log/mysql/mysql.log
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="CREATE DATABASE IF NOT EXISTS $SCIBIB_MYSQL_DATABASE;" >> /var/log/mysql/mysql.log
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="CREATE USER IF NOT EXISTS '$SCIBIB_MYSQL_USER'@'%' IDENTIFIED BY '$SCIBIB_MYSQL_PASSWORD'; FLUSH PRIVILEGES" >> /var/log/mysql/mysql.log
# mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="SET PASSWORD FOR '$SCIBIB_MYSQL_USER'@'%' = '$SCIBIB_MYSQL_PASSWORD';" >> /var/log/mysql/mysql.log
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="GRANT USAGE ON *.* TO '$SCIBIB_MYSQL_USER'@'%' IDENTIFIED BY '$SCIBIB_MYSQL_PASSWORD';"
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="GRANT ALL PRIVILEGES ON $SCIBIB_MYSQL_DATABASE.* TO '$SCIBIB_MYSQL_USER'@'%' IDENTIFIED BY '$SCIBIB_MYSQL_PASSWORD'; FLUSH PRIVILEGES;" >> /var/log/mysql/mysql.log
