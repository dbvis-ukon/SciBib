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