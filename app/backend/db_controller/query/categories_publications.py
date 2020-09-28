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
# from flask_sqlalchemy import SQLAlchemy

from backend.db_controller.db import Categories_publications
from backend.db_controller.helper import isInt

db = SQLAlchemy()

def addCategoriesPublications(session, **columns):
    """
    Add categories <-> publications mapping to the database.
    @param session: An open database session
    @type session: SQLAlchemy session
    @param columns: a dict with keys for the 'category_id' and 'publication_id' to add
    @type columns: dict
    @return: the newly created CategoryPublications object
    @rtype: CategoryPublications object
    """
    if not isInt(columns.get('category_id', '') or not isInt(columns.get('publication_id', ''))):
        raise ValueError('Category_id and publication_id must be numbers')

    newAuthorsPublications = Categories_publications(
        category_id=columns['category_id'],
        publication_id=columns['publication_id'],
    )
    session.add(newAuthorsPublications)
    return newAuthorsPublications