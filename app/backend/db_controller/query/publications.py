#
   Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
   This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.

   SciBib is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   SciBib is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with SciBib.  If not, see <http://www.gnu.org/licenses/>.

#
#  SciBib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SciBib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SciBib.  If not, see <http://www.gnu.org/licenses/>.
#
#  SciBib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SciBib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SciBib.  If not, see <http://www.gnu.org/licenses/>.

from backend.db_controller.db import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import func, true, or_, false
from sqlalchemy.sql.expression import literal_column
from backend.db_controller.db import Documents, \
    Publications, Authors, Authors_publications, Categories, Categories_publications, Keywords_publication, \
    Keywords
import json

db = SQLAlchemy()

def uniquify(l):
    """
    Uniquify list of dicts
    @param l: a list of dicts
    @type l: list(dict)
    @return: a list with only unique dicts
    @rtype: list(dict)
    """
    s = set([json.dumps(i) for i in l])
    return [json.loads(i) for i in s]

def uniquifySorted(l):
    """
    Uniquify list of dicts + keep ordering
    @param l: list of dicts
    @type l: list(dict)
    @return: a list with only unique dicts while keeping the initial ordering
    @rtype: list(dict)
    """
    s = set([json.dumps(i) for i in l])
    u = [json.loads(i) for i in s]
    return sorted(u, key=lambda x: l.index(x))

def getPubAndAuthorsAndDocs():
    """
    Get a dict containing all publications + their authors and documents enumerated from 0 to n-1 as dict,
    e.g. {1: pub_dict_1, 2: pub_dict_2}.
    @return: A dict enumerating the publications
    @rtype: dict
    """
    # default is 1024 and too small for this query
    db.session.execute("SET SESSION group_concat_max_len = 100000")

    result = {i: {**r[0].to_dict(),
                'authors': uniquifySorted([{'id': a,
                             'forename': r[2].split(',')[j] if r[2] is not None else '',
                             'surname': r[3].split(',')[j] if r[3] is not None else '',
                             'cleanname': r[4].split(',')[j] if r[4] is not None else ''
                                            } for j, a in enumerate(r[1].split(',') if r[1] is not None else [])]),
                'documents': uniquify(
                    [
                        {
                        'id': d,
                        'publication_id': r[6].split(';')[j] if r[6] is not None else '',
                        'visible': r[7].split(';')[j] if r[7] is not None else '',
                        'remote': r[8].split(';')[j] if r[8] is not None else '',
                        'filename': r[9].split(';')[j] if r[9] is not None else ''
                         } for j, d in enumerate(r[5].split(';') if r[5] != None else [])
                    ])
                  }
               for i, r in enumerate(db.session.query(
                Publications,
                func.group_concat(func.ifnull(Authors.id, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.forename, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.surname, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.cleanname, '').op("ORDER BY")(Authors_publications.position)).label('authors'),
                func.group_concat(func.ifnull(Documents.id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.publication_id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.visible, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.remote, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.filename, '').op('SEPARATOR')(literal_column('\';\'')))
                )\
                .outerjoin(Documents, Documents.publication_id == Publications.id)\
                #.filter(Documents.publication_id == Publications.id )\
                .filter(Publications.id == Authors_publications.publication_id) \
                .filter(Authors.id == Authors_publications.author_id) \
                #.filter(Documents.visible == 1 or Documents.visible == None) \
                .group_by(Publications.id)\
                .order_by(Publications.year.desc(), Publications.id.desc())
                .all())}

    db.session.close()
    return result

