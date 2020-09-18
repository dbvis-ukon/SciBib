from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Authors_publications
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addAuthorsPublications(session, **columns):
    if not isInt(columns.get('author_id', '') or not isInt(columns.get('publication_id'))) or not isInt(columns.get('position')):
        raise ValueError('Author_id, publication_id and position must be numbers')

    newAuthorsPublications = Authors_publications(
        author_id=columns['author_id'],
        publication_id=columns['publication_id'],
        position=columns['position']
    )
    session.add(newAuthorsPublications)
    return newAuthorsPublications