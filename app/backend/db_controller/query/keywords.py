from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Keywords


db = SQLAlchemy()


def getKeywords():
    result = [r.to_dict() for r in db.session.query(Keywords)]

    db.session.close()
    return result

def getKeywordByName(name):
    keyword = db.session.query(Keywords).filter(Keywords.name == name).first()

    db.session.close()
    return keyword.to_dict() if keyword is not None else {}

def addKeyword(session, **columns):
    if not columns.get('name', ''):
        raise ValueError('Keyword name required to add a new keyword.')

    newKeyword = Keywords(
        name=columns['name']
    )
    session.add(newKeyword)
    return newKeyword
