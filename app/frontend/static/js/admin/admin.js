'use strict';

$(document).ready(function () {
    // Nicely format Authors Table
    $('#table-latest_publications').DataTable({
        'order': [[1, "desc"]],
        'initComplete': function () {
            $(this).removeClass('d-none');
            $('#spinner').remove();
        }
    });

    $('.delete-publication-btn').on('click', function () {
        let publication_id = $(this).data().publicationid;
        DeleteDialog(
            "Delete Publication from Database",
            "Are you sure you want to remove the publication from the database? <br> The action can <b>not</b> be reversed.",
            "publication",
            publication_id
        );
    });

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