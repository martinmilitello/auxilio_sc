<?php
set_time_limit (5000);

if($_SERVER['REQUEST_METHOD'] == "POST" && isset($_FILES["nombrearchivo"]["type"]))
{
	

	
	$target_file = basename($_FILES["nombrearchivo"]["name"]);
	
	$uploadOk = 1;
	$xlsxFileType = pathinfo($target_file,PATHINFO_EXTENSION);

	// print_r($xlsxFileType); 
    // Check file size
    
	if ($_FILES["nombrearchivo"]["size"] > 67108864) {
		$errors[]= "Lo sentimos, el archivo es demasiado grande.  Tamaño máximo admitido: 0.5 MB";
		$uploadOk = 0;
	}
	// Allow certain file formats
	if((strtoupper($xlsxFileType) != "TXT")) {
		$errors[]= "Lo sentimos, sólo archivos txt son permitidos.";
		$uploadOk = 0;
	}
	// Check if $uploadOk is set to 0 by an error
	if ($uploadOk == 0) {
		$errors[]= "Lo sentimos, tu archivo no fue subido.";
	// if everything is ok, try to upload file
	} else {
		if (move_uploaded_file($_FILES["nombrearchivo"]["tmp_name"], $target_file)) {
		$messages[]= "El Archivo ha sido subido correctamente.";
		
		
		} else {
		$errors[]= "Lo sentimos, hubo un error subiendo el archivo.".$_FILES["nombrearchivo"];
		}
	}

	if (isset($errors)){
		?>
		<div class="alert alert-danger alert-dismissible" role="alert">
	        <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
	        <strong>Error!</strong> 
	
		<?php
		foreach ($errors as $error){
			echo"<p>$error</p>";
		}
		
		?>
		</div>
		<?php
	}

	if (isset($messages)){
		?>
			<div class="alert alert-success alert-dismissible" role="alert">
				<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
				<strong>Aviso!</strong> 
	
		<?php
		foreach ($messages as $message){
			echo"<p>$message</p>";
		}
		// echo $message;
		?>
		</div>

		
		<?php
	}
}
?>