def getPubAndAuthorsAndDocsOffset(offset, limit):
    """
    Get a chunk of publications with corresponding authors and documents starting at 'offset' and using 'limit' publications
    @param offset: database table offset
    @type offset: int
    @param limit: number of publications to fetch from offset
    @type limit: int
    @return: dict enumerating the publications
    @rtype: dict
    """
    # default is 1024 and too small for this query
    db.session.execute("SET SESSION group_concat_max_len = 100000")

    result = {i: {**r[0].to_dict(),
                'authors': uniquifySorted([{'id': a,
                             'forename': r[2].split(',')[j] if r[2] is not None else '',
                             'surname': r[3].split(',')[j] if r[3] is not None else '',
                             'cleanname': r[4].split(',')[j] if r[4] is not None else ''
                                            } for j, a in enumerate(r[1].split(',') if r[1] is not None else [])]),
                'documents': uniquify(
                    [
                        {
                        'id': d,
                        'publication_id': r[6].split(';')[j] if r[6] is not None else '',
                        'visible': r[7].split(';')[j] if r[7] is not None else '',
                        'remote': r[8].split(';')[j] if r[8] is not None else '',
                        'filename': r[9].split(';')[j] if r[9] is not None else ''
                         } for j, d in enumerate(r[5].split(';') if r[5] is not None else [])
                    ])
                  }
               for i, r in enumerate(db.session.query(
                Publications,
                func.group_concat(func.ifnull(Authors.id, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.forename, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.surname, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.cleanname, '').op("ORDER BY")(Authors_publications.position)).label('authors'),
                func.group_concat(func.ifnull(Documents.id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.publication_id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.visible, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.remote, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.filename, '').op('SEPARATOR')(literal_column('\';\'')))
                )\
                .outerjoin(Documents, Documents.publication_id == Publications.id)\
                .filter(Publications.id == Authors_publications.publication_id) \
                .filter(Authors.id == Authors_publications.author_id) \
                .group_by(Publications.id)\
                .order_by(Publications.year.desc(), Publications.id.desc())
                .offset(offset)
                .limit(limit))}

    db.session.close()
    return result

def getPubAndAuthorsAndDocsWithFilter(filters):
    """
    Get publications with authors and documents after applying filters.
    Filters can be
      * by year
      * by type
      * by keyword
      * by substring matching
    @param filters: dict with filter criteria
    @type filters: dict
    @return: an enumerated dict of filtered publications
    @rtype: dict
    """
    # default is 1024 and too small for this query
    db.session.execute("SET SESSION group_concat_max_len = 100000")

    result = {i: {**r[0].to_dict(),
                'authors': uniquifySorted(
                    [
                        {'id': a,
                             'forename': r[2].split(',')[j] if r[2] is not None else '',
                             'surname': r[3].split(',')[j] if r[3] is not None else '',
                             'cleanname': r[4].split(',')[j] if r[4] is not None else ''
                        } for j, a in enumerate(r[1].split(',') if r[1] is not None else [])
                    ]),
                'documents': uniquify(
                    [
                        {
                        'id': d,
                        'publication_id': r[6].split(';')[j] if r[6] is not None else '',
                        'visible': r[7].split(';')[j] if r[7] is not None else '',
                        'remote': r[8].split(';')[j] if r[8] is not None else '',
                        'filename': r[9].split(';')[j] if r[9] is not None else ''
                         } for j, d in enumerate(r[5].split(';') if r[5] is not None else [])
                    ]),
                'keywords': uniquify(
                    [
                        {
                            'id': d,
                            'name': r[12].split(';')[k] if r[12] is not None else ''
                        } for k, d in enumerate(r[11].split(';') if r[11] is not None else [])
                    ])
                }
               for i, r in enumerate(db.session.query(
                Publications,
                func.group_concat(func.ifnull(Authors.id, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.forename, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.surname, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.cleanname, '').op("ORDER BY")(Authors_publications.position)).label('authors'),
                func.group_concat(func.ifnull(Documents.id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.publication_id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.visible, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.remote, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.filename, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Keywords_publication.keyword_id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(Keywords.id.op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(Keywords.name.op('SEPARATOR')(literal_column('\';\'')))
                )\
                .outerjoin(Documents, Documents.publication_id == Publications.id)\
                .outerjoin(Keywords_publication, Keywords_publication.publication_id == Publications.id)\
                .outerjoin(Keywords, Keywords_publication.keyword_id == Keywords.id) \
                .filter(Publications.id == Authors_publications.publication_id) \
                .filter(Publications.public == 1) \
                .filter(Authors.id == Authors_publications.author_id) \
                .filter(Publications.year.in_(filters['year']) if 'year' in filters else true() ) \
                .filter(Publications.type.in_(filters['type']) if 'type' in filters else true() ) \
                .filter(Keywords_publication.keyword_id.in_(filters['keyword']) if 'keyword' in filters else true()) \
                .having(or_(Publications.title.like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Authors.cleanname.op("ORDER BY")(Authors_publications.position)).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Authors.forename.op("ORDER BY")(Authors_publications.position)).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Authors.surname.op("ORDER BY")(Authors_publications.position)).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Keywords.name).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Publications.journal).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Publications.booktitle).like('%' + filters['search'] + '%') if 'search' in filters else true()))\
                .having(func.group_concat(Authors.id).op('regexp')('(^|,)' + str(filters['author']) + '(,|$)') if 'author' in filters else true())\
                .group_by(Publications.id)\
                .order_by(Publications.year.desc(), Publications.id.desc())
    )}

    db.session.close()
    return result

