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
Config of the project

"""

import os
import logging
from distutils.util import strtobool

# DB credentials
MYSQL_URL = os.environ['SCIBIB_MYSQL_HOST']
MYSQL_DB = os.environ['SCIBIB_MYSQL_DATABASE']
MYSQL_USER = os.environ['SCIBIB_MYSQL_USER']
MYSQL_PW = os.environ['SCIBIB_MYSQL_PASSWORD']

# Mail Configuration
MAIL_SERVER = os.environ['MAIL_SERVER']
MAIL_PORT = int(os.environ['MAIL_PORT'])
MAIL_USE_SSL = bool(strtobool(os.environ['MAIL_USE_SSL']))
MAIL_USERNAME = os.environ['MAIL_USERNAME']

SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']

# secret to encrypt cookies
SECRET = os.environ['SECRET']

BEHIND_PROXY = bool(strtobool(os.environ['BEHIND_PROXY']))

DB_URL = 'mysql://{user}:{pw}@{url}/{db}?charset=utf8'.format(
     user=MYSQL_USER,
     pw= MYSQL_PW,
     url= MYSQL_URL,
     db=MYSQL_DB
)

# E-Mail Sender account
EMAIL_SENDER = os.environ['SCIBIB_EMAIL_SENDER']

# Amount of Publications to lazy load
load_quantity = 40


STATIC_FOLDER = os.path.join('frontend', 'static')
TEMPLATE_FOLDER = os.path.join('frontend', 'templates')
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploadedFiles')
PDF_FOLDER = os.path.join(UPLOAD_FOLDER)
THUMB_FOLDER = os.path.join(UPLOAD_FOLDER, 'thumbs')

LOG_FOLDER = os.path.join('var', 'log', 'scibib.log')
LOG_LEVEL = logging.DEBUG

type_to_color = {
     'Inproceedings': '#1f78b4',
     'Conference':     '#8B4513',
     'Book':        '#e31a1c',
     'Inbook':      '#fb9a99',
     'Booklet':      '#cab2d6',
     'Incollection':  '#ff7f00',
     'Masterthesis':  '#b2df8a',
     'PhDThesis':     '#33a02c',
     'Article':      '#6a3d9a',
     'Manual':         '#b15928',
     'Proceedings':    '#fdbf6f',
     'Techreport':   '#f0e130',
      'Misc':        '#000000',
      'Unpublished': '#808080'
}

valid_publication_types = ["Article", "Book", "Booklet", "Conference", "Inbook", "Incollection", "Inproceedings",
                           "Manual", "Masterthesis", "Misc", "PhDThesis", "Proceedings", "Techreport", "Unpublished"]

class BaseCongig(object):
     '''
     Base config class
     '''
     DEBUG = True
     TESTING = False

class ProductionConfig(BaseCongig):
     """
     Production specific config
     """
     DEBUG = False

class DevelopmentConfig(BaseCongig):
     """
     Development environment specific configuration
     """
     DEBUG = True
     TESTING = True