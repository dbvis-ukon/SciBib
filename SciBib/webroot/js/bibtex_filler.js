/**Copyright {2017} {University Konstanz -  Data Analysis and Visualization Group}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

  Udo Schlegel - Udo.3.Schlegel(at)uni-konstanz.de
  11/05/16
*/

$(document).ready(function () {

    // Toggle Tooltip
    $("#bibtex_icon").click(function () {
        $('#bibtex_help_text').toggle("slow");
    });
    $('#bibtex_help_text').hide();

    // Handle click on "Bibtex Fill In"
    $("#bibtex_fill_in").click(function() {
        var bibtex_object = "";

        // Try to parse bibtex code
        $("#bibtex_error").html("");
        try {
            var data = $("#bibtex_textarea").val();
            data = data.replace('+', '');
            bibtex_object = doParse(data);
        } catch (err) {
            console.log(err);
            $("#bibtex_error").html("There was an Error with your Bibtex Code.\n" +
                "Please change the Reference Name and try again.\n");
            return false;
        }

        // Iterate over the parsed bibtex code and fill in inputs
        for (var obj in bibtex_object) {
            if (obj != "@comments") { // ignore comments
                for (var key in bibtex_object[obj]) {

                    if (key == "entryType") {
                        var type = bibtex_object[obj]["entryType"].toLowerCase();
                        type = type[0].toUpperCase() + type.slice(1);
                        $("select[name=type]").val(type).change();
                    }

                    var input_id = key.toLowerCase();
                    if (input_id === "author") {

                        var authors = bibtex_object[obj][key].split(" and ");

                        for (var author in authors) {

                            author = authors[author].split(", ");
                            var surname = author[0];
                            var forename = author[1];

                            var author_id = -1;
                            var cleanname = "";

                            /* search for the authors surname in the authors array */
                            for (var keys in db_authors) {
                                if (db_authors[keys].indexOf(surname) > -1) {
                                    author_id = keys;
                                    cleanname = db_authors[keys];
                                }
                            }

                            if (author_id === -1) {
                                createAuthor(forename, surname);
                            } else {
                                addAuthor({'id': author_id, 'cleanname': cleanname});
                            }

                        }

                    }

                    $("input[name="+input_id+"]").val(bibtex_object[obj][key].replace("{", "").replace("}", ""));
                    $("select[name="+input_id+"]").val(bibtex_object[obj][key].replace("{", "").replace("}", "")).change();

                }

            }
        }
    });
});
