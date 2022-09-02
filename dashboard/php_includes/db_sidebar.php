<?php
require('openconn.php');

if(isset($_POST['res'])){    
    $result = $db_connect->query("SELECT sensor.metric_name, sensor.status, station.name FROM `station` LEFT JOIN `sensor` ON station.id = sensor.station_id;");
    $row = $result->fetch_all(MYSQLI_ASSOC);

    if($_POST['res'] == 1){
        echo json_encode($row);
    }
}

?>