def getPubAndAuthorsAndDocsWithOffsetAndFilter(offset, limit, filters):
    """
    Get chunk of publications with corresponding authors and documents after applying filters.
    @param offset: database table offset
    @type offset: int
    @param limit: number of publications to fetch starting at offset
    @type limit: int
    @param filters: dict of filter criteria
    @type filters: dict
    @return: enumerated dict of publications
    @rtype: dict
    """
    # default is 1024 and too small for this query
    db.session.execute("SET SESSION group_concat_max_len = 100000")

    result = {i: {**r[0].to_dict(),
                'authors': uniquifySorted(
                    [
                        {'id': a,
                             'forename': r[2].split(',')[j] if r[2] is not None else '',
                             'surname': r[3].split(',')[j] if r[3] is not None else '',
                             'cleanname': r[4].split(',')[j] if r[4] is not None else ''
                        } for j, a in enumerate(r[1].split(',') if r[1] is not None else [])
                    ]),
                'documents': uniquify(
                    [
                        {
                        'id': d,
                        'publication_id': r[6].split(';')[j] if r[6] is not None else '',
                        'visible': r[7].split(';')[j] if r[7] is not None else '',
                        'remote': r[8].split(';')[j] if r[8] is not None else '',
                        'filename': r[9].split(';')[j] if r[9] is not None else ''
                         } for j, d in enumerate(r[5].split(';') if r[5] is not None else [])
                    ]),
                'keywords': uniquify(
                    [
                        {
                            'id': d,
                            'name': r[12].split(';')[k] if r[12] is not None else ''
                        } for k, d in enumerate(r[11].split(';') if r[11] is not None else [])
                    ])
                }
               for i, r in enumerate(db.session.query(
                Publications,
                func.group_concat(func.ifnull(Authors.id, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.forename, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.surname, '').op("ORDER BY")(Authors_publications.position)),
                func.group_concat(func.ifnull(Authors.cleanname, '').op("ORDER BY")(Authors_publications.position)).label('authors'),
                func.group_concat(func.ifnull(Documents.id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.publication_id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.visible, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.remote, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Documents.filename, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(func.ifnull(Keywords_publication.keyword_id, '').op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(Keywords.id.op('SEPARATOR')(literal_column('\';\''))),
                func.group_concat(Keywords.name.op('SEPARATOR')(literal_column('\';\'')))
                )\
                .outerjoin(Documents, Documents.publication_id == Publications.id)\
                .outerjoin(Keywords_publication, Keywords_publication.publication_id == Publications.id)\
                .outerjoin(Keywords, Keywords_publication.keyword_id == Keywords.id) \
                .filter(Publications.id == Authors_publications.publication_id) \
                .filter(Publications.public == 1) \
                .filter(Authors.id == Authors_publications.author_id) \
                .filter(Publications.year.in_(filters['year']) if 'year' in filters else true() ) \
                .filter(Publications.type.in_(filters['type']) if 'type' in filters else true() ) \
                .filter(Keywords_publication.keyword_id.in_(filters['keyword']) if 'keyword' in filters else true()) \
                .having(or_(Publications.title.like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Authors.cleanname.op("ORDER BY")(Authors_publications.position)).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Authors.forename.op("ORDER BY")(Authors_publications.position)).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Authors.surname.op("ORDER BY")(Authors_publications.position)).like('%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Keywords.name).like(
                                '%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Publications.journal).like(
                                '%' + filters['search'] + '%') if 'search' in filters else true(),
                            func.group_concat(Publications.booktitle).like(
                                '%' + filters['search'] + '%') if 'search' in filters else true(),
                            (Publications.year == int(filters['search']) if filters['search'].isdigit() else false()) if 'search' in filters else true()
                            )
                        )\
                # .having(func.group_concat(Authors.id).op('regexp')('(^|,)' + str(filters['author']) + '(,|$)') if 'author' in filters else true())\
                .having(or_((func.group_concat(Authors.id).op('regexp')('(^|,)' + str(a) + '(,|$)') for a in filters['author'].split(',')) if 'author' in filters else true()))
                .group_by(Publications.id)\
                .order_by(Publications.year.desc(), Publications.id.desc())
                .offset(offset)
                .limit(limit))}

    db.session.close()
    return result

