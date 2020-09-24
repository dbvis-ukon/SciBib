from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Keywords


db = SQLAlchemy()


def getKeywords():
    """
    Get a list of all keywords
    @return: a list of keywords
    @rtype: list(dict)
    """
    result = [r.to_dict() for r in db.session.query(Keywords)]

    db.session.close()
    return result

def getKeywordByName(name):
    """
    Get a keyword by its name
    @param name: the name of the keyword
    @type name: string
    @return: the keyword info
    @rtype: dict
    """
    keyword = db.session.query(Keywords).filter(Keywords.name == name).first()

    db.session.close()
    return keyword.to_dict() if keyword is not None else {}

def addKeyword(session, **columns):
    """
    Add a keyword to the database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param columns: A dict containing the 'name' of the keyword
    @type columns: dict
    @return: the newly created keyword object
    @rtype: keyword object
    """
    if not columns.get('name', ''):
        raise ValueError('Keyword name required to add a new keyword.')

    newKeyword = Keywords(
        name=columns['name']
    )
    session.add(newKeyword)
    return newKeyword
