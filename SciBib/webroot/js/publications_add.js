/*********************
 * ON DOCUMENT READY *
 *********************/

$(document).ready(function() {

    /*
     *
     * BIBTEX
     *
     *
     */

    // Bibtex array:  0 = article, 1 = book etc.
    var bibtex = {
        Article: [false, false, false, false, false, false, false, true, true, true, true, false, true, false, false, true, false],
        Book: [true, false, false, true, true, false, false, false, true, true, true, false, false, false, true, true, true],
        Booklet: [true, false, false, false, false, true, false, false, true, true, false, false, false, false, false, false, false],
        Conference: [true, true, false, false, true, false, false, false, true, true, true, true, true, false, true, true, true],
        Inbook: [true, false, true, true, true, false, false, false, true, true, true, false, true, false, true, true, true],
        Incollection: [true, true, true, true, true, false, false, false, true, true, true, false, true, false, true, true, true],
        Inproceedings: [true, true, false, false, true, false, false, false, true, true, true, true, true, false, true, true, true],
        Manual: [true, false, false, true, false, false, false, false, true, true, false, true, false, false, false, false, false],
        Masterthesis: [true, false, false, false, false, false, false, false, true, true, false, false, false, true, false, false, false],
        Misc: [false, false, false, false, false, true, false, false, true, true, false, false, false, false, false, false, false],
        PhDThesis: [true, false, false, false, false, false, false, false, true, true, false, false, false, true, false, false, false],
        Proceedings: [true, false, false, false, true, false, false, false, true, true, true, true, false, false, true, true, true],
        Techreport: [true, false, false, false, false, false, true, false, true, true, true, false, false, false, false, false, false],
        Unpublished: [false, false, false, false, false, false, false, false, true, true, false, false, false, false, false, false, false]
    };

    // On change  change the bibtex fields in the add method
    $("#typebox").change(function() {
        for (var i = 0; i < 17; i++) {
            if (bibtex[$("#typebox option:selected").text()][i]) {
                $('#BibtexFields > div:nth-child(' + (i + 1) + ')').show();
            } else {
                $('#BibtexFields > div:nth-child(' + (i + 1) + ')').hide();
                //Delete the input of the now hidden field
                $('#BibtexFields > div:nth-child(' + (i + 1) + ') :input').val('');
            }
        }
    });

    // Trigger for the first time
    $("#typebox").trigger("change");

    /*
     *
     * PUBLICATION STATUS
     *
     */
    $("#PublicationPublicationdate").datepicker({
        showButtonPanel: true,
        minDate: +1,
        showOn: "both",
        buttonImage: '/img/date-picker.png',
        buttonImageOnly: true,
        dateFormat: "yy-mm-dd",
        inline: true
    });

    // By default the datepicker is disabled
    $("#PublicationPublicationdate").datepicker('disable');

    // Feedback Text
    $("#PublicationSubmitted").change(function() {
        var beginActive = '<span style="color: green;">';
        var endActive = "</span>";
        var beginInactive = '<span style="color: darkorange;">';
        var endInactive = "</span>";
        var beginWarning = '<span class="statusWarning">';
        var endWarning = '</span>';
        var isSubmitted = $("#PublicationSubmitted").prop('checked');
        var isPublished = $("#PublicationPublished").prop('checked');
        var isPublic = $("#PublicationPublic").prop('checked');
        var isPublicDate = $("#PublicationDate").prop('checked');
        var stateString = "This paper ";
        var warningString = "";
        if (isSubmitted) {
            if (isPublished) {
                stateString += "was " + beginActive + "successfully published" + endActive + " ";
            } else {
                stateString += "was " + beginActive + "submitted" + endActive + " but is " + beginInactive + "yet to appear" + endInactive + " ";
            }
        } else {
            if (!isPublished) {
                stateString += "is " + beginInactive + "not yet published" + endInactive + " ";
            }
        }
        if (isPublic && !isPublicDate) {
            stateString += "and " + beginActive + "can be viewed by everyone" + endActive + " ";
        } else if (isPublicDate) {
            stateString += "and " + beginActive + "can be viewed by everyone from the date " + $("#PublicationPublicationdate").datepicker('getDate') + endActive + " ";
        } else {
            stateString += "and is " + beginInactive + "hidden from public" + endInactive + " ";
        }
        //Create warnings
        if (isPublished && !isSubmitted)
            warningString = "A publication usually needs to be submitted before it can be published.";
        else if (isPublic && (!isSubmitted || !isPublished))
            warningString = "A publication is usually hidden from public until it is successfully published.";
        if (warningString.length > 0) {
            warningString = '<img src="/img/warning.png" class="icon" style="width: 20px; height: 20px;"> ' + warningString;
            $("#publicationStatusWarning").html(beginWarning + warningString + endWarning);
            $("#publicationStatusMessage").css('display', 'none');
            $("#publicationStatusWarning").css('display', '');
        } else {
            $("#publicationStatusMessage").html(stateString);
            $("#publicationStatusMessage").css('display', '');
            $("#publicationStatusWarning").css('display', 'none');
        }
    });

    // On change functions for the buttons
    $("#PublicationPublished").change(function() {
        $("#PublicationSubmitted").trigger("change");
    });
    $("#PublicationPublic").change(function() {
        $("#PublicationSubmitted").trigger("change");
        $("#data-publication-publicitystatus-2").trigger("change");
    });
    $("#PublicationSubmitted").trigger("change");
    $('#PublicationDate').change(function() {
        if ($("#PublicationDate").prop('checked')) {
            $("#PublicationPublicationdate").datepicker('enable');
            $("#PublicationPublic").prop('checked', true);
            $("#PublicationPublic").attr("disabled", true);
        } else {
            $("#PublicationPublicationdate").datepicker('disable');
            $("#PublicationPublic").attr("disabled", false);
            $("#PublicationPublicationdate").datepicker("setDate", null);
        }
        $("#PublicationSubmitted").trigger("change");
    });
    $("#PublicationPublicationdate").change(function() {
        $("#PublicationSubmitted").trigger("change");
    });

    /*
     *
     * CATEGORY
     *
     */

    // Use the Plugin Select2
    $("#categories-ids").select2({
        tags: true,
        placeholder: 'Select categories from the menu to add them to the list',
        templateSelection: categoriesText
    });

    /*
     * Remove whitespace from both sides of a string
     */
    function categoriesText(data, container) {
        return data.text.trim();
    }

    /*
     * On Change select all the children and parents in the hierarchie
     */
    $("#categories-ids").on("select2:select", function(e) {
        var selectedId = e.params.data.id;
        var nodes = getAllChildNodes(selectedId);
        nodes = nodes.concat(getAllParentNodes(selectedId));
        for (var i = 0; i < nodes.length; i++) {
            if (nodes[i]) {
                // set the categories true
                $("#categories-ids option[value='" + nodes[i] + "']").prop("selected", true);
            }
        }
        //change the view
        $("#categories-ids").trigger("change");
    });

    /*
     * On Change unselect all the children and parents in the hierarchie
     */
    $("#categories-ids").on("select2:unselect", function(e) {
        var selectedId = e.params.data.id;
        var nodes = getAllChildNodes(selectedId);
        for (var i = 0; i < nodes.length; i++) {
            if (nodes[i]) {
                // set the categories false
                $("#categories-ids option[value='" + nodes[i] + "']").prop("selected", false);
            }
        }
        //change the view
        $("#categories-ids").trigger("change");
    });

    /**
     * Get all children node ids of the category selected
     *
     * @param selectedId category id.
     * @return array of ids of categories
     */
    function getAllChildNodes(selectedId) {
        //first level of recursion
        var nodes = [];
        for (var i = 0; i < categories.length; i++) {
            if (selectedId == categories[i].parent_id) {
                nodes.push(categories[i].id);
            }
        }
        // recursion call and concat
        var children = [];
        for (var i = 0; i < nodes.length; i++) {
            children = children.concat(getAllChildNodes(nodes[i]));
        }
        return nodes.concat(children);
    }

    /**
     * Get all parent node ids of the category selected
     *
     * @param selectedId category id.
     * @return array of ids of categories
     */
    function getAllParentNodes(selectedId) {
        //first level of recursion
        var nodes = [];
        for (var i = 0; i < categories.length; i++) {
            if (selectedId == categories[i].id) {
                nodes.push(categories[i].parent_id);
            }
        }
        //get the parent of the parent and add it to the nodes
        if (nodes[0]) {
            nodes = nodes.concat(getAllParentNodes(nodes[0]));
        }
        return nodes;
    }

    /*
     *
     * Abstract Photo Preview
     *
     */
    $("#imagePreview2").hide();
    $("#abstractphoto").on("change", function() {
        $("#imagePreview2").show();
        $("#imagePreview2").empty();
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader)
            return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function() { // set image data as background of div
                $("#imagePreview2").css("background-image", "url(" + this.result + ")");
            };
        }
    });

    /*
     *
     * Thumb Preview
     *
     */
    $("#imagePreview").hide();
    $("#thumb").on("change", function() {
        $("#imagePreview").show();
        $("#imagePreview").empty();
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader)
            return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function() { // set image data as background of div
                $("#imagePreview").css("background-image", "url(" + this.result + ")");
            };
        }
    });

    /*
     *
     * AUTHORS
     *
     */

    // Use the Plugin Select2
    $("#authors-ids").select2({
        tags: true,
        placeholder: 'Start typing a surname to get suggestions',
        minimumInputLength: 3
    });

    /*
     * On Change add the author to the list
     */
    $("#authors-ids").on("select2:select", function(e) {
        var selectedId = e.params.data.id;
        var selectedName = e.params.data.text;
        $("#authorsSortable").append('<li id="' + selectedId + '"> <span class="drag-handle">☰</span>' +
            selectedName + '</li>');
    });

    /*
     * On Change remove the author to the list
     */
    $("#authors-ids").on("select2:unselect", function(e) {
        var selectedId = e.params.data.id;
        $("#authorsSortable #" + selectedId).remove();
    });

    // Authors position
    var list = document.getElementById("authorsSortable");
    Sortable.create(list, {
        animation: 150, // ms, animation speed moving items when sorting, `0` — without animation
    });

    // If the mode is the edit mode get the authors sorted
    if (window.location.href.indexOf("edit") > -1) {
        var authorsPosition = "";

        for (var i = 0; i < selectedAuthors.length; i++) {
            var selectedId = selectedAuthors[i].id;
            var selectedName = selectedAuthors[i].cleanname;
            $("#authorsSortable").append('<li id="' + selectedId + '"> <span class="drag-handle">☰</span>' +
                selectedName + '</li>');
            authorsPosition = authorsPosition + selectedId + ',' + i + ';';
        }

        $('#authorsPos').val(authorsPosition);
    }

    // Observer for the order of the authors
    // We add the ordering to a string
    // Then we put it into the hidden form so we have it on the server side also
    var observer = new MutationObserver(function() {
        // Fresh string
        var authorsPosition = "";
        $('#authorsSortable li').each(function(li) {
            // For each author save the => id,position;
            authorsPosition = authorsPosition + $(this).attr('id') + ',' + li + ';';
        });
        // Add all to the hidden input
        $('#authorsPos').val(authorsPosition);
    });
    // Configuration of the observer:
    var config = {
        attributes: false,
        childList: true,
        characterData: true,
        subtree: true
    };
    // Pass in the target node, as well as the observer options
    observer.observe(document.querySelector('#authorsSortable'), config);

    /*
     *
     * KEYWORDS
     *
     */

    // Use the Plugin Select2
    $("#keywords-ids").select2({
        tags: true,
        placeholder: 'Start typing to get suggestions',
    });

    /*
     *
     * Info Icon
     *
     */
    $("#info_icon").click(function() {
        $('#abstractInfoText').toggle("slow");
    });
    $('#abstractInfoText').hide();

    /*
     * AUTHORS add new
     */
    $("#addAuthorButton").click(function() {
        $("#addAuthorButton").slideUp();
        $("#addAuthorTable").css('display', 'block');
    });
    $("#SubmitAuthor").click(function() {
        var forename = $("#AddForename").val();
        var surname = $("#AddSurname").val();
        if (forename && surname) {
            createAuthor(forename, surname);
        } else {
            $("#CreateAuthorError").empty().append('<span class="error">Unable to create a new author</span>');
        }
    });

    /*
     * Keyword add new
     */
    $("#addKeywordButton").click(function() {
        $("#addKeywordButton").slideUp();
        $("#addKeywordTable").css('display', 'block');
    });
    $("#SubmitKeyword").click(function() {
        var keyword = $("#AddKeyword").val();
        if (keyword) {
            createKeyword(keyword);
        } else {
            $("#CreateKeywordError").empty().append('<span class="error">Unable to create a new keyword</span>');
        }

    });

});

