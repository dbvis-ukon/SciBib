<!--
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
-->
<?php

if (isset($publication)) {

    //
    // TYPE BASED ADDITIONS
    //
	$typeAdditions = "";
    if ($publication->type === 'Article') {
        if ($publication->journal) {
            $typeAdditions = $publication->journal;
            if ($publication->publisher) {
                $typeAdditions .= ", ";
                $typeAdditions .= $publication->publisher;
            }
            if ($publication->volume) {
                $typeAdditions .= ", ";
                $typeAdditions .= $publication->volume . "(" . $publication->number . ")";
                if ($publication->pages) {
                    $typeAdditions .= ":" . $publication->pages;
                }
            }
        }

        $typeAdditions = h($typeAdditions);
    }

    if ($publication->type === 'Inproceedings' || $publication->type === 'Conference') {
        if ($publication->booktitle) {
            $typeAdditions = '<span class="publicationBookTitle">' . h($publication->booktitle) . '</span>';
            if ($publication->publisher) {
                $typeAdditions .= ", ";
                $typeAdditions .= $publication->publisher;
            }
            if ($publication->pages) {
                $typeAdditions .= ", ";
                $typeAdditions .= "pages " . $publication->pages;
            }
        }
    }

    if ($publication->type === 'Book') {
        if ($publication->publisher) {
            $typeAdditions = $publication->publisher;
        }
    }

    if ($publication->type === 'Inbook' || $publication->type === 'Incollection') {
        if ($publication->booktitle) {
            $typeAdditions = '<span class="publicationBookTitle">' . h($publication->booktile) . '</span>';
            if ($publication->publisher) {
                $typeAdditions .= ", ";
                $typeAdditions .= $publication->publisher;
            }
            if ($publication->pages) {
                $typeAdditions .= ", ";
                $typeAdditions .= "pages " . $publication->pages;
            }
        }
    }

    if ($publication['Publication']['type'] == 'Misc') {
        if ($publication->note) {
            $typeAdditions = h($publication->note);
        }
    }

    //
    // CREATE TO APPEAR STRING
    //

	$toAppearString = '';
    if ($publication->published == false) {
        if (strlen($typeAdditions) < 1) {
            $toAppearString = "To appear";
        } else {
            $toAppearString = ', to appear';
        }
    }

    //
    // CREATE YEAR STRING
    //
	$yearString = "";
    if (strlen($typeAdditions) > 0 || strlen($toAppearString) > 0 || strlen($doiString) > 0) {
        $yearString = ", ";
    }
    $yearString .= $publication->year;

    $doiString = $publication->doi;

    if ($doiString) {
        $doiString = 'DOI: <a href="http://dx.doi.org/' . $doiString . '" target="_blank">' . $doiString . "</a>";
    }

    //change formatting for copyable print
    $newline = '<br />';
    $cssClass = 'publicationText';
    $beforeAuthors = '';
    $afterAuthors = '.';
    $beforeTitle = '';
    $afterTitle = '.';
    if ($renderCopyable) {
        $newline = '&nbsp;';
        $cssClass = 'publicationTextCopyable';
        $beforeAuthors = '';
        $afterAuthors = ':';
        $beforeTitle = "'";
        $afterTitle = "',";
    } else {

    }

    $returnString = '<span class="' . $cssClass . '">';
	$doiAddition = $typeAdditions;
	if (strlen($typeAdditions) > 0 && strlen($doiString) > 0) {
		$doiAddition = $typeAdditions . ", " . $doiString . " ";
	} else if (strlen($doiString) > 0) {
		$doiAddition = $doiString . " ";
	}
    $returnString .= '<span class="publicationAdditionalInfo">' . $doiAddition . $toAppearString . $yearString . '.</span>';
    $returnString .= '</span>';
    echo $returnString;
}
?>
