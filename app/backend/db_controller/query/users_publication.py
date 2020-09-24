from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Users_publication
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addUsersPublication(session, **columns):
    """
    Add users <-> publication mapping to the database.
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param columns: a dict containing user_id and publication_id
    @type columns: dict
    @return: the new UsersPublications object
    @rtype: UsersPublication object
    """
    if not isInt(columns.get('user_id') or not isInt(columns.get('publication_id'))):
        raise ValueError('User_id and publication_id must be numbers')

    newUsersPublications = Users_publication(
        user_id=columns['user_id'],
        publication_id=columns['publication_id'],
    )
    session.add(newUsersPublications)
    return newUsersPublications