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