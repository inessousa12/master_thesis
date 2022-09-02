<?php
require('openconn.php');

if(isset($_POST['metric_name'])){    
    $metric = $_POST['metric_name'];
    $result = $db_connect->query("INSERT INTO `metric` (`name`) VALUES ('$metric')");

    if ($result === TRUE) {
        echo "New record created successfully";
    } else {
        die(json_encode(array('message' => $db_connect->error)));
    }
}
?>