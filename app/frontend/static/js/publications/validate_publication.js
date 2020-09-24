'use strict';

let required_inputs_publication = {
    Article: ['select-authors', 'input-title', 'input-bibtex-7', 'input-year', 'input-bibtex-15'],
    Book: ['select-authors',  'input-title', 'input-bibtex-16', 'input-year'],
    Booklet: ['input-title'],
    Conference: ['select-authors', 'input-title', 'input-bibtex-1', 'input-year'],
    Inbook: ['select-authors', 'input-title', 'input-bibtex-2', 'input-bibtex-12', 'input-bibtex-16', 'input-year'],
    Incollection: ['select-authors', 'input-title', 'input-bibtex-2', 'input-bibtex-12', 'input-bibtex-16', 'input-year'],
    Inproceedings: ['select-authors', 'input-title', 'input-bibtex-1', 'input-year'],
    Manual: ['input-title'],
    Masterthesis: ['select-authors', 'input-title', 'input-bibtex-13', 'input-year'],
    Misc: ['input-title'],
    PhDThesis: ['select-authors', 'input-title', 'input-bibtex-13', 'input-year'],
    Proceedings: ['input-title', 'input-year'],
    Techreport: ['select-authors', 'input-title', 'input-bibtex-6', 'input-year'],
    Unpublished: ['select-authors', 'input-title', 'input-bibtex-9']
};

/*
Validate publication form
 */
$('#submit-publication').on('submit click', function(event) {
    event.preventDefault();

    let type = $('#input-type').val();

    let count_invalid = required_inputs_publication[type].map((input) => {
        if($('#' + input).val().length) {
            $('#' + input).removeClass('is-invalid');
            return 0;
        }
        else {
            $('#' + input).addClass('is-invalid');
            return 1;
        }
    }).reduce((a, b) => a + b, 0);

    if(count_invalid === 0) {
        $('#publication-form').submit();
        // $(this).submit();
    } else {
        addStatusMessage('Please provide the missing informations (marked red).', false);
    }
});