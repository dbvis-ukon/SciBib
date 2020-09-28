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

import 'bootstrap/dist/css/bootstrap.min.css';
import '../css/main.css';
import $ from 'jquery';
import 'popper.js';
import 'bootstrap';
import 'font-awesome/css/font-awesome.css';
import 'datatables.net-responsive-bs4';

import 'select2/dist/js/select2';
import 'select2/dist/css/select2.css'
import '@ttskch/select2-bootstrap4-theme/dist/select2-bootstrap4.css';

import {Sortable, Swap} from 'sortablejs/modular/sortable.core.esm';

Sortable.mount(new Swap());

window.jQuery = $;
window.$ = $;
window.Sortable = Sortable;

import 'jquery-sortablejs/jquery-sortable.js';

import {parseBibFile, normalizeFieldValue} from "bibtex";
window.parseBibFile = parseBibFile;
window.normalizeFieldValue = normalizeFieldValue;



