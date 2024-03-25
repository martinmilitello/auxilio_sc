<!doctype html>
<html lang="en">
  <head>
    <title>Quita337</title>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS v5.0.2 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"  integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <link rel="stylesheet" href="css/esperar.css">
    
    <style>
        .my-custom-scrollbar {
            position: relative;
            height: 300px;
            overflow: auto;
        }
        .table-wrapper-scroll-y {
        display: block;
        }

        .btn-file {
      position: relative;
      overflow: hidden;
        }
        .btn-file input[type=file] {
          position: absolute;
          top: 0;
          right: 0;
          min-width: 100%;
          min-height: 100%;
          font-size: 100px;
          text-align: right;
          filter: alpha(opacity=0);
          opacity: 0;
          outline: none;
          background: white;
          cursor: inherit;
          display: block;
        }
        .cargararchivos{
          font-size: 20px;
        }
    </style>
    <?php
        $fecha =  date("Y-m-d");
        $fechaComoEntero = strtotime($fecha);
        $anio = date("Y", $fechaComoEntero);
        $mes = date("m", $fechaComoEntero);
    ?>
  </head>
  <body style="background-color: #E1E5E1 ;">

    <div class="container">

      <div class="container p-3 my-4 shadow bg-light text-black rounded">
                 
          <div class="row h-100 justify-content-center">
          
              <div class="col-md-1">
                  <div class="container shadow bg-light rounded">
                      
                      <span> <i class="fas fa-toolbox fa-3x" style="color:red" > </i></span>
                  </div>
              </div>
             
                  <div class="col-md-10">
                     
                          <h3>Recupera pedidos que DL descartó</h3>
                     
                  </div>
            
          
              <div class="col-md-1">
                  <div class="container shadow bg-primary rounded">
                      <div class="top-bg"></div>
                      
                  </div>
                  
              </div>
          </div>
      </div>

      <div class="row">
         

          <div class="col-md-6">
              <div class="container p-3 shadow bg-light text-black rounded" >
                <div class="d-flex justify-content-center">
                    <h4>Proceso de Python Obtiene Excel </h4>
                </div>
                  <div id = "contenedor_carga">
                      <div id="carga"></div>
                  </div>
                  <form>
                      <div class="form-group ">
                        <label for="fecha">Año</label>
                        <input type="text" class="form-control" id="anio" placeholder=<?php echo $anio?> aria-describedby="anioHelp" >
                      </div>

                      <div class="form-group ">
                        <label for="fecha">Mes</label>
                        <input type="text" class="form-control" id="mes" placeholder=<?php echo $mes ?> aria-describedby="mesHelp" >
                      </div>
         
                      <div class="form-group">
                          <label for="rutaped">Ruta o Path Planilla XLSX:</label>
                          <input type="text" class="form-control" id="rutaped" value ="/SUBIDASX/"aria-describedby="rutaHelp" readonly>
                          <small id="passHelp" class="form-text text-muted"></small>
                      </div>
                      <p>     </p>
                          <div class="d-flex justify-content-around">
                            
                              <button id="btnejexlsx" type="button" class="btn btn-primary" data-toggle="tooltip" data-placement="top" title="Genera la planilla con las zonas disponibles según el Año y el Mes proporcionado y deja la planilla en la carpeta SUBIDASX">Obtiene XLSX</button>
                          </div>
                      
                      <div>
                          <h5><p id = "pyshow"></p></h5> 
                           
                      </div>
                  
                </form>
                      
                      <p>     </p>
                <form>
                    <div class="container shadow p-3 text-black rounded" >
                            <div class="d-flex justify-content-around">
                                <h4>Proceso de Python Obtiene ZONAS  </h4>
                            </div>
                        
                           

                            <div class="row g-3 align-items-center">
                                <div class="col-md-1">
                                    <label for="aniozo" class="col-form-label">Año</label>
                                </div>
                                <div class="col-md-3">
                                    <input type="text" class="form-control" id="aniozo" placeholder=<?php echo $anio?> aria-describedby="anioHelp" >
                                </div>
                                <div class="col-md-1">
                                    <span id="meszo1" class="form-group">
                                        <label for="zona">Mes</label>
                                    </span>
                                      
                                </div>
                                <div class="col-md-3">
                                    <span id="meszo2" class="form-group">
                                    <input type="text" class="form-control" id="meszo" placeholder=<?php echo $mes ?> aria-describedby="mesHelp" >
                                    </span>
                                      
                                </div>
                              
                                    <div class="col-md-1">
                                        <span id="meszo3" class="form-group">
                                            <label for="zona">Zona</label>
                                        </span>
                                        
                                    </div>
                                    <div class="col-md-3">
                                        <span id="meszo4" class="form-group">
                                        <input type="text" class="form-control" id="zona" placeholder=<?php echo 'Ej:996' ?> aria-describedby="mesHelp" >
                                        </span>
                                        
                                    </div>
                                 
                            </div>
                       
                        

                        <p>     </p>
                            <div class="d-flex justify-content-around">
                                <button id="btntraezona" type="button" class="btn btn-primary" data-toggle="tooltip" data-placement="top" title="Con la planilla marcada con 'X' en las zonas y haber elegido una zona de salida Ej:996 genera los TXT en la carpeta /SUBIDASX/ del servidor ">Obtiene Zonas</button>
                            </div>
                        <p>     </p>
                        <div>
                            <h5><p id = "pyshow1"></p></h5> 
                        </div>
                    </div>
                </form>
                 
              </div>


            </div>

            <div class="col-md-6">
            
            
              <div class="container shadow p-3 text-black rounded" style="background-color: #E5F0E2 ;">
                      <div class="d-flex justify-content-start">
                          <h4>Cargar Archivos</h4>
                      </div>
      
                              <div class="d-flex justify-content-center">
                                   <div class="upload-div">
                                        <!-- Form de upload Archivo  -->
                                        <form id="uploadForm" enctype="multipart/form-data">
                                            <label>Seleccione los CSV Cabeceras,Detalles y Clientes</label>
                                            <input type="file" name="texto[]" id="fileInput" multiple >
                                            <button class="btn btn-primary" type="submit" name="submit"><span> <i class="bi bi-upload"></i></span>&nbsp;&nbsp;SUBIR</button>
                                        </form>
                                            
                                        <!-- Display upload status -->
                                        <div id="uploadStatus"></div>
                                    </div>
                              </div>
                  </div> <!-- container shadow  -->
