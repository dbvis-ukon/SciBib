from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Categories_publications
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addCategoriesPublications(session, **columns):
    if not isInt(columns.get('category_id', '') or not isInt(columns.get('publication_id', ''))):
        raise ValueError('Category_id and publication_id must be numbers')

    newAuthorsPublications = Categories_publications(
        category_id=columns['category_id'],
        publication_id=columns['publication_id'],
    )
    session.add(newAuthorsPublications)
    return newAuthorsPublications