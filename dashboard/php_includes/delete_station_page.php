<?php
	ini_set('display_errors', 1);
    $_POST['res'] = 2;

    include 'db_sidebar.php';

    $stations= array();
    for($i = 0; $i < count($row); $i++) {
        if (in_array($row[$i]["name"], $stations) == false) {
            array_push($stations, $row[$i]["name"]);
        }
    }

    for($i = 0; $i < count($stations); $i++) {
        $html = "<div class='station' id='" . $stations[$i] . "'><span class='station_inline'><h3>" . $stations[$i] . "</h3><img class='img_button' id='delete_station_button' src='../img/close.png' alt='Delete Station'></span>";

        $html = $html . "<div class='popup_inline'><div class='first_column'><label class='form-label'>Name:</label>" .
                "<input class='form-input-text' type='text' value='" . $stations[$i] . "' name='name' disabled='disabled' /></div>" .
                "<div class='second_column' name='" . $stations[$i] . "'><label class='form-label'>Devices:</label>";

        for($j = 0; $j < count($row); $j++) {
            if($row[$j]["name"] == $stations[$i]) {
                $html = $html . "<span id='device_info'><input class='form-input-text' type='text' name='device_metric' value='" . $row[$j]["metric_name"] . "' disabled='disabled'> " .
                "<input class='form-input-text' type='text' name='status' value='" . $row[$j]["status"] . "' disabled='disabled'>" .
                "</span>";
            }
        }

        $html = $html . "</div></div></div>";
        echo $html;
    }
?>