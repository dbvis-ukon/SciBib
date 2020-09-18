var type_to_color = {
     'Inproceedings' : '#1f78b4',
     'Conference':     '#8B4513',
     'Book' :        '#e31a1c',
     'Inbook':      '#fb9a99',
     'Booklet' :      '#cab2d6',
     'Incollection':  '#ff7f00',
     'Masterthesis':  '#b2df8a',
     'PhDThesis':     '#33a02c',
     'Article' :      '#6a3d9a',
     'Manual':         '#b15928',
     'Proceedings':    '#fdbf6f',
     'Techreport':   '#f0e130',
      'Misc':        '#000000',
      'Unpublished': '#808080'
};

if(typeof String.prototype.toProperCase === "undefined") {
    String.prototype.toProperCase = function () {
        return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
    };
}

if(typeof(String.prototype.trim) === "undefined") {
    String.prototype.trim = function() {
        return String(this).replace(/^\s+|\s+$/g, '');
    };
}

function isValidURL(str) {
   var a  = document.createElement('a');
   a.href = str;
   return (a.host && a.host !== window.location.host);
}

function validateEmail(email_str) {
    let email_regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i;
    return email_regex.test(email_str)
}

function initSelect2(id) {
    $('#' + id).select2({
        theme: 'bootstrap4',
        width: '100%',
        templateSelection: function (data, container) {
            return data.text.trim()
        }
    });
}

function addStatusMessage(message, is_success, refresh_url) {
    let template = $(document.querySelector('#alert').content.cloneNode(true));
    let content = $('#content');

    template.find('#alert-msg').html(message);
    template.find('#alert-msg').addClass(is_success ? 'alert-success' : 'alert-danger');
    if (is_success && refresh_url)
        $(template.find('#alert-msg'))
            .append($('<a>', {href: refresh_url, html: '  '})
                .append($('<i>', {class: 'fa fa-refresh'})));
        // $(template).find('#alert-msg').append('  <a href="' + refresh_url + '"><i class="fa fa-refresh"></i></a>');
    else
        $(template).find('#alert-msg')
            .append($('<button>', {type: 'button', class: 'btn btn-sm', click: function() {$(this).parent().parent().parent().remove()}})
                .append($('<i>', {class: 'fa fa-times'})));
        // $(template).find('#alert-msg').append('  <button type="button" class="btn btn-sm"><i class="fa fa-times"></i></a>');
    template.find('#alert-msg').attr('id', '');

    content.parent().prepend(template);

    $("html, body").animate({scrollTop: 0}, "slow");
}

function DeleteDialog(title, message, del_type, del_id) {
    let modal_id = "modal-delete-" + del_id;
    $('#content')
        .append($("<div>", {
                class: "modal fade",
                id: modal_id,
                tabindex: "-1",
                role: "dialog",
                "aria-labelledby": "modal-title-" + del_id
            })
                .append($("<div>")
                    .addClass("modal-dialog")
                    .append($("<div>", {class: "modal-content bg-light text-dark"})
                        .append($("<div>")
                            .addClass("modal-header")
                            .append($("<h5>", {class: "modal-title", user_id: "modal-title-" + del_id, html: title}))
                        )
                        .append($("<div>", {class: "modal-body"})
                            .append($("<p>", {html: message}))
                        )
                        .append($("<div>", {class: "modal-footer"})
                            .append($("<button>", {
                                class: "btn btn-primary close-dialog",
                                type: "button",
                                text: "Cancel",
                                "data-id": modal_id,
                                "data-toggle": "modal",
                                "data-target": modal_id
                            }))
                            .append($("<button>", {
                                class: "btn btn-danger delete-dialog",
                                type: "button",
                                text: "Delete",
                                "data-delid": del_id,
                                "data-deltype": del_type
                            }))
                        )
                    )
                )
        );

    $('.close-dialog').on("click", function () {
        $('.modal-backdrop').remove();
        $('body').removeClass("modal-open");
        $('#' + modal_id).remove();
    });

    $('.delete-dialog').on("click", function () {
        let del_id = $(this).data().delid;
        let del_type = $(this).data().deltype;

        let data = {};
        let msg = '';
        let url = '';
        let refresh_url = '';

        switch (del_type) {
            case "publication":
                data['publication_id'] = del_id;
                msg = 'Successfully <b>removed</b> publication.';
                url = '/delete/publication/';
                refresh_url = '/admin/publications';
                break;
            case "author":
                data['author_id'] = del_id;
                msg = 'Successfully <b>removed</b> author.';
                url = '/delete/author/';
                refresh_url = '/admin/authors';
                break;
            case "keyword":
                data['keyword_id'] = del_id;
                msg = 'Successfully <b>removed</b> keyword.';
                url = '/delete/keyword/';
                refresh_url = '/admin/keywords';
                break;
            case "category":
                data['category_id'] = del_id;
                msg = 'Successfully <b>removed</b> category.';
                url = '/delete/category/';
                refresh_url = '/admin/categories';
                break;
            case "user":
                data['user_id'] = del_id;
                msg = "Successfully <b>removed</b> user.  ";
                url = '/delete/user/';
                refresh_url = '/admin/users';
                break;
            case "role":
                data['role_id'] = del_id;
                msg = "Successfully <b>removed</b> role.  ";
                url = '/delete/role/';
                refresh_url = '/admin/users';
                break;
            default:
                break;
        }

        $.ajax({
            url: url,
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify(data)
        })
            .done(function (response) {
                $('.modal-backdrop').remove();
                $('body').removeClass("modal-open");
                $('#' + modal_id).remove();

                if (del_type === 'keyword')
                    $('#keyword_' + del_id).remove();
                if (del_type === 'author')
                    $('#author_' + del_id).remove();
                if (del_type === 'role')
                    $('#role_' + del_id).remove();
                if (del_type === 'user')
                    $('#user_' + del_id).remove();

                addStatusMessage(msg, true, refresh_url);
            })
            .fail(function (response) {
                addStatusMessage(response.responseText, false);

                $("html, body").animate({scrollTop: 0}, "slow");

                $('.modal-backdrop').remove();
                $('body').removeClass("modal-open");
                $('#' + modal_id).remove();
            });
    });

    $("#" + modal_id).modal();
}

