<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <script src="https://code.jquery.com/jquery-3.6.0.js" integrity="sha256-H+K7U5CnXl1h5ywQfKtSj8PCmoN9aaq30gDh27Xc0jk=" crossorigin="anonymous"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.2/font/bootstrap-icons.css">
    
    <!-- JavaScript Bundle with Popper -->
   
    <title>Herramientas de Auxilio al Sistema Contable</title>
   
    
</head>
<body>
  
      <nav class="navbar  navbar-dark navbar-expand-lg  bg-primary">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">
             <img src="First-Aid.png" alt="Logo" width="50">
            </a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">Incio</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">Instructivo</a>
              </li>
             
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Herramientas Python
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <!--Utilizo una clase para acceder a javascript y llamar al modal-->
                  <li class="<?php echo $pagina == 'quita337' ? 'active': '';?> " href="?p=quita337"><a>Quita 337</a></li>
                  <li class="<?php echo $pagina == 'dividezonas' ? 'active': '';?>" href="?p=dividezonas"><a>divide zonas</a></li>
                  <li class="<?php echo $pagina == 'dividezonas1' ? 'active': '';?>" href="?p=dividezonas1"><a>divide zonas1</a></li>
                  
                </ul>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled">Acerca de</a>
              </li>
            </ul>
           
          </div>
        </div>
      </nav>
   

</body>
</html>

<script>
  /*
    $(document).ready(function (){
        
        $('.quita337').on('click', function (e){
            e.preventDefault();
            $('#quita337').modal('show');
        })
        $('#continuar').on('click', function(e){
            e.preventDefault();
            alert('Hola Estamos yendo a quitar los 337 de la facturacion del dia')
           
        })

        
        $('.dividezona').on('click', function (e){
            e.preventDefault();
            $('#dividezona').modal('show');
            window.location.href = "http://MARTIN:8081/cambiazonas/";
        })

    
        
    })
  */
</script>

<!-- Modal -->
<div class="modal fade" id= "quita337" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Quita 337</h5>
          <button type="button" class="btn btn-danger" data-bs-dismiss="modal" aria-label="Close">X</button>
        </div>
        <div class="modal-body">
          <p>Los archivos CSV del día deberan estar en la carpeta SUBIDAS del sitio </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
          <button type="button" class="btn btn-primary" id="continuar">Continuar</button>
        </div>
      </div>
    </div>
  </div>
  <!-- Modal -->
<div class="modal fade" id= "dividezona" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Divide los CSV de las zonas 22-221-703</h5>
          <button type="button" class="btn btn-danger" data-bs-dismiss="modal" aria-label="Close">X</button>
        </div>
        <div class="modal-body">
          <p>Los archivos CSV del día deberan estar en la carpeta SUBIDAS del sitio </p>
          <p>El archivo XLSX "demapas.csv" Tiene que ser actualizado con la planilla enviada por MAPAS </p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
          <button type="button" id="continuar" class="btn btn-primary">Continuar</button>
        </div>
      </div>
    </div>
  </div>
