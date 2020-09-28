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