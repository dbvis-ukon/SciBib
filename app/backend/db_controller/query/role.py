from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import role


db = SQLAlchemy()

def addRole(session, **columns):
    if columns.get('name', '') == '':
        raise ValueError("Cannot create a new role without role name")

    newRole = role(
        name=columns['name'],
        description=columns.get('description', '')
    )
    session.add(newRole)
    return newRole