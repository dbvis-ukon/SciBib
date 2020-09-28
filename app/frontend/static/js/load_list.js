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

const isUrl = (str) => {
  try {
    new URL(str);
    return true;
  } catch (exception) {
    return false;
  }
};

$(document).ready(function () {

    let scroller = document.querySelector('#publications');
    let template_light = document.querySelector('#template_publication_item_light');
    let template_dark = document.querySelector('#template_publication_item_dark');
    let pdf_item_light = document.querySelector('#pub_item_pdf_light');
    let pdf_item_dark = document.querySelector('#pub_item_pdf_dark');
    let bibtex_item_light = document.querySelector('#pub_item_bibtex_light');
    let bibtex_item_dark =  document.querySelector('#pub_item_bibtex_dark');

    let sentinel = document.querySelector('#sentinel');
    let counter = 0;

    function loadItems() {
        if (!(scroller))
            return;

        fetch('/loadItems?c=' + counter).then((response) => {
            response.json().then((data) => {
                if (!data.length)
                    sentinel.innerHTML = "No more publications";

                data.forEach((pub, i) => {
                    let template_pub = i % 2 === 0 ? template_light.content.cloneNode(true) : template_dark.content.cloneNode(true);
                    template_pub.querySelector('#p-authors').innerHTML = pub['authors'].map(function(elem) { return elem.cleanname }).join(', ');
                    template_pub.querySelector('#p-title').innerHTML = pub['title'];
                    template_pub.querySelector('#p-year').innerHTML = pub['year'];
                    if (pub['thumb'])
                        template_pub.querySelector('#pub-thumb').src += pub['thumb'];
                    else
                        template_pub.querySelector('#pub-thumb').src = '/static/images/thumb-default.png';

                    pub['documents'].forEach((doc, j) => {
                        if(!doc['filename'].endsWith('.pdf') || doc['filename'] !== pub['mainfile'])
                            return;
                        // if (isUrl(doc['filename'])) // || doc['filename'] !== pub['mainfile'])
                        //     return;
                        let template_pdf = i % 2 === 0 ? pdf_item_light.content.cloneNode(true) : pdf_item_dark.content.cloneNode(true);
                        template_pdf.querySelector('#pdf-link').href += doc['filename'];
                        template_pub.querySelector('#pub-downloads').appendChild(template_pdf);
                    });

                    pub['documents'].forEach((doc, j) => {
                        if (isUrl(doc['filename']) || doc['filename'] !== pub['mainfile'])
                            return;
                        let template_bibtex = i % 2 === 0 ? bibtex_item_light.content.cloneNode(true) : bibtex_item_dark.content.cloneNode(true);
                        template_bibtex.querySelector('#bibtex-link').href += doc['publication_id'];
                        template_pub.querySelector('#pub-downloads').appendChild(template_bibtex);
                    });

                    scroller.appendChild(template_pub);
                    counter++;
                });
            })
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