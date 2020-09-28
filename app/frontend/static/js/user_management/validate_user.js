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

let required_inputs_user = ['input-email'];

/*
Validate form to add new user
 */
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