/********************
 * HELPER FUNCTIONS *
 ********************/

/**
 * Create Author with ajax
 */
function createAuthor(forename, surname) {
    $.ajax({
        type: 'post',
        url: "/authors/ajaxCreate/?forename=" + forename + "&surname=" + surname,
        dataType: 'json',
        success: function(data) {
            $("#CreateAuthorSuccess").empty().append('<span class="success">Author created</span>');
            addAuthor(data);
        },
        error: function(one, two, three) {
            $("#CreateAuthorError").empty().append('<span class="error">Unable to create a new author</span>');
        },
    });
}

/**
 * Add author to the select2 component
 */
function addAuthor(author) {
    var select = $('#authors-ids');
    var option = $('<option></option>').
    attr('selected', true).
    text(author['cleanname']).
    val(author['id']);
    option.appendTo(select);
    select.trigger('change');
    $("#authorsSortable").append('<li id="' + author['id'] + '"> <span class="drag-handle">☰</span>' +
        author['cleanname'] + '</li>');
    setTimeout(function() {
        if ($(".success").length > 0) {
            $(".success").remove();
        }
    }, 5000)
}

/* KEYWORDS */

/**
 * Create Keyword with ajax
 */
function createKeyword(keyword) {
    $.ajax({
        type: 'post',
        url: '/keywords/add/?keyword=' + keyword,
        dataType: 'json',
        success: function(data) {
            addKeyword(data);
        },
        error: function(one, two, three) {
            $("#CreateKeywordError").empty().append('<span class="error">Unable to create a new keyword</span>');
        },
    });
}

