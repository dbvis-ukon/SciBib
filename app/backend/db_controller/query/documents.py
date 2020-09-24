from backend.db_controller.db import SQLAlchemy
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Documents
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def getDocumentById(session, id):
    """
    Get a document by ID
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param id: the database ID of the document
    @type id: int
    @return: the document info
    @rtype: dict
    """
    res = session.query(Documents).filter(Documents.id == id).first()
    return res.to_dict() if res is not None else {}

def getDocumentsOfPub(session, pub_id):
    """
    Get all documents related to a publication
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param pub_id: the database publication ID
    @type pub_id: int
    @return: a list of documents
    @rtype: list(dict)
    """
    return [ r.to_dict() for r in session.query(Documents).filter(Documents.publication_id == pub_id).order_by(Documents.id.asc()).all() ]

def addDocument(session, **columns):
    """
    Add a new document to the database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param columns: At least a dict with a 'publication_id' and a 'filename'
    @type columns: dict
    @return: the newly created document object
    @rtype: document object
    """
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