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

from backend.db_controller.db import SQLAlchemy

from backend.db_controller.db import Authors_publications
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addAuthorsPublications(session, **columns):
    """
    Add authors <-> publications mapping to the database
    @param session: An open database session
    @type session: SQLAlchemy Session
    @param columns: a dict containing an 'author_id', 'publication_id' and the 'position' of the author in the paper
    @type columns: dict
    @return: the newly created AuthorPublications object
    @rtype: AuthorsPublication object
    """
    if not isInt(columns.get('author_id', '') or not isInt(columns.get('publication_id'))) or not isInt(columns.get('position')):
        raise ValueError('Author_id, publication_id and position must be numbers')

    newAuthorsPublications = Authors_publications(
        author_id=columns['author_id'],
        publication_id=columns['publication_id'],
        position=columns['position']
    )
    session.add(newAuthorsPublications)
    return newAuthorsPublications