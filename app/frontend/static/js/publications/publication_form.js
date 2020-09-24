/*
 * Copyright (C) 2020 University of Konstanz -  Data Analysis and Visualization Group
 * This file is part of SciBib <https://github.com/dbvis-ukon/SciBib>.
 *
 * SciBib is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SciBib is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SciBib.  If not, see <http://www.gnu.org/licenses/>.
 */

'use strict';

/*
Activate interactive elements for publication forms.
 */
$(document).ready(function () {
    // Define text hints when checking/changing buttons for submitting/publishing publications
    let no_selection_text = 'This paper is <span class="text-warning">not yet published</span> and is <span class="text-warning">hidden from public</span>';
    let only_submitted_text = 'This paper was <span class="text-success">submitted</span > but is <span class="text-warning">yet to appear</span> and is <span class="text-warning">hidden from public</span>';
    let submitted_published_text = 'This paper was <span class="text-success">was successfully published</span> and is <span class="text-warning">hidden from public</span>';
    let submitted_published_public = 'This paper was <span class="text-success">successfully published</span> and <span class="text-success">can be viewed by everyone</span>';
    let submitted_ispublic = '<span class="text-warning"><i class="fa fa-exclamation-triangle"></i></span> A publication is usually hidden from public until it is successfully published';
    let published_ispublic = '<span class="text-warning"><i class="fa fa-exclamation-triangle"></i></span> A publication usually needs to be submitted before it can be published';
    let submitted_published = 'This paper was <span class="text-success">successfully published</span> and is <span class="text-warning">hidden from public</span>';

    /*
    Handle rendering of appropriate texts when checking/changing buttons for submitting/publishing publications
     */
    $('.form-check-input').on('change', function () {
            let submitted = $('#input-submitted').is(":checked");
            let published = $('#input-published').is(":checked");
            let is_public = $('#input-public').is(":checked");
            let made_public_on = $('#input-madepublic').is(":checked");
            let made_public_date = $('#input-pubdate').val();

            if (submitted && published && is_public) {
                $('#info-public-check').html(submitted_published_public);
            } else if (submitted && published && !is_public) {
                $('#info-public-check').html(submitted_published);
            } else if (submitted && !published && is_public) {
                $('#info-public-check').html(submitted_ispublic);
            } else if (!submitted && published && is_public) {
                $('#info-public-check').html(published_ispublic);
            } else if (submitted && !published && !is_public) {
                $('#info-public-check').html(only_submitted_text);
            } else if (!submitted && !published && is_public) {
                $('#info-public-check').html(submitted_ispublic);
            } else if (!submitted && !published && !is_public) {
                $('#info-public-check').html(no_selection_text);
            }

            if (submitted && published && made_public_on) {
                document.querySelector('#info-public-check').innerHTML += ' from the date ' + made_public_date;
            }
        }
    );
    $('.form-check-input').trigger('change');

    /*
    Define bibtex entries for different publications types
     */
    let bibtex = {
        Article: [false, false, false, false, false, false, false, true, true, true, true, false, true, false, false, true, false],
        Book: [true, false, false, true, true, false, false, false, true, true, true, false, false, false, true, true, true],
        Booklet: [true, false, false, false, false, true, false, false, true, true, false, false, false, false, false, false, false],
        Conference: [true, true, false, false, true, false, false, false, true, true, true, true, true, false, true, true, true],
        Inbook: [true, false, true, true, true, false, false, false, true, true, true, false, true, false, true, true, true],
        Incollection: [true, true, true, true, true, false, false, false, true, true, true, false, true, false, true, true, true],
        Inproceedings: [true, true, false, false, true, false, false, false, true, true, true, true, true, false, true, true, true],
        Manual: [true, false, false, true, false, false, false, false, true, true, false, true, false, false, false, false, false],
        Masterthesis: [true, false, false, false, false, false, false, false, true, true, false, false, false, true, false, false, false],
        Misc: [false, false, false, false, false, true, false, false, true, true, false, false, false, false, false, false, false],
        PhDThesis: [true, false, false, false, false, false, false, false, true, true, false, false, false, true, false, false, false],
        Proceedings: [true, false, false, false, true, false, false, false, true, true, true, true, false, false, true, true, true],
        Techreport: [true, false, false, false, false, false, true, false, true, true, true, false, false, false, false, false, false],
        Unpublished: [false, false, false, false, false, false, false, false, true, true, false, false, false, false, false, false, false]
    };

    /*
    Render only the bibtex entries for the selected publication type
     */
    $('#input-type').on('change', function () {
        let bibtext_input_row = 'bibtex-info-r-';
        let bibtex_input = 'input-bibtex-';

        for (let i = 0; i < bibtex['Article'].length; i++) {
            if (bibtex[$('#input-type option:selected').text()][i]) {
                $('#' + bibtext_input_row + i).show();
            } else {
                $('#' + bibtext_input_row + i).hide();
                $('#' + bibtex_input + i).val('');
            }
        }

        let val = $('#input-type option:selected').val();
        $('#input-type option').attr('selected', false);
        $('#input-type option[value=' + val +']').attr('selected', true);
    });
    $('#input-type').trigger('change');


    /*
    Init author list when editing a publication
     */
    $('#select-authors option:selected').each(function () {
        let _selected = $(this);
        $('#author-list').append($('<li>', {
            id: _selected.html().replace(/\s/g, ''),
            class: "list-group-item list-group-item-action",
            data: {
                'value': _selected.val()
            },
            html: _selected.html()
        }));
    });

    /*
      Make author list sortable
    */
    let el = document.getElementById('author-list');
    new Sortable(el, {
        swap: true,
        swapClass: "highlight",
        wdith: "100%",
        onUpdate: function (event, ui) {

            let id_old = $('#author-list li').eq(event.oldIndex).data().value;
            let id_now = $('#author-list li').eq(event.newIndex).data().value;

            let elemOld = $('#select-authors option[value="' + id_old + '"]');
            let elemNew = $('#select-authors option[value="' + id_now + '"]');
            let cloneOld = $('#select-authors option[value="' + id_old + '"]').clone();
            let cloneNew = $('#select-authors option[value="' + id_now + '"]').clone();

            let oldText = cloneOld.text();
            let oldVal = cloneOld.val();
            let oldData = cloneOld.data().select2Id;
            let newText = cloneNew.text();
            let newVal = cloneNew.val();
            let newData = cloneNew.data().select2Id;

            elemOld.val(newVal);
            elemOld.text(newText);
            elemOld.attr('data-select2-id', newData);
            elemNew.val(oldVal);
            elemNew.text(oldText);
            elemNew.attr('data-select2-id', oldData);

            $('#select-authors').select2({theme: 'bootstrap4'}).trigger("change");
        }
    });

    /*
    Use Select2 package to convert select to mutli-value select boxes
    */

    /* Categories select to select2 multi-value select box */
    initSelect2('select-categories');

    /* Keywords select to select2 multi-value select box */
    initSelect2('select-keywords');

    /* Authors select to select2 multi-value select box */
    initSelect2('select-authors');


    $('#select-authors').on('select2:select', function (e) {
        let element = e.params.data.element;
        let $element = $(element);

        $element.detach();
        $(this).append($element);
        $(this).trigger("change");
        $('#author-list').append('<li id="' + e.params.data.text.replace(/\s/g, '') + '" data-value="' + $element.val() + '" class="list-group-item list-group-item-action">' + e.params.data.text + '</li>');
    });

    $('#select-authors').on('select2:unselect', function (e) {
        $(document.getElementById(e.params.data.text.replace(/\s/g, ''))).remove();
    });

    /*
      Change text on submitting status dynamically
    */
    $('#input-madepublic').on('change', function () {
        let is_checked = $('#input-madepublic').is(":checked");
        $('#input-pubdate').prop('disabled', !is_checked);
    });

    /*
    Add author form submit actions
    */
    $('#add-author-form').on('submit', function () {
        $.post($(this).attr('action'), $(this).serialize(), function (response) {
            // addStatusMessage(response.msg, true);
            $('#add-author-modal').modal('toggle');

            let name = response.author.forename + " " + response.author.surname;
            $('#select-authors').append($('<option>', {'value': response.author.id, 'html': name}));
            // $('#select-authors').select2({theme: 'bootstrap4'}).trigger("change");

            let values = $('#select-authors').val();
            values.push(typeof response.author.id === 'number' ? response.author.id.toString() : response.author.id);
            $('#select-authors').val(values);
            $('#select-authors').select2({theme: 'bootstrap4'}).trigger("change");
            $('#author-list').append('<li id="' + name.replace(/\s/g, '') + '" data-value="' + response.author.id + '" class="list-group-item list-group-item-action">' + name + '</li>');
        }, 'json')
            .fail(function (response) {
                addStatusMessage(response.msg, false);

                $('#add-author-modal').modal('toggle');
            });
        return false;
    });


    /*
    Add Keyword form submit actions
     */
    $('#add-keyword-form').on('submit', function () {
        $.post($(this).attr('action'), $(this).serialize(), function (response) {
            // addStatusMessage(response.msg, true);
            $('#select-keywords').append($('<option>', {'value': response.keyword.id, 'html': response.keyword.name}));
            // $('#select-keywords').select2({theme: 'bootstrap4'}).trigger("change");

            let values = $('#select-keywords').val();
            values.push(typeof response.keyword.id === 'number' ? response.keyword.id.toString() : response.keyword.id);
            $('#select-keywords').val(values);
            $('#select-keywords').select2({theme: 'bootstrap4'}).trigger("change");

            $('#add-keyword-modal').modal('toggle');
        }, 'json')
            .fail(function (response) {
                addStatusMessage(response.msg, false);

                $('#add-keyword-modal').modal('toggle');
            });
        return false;
    });

    /*
    Append a new row for a new link to an external resource
     */
    $('#btn-add-external-doc')
        .on('click', function () {
            let nRows = $('#input-docs-table tr.input-docs-external').length;

            $("#input-docs-table").find('tbody')
                .append($('<tr>')
                    .addClass('input-docs-external')
                    .attr("id", "tr-input-docs-external-" + nRows)
                    .append($('<td>'))
                    .append($('<td>')
                        .append($('<div>')
                            .append($('<input>')
                                .addClass('form-control')
                                .attr("type", "text")
                                .attr("id", "input-docs-external-" + nRows)
                                .attr("name", "input-docs-external-" + nRows)
                                .attr("placeholder", "http://www.external.com/external.pdf")
                            )
                        )
                    )
                    .append($('<td>')
                        .addClass('center-vertical')
                        .append($('<button>')
                            .addClass('btn center-vertical input-docs-del-external')
                            .attr("type", "button")
                            .attr("data-inputid", nRows)
                            .append($('<i>')
                                .addClass("fa fa-times text-danger")
                            )
                        )
                    )
                );

            /* Add listener to delete documents */
            $('.input-docs-del-external').on("click", function () {
                let inputId = $(this).data().inputid;
                $('#tr-input-docs-external-' + inputId).remove();
            });
        });


    /*
    Listener to delete a document
     */
    $('.input-docs-db-del').on("click", function () {
        let id = $(this).data().dbid;
        let rowId = $(this).data().inputid;
        let pubid = $(this).data().pubid;

        DeleteDocumentDialog('Are you sure', id, rowId, pubid);
    });

    /*
    Display thumbnail if exists
     */
    $('#input-thumbnail').on('change', function () {
        if (this.files && this.files[0])
            document.getElementById('thumbnail-preview').src = window.URL.createObjectURL(this.files[0]);
        else
            document.getElementById('thumbnail-preview').src = '/static/images/thumb-default.png';
    });

});
