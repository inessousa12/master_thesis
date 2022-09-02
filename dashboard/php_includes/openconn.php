<?php
    // The MySQL service named in the docker-compose.yml.
    $host = 'mysql';

    // Database use name
    $user = 'aquamon';

    //database user password
    $pass = 'password';

    // check the MySQL connection status
    $db_connect = new mysqli($host, $user, $pass, 'aquamon');

    // Check connection
   
    if (!$db_connect) {
        die("Connection failed: " . mysqli_connect_error());
    }
    
    $db_connect->set_charset("utf8");

?>