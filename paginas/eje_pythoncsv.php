<?php


if (isset($_POST['fecha'])  &&  isset($_POST['hora'])){
           $fecha = $_POST['fecha'];
           $hora  = $_POST['hora'];
           $zona  = $_POST['zona'];
        
          // var_dump($_POST['hora']);
          // var_dump($_POST['fecha']);
         //  $outsolo = "python separar221.py ".$fecha." ".$hora." ".$pathpos." ".$pathcli;
        // redirigir errores a la salida estandar

          ini_set('display_errors', '1');
          ini_set('error_reporting', E_ALL);

         $output = shell_exec("python ../dividecsv.py ".$fecha." ".$hora." ".$zona);  

         $error = error_get_last();
         if ($error['type'] === E_ERROR){
          $errorpython = $error['message'];
         }

         //$output = shell_exec("python ../kk.py ".$fecha." ".$hora." ".$zona); 
           write_to_console($_POST['hora']);
           write_to_console($_POST['zona']);
           write_to_console($_POST['fecha']);
           write_to_console($output);     
           // Display output python
           if($output == ""){
                       
            echo "<div   class='alert alert-warning alert-dismissible' role='alert'>
                <button class='close btn-danger' data-bs-dismiss='alert' id='aviso'>X</button>
                <strong>Correcto!!!!</strong> Se han divido las zonas".$output.$errorpython.
            "</div>";
          }
          else {
              echo "<div class='alert alert-danger alert-dismissible' role='alert'>
                    <button type='button' id='btnaviso' class='btn-danger' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
                    <strong>Error!</strong>".$output.":".$fecha."-".$hora.",".$zona.$errorpython."</p>"."</div>";
               
          }
}
else{
           echo "No llego la variable ";
}
      
function write_to_console($data) {
  $console = $data;
  if (is_array($console))
  $console = implode(',', $console);
 
  echo "<script>console.log('Console: " . $console . "' );</script>";
 }    
      

?>