|           
                 
                  <div class="container shadow p-3 bg-light text-black rounded">
                          <h4>Descargas Disponibles en: SUBIDASX\</h4>
                          <div class="table-wrapper-scroll-y my-custom-scrollbar">
                              <table class="table table-success table-bordered" style='color: black'>
                                  <thead>
                                      <tr>
                                      <th width="7%">#</th>
                                      <th width="70%">Nombre del Archivo</th>
                                      <th width="13%">Descargar</th>
                                      <th width="10%">Eliminar</th>
                                      </tr>
                                  </thead>
                                  <tbody>
                                      <?php
                                      $archivos = scandir("subidasx");
                                      $num=0;
                                      for ($i=2; $i<count($archivos); $i++)
                                      {$num++;
                                      ?>
                                      <p>     </p>
                              
                                      <tr class="table-primary" style='color:black'>
                                          <th scope="row"><?php echo $num;?></th>
                                          <td><?php echo $archivos[$i]; ?></td>
                                          <td><a title="Descargar Archivo" href="subidasx/<?php echo $archivos[$i]; ?>" download="<?php echo $archivos[$i]; ?>" style="color: blue; font-size:18px;"> <span class="bi bi-download" aria-hidden="true"></span> </a></td>
                                          <td><a title="Eliminar Archivo" href="paginas/Eliminar.php?name=../subidasx/<?php echo $archivos[$i]; ?>" style="color: red; font-size:18px;" onclick="return confirm('Esta seguro de eliminar el archivo?');"> <span class="bi bi-trash" aria-hidden="true"></span> </a></td>
                                      </tr>

                                      <?php }?> 

                                  </tbody>
                              </table>
                          </div> <!-- table-wrapper-scroll  -->


                  </div> <!-- container shadow  -->
  
            </div>
                
      </div>

