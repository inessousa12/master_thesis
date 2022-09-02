<?php
    require('openconn.php');
	ini_set('display_errors', 1);
    
    if(isset($_POST['metric'])) {
        $query = "SELECT * FROM `metric`";
		$result = $db_connect->query($query);
        $metrics = $result->fetch_all(MYSQLI_ASSOC);

        if(isset($_POST['metric_echo'])) {
            echo json_encode($metrics);
        }
    }
?>