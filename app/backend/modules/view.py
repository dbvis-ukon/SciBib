from flask import Blueprint, render_template,  abort
from flask_security import login_required
from backend.db_controller.query.categories import getPubsOfCat, getRelatedCategories, getNameById
from backend.db_controller.query.publications import getPubAndAuthorsAndDocsById, getKeywordsOfPub, getPublicationsOfAuthorWithLimit
from backend.db_controller.query.authors import getPubsOfAuthor, getAuthorById

view_blueprint = Blueprint('view', __name__)

@view_blueprint.route('/view/categories/<id>')
@login_required
def render_view_category(id):
    """
    Render view to get info on a specific category.
    @param id: the database ID of the category
    @type id: int
    @return: the view to render
    @rtype: unicode string
    """
    data = {}
    publications = getPubsOfCat(id)
    related = getRelatedCategories(id)

    if len(related) == 0:
        abort(404, description="Category not found.")

    # related[0] is this category
    parent = getNameById(related[0]['parent_id'])

    data['category'] = related[0]
    data['publications'] = publications
    data['related'] = related
    data['parent'] = parent['id'] if parent != None and len(parent) > 0 else []
    return render_template('public/view/category.html', data=data)

@view_blueprint.route('/publications/view/<id>')
def render_view_publication(id):
    """
    Render view to get info on a specific publication.
    @param id: the database ID of the publication
    @type id: int
    @return: the view to render
    @rtype: unicode string
    """
    data = {}

    publication = getPubAndAuthorsAndDocsById(id)
    data['publication'] = publication
    data['keywords'] = getKeywordsOfPub(id)

    main_author = publication['authors'][0] if 'authors' in publication and len(publication['authors']) > 0 else None
    if main_author is not None:
        data['related_publications'] = getPublicationsOfAuthorWithLimit(data['publication'], main_author['id'], 5)

    return render_template('public/view/publication.html', data=data)

@view_blueprint.route('/view/authors/<id>')
def render_view_author(id):
    """
    Render view to get info a specific author.
    @param id: the database ID of the author
    @type id: int
    @return: the view to render
    @rtype: unicode string
    """
    data = {}

    # query data
    publications = getPubsOfAuthor(id)
    author = getAuthorById(id)

    data['publications'] = publications
    data['author'] = author
    return render_template('public/view/author.html', data=data)

