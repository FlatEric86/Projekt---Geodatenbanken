<html>
    <meta charset="UTF-8">
    <header><title>Sehenswürdigkeiten</title></header>
<body>
<?php

$target_dir = "C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/upload/";
$target_file = $target_dir . basename($_FILES["fileToUpload"]["name"]);

// verschiebe die Bilddatei aus dem Temporärverzeichnis in das Uploadverzeichnis
move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file);

$text_beschr = $_POST["info_text"];
$latitude    = $_POST["latitude"];
$longitude   = $_POST["longitude"];


// schreibe die Textinformatione sowie die GPS-Koordinate in eine Textdatei
$fp = fopen('C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/upload/data.txt', 'w');
fwrite($fp, $text_beschr.'$$token$$');
fwrite($fp, $latitude.'$$token$$');
fwrite($fp, $longitude);
fclose($fp);



// rufe Python-Skript auf, welches die Daten in die Datenbank schreibt

$py_cmd = "py C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/skripte/do_files_into_database.py";
$err_code = exec($py_cmd);


if ($err_code == "err_equal_data") {
    echo 'Diese Sehenswuerdigkeit befindet sich vermutlich schon in der Datenbank.';
}

if ($err_code == "err_not_in_area") {
    echo 'Die Sehenswürdigkeit befindet sich außerhalb des Bereiches oder die GPS-Koordinaten sind falsch.';
}

echo "<br/> Bitte schließen Sie diese Seite. Sofern kein Fehler aufgetreten ist, sollte alles im System eingetragen wurden sein."

?>

</body>
</html>