def getPubAndAuthorsAndDocsById(id):
    """
    Retrieve a single publication with its corresponding authors and documents by the publication's database ID.
    @param id: the database ID of the publication
    @type id: int
    @return: return a dict of the publication or None
    @rtype: dict
    """
    documents = [ doc.to_dict()
                  for doc in db.session.query(Documents).filter(Documents.publication_id == id).all()
                  if doc.to_dict()['visible'] == 1 ]
    result = db.session.query(
        Publications,
        func.group_concat(Authors.cleanname.op("ORDER BY")(Authors_publications.position)),
        func.group_concat(Authors.id.op("ORDER BY")(Authors_publications.position))
    )\
        .filter(Authors_publications.publication_id == Publications.id)\
        .filter(Authors.id == Authors_publications.author_id) \
        .filter(Publications.id == id) \
        .group_by(Publications.id)

    result = [{
        **r[0].to_dict(),
        'authors': [{'name': a,
                     'id': r[2].split(',')[i] if r[2] is not None else ''}
                    for i, a in enumerate(r[1].split(',') if r[1] is not None else [])],
        'documents': documents
    } for r in result]

    db.session.close()
    return result[0] if len(result) > 0 else None

def getKeywordsOfPub(id):
    """
    Retrieve all keywords for a publication by ID
    @param id: the database ID of the publication
    @type id: int
    @return: a list of keywords
    @rtype: list(dict)
    """
    result = db.session.query(
        Publications.id,
        func.group_concat(Keywords.id),
        func.group_concat(Keywords.name)
    )\
    .outerjoin(Keywords_publication, Publications.id == Keywords_publication.publication_id)\
    .outerjoin(Keywords, Keywords.id == Keywords_publication.keyword_id)\
    .filter(Keywords.id == Keywords_publication.keyword_id)\
    .filter(Keywords_publication.publication_id == id)\
    .group_by(Publications.id).first()

    if result is None:
        return []

    result = [{'id': id,
               'name': result[2].split(',')[i] if result[2] is not None else ''} for i, id in enumerate(result[1].split(',') if result[1] is not None else [])]
    db.session.close()
    return result

def getLatestPublications():
    """
    Get the list of publication ordered by ID
    @return: list of publications
    @rtype: list(dict)
    """
    return [p.to_dict() for p in Publications.query.order_by(Publications.id.desc()).all()]

def getPublications():
    """
    Get the list of publications ordered by year and id
    @return: list of publications
    @rtype: list(dict)
    """
    return [p.to_dict() for p in Publications.query.order_by(Publications.year.desc(), Publications.id.desc()).all()]

def getPublicationById(id):
    """
    Get a publication by id
    @param id: the database ID of the publication
    @type id: int
    @return: a dict containing the info of the publication
    @rtype: dict
    """
    result = db.session.query(Publications).filter(Publications.id == id).first()

    db.session.close()
    return result.to_dict() if result is not None else {}

def getDocsOfPublicationById(id):
    """
    Get the documents of a publication by the publication's ID
    @param id: the database ID of the publication
    @type id: int
    @return: the list of documents
    @rtype: list(dict)
    """
    result = [ doc.to_dict() for doc in db.session.query(Documents)\
            .filter(Publications.id == id)\
            .filter(id == Documents.publication_id)\
            .order_by(Documents.id.asc())\
            .all() ]

    db.session.close()
    return result

def getCategoryIdsOfPub(id):#
    """
    Get the category IDs of the categories for a specific publication
    @param id: the database ID of the publication
    @type id: int
    @return: the list of category IDs
    @rtype: list(int)
    """
    result = [category[0] for category in db.session.query(Categories.id)\
                .filter(Publications.id == Categories_publications.publication_id)\
                .filter(Categories.id == Categories_publications.category_id)\
                .filter(Publications.id == id).all() ]

    db.session.close()
    return result

