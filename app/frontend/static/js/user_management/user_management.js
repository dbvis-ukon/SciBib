'use strict';

/*
Create dialog to edit a role
 */
function createEditRoleDialog(data) {
    let modal_id = 'edit-role-modal';

    let template = $(document.querySelector('#edit-role-modal_template').content.cloneNode(true));
    let content = $('#content');

    template.find('#edit-role-form').attr('action', '/edit/role/' + data['id']);
    template.find('#input-name').val(data['name']);
    template.find('#input-description').val(data['description']);

    template.find('.close-edit-dialog').on('click', function () {
        $('.modal-backdrop').remove();
        $('body').removeClass("modal-open");
        $('#' + modal_id).remove();
    });

    template.find('#edit-role-form').on('submit', function () {
        let required_inputs_role = ['input-name'];

        let count_invalid = required_inputs_role.map((input) => {
            if ($('#' + input).val().trim().length) {
                $('#' + input).removeClass('is-invalid');
                return 0;
            } else {
                $('#' + input).addClass('is-invalid');
                return 1;
            }
        }).reduce((a, b) => a + b, 0);

        if (count_invalid === 0) {
            $.post($(this).attr('action'), $(this).serialize(), function (response) {
                addStatusMessage(response.msg, true);
                $('#edit-role-modal').modal('toggle');

                let role = response.role;
                $('#role_' + role.id).find('td:eq(0)').html(role.name);
                $('#role_' + role.id).find('td:eq(1)').html(role.description);
            }, 'json')
                .fail(function (response) {
                    addStatusMessage(response.responseText, false);

                    $('#edit-role-modal').modal('toggle');
                });
        }
        return false;
    });

    content.parent().prepend(template);
    $('#' + modal_id).modal();

    return false;
}

/*
Create dialog to edit a user
 */
function createEditUserDialog(data) {
    let modal_id = 'edit-user-modal';

    let template = $(document.querySelector('#edit-user-modal_template').content.cloneNode(true));
    let content = $('#content');

    template.find('#edit-user-form').attr('action', '/edit/user/' + data['id']);
    template.find('#input-firstname').val(data['first_name']);
    template.find('#input-lastname').val(data['last_name']);
    template.find('#input-username').val(data['username']);
    template.find('#input-username-hidden').val(data['username']);
    template.find('#input-email').val(data['email']);
    for (const role of data['roles'])
        template.find('#edit-select-roles option[value="' + role['id'] + '"]').attr('selected', 'selected');
    data['active'] === 1 ?
        template.find('#input-active').prop('checked', true) : template.find('#input-active').prop('checked', false);

    template.find('.close-edit-dialog').on('click', function () {
        $('.modal-backdrop').remove();
        $('body').removeClass("modal-open");
        $('#' + modal_id).remove();
    });

    template.find('#edit-user-form').on('submit', function () {
        let required_inputs_user = ['input-email'];

        let count_invalid = required_inputs_user.map((input) => {
            if (input === 'input-email' && (validateEmail($('#' + input).val().trim()) || $('#input-username').val() === 'admin')) {
                $('#' + input).removeClass('is-invalid');
                return 0;
            } else if ($('#' + input).val().trim().length) {
                $('#' + input).removeClass('is-invalid');
                return 0;
            } else {
                $('#' + input).addClass('is-invalid');
                return 1;
            }
        }).reduce((a, b) => a + b, 0);

        if (count_invalid === 0) {
            $.post($(this).attr('action'), $(this).serialize(), function (response) {
                addStatusMessage(response.msg, true);
                $('#edit-user-modal').modal('toggle');

                let user = response.user;
                let row = $('#user_' + user.id);
                row.find('td:eq(0)').html(user.username);
                row.find('td:eq(1)').html(user.email);
                row.find('td:eq(2)').html(user.roles.join(', '));

                row.find('td:eq(3)').find('span').removeClass(user.active === 0 ? 'text-success' : 'text-danger');
                row.find('td:eq(3)').find('span').addClass(user.active === 0 ? 'text-danger' : 'text-success');
                row.find('td:eq(3)').find('i').addClass(user.active === 0 ? 'fa-times' : 'fa-check');
                row.find('td:eq(3)').find('i').removeClass(user.active === 0 ? 'fa-check' : 'fa-times');
            }, 'json')
                .fail(function (response) {
                    addStatusMessage(response.responseText, false,);

                    $('#edit-user-modal').modal('toggle');
                });
        }
        return false;
    });

    content.parent().prepend(template);

    $('#edit-select-roles').select2({
        theme: 'bootstrap4',
        width: '100%',
        templateSelection: function (data, container) {
            return data.text.trim()
        }
    });

    $('#' + modal_id).modal();
}

