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
Create a new dialog to edit a category
 */
function createEditCategoryDialog(data) {
    let modal_id = 'edit-category-modal';

    let template = $(document.querySelector('#edit-category-modal_template').content.cloneNode(true));
    let content = $('#content');

    template.find('#edit-category-form').attr('action', '/edit/category/' + data['id']);
    template.find('#input-name').val(data['name']);
    template.find('#input-description').val(data['description']);

    template.find('.close-category-dialog').on('click', function () {
        $('.modal-backdrop').remove();
        $('body').removeClass("modal-open");
        $('#' + modal_id).remove();
    });

    template.find('#edit-category-form').on('submit', function () {
        let count_invalid = required_inputs.map((input) => {
            if($('#' + input).val().trim().length) {
                $('#' + input).removeClass('is-invalid');
                return 0;
            } else {
                $('#' + input).addClass('is-invalid');
                return 1;
            }
        }).reduce((a, b) => a + b, 0);

        if(count_invalid === 0) {
            $.post($(this).attr('action'), $(this).serialize(), function (response) {


                addStatusMessage(response.msg, true, "/view/categories/" + data['id']);
                $('#edit-category-modal').modal('toggle');
        }, 'json')
            .fail(function (response) {
                addStatusMessage(response.responseText, false,);
                $('#edit-category-modal').modal('toggle');
            });
        }
    });
    content.parent().prepend(template);
    $('#' + modal_id).modal();

    return false;
}

/*
Activate buttons to edit/delete categories.
 */
$(document).ready(function () {
    $('.edit-category-btn').on('click', function() {
        let category_id = $(this).data().categoryid;

        $.ajax({
            url: "/edit/category/" + category_id,
            type: 'GET'
        }).done(function (resp) {
            createEditCategoryDialog(resp);
        }).fail(function (response) {
            addStatusMessage(response.responseText, false);

            $("html, body").animate({scrollTop: 0}, "slow");
            $('#' + modal_id).modal("hide");
        });
    });

    $('.delete-category-btn').on('click', function() {
        let category_id = $(this).data().categoryid;

        DeleteDialog(
            "Delete Category from Database",
            "Are you sure you want to remove the Category from the database? <br> Removing the category will also <b>remove all</b> child categories and can <b>not</b> be reversed.",
            "category",
            category_id
        )
    })
});