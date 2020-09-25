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

from flask import Blueprint, request, jsonify, render_template, url_for, redirect, flash, current_app as app, abort
from flask_security import login_required, current_user, roles_accepted
from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import pwd
import contextlib
from datetime import datetime
from PIL import Image
from sqlalchemy import exc

from backend.db_controller.query.publications import getPublicationById, getCategoryIdsOfPub, \
    getAuthorsOfPub, getKeywordsOfPub, getDocsOfPublicationById, addPublication
from backend.db_controller.query.authors import getAuthors, addAuthor, getAuthorsById, getAuthorById
from backend.db_controller.query.keywords import getKeywords
from backend.db_controller.query.categories import getCategories
from backend.db_controller.query.authors_publications import addAuthorsPublications
from backend.db_controller.query.categories_publications import addCategoriesPublications
from backend.db_controller.query.keywords_publications import addKeywordsPublications
from backend.db_controller.query.documents import addDocument, getDocumentById, getDocumentsOfPub
from backend.db_controller.query.users_publication import addUsersPublication
from backend.db_controller.query.keywords import addKeyword
from backend.db_controller.db import Authors, Categories, Publications,\
    Authors_publications, Keywords_publication, Categories_publications, Documents, Keywords, Users_publication
from backend.db_controller.helper import _createCiteName
from configurations import valid_publication_types

from backend.db_controller.helper import _is_authorized

manipulate_db = Blueprint('manipulate_db', __name__)
db = SQLAlchemy()

def _addDir(path):
    """
    Add a new directory
    :param path: the directory to add
    :return: None
    """
    os.makedirs(path, exist_ok=True)
    uid, gid = pwd.getpwnam('www-data').pw_uid, pwd.getpwnam('www-data').pw_uid
    os.chown(path, uid, gid)
    app.logger.info("%(filename)s %(funcname)s: Created directory {}".format(path))

def _addDoc(file_obj, dir, file_name):
    """
    Add the document to directory
    :param file_obj: the file object
    :param title:    the title of the publication to create an own folder for the thumbnail
    :return: filename
    """
    # uniquify name
    i = 0
    splitted = file_name.split('.')
    name = ".".join(splitted[:-1])
    suffix = splitted[-1] if len(splitted) > 1 else 'pdf'
    file_name = ".".join([name, suffix])
    file_path = os.path.join(dir, file_name)
    while os.path.exists(file_path):
        new_name = "{}_{}".format(name, i)
        file_name = ".".join([new_name, suffix])
        file_path = os.path.join(dir, file_name)
        i = i + 1
        # file_name = os.path.join(dir, ".".join([new_name, suffix]))
    # store file to filesystem
    file_obj.save(os.path.join(dir, file_name))
    return file_name

def _rmDir(path):
    """
    Remove a directory of already uploadeded PDFs or thumbnails of a publication.
    :param dir: the directory to remove
    :return: None
    """
    if not path.startswith(app.config['UPLOAD_FOLDER'] + os.sep):
        app.logger.warning("%(filename)s %(funcName)s: Abort. Tried to delete a file outside uploaded files directory.")
        return
    with contextlib.suppress(FileNotFoundError):
        os.rmdir(path)

def _rmDoc(filename):
    """
    Remove an uploaded file
    :param filename: directory path + filename
    :return: None
    """
    # make sure only uploaded files are deleted
    if not filename.startswith(app.config['UPLOAD_FOLDER'] + os.sep):
        app.logger.warning("%(filename)s %(funcName)s: Abort. Tried to delete a file outside uploaded files directory.")
        return
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)

def _resizeImg(filename):
    img = Image.open(filename)
    img = img.resize((74, 74))
    img.save(filename)

# def _createCiteName(authors, year, title):
#     citename = ''.join([a[:2].title() for a in authors[:3]])
#     if len(authors) > 3:
#         citename += '+'
#     citename += year
#     citename += title.split()[0]
#     return citename


# helper to create cleanname column in author table
def nameToCleanname(forname, surname):
    fornames = []
    for n in forname.split(' '):
        fornames.append('-'.join([n2[0].capitalize() + '.' for n2 in n.split('-') if len(n2) > 0]))
    return "{} {}".format(' '.join(fornames), surname.title())

@manipulate_db.route('/add/author', methods=['POST'])
@login_required
@roles_accepted('editor', 'admin')
def add_author():

    session = db.session()
    try:
        if not 'input-surname' in request.form or len(request.form['input-surname']) == 0 or\
           not 'input-forename' in request.form or len(request.form['input-forename']) == 0:
            raise ValueError("a forname and surname must be specified.")

        surname = request.form['input-surname']
        forename = request.form['input-forename']

        if ',' in surname or ',' in forename:
            raise ValueError("Names are not allowed to contain ','")

        website = request.form['input-website'] if 'input-website' in request.form else ''

        cleanname = nameToCleanname(forename, surname)

        newAuthor = addAuthor(session, surname=surname, forename=forename, cleanname=cleanname)
        session.commit()

        app.logger.info("{} {}: Succesfully added author {}".format(__file__, __name__, cleanname))
        return jsonify({
            'msg': 'Author {} {} added successfully!'.format(forename, surname),
            'author': newAuthor.to_dict()
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to add an author:".format(
            __file__, __name__
        ))
        session.rollback()
        return ('500 Internal Server Error. Could not add Author', 500)
    finally:
        session.close()