/**
 * Add Keyword to the select2 component
 */
function addKeyword(keyword) {
    var select = $('#keywords-ids');
    var option = $('<option></option>').
    attr('selected', true).
    text(keyword['name']).
    val(keyword['id']);
    option.appendTo(select);
    select.trigger('change');
    $("#CreateKeywordSuccess").empty().append('<span class="success">Keyword created</span>');
    setTimeout(function() {
        if ($(".success").length > 0) {
            $(".success").remove();
        }
    }, 5000)
}

function addDocument(external, remove, externalStart, filesStart) {

    if (typeof externalStartl == 'undefined') {
        externalStart = 0;
    }

    if (typeof filesStart == 'undefined') {
        filesStart = 0;
    }

    if (typeof addDocument.external == 'undefined') {
        addDocument.external = 0 + externalStart;
        addDocument.files = 1 + filesStart;
    }

    if ((!external && addDocument.files > 4) || (external && addDocument.external > 4)) {
        return -1;
    }

    var table_row = "<tr>";
    table_row += "<td>";
    if (!external) {
        table_row += '<input type="radio" name="file" value="files['+addDocument.files+']">';
    }
    table_row += "</td>";
    table_row += "<td>";
    if (external) {
        table_row += '<input type="text" name="external['+addDocument.external+']">';
        ++addDocument.external;
    } else {
        table_row += '<input type="file" name="files['+addDocument.files+']">';
        ++addDocument.files;
    }
    table_row += "</td>";
    table_row += "<td>";
    table_row += '<img onclick="$(this).parent().parent().remove();" src="' + remove + '" width="16" height="16">';
    table_row += "</td>";
    table_row += "</tr>";

    $('#documents tr:last').after(table_row);
}

/**
 * valid - Validation function to check if inputs are set
 */

function valid(event) {

    // selector for inputs
    var check_value_ids = ['#title'];
    // selector to show user whats missing
    var alert_value_ids = ['#title'];

    for (var id in check_value_ids) {
        if (!$(check_value_ids[id]).val()) {

            $(alert_value_ids[id]).css("border", "solid red 2px");
            $('html, body').animate({
                scrollTop: $(alert_value_ids[id]).offset().top
            }, 2000);

            event.preventDefault();
            return 0;
        }
    }

    // selector for html
    var check_html_ids = ['#authorsSortable'];
    // selector to show user whats missing
    var alert_html_ids = ['#authors'];

    for (var id in check_html_ids) {
        if ($(check_html_ids[id]).html().replace(/\s/g, "") == "") {

            $(alert_html_ids[id]).css("border", "solid red 2px");
            $('html, body').animate({
                scrollTop: $(alert_html_ids[id]).offset().top
            }, 2000);

            event.preventDefault();
            return 0;
        }
    }

    return 1;
}
