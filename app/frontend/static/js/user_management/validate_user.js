'use strict';

let required_inputs_user = ['input-email'];

$('#submit-add-user').on('submit click', function () {
    event.preventDefault();

    let count_invalid = required_inputs_user.map((input) => {
        if (input === 'input-email' && (validateEmail($('#' + input).val().trim()) || $('#input-username').val() === 'admin')) {
            $('#' + input).removeClass('is-invalid');
            return 0;
        } else if(input !== 'input-email' && $('#' + input).val().trim().length) {
            $('#' + input).removeClass('is-invalid');
            return 0;
        } else {
            $('#' + input).addClass('is-invalid');
            return 1;
        }
    }).reduce((a, b) => a + b, 0);

    if(count_invalid === 0) {
        $('#add-user-form').submit();
    }
});

