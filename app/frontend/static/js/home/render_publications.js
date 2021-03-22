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

/**
 * Lazy loading of the publications
 */

'use strict';

/*
Check if a string is a valid URL
 */
const isUrl = (str) => {
  try {
    new URL(str);
    return true;
  } catch (exception) {
    return false;
  }
};

/*
Handle lazy loading of the publications. Keeps track of the position of already loaded publications and loads next
chunk of publications when scrolling to page end.
 */
$(document).ready(function () {

    let scroller = document.querySelector('#publications');
    let template_pub = document.querySelector('#template-publication');

    let sentinel = document.querySelector('#sentinel');
    let counter = 0;

    async function loadItems() {
        if (!(scroller))
            return;

        // get filters if there are some
        let params = window.location.search.substring(1);

        //fetch('/loadItems?c=${counter}').then((response) => {
        fetch('/loadItems?offset=' + counter + '&' + params).then(async (response) => {
            let pubs_loaded = 0;

            await response.json().then((data) => {
                if (!data.length)
                    sentinel.innerHTML = "No more publications";

                data.forEach((pub_in_year) => {
                    let year = pub_in_year[0];
                    let publications = pub_in_year[1];

                    // add title containing the year
                    if (!($('#heading-year-' + year.toString()).length))
                        $(scroller)
                            .append($('<div>', {class: 'row border-bottom mb-1 pl-2 pr-2', id: "heading-year-" + year.toString()})
                                .append($('<div>', {class: 'col-lg-12 bg-light color-lightslategray'})
                                    .append($('<h3>', {text: year}))
                                )
                            );

                    publications.forEach((pub, i) => {
                        let new_pub = template_pub.content.cloneNode(true);

                        for (const [i, author] of pub['authors'].entries())
                            $(new_pub).find('#authors').first().append($('<a>', {class: 'text-muted', href: '/?author=' + author['id'],
                                                                    html: author['cleanname'] + (i === pub['authors'].length - 1 ? '' : ', ')}));

                        $(new_pub).find('#title').first().attr('href', '/publications/view/' + pub['id']);
                        $(new_pub).find('#title').first().html(pub['title']);

                        // add color of circle indicating the publication type
                        if(type_to_color[pub['type']]) {
                            $(new_pub.querySelector('#circle-type')).css("color", type_to_color[pub['type']]);
                            $(new_pub.querySelector('#circle-type')).attr("title", pub['type']);
                        }
                        else {
                            $(new_pub.querySelector('#circle-type')).css("color", type_to_color['Misc']);
                            $(new_pub.querySelector('#circle-type')).attr("title", "Misc");
                        }

                        // add doi if available else add disabled button
                        if (pub['doi'])
                            $(new_pub).find('#doi-item').append($('<a>', {class: 'btn btn-xsm btn-dark', html: 'DOI',
                                                                            role: 'button', href: 'http://dx.doi.org/' + pub['doi']}));
                        else
                            $(new_pub).find('#doi-item').append($('<button>', {class: 'btn btn-xsm btn-dark cursor-default', html: 'DOI',
                                                                               role: 'button', disabled: true}));

                        // add bib item if type is available else add disabled button
                        // if(pub['type'])
                        $(new_pub).find('#bib-item').append($('<a>', {class: 'btn btn-xsm btn-dark', html: 'TeX',
                                                                            role: 'button', href: '/publications/bibtex/' + pub['id']}));
                        // else
                        //     $(new_pub).find('#bib-item').append($('<button>', {class: 'btn btn-xsm btn-dark', html: 'TeX',
                        //                                                        role: 'button', disabled: true}));

                        // add a button for the main file
                        if (pub['mainfile'] && pub['mainfile'].trim()) {
                            // might be a URL
                            if (isValidURL(pub['mainfile'])) {
                                $(new_pub).find('#url-item').append($('<a>', {class: 'btn btn-xsm btn-dark', html: 'URL',
                                                                            role: 'button', href: pub['mainfile']}));
                                $(new_pub).find('#pdf-item').append($('<button>', {class: 'btn btn-xsm btn-dark cursor-default', html: 'PDF',
                                                                               role: 'button', disabled: true}));
                            }
                            else {
                                $(new_pub).find('#pdf-item').append($('<a>', {class: 'btn btn-xsm btn-dark', html: 'PDF',
                                                                            role: 'button', href: '/uploadedFiles/' + pub['mainfile']}));
                                let urls = pub['documents'].filter((doc) => doc['filename'] && doc['filename'].trim() && doc['filename'] !== pub['mainfile'] && isValidURL(doc['filename']));
                                if (urls.length === 0)
                                    $(new_pub).find('#url-item').append($('<button>', {class: 'btn btn-xsm btn-dark cursor-default', html: 'URL',
                                                                               role: 'button', disabled: true}));
                                else
                                    $(new_pub).find('#url-item').append($('<a>', {class: 'btn btn-xsm btn-dark', html: 'URL',
                                                                            role: 'button', href: urls[0]['filename']}));
                            }
                        } else {
                            $(new_pub).find('#pdf-item').append($('<button>', {
                                class: 'btn btn-xsm btn-dark cursor-default', html: 'PDF',
                                role: 'button', disabled: true
                            }));
                            let urls = pub['documents'].filter((doc) => doc['filename'] && doc['filename'].trim() && doc['filename'] !== pub['mainfile'] && isValidURL(doc['filename']));
                            if (urls.length === 0)
                                $(new_pub).find('#url-item').append($('<button>', {
                                    class: 'btn btn-xsm btn-dark cursor-default', html: 'URL',
                                    role: 'button', disabled: true
                                }));
                            else
                                $(new_pub).find('#url-item').append($('<a>', {
                                    class: 'btn btn-xsm btn-dark', html: 'URL',
                                    role: 'button', href: urls[0]['filename']
                                }));
                        }

                        // add thumbnail
                        if (pub['thumb'])
                            $(new_pub).find('#thumb-item').first().attr('src', function() { return $(this).attr('src') + pub['thumb']});
                        else
                            $(new_pub).find('#thumb-item').first().attr('src', "/static/images/thumb-default.png");
                            // $(new_pub).find('#thumb-item').each((i, elem) => {$(elem).attr('src', $(elem).attr('src') + pub['thumb'])});
                        // add info about journal and publication year
                        let info = [];
                        if (pub['booktitle'])
                            info.push(pub['booktitle']);
                        else if (pub['journal'])
                            info.push(pub['journal']);
                        if (pub['year'])
                            info.push(pub['year']);
                        new_pub.querySelector('#info-item').innerHTML = info.join(', ');

                        if (pub['keywords'])
                            for (const keyword of pub['keywords']) {
                                $(new_pub).find('#keywords').append($('<a>', {
                                    class: 'btn btn-outline-secondary btn-xsm',
                                    href: '/?keyword=' + keyword['id'],
                                    html: keyword['name']
                                }));
                            }

                        $(scroller).append($('<div>', {class: 'row ' + (counter % 2 === 1 ? 'hover-pub-item-light' : 'background-color-whitesmoke hover-pub-item-dark')}).append(new_pub));
                        counter++;
                        pubs_loaded++;
                    })
                });
            });
            // Remove loading icon if no more publications can be found and the intersection observer was not triggered
            // because not enough publications have been found for it to leave the current view
            if (pubs_loaded < 20)
                sentinel.innerHTML = "No more publications";
        })
    }

    let intersectionObserver = new IntersectionObserver(entries => {
        if (entries[0].intersectionRatio <= 0)
            return;

        loadItems();
    });

    if (sentinel)
        intersectionObserver.observe(sentinel);
});
