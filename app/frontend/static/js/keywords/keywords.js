'use strict';

/*
Create new dialog to edit a keyword
 */
function createEditKeywordDialog(data) {
    let modal_id = 'edit-keyword-modal';

    let template = $(document.querySelector('#edit-keyword-modal_template').content.cloneNode(true));
    let content = $('#content');

    template.find('#edit-keyword-form').attr('action', '/edit/keyword/' + data['id']);
    template.find('#input-name').val(data['name']);

    template.find('.close-keyword-dialog').on('click', function () {
        $('.modal-backdrop').remove();
        $('body').removeClass("modal-open");
        $('#' + modal_id).remove();
    });

    template.find('#edit-keyword-form').on('submit', function (event) {
        event.preventDefault();
        let required_inputs_keyword = ['input-name'];

        let count_invalid = required_inputs_keyword.map((input) => {
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
                $('#edit-keyword-modal').modal('toggle');
                let keyword = response.keyword;
                $('#keyword_' + keyword.id).find('td:eq(0)').html(keyword.name)
            }, 'json')
                .fail(function (response) {
                    addStatusMessage(response.responseText, false,);
                    $('#edit-keyword-modal').modal('toggle');
                });
        }
    });

    content.parent().prepend(template);
    $('#' + modal_id).modal();

    return false;
}


/*
Fetch info on keyword and render edit keyword dialog
 */
function editKeyword() {
    let keyword_id = $(this).data().keywordid;
    $.ajax({
        url: "/edit/keyword/" + keyword_id,
        type: 'GET'
    }).done(function (resp) {
        createEditKeywordDialog(resp);
    }).fail(function (response) {
        addStatusMessage(response.responseText, false);
        $("html, body").animate({scrollTop: 0}, "slow");
        $('#' + modal_id).modal("hide");
    });
}

/*
Render confirmation dialog to delete a keyword.
 */
function deleteKeyword() {
    let keyword_id = $(this).data().keywordid;

    DeleteDialog(
        "Delete Keyword from Database",
        "Are you sure you want to remove the Keyword from the database? <br> The action can <b>not</b> be reversed.",
        "keyword",
        keyword_id
    )
}

/*
Submit new keyword and update page to display newly added keyword
 */
function addKeyword() {
    $.post($(this).attr('action'), $(this).serialize(), function (response) {
        addStatusMessage(response.msg, true);
        $('#add-keyword-modal').modal('toggle');

        let keyword = response.keyword;
        let newRow = $('#table-keywords').DataTable().row.add([keyword.name, '', '']).draw().node();
        $(newRow).attr("id", "keyword_" + keyword.id);
        $(newRow).find('td:eq(1)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-primary edit-keyword-btn p-0',
                'data-Keywordid': keyword.id,
                click: editKeyword
            }).append($('<i>', {class: 'fa fa-edit'})));
        $(newRow).find('td:eq(2)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-danger delete-keyword-btn p-0',
                'data-Keywordid': keyword.id,
                click: deleteKeyword
            }).append($('<i>', {class: 'fa fa-times'})));
    }, 'json')
        .fail(function (response) {
            addStatusMessage(response.responseText, false);

            $('#add-keyword-modal').modal('toggle');
        });
    return false;
}

/*
Activate add/edit/delete keyword buttons and format HTML table
 */
$(document).ready(function () {
    $('.edit-keyword-btn').on('click', editKeyword);

    $('.delete-keyword-btn').on('click', deleteKeyword);

    $('#add-keyword-form').on('submit', addKeyword);

    // Nicely format Keywords Table
    $('#table-keywords').DataTable({
        'initComplete': function () {
            $(this).removeClass('d-none');
            $('#spinner').remove();
        }
    });
});