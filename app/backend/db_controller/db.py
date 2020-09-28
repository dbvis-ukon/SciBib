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

"""

DB_Controller for the scibib database

"""

from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.dialects.mysql import TINYINT, MEDIUMTEXT, ENUM, DATETIME, YEAR, INTEGER
from flask_security import UserMixin, RoleMixin
from datetime import datetime

# See https://github.com/pallets/flask-sqlalchemy/issues/589#issuecomment-361075700
class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True


db = SQLAlchemy()

class Authors(db.Model, SerializerMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    surname = db.Column(db.String(255))
    forename = db.Column(db.String(255))
    cleanname = db.Column(db.String(255))


class Authors_publications(db.Model, SerializerMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer())
    publication_id = db.Column(db.Integer())
    position = db.Column(db.Integer())

class Categories(db.Model, SerializerMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer())
    lft = db.Column(db.Integer())
    rght = db.Column(db.Integer())
    description = db.Column(db.String(255))


class Categories_publications(db.Model, SerializerMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer())
    publication_id = db.Column(db.Integer())

class Documents(db.Model, SerializerMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    publication_id = db.Column(db.Integer())
    visible = db.Column(TINYINT)
    remote = db.Column(TINYINT)
    filename = db.Column(db.String(255))
    description = db.Column(db.String(255))

class Keywords(db.Model, SerializerMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)

class Keywords_publication(db.Model, SerializerMixin):
    keyword_id = db.Column(db.Integer(), db.ForeignKey('keywords.id'), primary_key=True)
    publication_id = db.Column(db.Integer(), db.ForeignKey('publications.id'), primary_key=True)

class Posts(db.Model, SerializerMixin):
    id = db.Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(255))
    created = db.Column(DATETIME)
    modified = db.Column(DATETIME)

class Publications(db.Model, SerializerMixin):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    address = db.Column(MEDIUMTEXT)
    booktitle = db.Column(db.String(255))
    chapter = db.Column(db.Integer())
    edition = db.Column(db.String(255))
    editor = db.Column(db.String(255))
    howpublished = db.Column(MEDIUMTEXT)
    institution = db.Column(db.String(255))
    journal = db.Column(db.String(255))
    month = db.Column(db.String(3))
    note = db.Column(MEDIUMTEXT)
    number = db.Column(db.String(255))
    organization = db.Column(db.String(255))
    pages = db.Column(db.String(255))
    school = db.Column(db.String(255))
    series = db.Column(db.String(255))
    title = db.Column(db.String(255))
    volume = db.Column(db.String(255))
    url = db.Column(db.String(255))
    doi = db.Column(db.String(255))
    year = db.Column(YEAR)
    citename = db.Column(db.String(255), unique=True)
    publisher = db.Column(db.String(255))
    published = db.Column(TINYINT)
    submitted = db.Column(TINYINT)
    public = db.Column(TINYINT)
    created = db.Column(db.DateTime, default=datetime.now())
    modified = db.Column(db.DateTime, default=datetime.now())
    copyright_id = db.Column(db.Integer(), index=True)
    type = db.Column(ENUM("Inproceedings", "Article", "Techreport", "Inbook",
                                         "Book", "Booklet", "Conference", "Incollection",
                                         "Manual", "Masterthesis", "Misc", "PhDThesis",
                                         "Proceedings", "Unpublished"))
    thumb = db.Column(db.String(255))
    mainfile = db.Column(MEDIUMTEXT)
    publicationdate = db.Column(db.Date, index=True)
    kops = db.Column(db.String(255))
    other = db.Column(db.TEXT)
    abstract = db.Column(MEDIUMTEXT)

roles_users = db.Table('roles_users',
                      db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Users_publication(db.Model, SerializerMixin):
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    publication_id = db.Column(db.Integer(), db.ForeignKey('publications.id'), primary_key=True)

class role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))

    users = db.relationship("users", secondary="roles_users",
                            backref=db.backref("users"))

class users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    token = db.Column(db.String(255))
    token_expires = db.Column(DATETIME)
    api_token = db.Column(db.String(255))
    activation_date = db.Column(DATETIME)
    tos_date = db.Column(DATETIME)
    active = db.Column(TINYINT)
    is_superuser = db.Column(TINYINT)
    created = db.Column(DATETIME)
    modified = db.Column(DATETIME)
    roles = db.relationship('role', secondary="roles_users",
                            backref=db.backref('roles', lazy='dynamic'))

