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
            </a><h1 style="color:white;">Ayuda al Sistema Contable &nbsp;&nbsp;</h1>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class=" <?php echo $pagina == 'inicio' ? 'active' : '/'; ?>nav-item">
                <a class="nav-link active" aria-current="page" href="?p=inicio">Incio</a>
              </li>
              <li class="<?php echo $pagina == 'instructivo' ? 'active' : '/'; ?> nav-item">
                <a class="nav-link" href="?p=instructivo">Instructivo</a>
              </li>
             
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                  Herramientas Python
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                    <!--Utilizo una clase para acceder a javascript y llamar al modal-->
                    <li class="<?php echo $pagina == 'quita337' ? 'active' : '/'; ?> ">
                        <a class="dropdown-item" href="?p=quita337"><i class="bi bi-life-preserver"></i>&nbsp;&nbsp;Quita 337</a>
                    </li>
                    <li class="<?php echo $pagina == 'dividezonas'   ? 'active' : '/'; ?> ">
                        <a class="dropdown-item" href="?p=dividezonas"><i class="bi bi-life-preserver"></i>&nbsp;&nbsp;Divide Zonas</a>
                    </li>
                    <li class="<?php echo $pagina == 'olvidadosxzona'   ? 'active' : '/'; ?> ">
                        <a class="dropdown-item" href="?p=olvidadosxzona"><i class="bi bi-life-preserver"></i>&nbsp;&nbsp;Olvidados X Zona</a>
                    </li>
                
                  
                </ul>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled">Acerca de</a>
              </li>
            </ul>
           
          </div>
        </div>
      </nav>
   
            

        </div>
     
   

</body>
</html>
