#  Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
#  This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.
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


from flask import Blueprint, render_template, request, jsonify, send_file, current_app as app
from configurations import load_quantity, type_to_color
from itertools import groupby
from operator import itemgetter
import os

from backend.db_controller.query.publications import \
    getPublicationTypes, getPublicationYears, getPubAndAuthorsAndDocsWithOffsetAndFilter, \
    getPubAndAuthorsAndDocsWithFilter

frontend_blueprint = Blueprint('frontend', __name__)

@frontend_blueprint.route('/')
def render_index():
    """
    Render the home page of SciBib.
    @return: the main view to render
    @rtype: unicode string
    """
    data = {}
    data['types'] = {t:  type_to_color.get(t, '#888888') for t in getPublicationTypes()}
    data['years'] = getPublicationYears()

    try:
        if 'year' in request.args:
            data['filter-years'] = request.args['year'].split(',')
        if 'type' in request.args:
            data['filter-types'] = request.args['type'].split(',')
        if 'keyword' in request.args:
            data['filter-keywords'] = request.args['keyword'].split(',')
        if 'search' in request.args:
            data['filter-search'] = request.args['search']
    except Exception:
        app.logger.exception(
            "{}: Exception occurred while parsing the filter parameters:".format(__name__))

    return render_template('public/index.html', data=data)

@frontend_blueprint.route('/all')
def render_index_all():
    """
    Render alternative view which renders all publications at once.
    @return: the view to render
    @rtype: unicode string
    """
    data = {}
    data['types'] = {t:  type_to_color.get(t, '#888888') for t in getPublicationTypes()}
    data['years'] = getPublicationYears()

    try:
        if 'year' in request.args:
            data['filter-years'] = request.args['year'].split(',')
        if 'type' in request.args:
            data['filter-types'] = request.args['type'].split(',')
        if 'keyword' in request.args:
            data['filter-keywords'] = request.args['keyword'].split(',')
        if 'search' in request.args:
            data['filter-search'] = request.args['search']
    except Exception:
        app.logger.exception(
            "{}: Exception occurred while parsing the filter parameters:".format(__name__))

    return render_template('public/index_all.html', data=data)

@frontend_blueprint.route('/loadAll')
def load_items_all():
    """
    Load all items
    @return: a list of dicts containing all publications
    @rtype: JSON
    """
    res = []
    filters = {}

    try:
        if 'year' in request.args:
            filters['year'] = request.args['year'].split(',')
        if 'type' in request.args:
            filters['type'] = request.args['type'].split(',')
        if 'search' in request.args:
            filters['search'] = request.args['search']
        if 'author' in request.args:
            filters['author'] = request.args['author']
        if 'keyword' in request.args:
            filters['keyword'] = request.args['keyword'].split(',')
    except Exception:
        app.logger.exception(
            "{}: Exception occurred while parsing the filter parameters:".format(__name__))
    publications = [pub for key, pub in getPubAndAuthorsAndDocsWithFilter(filters).items()]
    res = [ (year, list(item)) for year, item in groupby(publications, key=itemgetter('year')) ]

    return jsonify(res)

@frontend_blueprint.route('/loadItems')
def load_items():
    """
    Implements lazy loading of the list view. Offset is stored in the frontend and the number of
    publications is managed via the global parameter 'load_quantity' (default 40 publications) in configurations.py.
    @return: a list of the next X publications in the database.
    @rtype: unicode string
    """
    res = []

    if not request.args:
        return jsonify(res)

    offset = int(request.args.get('offset') if 'offset' in request.args else 0)
    filters = {}

    try:
        if 'year' in request.args:
            filters['year'] = request.args['year'].split(',')
        if 'type' in request.args:
            filters['type'] = request.args['type'].split(',')
        if 'search' in request.args:
            filters['search'] = request.args['search']
        if 'author' in request.args:
            filters['author'] = request.args['author']
        if 'keyword' in request.args:
            filters['keyword'] = request.args['keyword'].split(',')
    except Exception:
        app.logger.exception(
            "{}: Exception occurred while parsing the filter parameters:".format(__name__))

    publications = [pub for key, pub in getPubAndAuthorsAndDocsWithOffsetAndFilter(offset, load_quantity, filters).items()]
    res = [ (year, list(item)) for year, item in groupby(publications, key=itemgetter('year')) ]

    return jsonify(res)

@frontend_blueprint.route('/favicon')
def send_favicon():
    """
    Render the favicon.
    @return: the favicon image
    @rtype: png image
    """
    path_to_icon = os.path.join(app.config['STATIC_FOLDER'], 'images', 'favicon.png')
    return send_file(path_to_icon)
