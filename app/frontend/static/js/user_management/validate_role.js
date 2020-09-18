'use strict';

let required_inputs_role = ['input-name'];

$('#submit-add-role').on('submit click', function () {
    event.preventDefault();

    let count_invalid = required_inputs_role.map((input) => {
        if($('#' + input).val().trim().length) {
            $('#' + input).removeClass('is-invalid');
            return 0;
        } else {
            $('#' + input).addClass('is-invalid');
            return 1;
        }
    }).reduce((a, b) => a + b, 0);

    if(count_invalid === 0) {
        $('#add-role-form').submit();
    }
});

