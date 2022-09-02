<?php
    require('openconn.php');
	ini_set('display_errors', 1);
    $_POST['metric'] = 1;
    
    if(isset($_POST['all'])) {
        $query = "SELECT * FROM `station`";
		$result = $db_connect->query($query);
        $row = $result->fetch_all(MYSQLI_ASSOC);
        if($_POST['res'] == 1){
            echo json_encode($row);
        }
    }
?>