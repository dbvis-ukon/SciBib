'use strict';

/*
Handles interactive elements only needed when editing a publication
 */
$(document).ready(function () {
    $('#input-docs').on('change', function () {
        let val = $('#input-docs-table tr.input-docs-db').length;
        val = val ? val : 0;
        let nRows = $('#input-docs-table tr.input-docs-toadd').length;
        nRows = nRows ? nRows : 0;
        let isChecked = $('#input-docs-checkbox').is(':checked');

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
                .attr('id', 'tr-input-docs-' + (val + nRows))
                .append($('<td>')
                    .append($('<div>')
                        .addClass('form-check')
                        .append($('<input>')
                            .addClass('form-check-input')
                            .attr("type", "radio")
                            .attr("name", "input-docs-checkbox")
                            .attr("id", "input-docs-checkbox")
                            .attr("value", val)
                            .prop('checked', !isChecked)
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
                        .attr("data-inputid", (val + nRows))
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
