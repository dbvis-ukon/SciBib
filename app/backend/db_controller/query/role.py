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