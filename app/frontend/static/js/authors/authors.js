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
Create a new dialog to edit an author. Auto-updates author information in HTML table on success.
 */
function createEditAuthorDialog(data) {
    let modal_id = 'edit-author-modal';

    let template = $(document.querySelector('#edit-author-modal_template').content.cloneNode(true));
    let content = $('#content');

    template.find('#edit-author-form').attr('action', '/edit/author/' + data['id']);
    template.find('#input-forename').val(data['forename']);
    template.find('#input-surname').val(data['surname']);

    template.find('.close-author-dialog').on('click', function () {
        $('.modal-backdrop').remove();
        $('body').removeClass("modal-open");
        $('#' + modal_id).remove();
    });

    template.find('#edit-author-form').on('submit', function (event) {
        event.preventDefault();

        let required_inputs_author = ['input-forename', 'input-surname'];

        let count_invalid = required_inputs_author.map((input) => {
            if ($('#' + input).val().trim().length) {
                $('#' + input).removeClass('is-invalid');
                return 0;
            } else {
                $('#' + input).addClass('is-invalid');
                return 1;
            }
        }).reduce((a, b) => a + b, 0);

        if (count_invalid === 0) {
            $.post($(this).attr('action'), $(this).serialize(), function (response) {
                addStatusMessage(response.msg, true);
                $('#edit-author-modal').modal('toggle');

                let author = response.author;
                $('#author_' + author.id).find('td:eq(0)').html(author.surname);
                $('#author_' + author.id).find('td:eq(1)').html(author.forename);
                $('#author_' + author.id).find('td:eq(2)').html(author.cleanname);
            }, 'json')
                .fail(function (response) {
                    addStatusMessage(response.responseText, false);

                    $('#edit-author-modal').modal('toggle');
                });
        }
    });

    content.parent().prepend(template);
    $('#' + modal_id).modal();

    return false;
}


/*
Fetches information on author from the database and renders a new dialog to edit an author
 */
function editAuthor() {
    let author_id = $(this).data().authorid;

    $.ajax({
        url: "/edit/author/" + author_id,
        type: 'GET',
    }).done(function (resp, xd, xhr) {
        createEditAuthorDialog(resp);
    }).fail(function (response) {
        addStatusMessage(response.responseText, false);

        $("html, body").animate({scrollTop: 0}, "slow");
        $('#' + author_id).modal("hide");
    });
}

/*
Submit form to add a new author.
 */
function addAuthor() {
    $.post($(this).attr('action'), $(this).serialize(), function (response) {
        addStatusMessage(response.msg, true);
        $('#add-author-modal').modal('toggle');

        let author = response.author;
        let newRow = $('#table-authors').DataTable().row.add([author.surname, author.forename, author.cleanname, '0', '', '', '']).draw().node();
        $(newRow).attr("id", "author_" + author.id);
        $(newRow).find('td:eq(4)')
            .append($('<a>', {'class': 'btn text-primary p-0', href: "/view/authors/" + author.id})
                .append($('<i>', {class: 'fa fa-external-link'})));
        $(newRow).find('td:eq(5)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-primary edit-author-btn p-0',
                'data-authorid': author.id,
                click: editAuthor
            }).append($('<i>', {class: 'fa fa-edit'})));
        $(newRow).find('td:eq(6)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-danger delete-author-btn p-0',
                'data-authorid': author.id,
                click: deleteAuthor
            }).append($('<i>', {class: 'fa fa-times'})));
    }, 'json')
        .fail(function (response) {
            addStatusMessage(response.responseText, false);

            $('#add-author-modal').modal('toggle');
        });
    return false;
}

function deleteAuthor() {
    let author_id = $(this).data().authorid;

    DeleteDialog(
        "Delete Author from Database",
        "Are you sure you want to remove the Author from the database? <br> The action can <b>not</b> be reversed.",
        "author",
        author_id
    )
}

/*
Activate buttons to add/edit/delete authors and format authors table.
 */
$(document).ready(function () {
    $('.edit-author-btn').on('click', editAuthor);

    $('.delete-author-btn').on('click', deleteAuthor);

    $('#add-author-form').on('submit', addAuthor);
    // Nicely format Authors Table
    $('#table-authors').DataTable({
        'order': [[3, "desc"]],
        'initComplete': function () {
            $(this).removeClass('d-none');
            $('#spinner').remove();
        }
    });
});