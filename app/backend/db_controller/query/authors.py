from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, and_

from backend.db_controller.db import Authors
from backend.db_controller.db import Authors_publications

db = SQLAlchemy()


def getAuthorsAndCountPubs():
    db.session.execute("SET SESSION group_concat_max_len = 100000")
    result = [{**a[0].to_dict(), 'count': len(a[1].split(',')) if a[1] is not None else 0}
            for a in db.session.query(Authors, func.group_concat(Authors_publications.publication_id))\
                .outerjoin(Authors_publications, Authors.id == Authors_publications.author_id)\
                .group_by(Authors.id).all()]

    db.session.close()
    return result

def getAuthors():
    return [ a.to_dict() for a in Authors.query.all()]

def getAuthorById(id):
    result = db.session.query(Authors).filter(Authors.id == id).first()

    db.session.close()
    return result.to_dict() if result is not None else {}

def getAuthorsById(ids):
    # use a loop and not the IN operator to keep the ordering of the ids intact
    return [getAuthorById(id) for id in ids]

def getPubsOfAuthor(id):
    result = db.engine.execute(
        """
        SELECT pub.id, auth.id, pub.title, pub.journal, pub.doi, pub.year, pub.booktitle, pub.publisher, pub.thumb, group_concat(auth2.cleanname ORDER BY auth_pub2.position) AS authors
        FROM authors AS auth
        JOIN authors_publications AS auth_pub ON auth_pub.author_id = auth.id
        JOIN publications AS pub ON auth_pub.publication_id = pub.id
        JOIN authors_publications AS auth_pub2 ON auth_pub2.publication_id = pub.id
        JOIN authors AS auth2 ON auth_pub2.author_id = auth2.id
        WHERE auth.id = %s AND pub.public = 1
        GROUP BY pub.id
        """, (id,)
    )

    result = [{'pub_id': r[0],
               'auth_id': r[1],
               'title': r[2],
               'journal': r[3],
               'doi': r[4],
               'year': r[5],
               'booktitle': r[6],
               'publisher': r[7],
               'thumb': r[8],
               'authors': r[9].replace(',', ', ')
               } for r in result]
    return result

def getAuthorByNames(forename, surname):
    author = db.session.query(Authors).filter(and_(Authors.forename == forename, Authors.surname == surname)).first()

    db.session.close()
    return author.to_dict() if author is not None else {}

def addAuthor(session, **columns):
    if columns.get('surname') == '' or columns.get('forename') == '' or columns.get('cleanname') == '':
        raise ValueError('surname, forename and cleanname must not be empty')

    newAuthor = Authors(
        surname=columns['surname'],
        forename=columns['forename'],
        cleanname=columns['cleanname']
    )
    session.add(newAuthor)
    return newAuthor