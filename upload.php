<?php
if(!empty($_FILES['texto'])){
    // Configuracion de lo sarchivos subidos

    // Borro los archivos que estan en la carpeta
    $files = glob('subidas/C*.csv'); // get all file names
    foreach($files as $file){ // iterate files
        if(is_file($file)) {
            unlink($file); // delete file
        }
    }


    $targetDir = "subidas/";
    $allowTypes = array('csv');
    print_r($_FILES);
    $images_arr = array();
    foreach($_FILES['texto']['name'] as $key=>$val){
        $csv_name = $_FILES['texto']['name'][$key];
        $tmp_name   = $_FILES['texto']['tmp_name'][$key];
        $size       = $_FILES['texto']['size'][$key];
        $type       = $_FILES['texto']['type'][$key];
        $error      = $_FILES['texto']['error'][$key];
        
        // Path del archivo subido
        $fileName = basename($_FILES['texto']['name'][$key]);
        $targetFilePath = $targetDir . $fileName;
        
        // Checkeo que el tipo de archivo sea válido
        $fileType = pathinfo($targetFilePath,PATHINFO_EXTENSION);
        if(in_array($fileType, $allowTypes)){    
            // Guardo los CSV en el servidor
            if(move_uploaded_file($_FILES['texto']['tmp_name'][$key],$targetFilePath)){
                echo "<span style='color:#3AFF00;'>Archivo ".$fileName ." subido con éxito!!<span>";
            }
        }
    }
    
   
}
?>