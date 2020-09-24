'use strict';

/*
Handle form to add a new category to the database.
 */
$(document).ready(function () {

    $('#add-category-form').on('submit', function (event) {
        event.preventDefault();

        $.post($(this).attr('action'), $(this).serialize(), function (response) {
            addStatusMessage(response.msg, true, '/admin/categories');
            $('#add-category-modal').modal('toggle');

            let category = response.category;

            if (category.parent_id !== null) {
                // get number of leading whitespaces
                let ws = $('#a_category_' + category.parent_id).html().search(/\S/);

                $('#category_' + category.parent_id)
                    .append($('<pre>', {'id': category.id, class: 'cat-list'})
                        .append($('<b>')
                            .append($('<a>', {
                                class: 'text-dark',
                                href: '/view/category/' + category.id,
                                html: new Array(ws + 4).join(' ') + category.name + ' - 0'
                            }))));
            } else {
                $('#categories_div')
                    .append($('<pre>', {'id': category.id, class: 'cat-list'})
                        .append($('<b>')
                            .append($('<a>', {
                                class: 'text-dark',
                                href: '/view/category/' + category.id,
                                html: category.name + ' - 0'
                            }))));
            }


        }, 'json')
            .fail(function (response) {
                addStatusMessage(response.responseText, false);
                $('#add-category-modal').modal('toggle');
            });
        return false;
    });

    /* Ajax query to get all categories */
    $.ajax({
        type: 'GET',
        url: '/get/categories',
        cache: false,
        success: function (data) {
            let select = $('#select-parent');
            for (const category of data)
                select.append('<option value="' + category['id'] + '">' + category['name'].replace(' ', '&nbsp;') + '</option>');
        }
    });
});