/*
Submit new role and add the new role interactively to the roles table
 */
function addRole() {
    $.post($(this).attr('action'), $(this).serialize(), function (response) {
        addStatusMessage(response.msg, true);
        $('#add-role-modal').modal('toggle');

        let role = response.role;
        let newRow = $('#table-roles').DataTable().row.add([role.name, role.description, '', '']).draw().node();
        $(newRow).attr("id", "role_" + role.id);
        $(newRow).find('td:eq(2)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-primary edit-role-btn p-0',
                'data-roleid': role.id,
                click: editRole
            }).append($('<i>', {class: 'fa fa-edit'})));
        $(newRow).find('td:eq(3)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-danger delete-role-btn p-0',
                'data-roleid': role.id,
                click: deleteRole
            }).append($('<i>', {class: 'fa fa-times'})));
    }, 'json')
        .fail(function (response) {
            addStatusMessage(response.responseText, false);

            $('#add-role-modal').modal('toggle');
        });
    return false;
}

/*
Submit new user and add the new user interactively to the users table
 */
function addUser() {
    $.post($(this).attr('action'), $(this).serialize(), function (response) {
        addStatusMessage(response.msg, true);
        $('#add-user-modal').modal('toggle');

        let user = response.user;
        let newRow = $('#table-users').DataTable().row.add([user.username, user.email, user.roles.join(', '), '', '', '']).draw().node();
        $(newRow).attr("id", "user_" + user.id);
        if (user.active === 1) {
            $(newRow).find('td:eq(3)')
                .append($('<span>', {class: 'text-success'})
                    .append($('<i>', {class: 'fa fa-check'})))
        } else if (user.active === 0) {
            $(newRow).find('td:eq(3)')
                .append($('<span>', {class: 'text-danger'})
                    .append($('<i>', {class: 'fa fa-times'})))
        }
        $(newRow).find('td:eq(4)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-primary edit-user-btn p-0',
                'data-Userid': user.id,
                click: editUser
            }).append($('<i>', {class: 'fa fa-edit'})));
        $(newRow).find('td:eq(5)')
            .append($('<button>', {
                type: 'button',
                'class': 'btn text-danger delete-user-btn p-0',
                'data-Userid': user.id,
                click: deleteUser
            }).append($('<i>', {class: 'fa fa-times'})));


    }, 'json')
        .fail(function (response) {
            addStatusMessage(response.responseText, false, "");

            $('#add-user-modal').modal('toggle');
        });
    return false;
}

/*
Fetch info on role to edit and create edit dialog
 */
function editRole() {
    let role_id = $(this).data().roleid;

    $.ajax({
        url: "/edit/role/" + role_id,
        type: 'GET'
    }).done(function (resp) {
        createEditRoleDialog(resp);
    }).fail(function (response) {
        addStatusMessage(response.responseText, false);

        $("html, body").animate({scrollTop: 0}, "slow");
        $('#' + modal_id).modal("hide");
    });
}

/*
Fetch info on user to edit and create edit dialog
 */
function editUser() {
    let user_id = $(this).data().userid;

    $.ajax({
        url: "/edit/user/" + user_id,
        type: 'GET'
    }).done(function (resp) {
        createEditUserDialog(resp);
    }).fail(function (response) {
        addStatusMessage(response.responseText, false);

        $("html, body").animate({scrollTop: 0}, "slow");
        $('#' + modal_id).modal("hide");
    });
}

/*
Create confirmation dialog when trying to delete a role
 */
function deleteRole() {
    let role_id = $(this).data().roleid;

    DeleteDialog(
        "Delete Role from Database",
        "Are you sure you want to remove the role from the database? <br> The action can <b>not</b> be reversed.",
        "role",
        role_id
    );
}

function deleteUser() {
    let user_id = $(this).data().userid;

    DeleteDialog(
        "Delete User from Database",
        "Are you sure you want to remove the user from the database? <br> The action can <b>not</b> be reversed.",
        "user",
        user_id
    );
}

$(document).ready(function () {
    $('.delete-user-btn').on("click", deleteUser);

    $('.delete-role-btn').on("click", deleteRole);

    $('#select-roles').select2({
        theme: 'bootstrap4',
        width: '100%',
        templateSelection: function (data, container) {
            return data.text.trim()
        }
    });

    $('#add-user-form').on('submit', addUser);

    $('#add-role-form').on('submit', addRole);

    $('.edit-user-btn').on('click', editUser);

    $('.edit-role-btn').on('click', editRole);


    $('#table-users').DataTable({
        'initComplete': function () {
            $(this).removeClass('d-none');
            $('#spinner-user').remove();
        }
    });
});