</div>
  

  <script>
      $(document).ready(function($){
          var e=this;

          $('[data-toggle="tooltip"]').tooltip();
         
          $('#contenedor_carga').hide();

          $('#btnejexlsx').on('click', function(){
                 
              var anio = $("#anio").val();
              var mes = $("#mes").val();
              var zona = 'NULL';
              var proc = 'xlsx';
              
              $('#contenedor_carga').show();
              // alert('Boton Ejecutar: '+fecha+';'+hora+';'+rutacli+';'+rutaped);

                $.ajax
                    ({
                        type:'POST',
                        data:{anio:anio,mes:mes,zona:zona,proc:proc} , 
                        url:"paginas/eje_pythonolvidadosxzona.php", 
                        success: function(result){
                          $('#pyalert').show();
                          $('#pyshow').html(result);
                        
                        }
                   
                });

               // Habilito el boton para poder recargar la pagina cuando cierro el Alert
                $('#pyshow').bind('DOMSubtreeModified', function(){
                           $('#aviso').on('click', function(){
                             location.reload();
                          });
                });
                $('#pyshow').bind('DOMSubtreeModified', function(){
                           $('#contenedor_carga').hide();
                });
                            

            });

            $('#btntraezona').on('click', function(){
                 
                 var zona = $("#zona").val();
                 var mes = $("#meszo").val();
                 var anio = $("#aniozo").val();
                 var proc = 'trae';

                 
                 
                 $('#contenedor_carga').show();
                 // alert('Boton Ejecutar: '+fecha+';'+hora+';'+rutacli+';'+rutaped);
   
                   $.ajax
                       ({
                           type:'POST',
                           data:{anio:anio,mes:mes,zona:zona,proc:proc} , 
                           url:"paginas/eje_pythonolvidadosxzona.php", 
                           success: function(result){
                             $('#pyalert').show();
                             $('#pyshow1').html(result);
                           
                           }
                      
                   });
   
                  // Habilito el boton para poder recargar la pagina cuando cierro el Alert
                   $('#pyshow1').bind('DOMSubtreeModified', function(){
                              $('#aviso').on('click', function(){
                                location.reload();
                             });
                   });
                   $('#pyshow1').bind('DOMSubtreeModified', function(){
                              $('#contenedor_carga').hide();
                   });
                               
   
               });

            

            $("#uploadForm").on('submit', function(e){
            e.preventDefault();
            $.ajax({
                type: 'POST',
                url: 'uploadolvidados.php',
                data: new FormData(this),
                contentType: false,
                cache: false,
                processData:false,
                beforeSend: function(){
                    $('#uploadStatus').html('<img src="images/uploading.gif"/>');
                },
                error:function(){
                    $('#uploadStatus').html('<span style="color:#051D99;">Subir archivos al sitio falló trate nuevamente.<span>');
                },
                success: function(data){
                    $('#uploadForm')[0].reset();
                    $('#uploadStatus').html('<span style="color:#051D99;">Archivos subidos correctamente.<span>');
                    
                }
            });
        });

       
        
        // Validacion del tipo de archivos para que solo pueda subir CSVs
        $("#fileInput").change(function(){
            var fileLength = this.files.length;
            var match= ["text/csv","text/plain","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
            var i;
            for(i = 0; i < fileLength; i++){ 
                var file = this.files[i];
                var archivocsv = file.type;
               
                if(!((archivocsv==match[0]) || (archivocsv==match[1]) || (archivocsv==match[2]) || (archivocsv==match[3]))){
                    alert('Por favor elija un archivo CSV válido (CSV).'+ archivocsv);
                    $("#fileInput").val('');
                    return false;
                }
            }
        });

        

           

      })

      function ver(){
         
          result = document.getElementById('file1').value;
          nombrearchivo = result.substr(12,50);
          alert(nombrearchivo);
          $('#muestraarchivo').html(nombrearchivo);
      }

     


  </script>

   
   
      
    <!-- Bootstrap JavaScript Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
  </body>
</html>