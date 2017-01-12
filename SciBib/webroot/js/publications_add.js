/**
Copyright {2017} {University Konstanz -  Data Analysis and Visualization Group}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
**/


/*********************
 * ON DOCUMENT READY *
 *********************/

$(document).ready(function () {

    /* 
     * 
     * BIBTEX
     * 
     *
     */

//bibtex array:  0 = article, 1 = book etc. 
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
    //on change  change the bibtex fields in the add method
    $("#typebox").change(function () {
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
    //trigger for the first time 
    $("#typebox").trigger("change");
    /* 
     * 
     * PUBLICATION STATUS
     * 
     *   */
    $("#PublicationPublicationdate").datepicker({
        showButtonPanel: true,
        minDate: +1,
        showOn: "both",
        buttonImage: '/img/date-picker.png',
        buttonImageOnly: true,
        dateFormat: "yy-mm-dd",
        inline: true
    });
    //by default the datepicker is disabled
    $("#PublicationPublicationdate").datepicker('disable');
    //Feedback Text 
    $("#PublicationSubmitted").change(function () {
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
    }
    );
    //On change functions for the buttons
    $("#PublicationPublished").change(function () {
        $("#PublicationSubmitted").trigger("change");
    });
    $("#PublicationPublic").change(function () {
        $("#PublicationSubmitted").trigger("change");
        $("#data-publication-publicitystatus-2").trigger("change");
    });
    $("#PublicationSubmitted").trigger("change");
    $('#PublicationDate').change(function () {
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
    $("#PublicationPublicationdate").change(function () {
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
    /**
     * Remove whitespace from both sides of a string
     */
    function categoriesText(data, container) {
        return data.text.trim();
    }

    /**
     * On Change select all the children and parents in the hierarchie
     */
    $("#categories-ids").on("select2:select", function (e) {
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
    /**
     * On Change unselect all the children and parents in the hierarchie
     */
    $("#categories-ids").on("select2:unselect", function (e) {
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
     *   */
    $("#imagePreview2").hide();
    $("#abstractphoto").on("change", function () {
        $("#imagePreview2").show();
        $("#imagePreview2").empty();
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader)
            return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { // set image data as background of div
                $("#imagePreview2").css("background-image", "url(" + this.result + ")");
            };
        }
    });
    /* 
     * 
     * Thumb Preview
     * 
     *   */
    $("#imagePreview").hide();
    $("#thumb").on("change", function () {
        $("#imagePreview").show();
        $("#imagePreview").empty();
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader)
            return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { // set image data as background of div
                $("#imagePreview").css("background-image", "url(" + this.result + ")");
            };
        }
    });
    /* 
     * 
     * AUTHORS
     * 
     *   */
    // Use the Plugin Select2
    $("#authors-ids").select2({
        tags: true,
        placeholder: 'Start typing a surname to get suggestions',
        minimumInputLength: 3
    });
    /**
     * On Change add the author to the list 
     */
    $("#authors-ids").on("select2:select", function (e) {
        var selectedId = e.params.data.id;
        var selectedName = e.params.data.text;
        $("#authorsSortable").append('<li id="' + selectedId + '"> <span class="drag-handle">☰</span>'
                + selectedName + '</li>');
    });
    /**
     * On Change remove the author to the list 
     */
    $("#authors-ids").on("select2:unselect", function (e) {
        var selectedId = e.params.data.id;
        $("#authorsSortable #" + selectedId).remove();
    });
    // authors position 
    var list = document.getElementById("authorsSortable");
    Sortable.create(list, {
        animation: 150, // ms, animation speed moving items when sorting, `0` — without animation
    }); // That's all.

    // if the mode is the edit mode get the authors sorted
    if (window.location.href.indexOf("edit") > -1) {
        for (var i = 0; i < selectedAuthors.length; i++) {
            var selectedId = selectedAuthors[i].id;
            var selectedName = selectedAuthors[i].cleanname;
            $("#authorsSortable").append('<li id="' + selectedId + '"> <span class="drag-handle">☰</span>'
                    + selectedName + '</li>');
        }
    }

    //observer for the order of the authors
    //we add the ordering to a string 
    //then we put it into the hidden form so we have it on the server side also
    var observer = new MutationObserver(function () {
        //fresh string
        var authorsPosition = "";
        $('#authorsSortable li').each(function (li) {
            //for each author save the => id,position;
            authorsPosition = authorsPosition + $(this).attr('id') + ',' + li + ';';
        });
        //add all to the hidden input
        $('#authorsPos').val(authorsPosition);
    });
    // configuration of the observer:
    var config = {attributes: false, childList: true, characterData: true, subtree: true};
    // pass in the target node, as well as the observer options
    observer.observe(document.querySelector('#authorsSortable'), config);
    /* 
     * 
     * KEYWORDS
     * 
     *   */

    // Use the Plugin Select2
    $("#keywords-ids").select2({
        tags: true,
        placeholder: 'Start typing to get suggestions',
    });
    /* 
     * 
     * Info Icon
     * 
     *   */
    $("#info_icon").click(function () {
        $('#abstractInfoText').toggle("slow");
    });
    $('#abstractInfoText').hide();
    /* AUTHORS add new */
    $("#addAuthorButton").click(function () {
        $("#addAuthorButton").slideUp();
        $("#addAuthorTable").css('display', 'block');
    });
    $("#SubmitAuthor").click(function () {
        var forename = $("#AddForename").val();
        var surname = $("#AddSurname").val();
        if (forename && surname) {
            createAuthor(forename, surname);
        } else {
            $("#CreateAuthorError").empty().append('<span class="error">Unable to create a new author</span>');
        }
    });
    /* Keyword add new */
    $("#addKeywordButton").click(function () {
        $("#addKeywordButton").slideUp();
        $("#addKeywordTable").css('display', 'block');
    });
    $("#SubmitKeyword").click(function () {
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

/* 
 * Create Author with ajax
 */
function createAuthor(forename, surname) {
    $.ajax({
        type: 'post',
        url: "/authors/ajaxCreate/?forename=" + forename + "&surname=" + surname,
        dataType: 'json',
        success: function (data) {
            $("#CreateAuthorSuccess").empty().append('<span class="success">Author created</span>');
            addAuthor(data);
        },
        error: function (one, two, three) {
            $("#CreateAuthorError").empty().append('<span class="error">Unable to create a new author</span>');
        },
    });
}
/* 
 * add author to the select2 component 
 */
function addAuthor(author) {
    var select = $('#authors-ids');
    var option = $('<option></option>').
            attr('selected', true).
            text(author['cleanname']).
            val(author['id']);
    option.appendTo(select);
    select.trigger('change');
    $("#authorsSortable").append('<li id="' + author['id'] + '"> <span class="drag-handle">☰</span>'
            + author['cleanname'] + '</li>');
    setTimeout(function () {
        if ($(".success").length > 0) {
            $(".success").remove();
        }
    }, 5000)
}

/* KEYWORDS */

/* 
 * Create Keyword with ajax
 */
function createKeyword(keyword) {
    $.ajax({
        type: 'post',
        url: '/keywords/add/?keyword=' + keyword,
        dataType: 'json',
        success: function (data) {
            addKeyword(data);
        },
        error: function (one, two, three) {
            $("#CreateKeywordError").empty().append('<span class="error">Unable to create a new keyword</span>');
        },
    });
}
/* 
 * add Keyword to the select2 component 
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
    setTimeout(function () {
        if ($(".success").length > 0) {
            $(".success").remove();
        }
    }, 5000)
}
