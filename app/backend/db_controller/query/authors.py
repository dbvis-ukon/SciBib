from backend.db_controller.db import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import func, and_

from backend.db_controller.db import Authors
from backend.db_controller.db import Authors_publications

db = SQLAlchemy()


def getAuthorsAndCountPubs():
    """
    Get list of authors with publication count
    @return: list: list of athors and their publication counts [(dict: author, int: publication count)]
    """
    db.session.execute("SET SESSION group_concat_max_len = 100000")
    result = [{**a[0].to_dict(), 'count': len(a[1].split(',')) if a[1] is not None else 0}
            for a in db.session.query(Authors, func.group_concat(Authors_publications.publication_id))\
                .outerjoin(Authors_publications, Authors.id == Authors_publications.author_id)\
                .group_by(Authors.id).all()]

    db.session.close()
    return result

def getAuthors():
    """
    Get list of authors
    @return: list: list of authors [dict: author]
    """
    return [ a.to_dict() for a in Authors.query.all()]

def getAuthorById(id):
    """
    Get an author by id
    @param id: the database ID of the author
    @return: dict: author
    """
    result = db.session.query(Authors).filter(Authors.id == id).first()

    db.session.close()
    return result.to_dict() if result is not None else {}

def getAuthorsById(ids):
    """
    Get a list of authors by their database IDs. Uses a loop instead of SQLAlchemy IN operator in order to preserve
    the ordering.
    @param ids: list of database IDs
    @type ids: list(int)
    @return: list of authors
    @rtype: list(dict)
    """
    return [getAuthorById(id) for id in ids]

def getPubsOfAuthor(id):
    """
    Get publications of an author by ID.
    @param id: database ID of the author
    @type id: int
    @return: list of publications
    @rtype: list(dict)
    """
    result = db.engine.execute(
        text("""
        SELECT pub.id, auth.id, pub.title, pub.journal, pub.doi, pub.year, pub.booktitle, pub.publisher, pub.thumb, group_concat(auth2.cleanname ORDER BY auth_pub2.position) AS authors
        FROM authors AS auth
        JOIN authors_publications AS auth_pub ON auth_pub.author_id = auth.id
        JOIN publications AS pub ON auth_pub.publication_id = pub.id
        JOIN authors_publications AS auth_pub2 ON auth_pub2.publication_id = pub.id
        JOIN authors AS auth2 ON auth_pub2.author_id = auth2.id
        WHERE auth.id = %s AND pub.public = 1
        GROUP BY pub.id
        """), (id,)
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
    """
    Get an author by its name.
    @param forename: the forename of the author
    @type forename: string
    @param surname: the surname of the author
    @type surname: string
    @return: author
    @rtype: dcit
    """
    author = db.session.query(Authors).filter(and_(Authors.forename == forename, Authors.surname == surname)).first()

    db.session.close()
    return author.to_dict() if author is not None else {}

def addAuthor(session, **columns):
    """
    Add an author to the database
    @param session: An open database session
    @type session: SQLAlchemy session
    @param columns: A dict with keys for 'surname', 'forename', and 'cleanname'
    @type columns: dict
    @return: the newly created author object
    @rtype: Author object
    """
    if columns.get('surname') == '' or columns.get('forename') == '' or columns.get('cleanname') == '':
        raise ValueError('surname, forename and cleanname must not be empty')

    newAuthor = Authors(
        surname=columns['surname'],
        forename=columns['forename'],
        cleanname=columns['cleanname']
    )
    session.add(newAuthor)
    return newAuthor