<?php

    print_r($_POST);

    if (move_uploaded_file($_FILES["file"]["tmp_name"], "subidas/".$_FILES['file']['name'])) {
        //more code here...
        $mensaje = "subidas/".$_FILES['file']['name'];
        header("Location: " . $_SERVER["HTTP_REFERER"]);

        echo "<div class='alert alert-success alert-dismissible' role='alert'>
				<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
				<strong>Aviso!</strong> " . "<p>".$mensaje." </p>";

    } else {
        echo 0;
    }



?>