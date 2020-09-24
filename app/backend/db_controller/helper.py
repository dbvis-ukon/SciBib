from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from backend.db_controller.db import Users_publication


db = SQLAlchemy()

def _is_authorized(pub_id, curr_user):
    """
    @note currently not in use.
    Check if a user is authorized to edit a publication. A user must either have created the publication or be an admin.
    @param pub_id: the database ID of the publication
    @type pub_id: int
    @param curr_user: the user object of the user trying to edit a publication
    @type curr_user: User object
    @return: if the user is authorized
    @rtype: bool
    """
    # check if the current user is the editor of the publication
    is_editor = db.session.query(
        db.session().query(Users_publication)\
        .filter(Users_publication.user_id == curr_user.get_id() and Users_publication.publication_id == pub_id).exists()
    ).scalar()

    db.session.close()
    return is_editor or curr_user.has_role('admin')

def _createCiteName(authors, year, title):
    """
    Create a name for a bibtex citation:
      * concat the first two letters of the first three author
      * with the publication year
      * and the first word of the publication title
    @param authors: the authors of a publication
    @type authors: list(Author)
    @param year: the publication year of a publication
    @type year: int
    @param title: the title of a publication
    @type title: string
    @return: the newly created citename for the publication
    @rtype: string
    """
    citename = ''.join([a['surname'][:2].title() for a in authors[:3]])
    if len(authors) > 3:
        citename += '+'
    citename += year
    citename += title.split()[0]
    return citename

def isInt(s):
    """
    Check if a string is secretly an int.
    @param s: string to check
    @type s: string
    @return: if the string is an int
    @rtype: bool
    """
    try:
        int(s)
        return True
    except ValueError:
        return False
