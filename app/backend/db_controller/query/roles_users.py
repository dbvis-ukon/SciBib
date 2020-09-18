from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.helper import isInt


db = SQLAlchemy()


def addRolesUsers(session, **columns):
    if not isInt(columns.get('user_id', '')) or not isInt(columns.get('role_id', '')):
        raise ValueError('Cannot add roles-user mapping. User_id and role_id as numbers required.')

    session.execute(
        """
        INSERT INTO roles_users(user_id, role_id) VALUES (:userid, :roleid)
        """, {'userid': columns['user_id'], 'roleid': columns['role_id']})

# def getRolesUsersByUser(session, user_id):
#     res = session.execute(
#         """
#         SELECT * FROM roles_users WHERE user_id = :userid
#         """, {'userid': user_id}
#     )
#     return [{'role_id': r.role_id} for r in res]

def deleteRolesUsersByUser(session, user_id):
    session.execute(
        """
        DELETE FROM roles_users
        WHERE user_id = :userid
        """, {'userid': user_id}
    )

def deleteRolesUsersByRole(session, role_id):
    session.execute(
        """
        DELETE FROM roles_users
        WHERE role_id = :roleid
        """, {'roleid': role_id}
    )