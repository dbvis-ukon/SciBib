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
    try:
        return send_file('{}/uploadedFiles/{}'.format(app.config['STATIC_FOLDER'], filename))
    except Exception:
        app.logger.exception("{} {}: Exception occurred while trying to upstream pdf:".format(__file__, __name__))
        return abort(404)

@upload_blueprint.route('/publications/bibtex/<pub_id>')
def send_bibtex(pub_id):
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