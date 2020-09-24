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

$(document).ready(function () {
    /*
    Format authors table in admin view and add confirmation dialog for deleting publications
     */

    // Nicely format Authors Table
    $('#table-latest_publications').DataTable({
        'order': [[1, "desc"]],
        'initComplete': function () {
            $(this).removeClass('d-none');
            $('#spinner').remove();
        }
    });

    /*
    Add confirmation dialog to delete button
     */
    $('.delete-publication-btn').on('click', function () {
        let publication_id = $(this).data().publicationid;
        DeleteDialog(
            "Delete Publication from Database",
            "Are you sure you want to remove the publication from the database? <br> The action can <b>not</b> be reversed.",
            "publication",
            publication_id
        );
    });

    /*
    Needed because of pagination. Ensures that the delete dialog is added when a new page is viewed.
     */
    $('#table-latest_publications').on('draw.dt', function () {
        $(".delete-publication-btn").unbind( "click" );
        $('.delete-publication-btn').on('click', function () {
            let publication_id = $(this).data().publicationid;
            DeleteDialog(
                "Delete Publication from Database",
                "Are you sure you want to remove the publication from the database? <br> The action can <b>not</b> be reversed.",
                "publication",
                publication_id
            );
        });
    });
});