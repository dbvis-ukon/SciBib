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
Activate delete button for the publications view and format publications table
 */
$(document).ready(function () {
    /*
    Display confirmation dialog when trying to delete a publiation.
     */
    $('.delete-publication-btn').on('click', function() {
        let publication_id = $(this).data().publicationid;

        DeleteDialog(
        "Delete Publication from Database",
        "Are you sure you want to remove the publication from the database? <br> The action can <b>not</b> be reversed.",
        "publication",
        publication_id
        );
    });

    // Nicely format publications table
    $('#table-publications').DataTable({
        'order': [[1, "desc"]],
        'initComplete': function() {
            $(this).removeClass('d-none');
            $('#spinner').remove();
        }
    });
});
