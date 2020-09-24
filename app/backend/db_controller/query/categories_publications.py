from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Categories_publications
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addCategoriesPublications(session, **columns):
    """
    Add categories <-> publications mapping to the database.
    @param session: An open database session
    @type session: SQLAlchemy session
    @param columns: a dict with keys for the 'category_id' and 'publication_id' to add
    @type columns: dict
    @return: the newly created CategoryPublications object
    @rtype: CategoryPublications object
    """
    if not isInt(columns.get('category_id', '') or not isInt(columns.get('publication_id', ''))):
        raise ValueError('Category_id and publication_id must be numbers')

    newAuthorsPublications = Categories_publications(
        category_id=columns['category_id'],
        publication_id=columns['publication_id'],
    )
    session.add(newAuthorsPublications)
    return newAuthorsPublications