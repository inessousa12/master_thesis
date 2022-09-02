<?php
    require('openconn.php');
	ini_set('display_errors', 1);
    $_POST['metric'] = 1;
    include 'get_metrics.php';
    
    if(isset($_POST['station_name'])) {
        $station = $_POST['station_name'];
        $query = "SELECT station.latitude, station.longitude, sensor.metric_name, sensor.status, sensor.id FROM `sensor`, `station` WHERE sensor.station_id = (SELECT `id` FROM station WHERE `name` = '$station') AND station.name = '$station'";
		$result = $db_connect->query($query);
        $row = $result->fetch_all(MYSQLI_ASSOC);

        if($row == []) {
            $query = "SELECT station.latitude, station.longitude FROM `station` WHERE station.name = '$station'";
            $result = $db_connect->query($query);
            $row = $result->fetch_all(MYSQLI_ASSOC);
        }
        echo json_encode(array("metrics" => $metrics, "station" => $row));
    }
?>