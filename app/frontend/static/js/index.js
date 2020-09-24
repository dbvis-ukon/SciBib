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