function DeleteDocumentDialog(message, id, row_id, pub_id) {
    let modal_id = "modal-delete-" + id;
    $('#content')
        .append($("<div>", {
                class: "modal fade",
                id: modal_id,
                tabindex: "-1",
                role: "dialog",
                "aria-labelledby": "modal-title-" + id
            })
                .append($("<div>")
                    .addClass("modal-dialog")
                    .append($("<div>", {class: "modal-content bg-light text-dark"})
                        .append($("<div>")
                            .addClass("modal-header")
                            .append($("<h5>", {
                                class: "modal-title",
                                id: "modal-title-" + id,
                                html: "Delete Document from Database"
                            }))
                        )
                        .append($("<div>", {class: "modal-body"})
                            .append($("<p>", {html: "Are you sure you want to remove the document from the database? <br> The action can not be reversed"}))
                        )
                        .append($("<div>", {class: "modal-footer"})
                            .append($("<button>", {
                                class: "btn btn-primary close-dialog",
                                type: "button",
                                text: "Cancel",
                                "data-id": modal_id,
                                "data-rowid": row_id,
                                "data-toggle": "modal",
                                "data-target": modal_id
                            }))
                            .append($("<button>", {
                                class: "btn btn-danger delete-dialog",
                                type: "button",
                                text: "Delete",
                                "data-id": id,
                                "data-pubid": pub_id
                            }))
                        )
                    )
                )
        );

    $('.close-dialog').on("click", function () {
        $('.modal-backdrop').remove();
        $('body').removeClass("modal-open");
        $('#' + modal_id).remove();
    });

    $('.delete-dialog').on("click", function () {
        let id = $(this).data().id;
        let pub_id = $(this).data().pubid;
        let table_row = "tr-input-docs-" + row_id;

        $.ajax({
            url: "/delete/document/",
            type: "POST",
            contentType: 'application/json;charset=UTF-8',
            data: JSON.stringify({
                "id": id,
                "pub_id": pub_id
            })
        })
            .done(function () {
                $('#' + table_row).remove();
                $('.modal-backdrop').remove();
                $('body').removeClass("modal-open");
                $('#' + modal_id).remove();
            })
            .fail(function (response) {
                let template = $(document.querySelector('#alert').content.cloneNode(true));
                let content = $('#content');

                template.find('#alert-msg').html(response.responseText);
                template.find('#alert-msg').addClass('alert-danger');
                //$(template).find('#alert-msg').append('  <a href="/admin/authors"><i class="fa fa-refresh"></i></a>');
                content.parent().prepend(template);

                $("html, body").animate({scrollTop: 0}, "slow");
                $('#' + modal_id).modal("hide");
            });
    });

    $("#" + modal_id).modal();
}
