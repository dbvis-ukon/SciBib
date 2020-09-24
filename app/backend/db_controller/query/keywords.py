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

from backend.db_controller.db import Keywords


db = SQLAlchemy()


def getKeywords():
    """
    Get a list of all keywords
    @return: a list of keywords
    @rtype: list(dict)
    """
    result = [r.to_dict() for r in db.session.query(Keywords)]

    db.session.close()
    return result

def getKeywordByName(name):
    """
    Get a keyword by its name
    @param name: the name of the keyword
    @type name: string
    @return: the keyword info
    @rtype: dict
    """
    keyword = db.session.query(Keywords).filter(Keywords.name == name).first()

    db.session.close()
    return keyword.to_dict() if keyword is not None else {}

def addKeyword(session, **columns):
    """
    Add a keyword to the database
    @param session: An open SQLAlchemy session
    @type session: SQLAlchemy session
    @param columns: A dict containing the 'name' of the keyword
    @type columns: dict
    @return: the newly created keyword object
    @rtype: keyword object
    """
    if not columns.get('name', ''):
        raise ValueError('Keyword name required to add a new keyword.')

    newKeyword = Keywords(
        name=columns['name']
    )
    session.add(newKeyword)
    return newKeyword
