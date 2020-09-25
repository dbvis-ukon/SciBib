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

from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from backend.db_controller.db import users
from flask_security.utils import hash_password


db = SQLAlchemy()

def addUser(session, **columns):
    """
    Add a new user to the database. At least a username and password are required
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param columns: a dict containing the columns to add.
    @type columns: dict
    @return: the new user object
    @rtype: User object
    """
    if columns.get('username', '') == '':
        raise ValueError('Cannot create a user without username')
    if columns.get('password', '') == '':
        raise ValueError('Cannot create a user without password')
    if len(columns.get('password', '')) < 6:
        raise ValueError('Password must be at least 6 characters long')

    newUser = users(
        first_name=columns.get('firstname', ''),
        last_name=columns.get('lastname', ''),
        username=columns['username'],
        email=columns.get('email', ''),
        password=hash_password(columns['password']),
        active=columns.get('active', 0),
        created=columns.get('created', datetime.now())
    )
    session.add(newUser)
    return newUser