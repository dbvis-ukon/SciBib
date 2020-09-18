from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Documents
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def getDocumentById(session, id):
    res = session.query(Documents).filter(Documents.id == id).first()
    return res.to_dict() if res is not None else {}

def getDocumentsOfPub(session, pub_id):
    return [ r.to_dict() for r in session.query(Documents).filter(Documents.publication_id == pub_id).order_by(Documents.id.asc()).all() ]

def addDocument(session, **columns):
    if not isInt(columns.get('publication_id', '')):
        raise ValueError('Publication_id must be a number')
    if columns.get('filename', '') == '':
        raise ValueError('Filename cannot be empty')

    newDocument = Documents(
        publication_id=columns['publication_id'],
        visible=columns.get('visible', 1),
        remote=columns.get('remote', 0),
        filename=columns['filename'],
        description=columns.get('description', '')
    )
    session.add(newDocument)
    return newDocument