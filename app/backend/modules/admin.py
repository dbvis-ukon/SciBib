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
    """
    Render the admin area.
    @return: the template for displaying the admin area with an object holding all publications.
    @rtype: unicode string
    """
    publications = getLatestPublications()
    return render_template('public/admin.html', publications=publications)

@admin_blueprint.route('/admin/publications')
@login_required
def edit_publications():
    """
    Render the publications section in the admin area.
    @return: the template for displaying the publications area with an object holding all publications.
    @rtype: unicode string
    """
    publications = getPublications()
    return render_template('public/admin/publications/publications.html', publications=publications)

@admin_blueprint.route('/admin/publications/add')
@login_required
def add_publication_view():
    """
    Render the form to add a new publication
    @return: the form template to add a new publication
    @rtype: unicode string
    """
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
    """
    Renders a view to add/edit/delete authors.
    @return: the view to render
    @rtype: unicode string
    """
    authors = getAuthorsAndCountPubs()
    return render_template('public/admin/authors/authors.html', authors=authors)

@admin_blueprint.route('/admin/keywords')
@login_required
def edit_keywords():
    """
    Renders a view add/edit/delete keywords.
    @return: the view to render
    @rtype: unicode string
    """
    keywords = getKeywords()
    return render_template('public/admin/keywords/keywords.html', keywords=keywords)

@admin_blueprint.route('/admin/categories')
@login_required
def edit_categories():
    """
    Renders a view to add/edit/delete categories.
    @return: the view to render
    @rtype: unicode string
    """
    categories = getCategories()
    return render_template('public/admin/categories/categories.html', categories=categories)

