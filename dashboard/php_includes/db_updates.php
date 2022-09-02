<?php
  require('openconn.php');

  if(isset($_POST['station_name'])){
    $station_name = $_POST['station_name'];		
		$metric = strval($_POST['metric']);
		$status = strval($_POST['status']);

    $query = "UPDATE `sensor` set sensor.status = '$status' WHERE sensor.metric_name = '$metric' AND sensor.station_id = (SELECT `id` FROM `station` WHERE station.name = '" .$station_name ."')";
    echo $query;
 
		$db_connect->query($query);
  }
?>