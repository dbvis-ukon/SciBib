from flask import Blueprint, render_template
from flask_security import login_required
from backend.db_controller.query.authors import getAuthors, getAuthorsAndCountPubs
from backend.db_controller.query.keywords import getKeywords
from backend.db_controller.query.categories import getCategories
from backend.db_controller.query.publications import getPublications, getLatestPublications
from _datetime import datetime

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/adminarea')
@login_required
def render_adminarea():
    publications = getLatestPublications()
    return render_template('public/admin.html', publications=publications)

@admin_blueprint.route('/admin/publications')
@login_required
def edit_publications():
    publications = getPublications()
    return render_template('public/admin/publications/publications.html', publications=publications)

@admin_blueprint.route('/admin/publications/add')
@login_required
def add_publication_view():
    data = {}
    data['authors'] = getAuthors()
    data['keywords'] = getKeywords()
    data['categories'] = getCategories()
    data['years'] = [{'year': year, 'current': True if year == datetime.today().year else False}
                     for year in range(1991, datetime.today().year + 2)]

    data['categories-selected'] = {}
    data['keywords-selected'] = {}
    data['authors-selected'] =  {}

    return render_template('public/admin/publications/add_publication_form.html', data=data)

@admin_blueprint.route('/admin/authors')
@login_required
def edit_authors():
    authors = getAuthorsAndCountPubs()
    return render_template('public/admin/authors/authors.html', authors=authors)

@admin_blueprint.route('/admin/keywords')
@login_required
def edit_keywords():
    keywords = getKeywords()
    return render_template('public/admin/keywords/keywords.html', keywords=keywords)

@admin_blueprint.route('/admin/categories')
@login_required
def edit_categories():
    #categories = [c.to_dict() for c in Categories.query.all()]
    categories = getCategories()
    return render_template('public/admin/categories/categories.html', categories=categories)

