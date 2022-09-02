<?php
	session_start();
    if(isset($_POST['name'])){
        // if($_SESSION['query_par'] == "ALL"){
        //     $_SESSION['query_par'] = $_POST['name'];
        // } elseif ($_SESSION['query_par'] == $_POST['name']){
        //     $_SESSION['query_par'] = "ALL";
        // }

        $_SESSION['query_par'] = $_POST['name'];
    }

    echo $_SESSION['query_par'];
?>