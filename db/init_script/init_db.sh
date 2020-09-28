#!/bin/bash

#  Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
#  This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.
#
#  SciBib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SciBib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SciBib.  If not, see <http://www.gnu.org/licenses/>.

echo "" > /var/log/mysql/mysql.log
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="CREATE DATABASE IF NOT EXISTS $SCIBIB_MYSQL_DATABASE;" >> /var/log/mysql/mysql.log
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="CREATE USER IF NOT EXISTS '$SCIBIB_MYSQL_USER'@'%' IDENTIFIED BY '$SCIBIB_MYSQL_PASSWORD'; FLUSH PRIVILEGES" >> /var/log/mysql/mysql.log
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="GRANT USAGE ON *.* TO '$SCIBIB_MYSQL_USER'@'%' IDENTIFIED BY '$SCIBIB_MYSQL_PASSWORD';"
mysql --user=root --password="$MYSQL_ROOT_PASSWORD" --execute="GRANT ALL PRIVILEGES ON $SCIBIB_MYSQL_DATABASE.* TO '$SCIBIB_MYSQL_USER'@'%' IDENTIFIED BY '$SCIBIB_MYSQL_PASSWORD'; FLUSH PRIVILEGES;" >> /var/log/mysql/mysql.log
