<?php
require('openconn.php');

if(isset($_POST['station_name'])){    
    $original_name = $_POST['original_station'];
    $station_name = $_POST['station_name'];
    $latitude = floatval($_POST['latitude']);
    $longitude = floatval($_POST['longitude']);
    $result = $db_connect->query("UPDATE `station` SET `name` = '$station_name', `latitude` = '$latitude', `longitude` = '$longitude' WHERE `name` = '$original_name'");

    $result = $db_connect->query("SELECT `id` FROM `station` WHERE `name` = '$station_name'");
    $row = $result->fetch_all(MYSQLI_ASSOC);

    $metric = $_POST['metric'];
    $status = $_POST['status'];
    $station_id = $row[0]["id"];
    $sensor_id = $_POST['sensor_id'];

    $result = $db_connect->query("UPDATE `sensor` SET `metric_name` = '$metric', `status` = '$status' WHERE `station_id` = '$station_id' AND `id` = '$sensor_id'");

    if ($result === TRUE) {
        echo "New record created successfully";
    } else {
        die(json_encode(array('message' => $db_connect->error)));
    }
}
?>