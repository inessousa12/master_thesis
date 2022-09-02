<?php
require('openconn.php');

if(isset($_POST['station_name'])){ 
    $station_name = $_POST['station_name'];
    $result = $db_connect->query("SELECT `id` FROM `station` WHERE `name` = '$station_name'");
    $row = $result->fetch_all(MYSQLI_ASSOC);

    $station_id = $row[0]["id"];
    echo $station_id;
    $metric = $_POST['metric'];
    $status = $_POST['status'];
    $result = $db_connect->query("INSERT INTO `sensor` (`metric_name`, `station_id`, `status`) VALUES ('$metric', '$station_id', '$status')");

    if ($result === TRUE) {
        echo "New record created successfully";
    } else {
        die(json_encode(array('message' => $db_connect->error)));
    }
}
?>