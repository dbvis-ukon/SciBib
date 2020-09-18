'use strict';

$(document).ready(function () {
    $('.delete-publication-btn').on('click', function() {
        let publication_id = $(this).data().publicationid;

        DeleteDialog(
        "Delete Publication from Database",
        "Are you sure you want to remove the publication from the database? <br> The action can <b>not</b> be reversed.",
        "publication",
        publication_id
        );
    });

    // Nicely format Authors Table
    $('#table-publications').DataTable({
        'order': [[1, "desc"]],
        'initComplete': function() {
            $(this).removeClass('d-none');
            $('#spinner').remove();
        }
    });
});
