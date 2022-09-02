<?php
	ini_set('display_errors', 1);
    $_POST['all'] = 1;
    $_POST['res'] = 2;

    include 'get_all_stations.php';

    $stations= array();
    for($i = 0; $i < count($row); $i++) {
        if (in_array($row[$i]["name"], $stations) == false) {
            array_push($stations, $row[$i]["name"]);
        }
    }

    $html = "<label>Select a station to edit:</label><select class='select_station'><option value='' disabled selected>Select your option</option>";

    for($i = 0; $i < count($stations); $i++) {
        $html = $html . "<option value='" . $stations[$i] . "'>" .  $stations[$i] . "</option>";
    }

    $html = $html . "</select><div class='edit_station_add'></div>";
    echo $html;
?>