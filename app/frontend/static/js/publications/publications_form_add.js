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
Handles interactive elements only needed when adding a new publication
 */
$(document).ready(function () {

    /* Events to handle uploading multiples files */
    $('#input-docs').on('change', function () {
        let nRows = $('#input-docs-table tr.input-docs-toadd').length;

        let clone = $(this).clone();
        clone
            .attr("id", "input-docs-" + nRows)
            .attr("name", "input-docs-" + nRows)
            .addClass("d-none");
        $(this).parent().append(clone);

        // number of already added documents minus header row
        $("#input-docs-table").find('tbody')
            .append($('<tr>')
                .addClass('input-docs-toadd')
                .attr('id', 'tr-input-docs-' + nRows)
                .append($('<td>')
                    .append($('<div>')
                        .addClass('form-check')
                        .append($('<input>')
                            .addClass('form-check-input')
                            .attr("type", "radio")
                            .attr("name", "input-docs-checkbox")
                            .attr("id", "input-docs-checkbox")
                            .attr("value", nRows)
                            .prop('checked', nRows === 0)
                        )
                    )
                )
                .append($('<td>')
                    .append(this.files[0].name)
                )
                .append($('<td>')
                    .append($('<button>')
                        .addClass('btn input-docs-del')
                        .attr("type", "button")
                        .attr("data-inputid", nRows)
                        .append($('<i>')
                            .addClass("fa fa-times text-danger")
                        )
                    )
                )
            );

        /* Add listener to delete documents */
        $('.input-docs-del').on("click", function () {
            let inputId = $(this).data().inputid;
            $('#input-docs-' + inputId).remove();
            $('#tr-input-docs-' + inputId).remove();
        });

        this.value = '';
        /* some extra safari bullshit */
        if (!/safari/i.test(navigator.userAgent)) {
            this.type = '';
            this.type = 'file';
        }
    });
});