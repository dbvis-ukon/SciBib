from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Keywords_publication
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addKeywordsPublications(session, **columns):
    """
    Add keyword <-> publication mapping to the database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param columns: a dict containing the 'keyword_id' and 'publication_id'
    @type columns: dict
    @return: the newly created KeywordsPublications object
    @rtype: KeywordsPublications object
    """
    if not isInt(columns.get('keyword_id', '') or not isInt(columns.get('publication_id', ''))):
        raise ValueError('Cannot add keywords-publication mapping. Keyword_id and publictation_id as numbers required.')


    newKeywordsPublications = Keywords_publication(
        keyword_id=columns['keyword_id'],
        publication_id=columns['publication_id'],
    )
    session.add(newKeywordsPublications)
    return newKeywordsPublications