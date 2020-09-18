from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy
from backend.db_controller.db import Users_publication


db = SQLAlchemy()

def _is_authorized(pub_id, curr_user):
    # check if the current user is the editor of the publication
    is_editor = db.session.query(
        db.session().query(Users_publication)\
        .filter(Users_publication.user_id == curr_user.get_id() and Users_publication.publication_id == pub_id).exists()
    ).scalar()

    db.session.close()
    return is_editor or curr_user.has_role('admin')

def _createCiteName(authors, year, title):
    citename = ''.join([a['surname'][:2].title() for a in authors[:3]])
    if len(authors) > 3:
        citename += '+'
    citename += year
    citename += title.split()[0]
    return citename

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
