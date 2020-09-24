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