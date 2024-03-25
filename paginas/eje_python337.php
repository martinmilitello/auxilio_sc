<?php


if (isset($_POST['fecha'])){
           $fecha = $_POST['fecha'];
          
        
          // var_dump($_POST['hora']);
          // var_dump($_POST['fecha']);
         //  $outsolo = "python separar221.py ".$fecha." ".$hora." ".$pathpos." ".$pathcli;
           
         $output = shell_exec("python ../quita337.py ");  
         //$output = shell_exec("python ../kk.py ".$fecha." ".$hora." ".$zona); 
        
           // Display output python
           if($output == ""){
                       
                echo "<div   class='alert alert-warning alert-dismissible' role='alert'>
                    <button class='close btn-danger' data-bs-dismiss='alert' id='aviso'>X</button>
                    <strong>Correcto!!!!</strong> Se han quitado todos los 337 de los archivos CSV. Puede copiar los archivos a la carpeta INTPEDIDOS".$output.
                "</div>";
           }
           else {
                  echo "<div class='alert alert-danger alert-dismissible' role='alert'>
                        <button type='button' id='btnaviso' class='btn-danger' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
                        <strong>Error!</strong>".$output.":".$fecha."-".$hora.",".$zona."</p>"."</div>";
                   
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