from flask import Blueprint, render_template, request, jsonify, send_file, current_app as app
from configurations import load_quantity, type_to_color
from itertools import groupby
from operator import itemgetter
import os

from backend.db_controller.query.publications import \
    getPublicationTypes, getPublicationYears, getPubAndAuthorsAndDocsWithOffsetAndFilter, \
    getPubAndAuthorsAndDocsWithFilter

frontend_blueprint = Blueprint('frontend', __name__)

# @frontend_blueprint.route('/getPublications')
# def get_AllPubs():
#     publications = [value for key, value in getPubAndAuthorsAndDocs().items()]
#     publications = [(year, list(item)) for year, item in groupby(publications, key=itemgetter('year'))]
#
#     return jsonify(publications)

@frontend_blueprint.route('/')
def render_index():
    data = {}
    # data['types'] = [{'type': t, 'color': type_to_color.get(t, '#888888')} for t in getPublicationTypes()]
    data['types'] = {t:  type_to_color.get(t, '#888888') for t in getPublicationTypes()}
    data['years'] = getPublicationYears()

    # data['publications'] = [{**value, 'keywords': getKeywordsOfPub(value['id'])} for key, value in getPubAndAuthorsAndDocs().items()][:200]
    # data['publications'] = [ (year, list(item)) for year, item in groupby(data['publications'], key=itemgetter('year')) ]

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
    data = {}
    # data['types'] = [{'type': t, 'color': type_to_color.get(t, '#888888')} for t in getPublicationTypes()]
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
    :return all public publications
    """
    res = []

    # if not request.args:
    #     return jsonify(res)
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
    Implement lazy loading of the list view
    :return: load_items publications
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
    path_to_icon = os.path.join(app.config['STATIC_FOLDER'], 'images', 'favicon.png')
    return send_file(path_to_icon)
