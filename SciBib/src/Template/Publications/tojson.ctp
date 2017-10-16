<?php

/*

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

*/

# Add file dir to let people know where files lay
# $publications['file_dir'] = WWW_ROOT . 'uploadedFiles' . DS;
$json = array();
$json['publications'] = $publications;
$json['file_dir'] = 'uploadedFiles';
$json = json_encode($json, JSON_PRETTY_PRINT);
echo $json;

?>
