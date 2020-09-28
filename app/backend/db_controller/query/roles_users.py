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
from sqlalchemy.sql import text

from backend.db_controller.helper import isInt


db = SQLAlchemy()


def addRolesUsers(session, **columns):
    """
    Add roles <-> users mapping to database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param columns: a dict containing the keys 'user_id' and 'role_id'
    @type columns: dict
    """
    if not isInt(columns.get('user_id', '')) or not isInt(columns.get('role_id', '')):
        raise ValueError('Cannot add roles-user mapping. User_id and role_id as numbers required.')

    session.execute(
        text("""
        INSERT INTO roles_users(user_id, role_id) VALUES (:userid, :roleid)
        """), {'userid': columns['user_id'], 'roleid': columns['role_id']})

# def getRolesUsersByUser(session, user_id):
#     res = session.execute(
#         """
#         SELECT * FROM roles_users WHERE user_id = :userid
#         """, {'userid': user_id}
#     )
#     return [{'role_id': r.role_id} for r in res]

def deleteRolesUsersByUser(session, user_id):
    """
    Remove roles <-> users mappings from database by user_id
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param user_id: the user_id to remove the mappings from
    @type user_id: int
    """
    session.execute(
        text("""
        DELETE FROM roles_users
        WHERE user_id = :userid
        """), {'userid': user_id}
    )

def deleteRolesUsersByRole(session, role_id):
    """
    Remove all roles <-> users mapping by role_id
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param role_id: the role_id to remove the mappings from
    @type role_id: int
    """
    session.execute(
        text("""
        DELETE FROM roles_users
        WHERE role_id = :roleid
        """), {'roleid': role_id}
    )