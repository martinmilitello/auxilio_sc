<?php
    
    $anio="2022";
    $mes="06";
    $output = shell_exec("python ../Evalua.py ".$anio." ".$mes);  

    var_dump($output);


?>