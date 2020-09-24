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

from flask import Blueprint, send_file, Response, current_app as app, abort
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

from backend.db_controller.query.publications import getPublicationById, getAuthorsOfPub
from backend.db_controller.helper import _createCiteName

upload_blueprint = Blueprint('upload', __name__)

bib_keys = [
    'address',
    'booktitle',
    'chapter',
    'edition',
    'editor',
    'howpublished',
    'institution',
    'journal',
    'month',
    'note',
    'number',
    'organization',
    'pages',
    'school',
    'series',
    'volume',
    'publisher',
    'doi',
    'other'
]

def _filterBibtexDataOfPublication(publication):
    """
    Helper function to prepare bibtex output. Fetches authors of a publication and handles special field 'Other', which
    generates a string separated by ; for all non-standard bibtex fields.
    @param publication: info on the publication to generate a bibtex string for
    @type publication: dict
    @return: dict containing info to generate a bibtex string for a publication
    @rtype: dict
    """
    if (len(publication) == 0):
        return {}

    authors = getAuthorsOfPub(publication['id'])

    bib_entries = {}

    bib_entries['title'] = publication['title']
    bib_entries['author'] = ' and '.join([', '.join([author['surname'].title(), author['forename'].title()]) for author in authors])
    bib_entries['year'] = str(publication['year']) if publication['year'] else None
    bib_entries['ID'] = publication['citename'] if publication['citename'] else _createCiteName(authors, bib_entries['year'], publication['title'])
    bib_entries['ENTRYTYPE'] = publication['type'].lower() if 'type' in publication and publication['type'] is not None else 'Misc'

    # fetch valid entries for the publication
    for entry in bib_keys:
        # treat special entries
        if entry == 'other' and publication['other']:
            for item in publication[entry].split(';'):
                keyVal = item.split('=')
                bib_entries[keyVal[0]] = keyVal[1]
        else:
            bib_entries[entry] = publication[entry] if publication[entry] else None

    # Remove empty fields
    bib_entries = {key: str(value) for key, value in bib_entries.items() if value is not None}
    return bib_entries

@upload_blueprint.route('/uploadedFiles/<filename>')
def send_pdf(filename):
    """
    Simply send a PDF from the uploads folder to the browser.
    @param filename: the file to send
    @type filename: string
    @return: the PDF
    @rtype: file
    """
    try:
        return send_file('{}/uploadedFiles/{}'.format(app.config['STATIC_FOLDER'], filename))
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to upstream pdf:".format(__file__, __name__))
        return abort(404)

@upload_blueprint.route('/publications/bibtex/<pub_id>')
def send_bibtex(pub_id):
    """
    Generates and sends a bibtex string for a publication to the frontend.
    @param pub_id: the database id of the publication
    @type pub_id: int
    @return: a bibtex string for the publication
    @rtype: bibtex in plain text
    """
    publication = getPublicationById(pub_id)
    bibtex_data = _filterBibtexDataOfPublication(publication)

    try:
        db = BibDatabase()
        db.entries = [bibtex_data]
        writer = BibTexWriter()
        return Response(writer.write(db), mimetype='text/plain')
    except KeyError:
        app.logger.exception("{} {}: Exception occurred while trying to upload bibtex:".format(__file__, __name__))
        return abort(404)