def getAuthorsOfPub(id):
    """
    Get the authors for a publication by the publication's ID
    @param id: the database ID of the publication
    @type id: int
    @return: the list of authors
    @rtype: list(dict)
    """
    result = [author.to_dict() for author in db.session.query(Authors)\
             .filter(Publications.id == Authors_publications.publication_id)\
             .filter(Authors.id == Authors_publications.author_id)\
             .filter(Publications.id == id)\
             .order_by(Authors_publications.position).all()]

    db.session.close()
    return result

def getPublicationTypes():
    """
    Get a list of all publication types present in the database
    @return: the list of publication types
    @rtype: list(string)
    """
    types = [type[0] for type in db.session.query(Publications.type).group_by(Publications.type) if type[0]]

    db.session.close()
    return types

def getPublicationYears():
    """
    Get a list of publication years for all publications
    @return: list of publication years
    @rtype: list(string)
    """
    years = [year[0] for year in db.session.query(Publications.year).group_by(Publications.year).order_by(Publications.year.asc()) if year[0]]

    db.session.close()
    return years


def getPublicationsOfAuthorWithLimit(pub, a_id, limit):
    """
    Get the first n publications of an author, excluding publication pub
    @param pub: the publication to exclude
    @type pub: dict
    @param a_id: the id of the author
    @type a_id: int
    @param limit: the number of publications to retrieve
    @type limit: int
    @return: the list of publications
    @rtype: list(dict)
    """
    # default is 1024 and too small for this query
    db.session.execute("SET SESSION group_concat_max_len = 100000")

    result = db.engine.execute(
        text("""
        SELECT publications.id,
               publications.title,
               publications.booktitle,
               publications.journal,
               publications.year,
               publications.thumb,
               group_concat(authors.id ORDER BY authors_publications.position) as agg,
               group_concat(authors.cleanname ORDER BY authors_publications.position SEPARATOR ';')
        FROM publications
        JOIN authors_publications ON authors_publications.publication_id = publications.id
        JOIN authors ON authors_publications.author_id = authors.id
        WHERE publications.id != :pub_id
        GROUP BY publications.id
        HAVING agg REGEXP :regex
        ORDER BY ABS(:year - CAST(publications.year AS SIGNED)) ASC
        LIMIT :limit
        """), pub_id=pub['id'], regex='^{}(,|$)'.format(a_id), year=pub['year'], limit=limit)

    result = [{'id': r[0],
      'title': r[1],
      'booktitle': r[2],
      'journal': r[3],
      'year': r[4],
      'thumb': r[5],
      'authors': [{
          'id': id,
          'name': r[7].split(';')[i]
        } for i, id in enumerate(r[6].split(','))]
      } for r in list(result)]

    db.session.close()
    return result


def addPublication(session, **kwargs):
    """
    Add a new publication to the database.
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param kwargs: the publication data
    @type kwargs: dict
    @return: the newly added publication object
    @rtype: Publication object
    """
    newPublication = Publications(
        address=kwargs['address'],
        booktitle=kwargs['booktitle'],
        chapter=kwargs['chapter'],
        edition=kwargs['edition'],
        editor=kwargs['editor'],
        howpublished=kwargs['howpublished'],
        institution=kwargs['institution'],
        journal=kwargs['journal'],
        month=kwargs['month'],
        note=kwargs['note'],
        number=kwargs['number'],
        organization=kwargs['organization'],
        pages=kwargs['pages'],
        school=kwargs['school'],
        series=kwargs['series'],
        title=kwargs['title'],
        volume=kwargs['volume'],
        url=kwargs['url'],
        doi=kwargs['doi'],
        year=kwargs['year'],
        citename=kwargs['citename'],
        publisher=kwargs['publisher'],
        published=kwargs['published'],
        submitted=kwargs['submitted'],
        public=kwargs['public'],
        created=kwargs['created'],
        modified=kwargs['modified'],
        copyright_id=kwargs['copyright_id'],
        type=kwargs['type'],
        thumb=kwargs['thumb'],
        mainfile=kwargs['mainfile'],
        publicationdate=kwargs['publicationdate'],
        kops=kwargs['kops'],
        other=kwargs['other'],
        abstract=kwargs['abstract']
    )
    session.add(newPublication)
    return newPublication