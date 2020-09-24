'use strict';

let required_inputs = ['input-name'];

/*
Validate form to add a new category.
 */
$('#submit-add-category').on('submit click', function () {
    event.preventDefault();

    let count_invalid = required_inputs.map((input) => {
        if($('#' + input).val().trim().length) {
            $('#' + input).removeClass('is-invalid');
            return 0;
        } else {
            $('#' + input).addClass('is-invalid');
            return 1;
        }
    }).reduce((a, b) => a + b, 0);

    if(count_invalid === 0) {
        $('#add-category-form').submit();
    }
});
