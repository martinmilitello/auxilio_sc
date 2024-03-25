<?php

$output = shell_exec("python ../kk.py");

print_r($output);
 
      
function write_to_console($data) {
  $console = $data;
  if (is_array($console))
  $console = implode(',', $console);
 
  echo "<script>console.log('Console: " . $console . "' );</script>";
 }    
      

?>