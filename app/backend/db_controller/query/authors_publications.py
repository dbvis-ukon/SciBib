from backend.db_controller.db import SQLAlchemy

from backend.db_controller.db import Authors_publications
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addAuthorsPublications(session, **columns):
    """
    Add authors <-> publications mapping to the database
    @param session: An open database session
    @type session: SQLAlchemy Session
    @param columns: a dict containing an 'author_id', 'publication_id' and the 'position' of the author in the paper
    @type columns: dict
    @return: the newly created AuthorPublications object
    @rtype: AuthorsPublication object
    """
    if not isInt(columns.get('author_id', '') or not isInt(columns.get('publication_id'))) or not isInt(columns.get('position')):
        raise ValueError('Author_id, publication_id and position must be numbers')

    newAuthorsPublications = Authors_publications(
        author_id=columns['author_id'],
        publication_id=columns['publication_id'],
        position=columns['position']
    )
    session.add(newAuthorsPublications)
    return newAuthorsPublications