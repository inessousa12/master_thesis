<?php
require('openconn.php');

if(isset($_POST['station_name'])){    
    $station_name = $_POST['station_name'];
    $result = $db_connect->query("DELETE FROM `station` WHERE `name` = '$station_name'");

    if ($result === TRUE) {
        echo "Record deleted successfully";
    } else {
        die(json_encode(array('message' => $db_connect->error)));
    }
}
?>