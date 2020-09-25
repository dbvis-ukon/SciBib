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

"""

Implementation of the JSON API

Link to Doku: https://github.com/dbvis-ukon/SciBib/wiki/URL-parameters - NOTE: Doku is not complete
The rest of the relevant info can be found in: https://github.com/dbvis-ukon/SciBib/blob/master/SciBib/src/Controller/PublicationsController.php

Further comments: tojson function MUST HAVE the same output as currently

@author Felix Löffler, Benedikt Bäumle
"""

from backend.db_controller.db import *
from backend.db_controller.query.authors import getAuthors, getAuthorByNames
from backend.db_controller.query.categories import getCategories
from backend.db_controller.query.keywords import getKeywordByName
from sqlalchemy.sql import operators
operators._PRECEDENCE['SEPARATOR'] = 0
from backend.db_controller.query.keywords import getKeywords

from flask import Blueprint, jsonify, request

from sqlalchemy.sql import func, literal_column, and_, or_, true
import json

api_blueprint = Blueprint('api', __name__)

@api_blueprint.after_request
def after_api_request(response):
    """
    Add Access-Control-Allow-Origin header to allow requests from public to the API.
    @param response: HTTP response without Access-Control-Allow-Origin header
    @type response: HTTP response
    @return: HTTP response with Access-Control-Allow-Origin header
    @rtype: HTTP response
    """
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

@api_blueprint.route('/get/authors')
def send_authors():
    """
    Send a list of all authors in the database.
    @return: a list of authors
    @rtype: JSON
    """
    return jsonify(getAuthors())


@api_blueprint.route('/get/keywords')
def send_keywords():
    """
    Send a list of all keywords in the database.
    @return: a list of keywords
    @rtype: JSON
    """
    return jsonify(getKeywords())

@api_blueprint.route('/get/categories')
def send_categories():
    """
    Send a list of all categories in the database
    @return: a list of categories
    @rtype: JSON
    """
    return jsonify(getCategories())

@api_blueprint.route('/get/authorByName', methods=['GET'])
def get_authorId_():
    """
    Send a dict containing the complete author object of the database by specifying the forename and surname.
    Useful to retrieve the ID of an author.
    @return: a dict of the author
    @rtype: JSON
    """
    author = getAuthorByNames(request.args['forename'], request.args['surname'])\
        if 'forename' in request.args and 'surname' in request.args else {}
    return jsonify(author)

@api_blueprint.route('/get/keywordByName', methods=['GET'])
def get_keywordId_():
    """
    Send a dict containing the keyword complete keyword object of the database by specifying the keyword name.
    Useful to retrieve the ID of a keyword.
    @return: a dict of the keyword
    @rtype: JSON
    """
    keyword = getKeywordByName(request.args['name']) if 'name' in request.args else {}
    return jsonify(keyword)

@api_blueprint.route('/publication')
def send_publication():
    """
    Send a list of all publications.
    @return: a list of all publications encoded as dict.
    @rtype: JSON
    """
    return jsonify([ p.to_dict() for p in Publications.query.order_by(Publications.id.desc()).all()])

def uniquify(l):
        """
        Uniquify list of dicts.
        @param l: the list of dicts
        @type l: list(dict)
        @return: the list of unique dicts
        @rtype: list(dict)
        """
        s = set([json.dumps(i) for i in l])
        return [json.loads(i) for i in s]


def uniquifySorted(l):
    """
    Uniquify list of dicts + keep ordering
    @param l: list of dicts
    @type l: list(dict)
    @return: the list of unique dicts
    @rtype: list(dict)
    """
    s = set([json.dumps(i) for i in l])
    u = [json.loads(i) for i in s]
    return sorted(u, key=lambda x: l.index(x))


def checkForEmtyDocument(r):
    """
    Checks whether a document(s) is available for the publication
    - 1. we have null values and
    - 2. we have pseudo null values which are empty strings for every key.
    in our db-table.
    """
    if not r[5]: # 1. null value
        return []

    '''
    If we want to avoid this kind of Output we have to check for empty r[5] strings.
    same for ceckForEmtyCategories().
        "documents": [
        {
          "filename": "", 
          "id": "", 
          "publication_id": "", 
          "remote": "", 
          "visible": ""
        }'''

    rFuenf = r[5].split(';')

    if rFuenf[0] == "": # 2. pseudo null value
        return []
    else:
        documents = uniquify([
                    {'id': d,
                     'publication_id': r[6].split(';')[j] if r[6] is not None else '',
                     'visible': r[7].split(';')[j] if r[7] is not None else '',
                     'remote': r[8].split(';')[j] if r[8] is not None else '',
                     'filename': r[9].split(';')[j] if r[9] is not None else ''
                    } for j, d in enumerate(rFuenf)])
        return documents



def ceckForEmtyCategories(r):
    """
    checks whether a category or categories were added. for mor information see checkForEmtyDocument()
    """

    if not r[10]:
        return []

    rZehn = r[10].split(';')

    if rZehn[0] == "":
        return[]

    categories = uniquify([
             {'id': e,
               'name': r[11].split(';')[j] if r[11] is not None else ''
             } for j, e in enumerate(rZehn)])

    return categories

