'use strict';

$(document).ready(function () {
    $('#search-input').on('keypress', function (event) {
        let keycode = event.keyCode ? event.keyCode : event.which;
        if (keycode == '13') {
            event.preventDefault();

            if ($(this).val().length > 2)
                applyFilter();
        }
    });

    $('#run-filters').on('click', function () {
        applyFilter();
    });


    function applyFilter() {
        let types = $('#filter-types').find('.active.clicky.dropdown-item').map(function() {return $(this).data().value}).get().join(',');
        let years = $('#filter-years').find('.active.clicky.dropdown-item').map(function() {return $(this).data().value}).get().join(',');
        let search = $('#search-input').val().trim();

        let types_param = types.length > 0 ? types : '';
        let years_param = years.length > 0 ? years : '';

        let param_str = '';
        if (types_param)
            param_str += param_str.length === 1 ? 'type=' + types_param : '&type=' + types_param;
        if (years_param)
            param_str += param_str.length === 1 ? 'year=' + years_param : '&year=' + years_param;
        if (search)
            param_str += param_str.length === 1 ? 'search=' + search : '&search=' + search;

        if (param_str)
            window.location.search = param_str;
    }
});
