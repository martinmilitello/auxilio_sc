
<?php   
    $pagina = isset($_GET['p'] ) ? strtolower($_GET['p']) : 'inicio'; // Tomo la variable p que viene de header con el nombre de la pagina a utilizar

            
    require_once('paginas/header1.php');
                          
    require_once('paginas/'.$pagina.'.php');  // Tomo la variable p que viene de header con el nombre de la pagina a utilizar

    // require_once('paginas/footer.php')
       
                // include_once('clases/footer.php');
      
?>