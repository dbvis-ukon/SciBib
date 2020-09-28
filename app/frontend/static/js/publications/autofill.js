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

/*
Activate autofill from bibtex functionality when adding a publication.
 */
$(document).ready(function () {
    $('#btn-autofill').on('click', function () {
        let bib_str = $('#input-bibtextcode').val();

        let count = 0;
        let replaceWith = 'U+0040';
        bib_str = bib_str.replace(/\@/g, function (match) {
            count++;
            if (count === 1)
                return match;
            else
                return replaceWith;
        });

        let bib = parseBibFile(bib_str);
        bib = bib.getEntry(Object.keys(bib.entries$)[0]);

        let additional_entries = [];

        // citename
        if (bib._id) {
            $('#input-bibtex-citename').val(bib._id);
        }
        if (bib.type) {
            $('#input-type option').attr('selected', false);
            $('#input-type option[value=' + bib.type.toProperCase() +']').attr('selected', true);
            $('#input-type').trigger('change');
        }

        Object.keys(bib.fields).forEach(function (key) {
            switch (key) {
                case "title":
                    let title = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-title').val(title);
                    break;
                case "address":
                    let address = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-0').val(address);
                    break;
                case "booktitle":
                    let booktitle = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-1').val(booktitle);
                    break;
                case "chapter":
                    let chapter = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-2').val(chapter);
                    break;
                case "edition":
                    let edition = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-3').val(edition);
                    break;
                case "editor":
                    let editor = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-4').val(editor);
                    break;
                case "howpublished":
                    let howpublished = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-5').val(howpublished);
                    break;
                case "institution":
                    let institution = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-6').val(institution);
                    break;
                case "journal":
                    let journal = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-7').val(journal);
                    break;
                case "month":
                    let month = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-8').val(month);
                    break;
                case "note":
                    let note = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-9').val(note);
                    break;
                case "number":
                    let number = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-10').val(number);
                    break;
                case "organization":
                    let organization = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-11').val(organization);
                    break;
                case "pages":
                    let pages = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-12').val(pages);
                    break;
                case "school":
                    let school = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-13').val(school);
                    break;
                case "series":
                    let series = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-14').val(series);
                    break;
                case "volume":
                    let volume = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-15').val(volume);
                    break;
                case "publisher":
                    let publisher = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-bibtex-16').val(publisher);
                    break;
                case "doi":
                    let doi = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-doi').val(doi);
                    break;
                case "year":
                    let year = typeof bib.fields[key].data === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-year option').attr('selected', false);
                    $('#input-year option[value=' + year + ']').attr('selected', true);
                    $('#input-year').trigger('change');
                    break;
                case "abstract":
                    let abstract = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    $('#input-abstract').val(abstract);
                    break;
                case "author":
                    let authors = bib.getField('author').authors$.map(async (author) => {
                        let forename = author.firstNames.join(' ');
                        let surname = author.lastNames.join(' ');
                        return await $.get('/get/authorByName', {forename: forename, surname: surname})
                            .then(async (res) => {
                                if (Object.keys(res).length > 0) {
                                    return res.id;
                                } else {
                                    // Add author to database and add it dynamically to the select
                                    let newA = await $.ajax({
                                        type: "POST",
                                        url: "/add/author2",
                                        data: JSON.stringify({forename: forename, surname: surname}),
                                        contentType: 'application/json',
                                        success: function(data) {return data}
                                    });

                                    $('#select-authors').append($('<option>', {'value': newA.author.id, 'html': newA.author.cleanname}));
                                    $('#select-authors').select2({theme: 'bootstrap4'}).trigger("change");
                                    return newA.author.id;
                                }
                            })
                            .catch(e => console.error(e));
                    });
                    Promise.all(authors).then(res => {
                        // Move the options in the select to the end to have the right ordering
                        for (const author_id of res) {
                            let elem = $('#select-authors option[value=' + author_id +']');
                            elem.detach();
                            $('#select-authors').append(elem);
                            $('#author-list').append('<li id="' + elem.text().replace(/\s/g, '') + '" data-value="' + elem.val() + '" class="list-group-item list-group-item-action">' + elem.text() + '</li>');
                        }
                        $('#select-authors').val(res);
                        $('#select-authors').select2({theme: 'bootstrap4'}).trigger("change");
                    });
                    break;
                case "keywords":
                    let keywords = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    keywords = keywords.split(',').map((keyword) => {return keyword.toProperCase()});
                    let keyword_ids = keywords.map(async (keyword) => {
                        return await $.get('/get/keywordByName', {name: keyword})
                            .then(async (res) => {
                                if (Object.keys(res).length > 0) {
                                    return res.id;
                                } else {
                                    // Add keyword to database and add it dynamically to the select
                                    let newK = await $.ajax({
                                        type: "POST",
                                        url: "/add/keyword2",
                                        data: JSON.stringify({name: keyword}),
                                        contentType: 'application/json',
                                        success: function(data) {return data}
                                    });

                                    $('#select-keywords').append($('<option>', {'value': newK.keyword.id, 'html': newK.keyword.name}));
                                    $('#select-keywords').select2({theme: 'bootstrap4'}).trigger("change");
                                    return newK.keyword.id;
                                }
                            })
                            .catch(e => console.error(e));
                    });
                    Promise.all(keyword_ids).then(res => {
                        // Move the options in the select to the end to have the right ordering
                        for (const keyword_id of res) {
                            let elem = $('#select-keywords option[value=' + keyword_id +']');
                            elem.detach();
                            $('#select-keywords').append(elem);
                        }
                        $('#select-keywords').val(res);
                        $('#select-keywords').select2({theme: 'bootstrap4'}).trigger("change");
                    });
                    break;
                case "categories":
                    let categories = typeof bib.fields[key] === 'object' ? bib.fields[key].data.join('') : bib.fields[key];
                    break;
                default:
                    additional_entries.push(key + '=' + bib.fields[key].data.join(''));
                    break;
            }
        });
    });
});
