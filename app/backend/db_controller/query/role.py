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

from backend.db_controller.db import role


db = SQLAlchemy()

def addRole(session, **columns):
    """
    Inserts a new role to the database table 'Role'
    @param session: An open database session
    @param columns: a dict containing a 'name' key and optionally a 'description' key
    @return: the newly created role object
    """
    if columns.get('name', '') == '':
        raise ValueError("Cannot create a new role without role name")

    newRole = role(
        name=columns['name'],
        description=columns.get('description', '')
    )
    session.add(newRole)
    return newRole