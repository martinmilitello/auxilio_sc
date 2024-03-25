<?php

/*
--------------------------------------------------------------------------------------------
|                          Ch4rl1X Desarrollo de aplicaciones web y móviles                |
|                                                                                          |
|                                  correo: charly@charlesweb.com.ar                        |
|                                     web: www.charlesweb.com.ar                           |
|                                                                                          |
| Este material es apto para ser difundido y compartido. Utilizalo bajo tu responsabilidad.|
--------------------------------------------------------------------------------------------
*/

$token = "f5zfd784-aa5z-45f7-a0e8-95165e4z0189_13145";
//Leo la URL desde tiendas y listo la lista de precios 1
$ch = curl_init('https://tiendas.axoft.com/api/Aperture/Price?pageSize=500&pageNumber=1&filter=1');



//$data_string = json_encode(array("Status"=>$status));

/*
IMPORTANTES LÍNEAS PARA DESACTIVAR EL USO DE CERTIFICADOS DEL SERVER
Desactivar el uso de certificados online en el server local*/
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
/*Desactivar el uso de certificados online en el server local*/


curl_setopt($ch, CURLOPT_POST, true);

curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");

/*Variable para el PUT*/
//curl_setopt($ch, CURLOPT_POSTFIELDS, array("Status"=>$_POST['Status']));

curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

//Generación del encabezado
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
   'Content-Type: application/json',
   'Expect:',
   'Content-Length: 0',
   'Authorization: Bearer ' . $token,
   'accesstoken: dez058cf-fz77-4f08-a068-772646z3af23_12542'
   ));

curl_setopt($ch, CURLOPT_VERBOSE, true);

$verbose = fopen('log_curl.txt', 'w+');
curl_setopt($ch, CURLOPT_STDERR, $verbose);

//Ejecución del curl
$data = curl_exec($ch);

//Devuelve la información del curl como HTTMP
$info = curl_getinfo($ch, CURLINFO_HTTP_CODE);

$data2 = json_decode($data, true);

/*Imprimo los registros*/
print_r($data2);

/*Cerramos la función predefinida de CURL*/
curl_close($ch);




?>