<?php

// anio:anio,mes:mes,zona:zona,proc:proc
if (isset($_POST['anio'])  &&  isset($_POST['mes'])  &&  isset($_POST['zona']) &&  isset($_POST['proc'])){
           $anio = $_POST['anio'];
           $mes = $_POST['mes'];
           $zona = $_POST['zona'];
           $proc = $_POST['proc'];
          
        
         //  var_dump($_POST['anio']);
          // var_dump($_POST['fecha']);
         //  $outsolo = "python separar221.py ".$fecha." ".$hora." ".$pathpos." ".$pathcli;
         if($proc == 'xlsx')  {
          $output = shell_exec("python ../Evalua.py ".$anio." ".$mes); 
         }
          if($proc=='trae'){
            $output = shell_exec("python ../traeesazon.py ".$anio." ".$mes." ".$zona);
          }
         //$output = shell_exec("python ../kk.py ".$fecha." ".$hora." ".$zona); 
        
           // Display output python
           if($output == ""){
                       
                echo "<div   class='alert alert-success alert-dismissible' role='alert'>
                    <button class='close btn-danger' data-bs-dismiss='alert' id='aviso'>X</button>
                    <strong>Correcto!!!!</strong> Se ha generado la planilla XLSX en la carpeta SUBIDASX/ del sitio".$output.
                "</div>";
           }
           else {
                  echo "<div class='alert alert-danger alert-dismissible' role='alert'>
                        <button type='button' id='btnaviso' class='btn-danger' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>
                        <strong>Error!</strong>".$output.":".$anio."-".$mes."-".$zona."</p>"."</div>";
                   
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