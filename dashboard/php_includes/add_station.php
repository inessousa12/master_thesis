<?php
require('openconn.php');

if(isset($_POST['station_name'])){    
    $station_name = $_POST['station_name'];
    $latitude = floatval($_POST['latitude']);
    $longitude = floatval($_POST['longitude']);
    $result = $db_connect->query("INSERT INTO `station` (`name`, `latitude`, `longitude`) VALUES ('$station_name', '$latitude', '$longitude')");

    $result = $db_connect->query("SELECT `id` FROM `station` WHERE `name` = '$station_name'");
    $row = $result->fetch_all(MYSQLI_ASSOC);

    $metric = $_POST['metric'];
    $status = $_POST['status'];
    $station_id = $row[0]["id"];

    $result = $db_connect->query("INSERT INTO `sensor` (`metric_name`, `station_id`, `status`) VALUES ('$metric', '$station_id', '$status')");

    if ($result === TRUE) {
        echo "New record created successfully";
    } else {
        die(json_encode(array('message' => $db_connect->error)));
    }
}
?>