def pubIDusesAllKeywords(keywords):
    #http://garmoncheg.blogspot.com/2018/04/sqlalchemy-flask-count-model-instances.html
    '''
    This function returns a List of all publicationIDs which have all keywords provided by the api.
    After the query collected all publications which have at least one of the provided keywords, we count the occurence of the publicationsIDs. If these occure as often,
    as the amount of keywords provided, we know that a Publication has all of the keywords set.
    '''
    keywords= keywords.split(',')
    publicationID_in_keywords_publication = db.session.query(Keywords_publication.publication_id, func.count(Keywords_publication.publication_id) == len(keywords)) \
        .filter(or_((Keywords_publication.keyword_id == keyW) for keyW in keywords)) \
        .group_by(Keywords_publication.publication_id) \
        .all()
    #print(publicationID_in_keywords_publication) #helps to understand the query!

    pubID_uses_all_keywords = []
    for tup in publicationID_in_keywords_publication:
        if tup[1] == True:
            pubID_uses_all_keywords.append(tup[0])

    return(pubID_uses_all_keywords)

@api_blueprint.route('/publications/tojson')
def send_json():
    '''
    api:

    year        - filter by year: year=2016 or year=2016,2018,..
    type        - filter by type: type=techreport or type=article. Possible types are:
            Incollection
            Inbook
            Inproceedings
            Article
            PhDThesis
            Book
            ""
            Misc
            Proceedings
            Conference
            Techreport
            <null>

    author      - filter by one or many authors: author=703 or author=703,709
    categories  - filter by category ID(s): categories=62 or categories=62,72
    kops        - if kops=true one will see all publications which are listed in kops. The DB contains <null> and "" values for Publications which are not listed in kops!
    keywords    - filter by keyword ID(s):
    '''
    # default is 1024 and too small for this query
    db.session.execute("SET SESSION group_concat_max_len = 1000000")

    cat_pub_subq = db.session.query(Categories.id.label("cat_id"), Categories.name.label("cat_name"),
                                           Categories.parent_id, Categories_publications.publication_id) \
            .join(Categories_publications, Categories.id == Categories_publications.category_id) \
            .join(Publications, Categories_publications.publication_id == Publications.id) \
            .subquery()

    '''
        You can dynamically construct the "OR" and "AND" --> see .filter in the query.
        Because of this feature one can define generic filters.
    '''
    filters = request.args.to_dict()

   # filters['keywords'] = (filters['keywords'].split(','))
   # print(filters['keywords'])



    result = {
        "publications": {i:
        {**r[0].to_dict(),
            'authors': uniquifySorted([
                {'id': a,
                 'forename': r[2].split(',')[j],
                 'surname': r[3].split(',')[j],
                 'cleanname': r[4].split(',')[j]
                 } for j, a in enumerate(r[1].split(','))]),

            'documents': checkForEmtyDocument(r),

            'categories': ceckForEmtyCategories(r)
        }
        for i, r in enumerate(db.session.query(
            Publications,
            func.group_concat(func.ifnull(Authors.id, '').op("ORDER BY")(Authors_publications.position)),
            func.group_concat(func.ifnull(Authors.forename, '').op("ORDER BY")(Authors_publications.position)),
            func.group_concat(func.ifnull(Authors.surname, '').op("ORDER BY")(Authors_publications.position)),
            func.group_concat(func.ifnull(Authors.cleanname, '').op("ORDER BY")(Authors_publications.position)),
            func.group_concat(func.ifnull(Documents.id, '').op("SEPARATOR")(literal_column('\';\''))),
            func.group_concat(func.ifnull(Documents.publication_id, '').op("SEPARATOR")(literal_column('\';\''))),
            func.group_concat(func.ifnull(Documents.visible, '').op("SEPARATOR")(literal_column('\';\''))),
            func.group_concat(func.ifnull(Documents.remote, '').op("SEPARATOR")(literal_column('\';\''))),
            func.group_concat(func.ifnull(Documents.filename, '').op("SEPARATOR")(literal_column('\';\''))),
            func.group_concat(func.ifnull(cat_pub_subq.c.cat_id, '').op("SEPARATOR")(literal_column('\';\''))),
            func.group_concat(func.ifnull(cat_pub_subq.c.cat_name, '').op("SEPARATOR")(literal_column('\';\''))),
            func.group_concat(func.ifnull(cat_pub_subq.c.parent_id, '').op("SEPARATOR")(literal_column('\';\''))),
        ) \
                              .outerjoin(Documents, Publications.id == Documents.publication_id) \
                              .outerjoin(cat_pub_subq, Publications.id == cat_pub_subq.c.publication_id) \
                              .filter(Publications.id == Authors_publications.publication_id) \
                              .filter(Authors.id == Authors_publications.author_id) \
                              .filter(Publications.year.in_(filters['year'].split(',')) if 'year' in filters else true()) \
                              .filter(Publications.type.in_([filters['type']]) if 'type' in filters else true()  )\
                              .having(or_((func.group_concat(Authors.id).op('regexp')('(^|,)' + str(a) + '(,|$)') for a in filters['author'].split(',')) if 'author' in filters else true())) \
                              .having(and_((func.group_concat(cat_pub_subq.c.cat_id).op('regexp')('(^|,)' + str(a) + '(,|$)') for a in filters['category'].split(',')) if 'category' in filters else true())) \
                              .filter((and_(Publications.kops != "", Publications.kops != None) if filters['kops'] == 'true' else or_(Publications.kops == None, Publications.kops == "")) if 'kops' in filters else true()) \
                              .filter((Publications.id.in_(pubIDusesAllKeywords(filters['keywords']))) if 'keywords' in filters else true())\
                              .filter(Publications.public == 1)\
                              .group_by(Publications.id) \
                              .order_by(Publications.year.desc(), Publications.id.desc())
                              .all())},
        "file_dir": "uploadedFiles"
    }
    return jsonify(result)