@manipulate_db.route('/add/author2', methods=['POST'])
@login_required
@roles_accepted('editor', 'admin')
def add_author2():
    """
    Add author via json post
    :return:
    """
    session = db.session()
    try:
        if not 'surname' in request.json or len(request.json['surname']) == 0 or\
           not 'forename' in request.json or len(request.json['forename']) == 0:
            raise ValueError("a forname and surname must be specified.")

        surname = request.json['surname']
        forename = request.json['forename']

        if ',' in surname or ',' in forename:
            raise ValueError("names are not allowed to contain ','")

        cleanname = nameToCleanname(forename, surname)

        newAuthor = addAuthor(session, surname=surname, forename=forename, cleanname=cleanname)
        session.commit()

        app.logger.info("{} {}: Succesfully added author {}".format(__file__, __name__, cleanname))
        return jsonify({
            'msg': 'Author {} {} added successfully!'.format(forename, surname),
            'author': newAuthor.to_dict()
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to add an author:".format(__file__, __name__))
        session.rollback()
        return ('500 Internal Server Error. Could not add Author', 500)
    finally:
        session.close()

@manipulate_db.route('/add/keyword2', methods=['POST'])
@login_required
@roles_accepted('editor', 'admin')
def add_keyword2():
    """
    Add keyword via json post
    :return:
    """
    session = db.session()
    try:
        if not 'name' in request.json or len(request.json['name']) == 0:
            raise ValueError('no keyword name specified')

        keyword = request.json['name'].title()
        try:
            newKeyword = addKeyword(session, name=keyword)
            session.commit()
        except exc.IntegrityError:
            app.logger.exception(
                "{} {}: Exception occurred while trying to add a keyword. Keyword {} already exists".format(__file__,
                                                                                                            __name__,
                                                                                                              keyword))
            session.rollback()

        app.logger.info("{} {}: Succesfully added keyword {}".format(__file__, __name__, keyword))
        return jsonify({
            'msg': 'Keyword {} added successfully!'.format(keyword),
            'keyword': newKeyword.to_dict()
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to add a keyword:".format(__file__, __name__))
        session.rollback()
        return ('500 Internal Server Error. Could not add Keyword.', 500)
    finally:
        session.close()

@manipulate_db.route('/add/keyword', methods=['POST'])
@login_required
@roles_accepted('editor', 'admin')
def add_keyword():
    session = db.session()
    try:
        if not 'input-name' in request.form or len(request.form['input-name']) == 0:
            raise ValueError('no keyword name specified')

        keyword = request.form['input-name'].title()
        try:
            newKeyword = addKeyword(session, name=keyword)
            session.commit()
        except exc.IntegrityError:
            app.logger.exception(
                "{} {}: Exception occurred while trying to add a keyword. Keyword {} already exists".format(__file__,
                                                                                                            __name__,
                                                                                                            keyword))
            session.rollback()

        app.logger.info("{} {}: Succesfully added keyword {}".format(__file__, __name__, keyword))
        return jsonify({
            'msg': 'Keyword {} added successfully!'.format(keyword),
            'keyword': newKeyword.to_dict()
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to add a keyword:".format(__file__, __name__))
        session.rollback()
        return ('500 Internal Server Error. Could not add Keyword.', 500)
    finally:
        session.close()


@manipulate_db.route('/add/category', methods=['POST'])
@login_required
@roles_accepted('editor', 'admin')
def add_category():
    session = db.session()

    try:
        if not 'input-name' in request.form or len(request.form['input-name']) == 0:
            raise ValueError('a category name must be specified.')

        category = request.form['input-name']
        parent = request.form['select-parent'] if 'select-parent' in request.form else '0'
        desc = request.form['input-desc'] if 'input-desc' in request.form else ''

        # no parent
        if parent == '0':
            # get the current maximal rght value of the tree
            max_row = db.session.query(Categories.id, Categories.name, Categories.rght).filter(Categories.parent_id == None).order_by(Categories.rght.desc()).first()
            max_row = [] if max_row == None else list(max_row)
            # max_row = list(db.session.query(Categories.id, Categories.name, Categories.rght).filter(Categories.parent_id == None).order_by(Categories.rght.desc()).first())

            # check if empty
            lft = int(max_row[2]) + 1 if len(max_row) > 0 else 1
            rght = lft + 3

            # session.add(Categories(name=category, lft=lft, rght=rght, description=desc))
            newCategory = Categories(name=category,
                                     lft=lft,
                                     rght=rght,
                                     description=desc)
            try:
                session.add(newCategory)
                session.commit()
            except exc.IntegrityError:
                app.logger.exception(
                    "{} {}: Exception occurred while trying to add a category. Category {} already exists".format(
                        __file__, __name__, category))
                session.rollback()

            app.logger.info("{} {}: Succesfully added category {}".format(__file__, __name__, category))
            return jsonify({
                'msg': 'Category {} added successfully!'.format(category),
                'category': newCategory.to_dict()
            })
        # has parent with id parent
        else:
            lft_of_parent = db.session.query(Categories.lft).filter(Categories.id == parent).first()[0]
            session.query(Categories).filter(Categories.rght > lft_of_parent).update({'rght': Categories.rght + 2})
            session.query(Categories).filter(Categories.lft > lft_of_parent).update({'lft': Categories.lft + 2})
            newCategory = Categories(name=category,
                                      parent_id=parent,
                                      lft=lft_of_parent + 1,
                                      rght=lft_of_parent + 2,
                                      description=desc)
            try:
                session.add(newCategory)
                session.commit()
            except exc.IntegrityError:
                app.logger.exception(
                    "{} {}: Exception occurred while trying to add a category. Category {} already exists".format(
                        __file__, __name__, category))
                session.rollback()

            app.logger.info("{} {}: Succesfully added category {}".format(__file__, __name__ , category))
            return jsonify({
                'msg': 'Category {} added successfully!'.format(category),
                'category': newCategory.to_dict()
            })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to add a category:".format(__file__, __name__))
        session.rollback()
        return ('500 Internal Server Error! Could not add Keyword', 500)
    finally:
        session.close()

@manipulate_db.route('/add/publication', methods=['POST'])
@login_required
@roles_accepted('editor', 'admin')
def add_publication():
    """
    Add a new publication to the database. It receives and processes a web form. See below for detailed comments.
    In any case of failure, everything's roled-back.
    @return: In case of success a HTTP 200 response. In  case of failure a HTTP 500 error response.
    @rtype: HTTP response
    """
    # create session for adding the publication
    session = db.session()

    user_id = current_user.get_id()
    thumb_name = ''
    thumb_dir = ''
    pdf_dir = ''
    id = None

    # start transaction to be able to rollback everything in case of any issues happeing
    try:
        if not 'input-title' in request.form or len(request.form['input-title']) == 0:
            raise ValueError("a title must be specified.")

        if not 'input-type' in request.form or request.form['input-type'] not in valid_publication_types:
            raise ValueError("a valid publication type must be specified")

        title = request.form['input-title']
        type = request.form['input-type']

        submitted = 1 if 'input-submitted' in request.form else 0
        published = 1 if 'input-published' in request.form else 0
        public = 1 if 'input-public' in request.form else 0
        madepublic = 1 if 'input-madepublic' in request.form else 0
        # format is YEAR-MONTH-DAY
        pubdate = request.form['input-pubdate'] if 'input-pubdate' in request.form and len(request.form['input-pubdate']) > 0 else None


        year = request.form['input-year'] if 'input-year' in request.form else datetime.now().year
        doi = request.form['input-doi'] if 'input-doi' in request.form else ''
        kops = request.form['input-kops'] if 'input-kops' in request.form else ''

        categories = request.form.getlist('select-categories') if 'select-categories' in request.form else []
        keywords = request.form.getlist('select-keywords') if 'select-keywords' in request.form else []
        copyright = request.form['select-copyright'] if 'select-copyright' in request.form else "1"

        authors = request.form.getlist('select-authors') if 'select-authors' in request.form else []
        authors_dict = [a for a in getAuthorsById(authors)]

        bibtex_address = request.form['input-bibtex-address'] if 'input-bibtex-address' in request.form and len(request.form['input-bibtex-address']) > 0 else None
        bibtex_booktitle = request.form['input-bibtex-booktitle'] if 'input-bibtex-booktitle' in request.form and len(request.form['input-bibtex-booktitle']) > 0 else None
        bibtex_chapter = request.form['input-bibtex-chapter'] if 'input-bibtex-chapter' in  request.form and len(request.form['input-bibtex-chapter']) > 0 else None
        bibtex_edition = request.form['input-bibtex-edition'] if 'input-bibtex-edition' in request.form and len(request.form['input-bibtex-edition']) > 0 else None
        bibtex_editor = request.form['input-bibtex-editor'] if 'input-bibtex-editor' in request.form and len(request.form['input-bibtex-editor']) > 0 else None
        bibtex_howpublished = request.form['input-bibtex-howpublished'] if 'input-bibtex-howpublished' in request.form and len(request.form['input-bibtex-howpublished']) > 0 else None
        bibtex_institution = request.form['input-bibtex-institution'] if 'input-bibtex-institution' in request.form and len(request.form['input-bibtex-institution']) > 0 else None
        bibtex_journal = request.form['input-bibtex-journal'] if 'input-bibtex-journal' in request.form and len(request.form['input-bibtex-journal']) > 0 else None
        bibtex_month = request.form['input-bibtex-month'] if 'input-bibtex-month' in request.form and len(request.form['input-bibtex-month']) > 0 else None
        bibtex_note = request.form['input-bibtex-note'] if 'input-bibtex-note' in request.form and len(request.form['input-bibtex-note']) > 0 else None
        bibtex_number = request.form['input-bibtex-number'] if 'input-bibtex-number' in request.form and len(request.form['input-bibtex-number']) > 0 else None
        bibtex_organization = request.form['input-bibtex-organization'] if 'input-bibtex-organization' in request.form and len(request.form['input-bibtex-organization']) > 0 else None
        bibtex_pages = request.form['input-bibtex-pages'] if 'input-bibtex-pages' in request.form and len(request.form['input-bibtex-pages']) > 0 else None
        bibtex_school = request.form['input-bibtex-school'] if 'input-bibtex-school' in request.form and len(request.form['input-bibtex-school']) > 0 else None
        bibtex_series = request.form['input-bibtex-series'] if 'input-bibtex-series' in request.form and len(request.form['input-bibtex-series']) > 0 else None
        bibtex_volume = request.form['input-bibtex-volume'] if 'input-bibtex-volume' in request.form and len(request.form['input-bibtex-volume']) > 0 else None
        bibtex_publisher = request.form['input-bibtex-publisher'] if 'input-bibtex-publisher' in request.form and len(request.form['input-bibtex-publisher']) > 0 else None
        bibtex_other = request.form['input-bibtex-additional'] if 'input-bibtex-additional' in request.form and len(request.form['input-bibtex-additional']) > 0 else None

        index_mainfile = int(request.form['input-docs-checkbox']) if 'input-docs-checkbox' in request.form else None
        mainfile = ''

        thumbnail = request.files['input-thumbnail'] if 'input-thumbnail' in request.files else {'filename': ''}
        thumb_name = secure_filename(thumbnail.filename) if thumbnail.filename != '' else None

        # get name of mainfile
        # mainfile = secure_filename(request.files['input-docs-' + str(index_mainfile)].filename) if 'input-docs-' + str(index_mainfile) in request.files else None

        abstract = request.form['input-abstract'] if 'input-abstract' in request.form else ''

        # print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

        # add thumbnail to filesystem
        if thumb_name is not None and len(thumb_name) > 0:
            thumb_dir = app.config['THUMB_FOLDER']
            _addDir(thumb_dir)
            thumb_name =_addDoc(thumbnail, thumb_dir, thumb_name)
            _resizeImg(os.path.join(thumb_dir, thumb_name))

        added_files = []
        # add PDF documents
        # already added documents are handled on frontend, so here we do not have to worry about this anymore
        if index_mainfile is not None:
            # add folder for the new documents
            # pdf_dir = os.path.join(app.config['PDF_FOLDER'], secure_filename(str(id)))
            pdf_dir = os.path.join(app.config['PDF_FOLDER'])
            _addDir(pdf_dir)

            i = 0
            inputname = 'input-docs-'
            while inputname + str(i) in request.files:
                file = request.files[inputname + str(i)]
                pdf_name = _addDoc(file, pdf_dir,
                                   secure_filename(file.filename))
                if i == index_mainfile:
                    mainfile = pdf_name
                added_files.append(pdf_name)
                i += 1

        newPublication = addPublication(session,
            address=bibtex_address,
            booktitle=bibtex_booktitle,
            chapter=bibtex_chapter,
            edition=bibtex_edition,
            editor=bibtex_editor,
            howpublished=bibtex_howpublished,
            institution=bibtex_institution,
            journal=bibtex_journal,
            month=bibtex_month,
            note=bibtex_note,
            number=bibtex_number,
            organization=bibtex_organization,
            pages=bibtex_pages,
            school=bibtex_school,
            series=bibtex_series,
            title=title,
            volume=bibtex_volume,
            url='',
            doi=doi,
            year=year,
            citename=_createCiteName(authors_dict, year, title),
            publisher=bibtex_publisher,
            published=published,
            submitted=submitted,
            public=public,
            created=None,#datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            modified=None,#datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            copyright_id=copyright,
            type=type,
            thumb=thumb_name,
            mainfile=mainfile,
            publicationdate=pubdate,
            kops=kops,
            other=bibtex_other,
            abstract=abstract
        )
        # via flush we can retrieve the new id without committing the publication
        session.flush()
        # ID of publication
        id = newPublication.id

        addUsersPublication(session,
                            user_id=user_id,
                            publication_id=id)
        app.logger.info(
            "{} {}: Succesfully added Users ({}) to Publication ({}) mapping to database".format(
                __file__, __name__, user_id, id))

        # Add Author<->Publication mappings
        for i, author in enumerate(authors):
            addAuthorsPublications(session,
                author_id=author,
                publication_id=id,
                position=i
            )
            app.logger.info(
                "{} {}: Succesfully added Author ({}) to Publication ({}) mapping to database".format(
                    __file__, __name__, author, id))

        # Add Category<->Publication mappings
        for category in categories:
            addCategoriesPublications(session,
                category_id=category,
                publication_id=id
            )
            app.logger.info(
                "{} {}: Succesfully added Category ({}) to Publication ({}) mapping to database".format(
                    __file__, __name__, category, id))

        # Keyword<->Publication mappings
        for keyword in keywords:
            addKeywordsPublications(session,
                keyword_id=keyword,
                publication_id=id
            )
            app.logger.info("{} {}: Succesfully added Keyword ({}) to Publication ({}) mapping to database"
                            .format(__file__, __name__, keyword, id))


        # Add PDF info to documents table
        if index_mainfile is not None:
            for filename in added_files:
                visible = 1
                remote = 0
                desc = ''
                addDocument(session,
                    publication_id=id,
                    visible=visible,
                    remote=remote,
                    filename=filename,
                    description=desc
                )
                app.logger.info(
                    "{} {}: Succesfully added document ({}) to database".format(
                        __file__, __name__, filename))

        # Add external links to documents table
        i = 0
        inputname = 'input-docs-external-'
        while inputname + str(i) in request.form:
            filename = request.form[inputname + str(i)]
            addDocument(session,
                publication_id=id,
                visible=1,
                remote=1,
                filename=filename,
                description=''
            )
            app.logger.info("{} {}: Succesfully added remote document ({}) mapping to database"
                            .format(__file__, __name__, filename))
            i += 1

        session.commit()

        flash('Publication has been added successfully.', 'success')

        app.logger.info("{} {}: Succesfully added publication {} ({})".format(__file__, __name__, title, id))
        return redirect('/admin/publications')
        # return jsonify({
        #     'msg': 'Publication {} added successfully!'.format(authors)
        # })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to add a publication:".format(__file__, __name__))

        # rollback added stuff
        session.rollback()
        # remove publication from database, has to be deleted extra since we flushed adding the publication to retrieve the id
        session.query(Publications).filter(Publications.id == id).delete()
        app.logger.debug("{} {}: Removed possibly added publication from database after exception".format(__file__, __name__))

        # remove already added PDFs
        if pdf_dir != '':
            i = 0
            inputname = 'input-docs-'
            while inputname + str(i) in request.files:
                filename = secure_filename(request.files[inputname + str(i)].filename)
                _rmDoc(os.path.join(pdf_dir, filename))
                i += 1
                app.logger.debug(
                    "{} {}: Removed document {} from filesystem after exception".format(os.path.join(pdf_dir, __file__), __name__, pdf_dir, filename))
            _rmDir(pdf_dir)
            app.logger.debug(
                "{} {}: Removed document directory {} from filesystem after exception".format(__file__, __name__, pdf_dir))

        # remove thumbnail
        if thumb_dir != '':
            filename = request.files['input-thumbnail'].filename
            _rmDoc(os.path.join(thumb_dir, filename))
            app.logger.debug("{} {}: Removed thumbnail {} from filesystem after exception"
                             .format(os.path.join(__file__, __name__, thumb_dir, filename)))
            _rmDir(thumb_dir)
            app.logger.debug("{} {}: Removed thumbnail directory {} from filesystem after exception"
                             .format(__file__, __name__, thumb_dir))
        return ('500 Internal Server Error! Could not add Publication', 500)
    finally:
        session.close()

@manipulate_db.route('/edit/publication/<pub_id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('editor', 'admin')
def edit_publication(pub_id):
    """
    Handles editing of publications. Handles the GET request to send the current status/information of a publications.
    And handles the POST request to submit changes to the publication. Everything's rolled-back in case of failure.
    @param pub_id: the database ID of the publication to add.
    @type pub_id: int
    @return: An HTTP response, either 200 in case of success or 500 in case of failure.
    @rtype: HTTP response
    """
    # check if the current user is the editor of the publication
    if not _is_authorized(pub_id, current_user):
       app.logger.warning("{} {}: Unauthorized user {} tried to edit publication {}".format(__file__, __name__, current_user.username, pub_id))
       flash('User not authorized to edit this publication')
       return redirect('/error')
    # return ("User not authorized to edit this publication", 403)

    # if get request, fetch all the info from the database
    if request.method == 'GET':
        try:
            publication = getPublicationById(pub_id)

            publication['categories-selected'] = {category: True for category in getCategoryIdsOfPub(pub_id)}
            publication['keywords-selected'] = {keyword['name']: True for keyword in getKeywordsOfPub(pub_id)}

            authors = getAuthorsOfPub(pub_id)
            publication['authors-selected'] = {a['id']: True for a in authors}

            publication['authors'] = authors + [a for a in getAuthors()
                                                if not publication['authors-selected'].get(a['id'], False) ]
            publication['keywords'] = getKeywords()
            publication['categories'] = getCategories()

            publication['published'] = True if publication['published'] == 1 else False
            publication['submitted'] = True if publication['submitted'] == 1 else False
            publication['public'] = True if publication['public'] == 1 else False
            publication = { key: value if value is not None else '' for key, value in publication.items() }

            publication['years'] = [{'year': year, 'current': True if year == publication['year'] else False}
                             for year in range(1991, datetime.today().year + 2)]
            # thumb = 'uploadedFiles/thumbs/{}'.format(publication['thumb']) if 'thumb' in publication and len(publication['thumb']) > 0 else 'images/thumb-default.png'
            # publication['thumb'] = thumb

            publication['abstract'] = publication['abstract'] if 'abstract' in publication else ''

            publication['docs'] = sorted(getDocsOfPublicationById(pub_id), key=lambda x: x['id'])

            return render_template('public/admin/publications/edit_publication_form.html', data=publication)
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit a publication:".format(__file__, __name__))
            return ('500 Internal Server Error!', 500)
    elif request.method == 'POST':
        session = db.session()

        thumb_name = request.form['input-current-thumbnail'] if 'input-current-thumbnail' in request.form and len(request.form['input-current-thumbnail']) > 0 else ''
        thumb_dir = ''
        pdf_dir = ''
        id = pub_id

        # start transaction to be able to rollback everything in case of any issues happeing

        try:
            if not 'input-title' in request.form or len(request.form['input-title']) == 0:
                raise ValueError("/edit/publication: A title must be specified")

            if not 'input-type' in request.form or request.form['input-type'] not in valid_publication_types:
                raise ValueError("/edit/publication: A valid publication type must be specified")

            title = request.form['input-title']
            type = request.form['input-type']

            submitted = 1 if 'input-submitted' in request.form else 0
            published = 1 if 'input-published' in request.form else 0
            public = 1 if 'input-public' in request.form else 0
            madepublic = 1 if 'input-madepublic' in request.form else 0
            # format is YEAR-MONTH-DAY
            pubdate = request.form['input-pubdate'] if 'input-pubdate' in request.form and len(
                request.form['input-bibtex-address']) > 0 else None

            year = request.form['input-year'] if 'input-year' in request.form else datetime.now().year
            doi = request.form['input-doi'] if 'input-doi' in request.form else ''
            kops = request.form['input-kops'] if 'input-kops' in request.form else ''

            categories = request.form.getlist('select-categories') if 'select-categories' in request.form else []
            keywords = request.form.getlist('select-keywords') if 'select-keywords' in request.form else []
            copyright = request.form['select-copyright'] if 'select-copyright' in request.form else None

            # add thumbnail
            thumbnail = request.files['input-thumbnail']
            if thumbnail.filename != '':
                thumb_dir = app.config['THUMB_FOLDER']
                _addDir(thumb_dir)
                thumb_name = _addDoc(thumbnail, thumb_dir,
                                     secure_filename('thumbnail_{}.{}'.format(pub_id, thumbnail.filename.split('.')[-1])))
                _resizeImg(os.path.join(thumb_dir, thumb_name))


            authors = request.form.getlist('select-authors') if 'select-authors' in request.form else []
            authors_dict = [a for a in getAuthorsById(authors)]

            bibtex_address = request.form['input-bibtex-address'] if 'input-bibtex-address' in request.form and len(
                request.form['input-bibtex-address']) > 0 else None
            bibtex_booktitle = request.form[
                'input-bibtex-booktitle'] if 'input-bibtex-booktitle' in request.form and len(
                request.form['input-bibtex-booktitle']) > 0 else None
            bibtex_chapter = request.form['input-bibtex-chapter'] if 'input-bibtex-chapter' in request.form and len(
                request.form['input-bibtex-chapter']) > 0 else None
            bibtex_edition = request.form['input-bibtex-edition'] if 'input-bibtex-edition' in request.form and len(
                request.form['input-bibtex-edition']) > 0 else None
            bibtex_editor = request.form['input-bibtex-editor'] if 'input-bibtex-editor' in request.form and len(
                request.form['input-bibtex-editor']) > 0 else None
            bibtex_howpublished = request.form[
                'input-bibtex-howpublished'] if 'input-bibtex-howpublished' in request.form and len(
                request.form['input-bibtex-howpublished']) > 0 else None
            bibtex_institution = request.form[
                'input-bibtex-institution'] if 'input-bibtex-institution' in request.form and len(
                request.form['input-bibtex-institution']) > 0 else None
            bibtex_journal = request.form['input-bibtex-journal'] if 'input-bibtex-journal' in request.form and len(
                request.form['input-bibtex-journal']) > 0 else None
            bibtex_month = request.form['input-bibtex-month'] if 'input-bibtex-month' in request.form and len(
                request.form['input-bibtex-month']) > 0 else None
            bibtex_note = request.form['input-bibtex-note'] if 'input-bibtex-note' in request.form and len(
                request.form['input-bibtex-note']) > 0 else None
            bibtex_number = request.form['input-bibtex-number'] if 'input-bibtex-number' in request.form and len(
                request.form['input-bibtex-number']) > 0 else None
            bibtex_organization = request.form[
                'input-bibtex-organization'] if 'input-bibtex-organization' in request.form and len(
                request.form['input-bibtex-organization']) > 0 else None
            bibtex_pages = request.form['input-bibtex-pages'] if 'input-bibtex-pages' in request.form and len(
                request.form['input-bibtex-pages']) > 0 else None
            bibtex_school = request.form['input-bibtex-school'] if 'input-bibtex-school' in request.form and len(
                request.form['input-bibtex-school']) > 0 else None
            bibtex_series = request.form['input-bibtex-series'] if 'input-bibtex-series' in request.form and len(
                request.form['input-bibtex-series']) > 0 else None
            bibtex_volume = request.form['input-bibtex-volume'] if 'input-bibtex-volume' in request.form and len(
                request.form['input-bibtex-volume']) > 0 else None
            bibtex_publisher = request.form[
                'input-bibtex-publisher'] if 'input-bibtex-publisher' in request.form and len(
                request.form['input-bibtex-publisher']) > 0 else None
            bibtex_other = request.form['input-bibtex-additional'] if 'input-bibtex-additional' in request.form and len(
                request.form['input-bibtex-additional']) > 0 else None

            index_mainfile = int(request.form['input-docs-checkbox']) if 'input-docs-checkbox' in request.form else None
            mainfile = ''

            # documents already existing in the database
            added_documents = getDocumentsOfPub(session, id)
            # check if one of them is newly marked as mainfile
            for i, doc in enumerate(added_documents):
                if i == index_mainfile:
                    mainfile = doc['filename']


            added_files = []
            # add PDF documents
            # already added documents are handled on frontend, so here we do not have to worry about this anymore
            if index_mainfile is not None:
                # add folder for the new documents
                # pdf_dir = os.path.join(app.config['PDF_FOLDER'], secure_filename(str(pub_id)))
                pdf_dir = os.path.join(app.config['PDF_FOLDER'])
                _addDir(pdf_dir)

                i = 0
                inputname = 'input-docs-'
                while inputname + str(i) in request.files:
                    file = request.files[inputname + str(i)]
                    pdf_name = _addDoc(file, pdf_dir, secure_filename(file.filename))
                    added_files.append(pdf_name)
                    if i + len(added_documents) == int(index_mainfile):
                        mainfile = pdf_name
                    i += 1
                    app.logger.info(
                        "{} {}: Succesfully added document ({}) to filesystem".format(
                            __file__, __name__, file))


            abstract = request.form['input-abstract'] if 'input-abstract' in request.form else ''

            # update Publication data
            session.query(Publications).filter(Publications.id == id).update({
                'address': bibtex_address,
                'booktitle': bibtex_booktitle,
                'chapter': bibtex_chapter,
                'edition': bibtex_edition,
                'editor': bibtex_editor,
                'howpublished': bibtex_howpublished,
                'institution': bibtex_institution,
                'journal': bibtex_journal,
                'month': bibtex_month,
                'note': bibtex_note,
                'number': bibtex_number,
                'organization': bibtex_organization,
                'pages': bibtex_pages,
                'school': bibtex_school,
                'series': bibtex_series,
                'title': title,
                'volume': bibtex_volume,
                'url': '',
                'doi': doi,
                'year': year,
                'citename': _createCiteName(authors_dict, year, title),
                'publisher': bibtex_publisher,
                'published': published,
                'submitted': submitted,
                'public': public,
                'modified': datetime.now(),
                'copyright_id': copyright,
                'type': type,
                'thumb': thumb_name,
                'mainfile': mainfile,
                'publicationdate': pubdate,
                'kops': kops,
                'other': bibtex_other,
                'abstract': abstract
            })
            app.logger.info(
                "{} {}: Succesfully updated publication ({})".format(
                    __file__, __name__, id))

            session.query(Authors_publications).filter(Authors_publications.publication_id == id).delete()
            # Add Author<->Publication mappings
            for i, author in enumerate(authors):
                addAuthorsPublications(session,
                                       author_id=author,
                                       publication_id=id,
                                       position=i
                                       )
                app.logger.info(
                    "{} {}: Succesfully updated Author ({}) to Publication ({}) mapping".format(
                        __file__, __name__, author, id))

            session.query(Categories_publications).filter(Categories_publications.publication_id == id).delete()
            # Add Category<->Publication mappings
            for category in categories:
                addCategoriesPublications(session,
                                          category_id=category,
                                          publication_id=id
                                          )
                app.logger.info(
                    "{} {}: Succesfully updated Category ({}) to Publication ({}) mapping".format(
                        __file__, __name__, category, id))

            session.query(Keywords_publication).filter(Keywords_publication.publication_id == id).delete()
            # Keyword<->Publication mappings
            for keyword in keywords:
                addKeywordsPublications(session,
                                        keyword_id=keyword,
                                        publication_id=id
                                        )
                app.logger.info(
                    "{} {}: Succesfully updated Keyword ({}) to Publication ({}) mapping".format(
                        __file__, __name__, keyword, id))

            # Add PDF info to documents table
            if index_mainfile is not None:
                for filename in added_files:
                    visible = 1
                    remote = 0
                    desc = ''
                    addDocument(session,
                                publication_id=id,
                                visible=visible,
                                remote=remote,
                                filename=filename,
                                description=desc
                                )
                    app.logger.info(
                        "{} {}: Succesfully updated Document ({}) in database".format(
                            __file__, __name__, filename))

            # Add external links to documents table
            i = 0
            inputname = 'input-docs-external-'
            while inputname + str(i) in request.form:
                # check if valid url
                filename = request.form[inputname + str(i)]
                addDocument(session,
                            publication_id=id,
                            visible=1,
                            remote=1,
                            filename=filename,
                            description=''
                            )
                app.logger.info(
                    "{} {}: Succesfully updated remote Document ({}) in database".format(
                        __file__, __name__, filename))
                i += 1

            session.commit()

            flash('Publication has been edited successfully.', 'success')
            app.logger.info(
                "{} {}: Succesfully updated publication {} ({})".format(__file__, __name__, title, id))
            return redirect('/edit/publication/{}'.format(pub_id))
            # return jsonify({
            #     'msg': 'Publication {} added successfully!'.format(authors)
            # })
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit publication ({}):".format(__file__, __name__, pub_id))

            # rollback added/updated stuff
            session.rollback()

            # remove already added PDFs
            if pdf_dir != '':
                i = 0
                inputname = 'input-docs-'
                while inputname + str(i) in request.files:
                    filename = secure_filename(request.files[inputname + str(i)].filename)
                    _rmDoc(os.path.join(pdf_dir, filename))
                    i += 1
                    app.logger.debug(
                        "{} {}: Remove possibly added document {} from filesystem".format(
                            __file__, __name__, os.path.join(pdf_dir, filename)))
            return ('500 Internal Server Error!', 500)
        finally:
            session.close()

@manipulate_db.route('/edit/author/<author_id>', methods=['GET', 'POST'])
@login_required
def edit_author(author_id):
    """
    Handles GET and POST requests to edit an author.
    @param author_id: the database ID of the author
    @type author_id: int
    @return: Either a HTTP 200 response in case of success or a HTTP 500 response in case of failure.
    @rtype: HTTP response
    """
    if not current_user.has_role('admin'):
        return ("User not authorized to edit author.", 403)

    if request.method == 'GET':
        session = db.session()

        try:
            a = session.query(Authors).filter(Authors.id == author_id).first()
            return jsonify({'id': a.id,
                            'forename': a.forename,
                            'surname': a.surname})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit author ({}):".format(__file__, __name__, author_id))
            session.rollback()
            return ("Something went wrong.", 500)
        finally:
            session.close()
    elif request.method == 'POST':
        session = db.session()

        try:
            if not 'input-forename' in request.form or len(request.form['input-forename']) == 0 or\
               not 'input-surname' in request.form or len(request.form['input-surname']) == 0:
                raise ValueError("/edit/author/{}: A forename and a surname must be specified to edit an author".format(author_id))

            forename = request.form['input-forename']
            surname = request.form['input-surname']

            cleanname = nameToCleanname(forename, surname)

            session.query(Authors).filter(Authors.id == author_id).update({
                'forename': forename,
                'surname': surname,
                'cleanname': cleanname
            })
            session.commit()

            app.logger.info(
                "{} {}: Successfully edited author ({}):".format(__file__, __name__, author_id))
            return jsonify({'msg': "Author edited successfully.",
                            'author': {'id': author_id, 'forename': forename, 'surname': surname, 'cleanname': cleanname}})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit author ({}):".format(__file__, __name__, (author_id)))
            session.rollback()
            return ("Something went wrong.", 500)
        finally:
            session.close()

@manipulate_db.route('/edit/keyword/<keyword_id>', methods=['GET', 'POST'])
@login_required
def edit_keyword(keyword_id):
    """
    Handles GET and POST requests to edit a keyword. Every change is rolled-back in case of failure.
    @param keyword_id: the database ID of the keyword to edit
    @type keyword_id: int
    @return: Either a HTTP 200 in case of success or a HTTP 500 in case of failure.
    @rtype: HTTP response
    """
    if not current_user.has_role('admin'):
        return ("User not authorized to edit keyword.", 403)

    if request.method == 'GET':
        session = db.session()

        try:
            k = session.query(Keywords).filter(Keywords.id == keyword_id).first()
            return jsonify({'id': k.id,
                            'name': k.name})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit keyword ({}):".format(__file__, __name__, keyword_id))
            return ("Something went wrong.", 500)
        finally:
            session.close()
    elif request.method == 'POST':
        session = db.session()

        try:
            if not 'input-name' in request.form or len(request.form['input-name']) == 0:
                raise ValueError('/edit/keyword/{}: A name must be specified to edit the keyword'.format(keyword_id))

            name = request.form['input-name']
            session.query(Keywords).filter(Keywords.id == keyword_id).update({
                'name': name
            })

            session.commit()
            app.logger.info(
                "{} {}: Successfully edited keyword ({}):".format(__file__, __name__, keyword_id))
            return jsonify({'msg': 'Keyword edited successfully.', 'keyword': {'id': keyword_id, 'name': name}})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit keyword ({}):".format(__file__, __name__, keyword_id))
            session.rollback()
            return ("Something went wrong.", 500)
        finally:
            session.close()

@manipulate_db.route('/edit/category/<category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """
    Handles GET and POST requests to edit a category.
    @param category_id: the database ID of the category
    @type category_id: int
    @return: Either an HTTP 200 response in case of success or an HTTP 500 in case of failure
    @rtype: HTTP response
    """
    if not current_user.has_role('admin'):
        return ("User not authorized to edit category.", 403)

    if request.method == 'GET':
        session = db.session()

        try:
            c = session.query(Categories).filter(Categories.id == category_id).first()

            if c is None:
                abort(404, "Category not found.")

            return jsonify({'id': c.id,
                            'name': c.name,
                            'description': c.description})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit category ({}):".format(__file__, __name__, category_id))
            return ("Something went wrong.", 500)
        finally:
            session.close()
    if request.method == 'POST':
        session = db.session()

        try:
            if not 'input-name' in request.form or len(request.form['input-name']) == 0:
                raise ValueError('/edit/category/{}: A name must be specified to edit a category.'.format(category_id))

            name = request.form['input-name']
            description = request.form['input-description'] if 'input-description' in request.form else ''

            session.query(Categories).filter(Categories.id == category_id).update({
                'name': name,
                'description': description
            })

            session.commit()
            app.logger.info(
                "{} {}: Successfully edited category ({}):".format(__file__, __name__, category_id))
            flash("Category edited successfully.")
            return redirect('/view/categories/{}'.format(category_id))
            # return jsonify({'msg': 'Category edited successfully.'})
        except Exception:
            app.logger.exception("{} {}: Exception occurred while trying to edit category ({}):".format(__file__, __name__, category_id))
            session.rollback()
            return ("Something went wrong.", 500)
        finally:
            session.close()

@manipulate_db.route('/delete/publication/', methods=['POST'])
@login_required
def delete_publication():
    """
    Handles POST requests to delete publications. Only an author that added the publication or an admin is allowed to
    delete a publication.
    @return: Either a HTTP 200 in case of success or a HTTP 500 in case of failure.
    @rtype: HTTP response
    """
    # if not current_user.has_role('admin'):
    #     return ("User not authorized to delete publication.", 403)

    session = db.session()
    try:
        if 'publication_id' not in request.json or not isinstance(request.json['publication_id'], int):
            raise ValueError("/delete/publication: A publication id must be specified")
        pub_id = request.json['publication_id']

        if not _is_authorized(pub_id, current_user):
            app.logger.warning(
                "{} {}: User {} not authorized to delete publication {}:".format(__file__, __name__, current_user.username, pub_id))
            return ("User not authorized to edit this publication", 403)

        publication = db.session.query(Publications).filter(Publications.id == pub_id).first()
        publication = publication.to_dict() if publication is not None else {}

        docs = getDocsOfPublicationById(pub_id)

        if len(publication) == 0:
            app.logger.debug(
                "{} {}: Publication to delete not found ({}):".format(__file__, __name__, pub_id))
            abort(404, description="Publication to delete not found.")

        # remove data in the database
        session.query(Keywords_publication).filter(Keywords_publication.publication_id == pub_id).delete()
        session.query(Authors_publications).filter(Authors_publications.publication_id == pub_id).delete()
        session.query(Categories_publications).filter(Categories_publications.publication_id == pub_id).delete()
        session.query(Users_publication).filter(Users_publication.publication_id == pub_id).delete()
        session.query(Documents).filter(Documents.publication_id == pub_id).delete()
        session.query(Publications).filter(Publications.id == pub_id).delete()

        # remove documents and thumbnail from filesystem
        # pdf_dir = os.path.join(app.config['PDF_FOLDER'], secure_filename(str(pub_id)))
        pdf_dir = os.path.join(app.config['PDF_FOLDER'])
        for doc in docs:
            file_path = os.path.join(pdf_dir, doc['filename'])
            _rmDoc(file_path)
            # if os.path.isdir(pdf_dir):
            #     _rmDoc(os.path.join(pdf_dir, doc['filename']))
            #     # rmtree(pdf_dir)
            app.logger.debug(
                    "{} {}: Removed documents of publication ({}):".format(__file__, __name__, pub_id))
        # thumb_dir = os.path.join(app.config['THUMB_FOLDER'], secure_filename(str(pub_id)))
        if publication['thumb'] is not None and len(publication['thumb']) > 0:
            thumb_dir = app.config['THUMB_FOLDER']
            thumb_path = os.path.join(thumb_dir, publication['thumb'])
            _rmDoc(thumb_path)
        # if os.path.isdir(thumb_dir):
        #     _rmDoc(os.path.join(thumb_dir, publication['thumb']))
            # rmtree(thumb_dir)
        app.logger.debug(
                "{} {}: Removed thumbnail of publication ({}):".format(__file__, __name__, pub_id))

        session.commit()
        app.logger.info(
            "{} {}: Successfully removed publication ({}):".format(__file__, __name__, pub_id))
        return jsonify({
            'msg': 'Publication removed successfully!'.format(publication['title'])
        })

    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to delete publication:".format(__file__, __name__))
        session.rollback()
        return ('500 Internal Server Error!', 500)
    finally:
        session.close()

@manipulate_db.route('/delete/document/', methods=['POST'])
@login_required
def delete_document():
    """
    Handles POST requests to delete a document from the database.
    @return: Either a HTTP 200 in case of success or a HTTP 500 in case of failure.
    @rtype: HTTP response
    """
    if not current_user.has_role('admin') and not current_user.has_role('editor'):
        return ("User not authorized to delete document.", 403)

    session = db.session()
    try:
        if not 'pub_id' in request.json or not isinstance(request.json['pub_id'], int):
            raise ValueError("/delete/document: Please specify a publication id of the document to delete.")
        if not 'id' in request.json or not isinstance(request.json['id'], int):
            raise ValueError("/delete/document: Please specify a document id of the document to delete.")

        pub_id = request.json['pub_id']
        id = request.json['id']

        if not _is_authorized(pub_id, current_user):
            app.logger.warning(
                "{} {}: User {} not authorized to delete document ({}):".format(__file__, __name__, current_user.username, id))
            return ("User not authorized to delete this document", 403)

        publication = session.query(Publications).filter(Publications.id == pub_id).first()
        publication = publication.to_dict() if publication is not None else {}
        document = getDocumentById(session, id)

        if len(publication) == 0:
            app.logger.debug(
                "{} {}: Publication of document to delete not found:".format(__file__, __name__))
            abort(404, description="Publication of document not found.")
        if len(document) == 0:
            app.logger.debug(
                "{} {}: document to delete not found:".format(__file__, __name__))
            abort(404, description="Document to delete not found.")

        # remove document from database + remove as mainfile if it was
        session.query(Documents).filter(Documents.id == id).delete()
        if publication['mainfile'] == document['filename']:
            session.query(Publications).filter(Publications.id == pub_id).update({'mainfile': None})

        # pdf_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'pdf', secure_filename(str(publication['id'])))
        _rmDoc(os.path.join(app.config['PDF_FOLDER'], document['filename']))

        session.commit()
        app.logger.info(
            "{} {}: Successfully deleted document ({}):".format(__file__, __name__, id))
        return jsonify({'msg': "Document successfully removed."})
    except Exception:
        app.logger.exception(
            "{} {}: An exception occurred while trying to delete document:".format(__file__, __name__))
        session.rollback()
        return (500, "Internal server error!")
    finally:
        session.close()

@manipulate_db.route('/delete/author/', methods=['POST'])
@login_required
def delete_author():
    """
    Handles POST requests to delete an author from the database.
    @return: Either a HTTP 200 in case of success or a HTTP 500 in case of failure.
    @rtype: HTTP response
    """
    if not current_user.has_role('admin'):
        return ("User not authorized to delete author.", 403)

    session = db.session()
    try:
        if 'author_id' not in request.json or not isinstance(request.json['author_id'], int):
            raise ValueError("/delete/author: Please specify an id to delete an author")

        author_id = request.json['author_id']

        author = getAuthorById(author_id)

        if len(author) == 0:
            abort(404, description="Author to delete not found.")

        session.query(Authors_publications).filter(Authors_publications.author_id == author_id).delete()
        session.query(Authors).filter(Authors.id == author_id).delete()
        session.commit()

        app.logger.info("{} {}: Successfully removed author ({})".format(__file__, __name__, author_id))
        return jsonify({
            'msg': 'Author successfully removed.'
        })
    except Exception:
        app.logger.exception(
            "{} {}: An exception occurred while trying to delete author ({}):".format(__file__, __name__, id))
        session.rollback()
        return ("Something went wrong. Could not remove author.", 500)
    finally:
        session.close()

@manipulate_db.route('/delete/keyword/', methods=['POST'])
@login_required
def delete_keyword():
    """
    Handles POST requests to delete keywords from the database.
    @return: Either a HTTP 200 in case of success or a HTTP 500 in case of failure.
    @rtype: HTTP response
    """
    if not current_user.has_role('admin'):
        return ("User not authorized to delete keyword.", 403)

    session = db.session()
    try:
        if not 'keyword_id' in request.json or not isinstance(request.json['keyword_id'], int):
            raise ValueError("/delete/keyword: An id of the keyword to delete must be specified")

        keyword_id = request.json['keyword_id']

        session.query(Keywords_publication).filter(Keywords_publication.keyword_id == keyword_id).delete()
        session.query(Keywords).filter(Keywords.id == keyword_id).delete()
        session.commit()

        app.logger.info("{} {}: Successfully deleted keyword:".format(__file__, __name__))
        return jsonify({
            'msg': 'Keyword successfully removed.'
        })
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to delete keyword:".format(__file__, __name__))
        session.rollback()
        return ("Something went wrong. Could not remove keyword.", 500)

@manipulate_db.route('/delete/category/', methods=['POST'])
@login_required
def delete_category():
    """
    Handles POST requests to delete a category from the database.
    @return: Either a HTTP 200 in case of success or a HTTP 500 in case of failure
    @rtype: HTTP response
    """
    if not current_user.has_role('admin'):
        return ("User not authorized to delete category.", 403)

    session = db.session()
    try:
        if not 'category_id' in request.json or not isinstance(request.json['category_id'], int):
            raise ValueError("/delete/category: An id of the category to remove must be specified.")

        category_id = request.json['category_id']

        c = session.query(Categories).filter(Categories.id == category_id).first()
        left = c.lft
        right = c.rght
        width = right - left + 1

        # delete category and all children
        session.query(Categories_publications).filter(Categories_publications.category_id == category_id).delete()
        session.query(Categories).filter(Categories.lft.between(left, right)).delete(synchronize_session='fetch')

        # update currently corrupted tree
        for r in session.query(Categories).filter(Categories.rght > right).all():
            r.rght = r.rght - width
        for r in session.query(Categories).filter(Categories.lft > right).all():
            r.lft = r.lft - width

        session.commit()
        app.logger.exception("{} {}: Successfully removed category:".format(__file__, __name__))
        flash('Category removed successfuly.', 'success')
        return redirect('/admin/categories')
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to delete category:".format(__file__, __name__))
        session.rollback()
        return ("Something went wrong. Could not remove category.", 500)
    finally:
        session.close()
