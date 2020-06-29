<html>
    <meta charset="UTF-8">
    <header><title>Sehenswürdigkeiten</title></header>
<body>
    <h1 style="font-size:28px">Sehenswürdigkeiten im Stadtkern von Köthen</h1>
    <div>
        <p>
            <!--
            Kopf der Seite mit Informationen über die Seite. Der Text endet mit 
            dynamischen Inhalt bzgl der Anzahl bisher eingetragenen Sehenswürdigkeiten
            -->
            In der folgenden Karte können Sie bereits hinzugefügte Sehesenwürdigkeiten
            im Stadtkern der Stadt Köthen finden und Information zu diesen
            Sehenswürdigkiten abrufen.<br>
            Klicken Sie dazu einfach auf eines der schwarzen runden Icons.<br>
            Wenn Sie selber eine Sehenswürdigkeit hinzufügen wollen, 
            nutzen Sie bitte das Formular unter der Karte.<br>
            <?php
                // ruf Python-Skript <get_number_of_rows.py> auf und lasse die Anzahl an Sehenswürdigkeiten
                // zurückgeben. Füge diese als Textinformation in das HTML-Document ein
                $N_rows_cmd = ("py C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/skripte/get_number_of_rows.py");
                $N_rows = exec($N_rows_cmd);
                echo "Derzeit wurden $N_rows Sehenswürdigketen in das System eingetragen.";

            ?>
        </p>
    </div>
    <div class="testdiv">
        <figure id="map">
            <svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1169 826" >              
                <image width="1169" height="826" xlink:href="/geodatenbanken_projekt/Karte/stadtkern_koethen_map.png"></image> 
                    <?php
                    try {
                        $db = new PDO("mysql:host=localhost; dbname=koethen; charset=UTF8", "sql_api", "db_koet_");
                        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                        $sql = "SELECT * from items";

                        // iteriere über die Tabelle <items> der Sehenswürdigkeiten und erzeuge die HTML-Links
                        foreach($db->query($sql) as $row) {
                            // hole die Pixelkoordinaten des zur Iteration aktuellen Hyperlinks per Aufruf des Python-Skripts <gps_to_pxl_transf.py>
                            // übergebe dazu die GPS-Koordinaten an das Python-Skript
                            $ext_py_get_pxl_coods = escapeshellcmd("py C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/skripte/gps_to_pxl_transf.py $row[1] $row[2]");
                            $pxl_coords = explode(";", exec($ext_py_get_pxl_coods));
                            // echo $pxl_coords[0];
                            // echo $pxl_coords[1];

                            // generiere aktuelles HTML-sub zur aktuellen Iteration
                            echo'<a xlink:href="sub_html/'.$row[0].'.html"><circle cx="'.$pxl_coords[0].'" cy="'.$pxl_coords[1].'" r="7" color="red" opacity="0.8" /></a>';



                            // generiere die aktuelle Seite der Sehenswürdigkeit
                            $py_cmd = "py C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/skripte/make_sub_site.py $row[0] ";
                            exec($py_cmd);

                        }
                    }   catch (PDOException $e) {
                        echo "Fehler bei der Datenbankenverbindung: ".$e->getMessage(); 
                    }
                    ?>
            </svg>
        </figure>                   
    <div>
        <p>
            Sie können gerne eigene Sehenswürdigkeiten hochladen.<br>
            Bitte nutzen Sie dazu das folgende Formular.<br>
            Beachten Sie, dass nur Sehenswürdigkeiten im Stadkern von Köthen erlaubt sind.<br>
            Es muss die GPS-Koordinate in Dezimalform, sowie ein Bild und eine kurze Beschreibung hochgeladen werden.<br>
        </p>
    </div>
    <div>
        <!-- Unterer Teil der Seite bestehend aus dem Datenübertragungsformular -->
        <form action="/geodatenbanken_projekt/skripte/file_upload.php" method="post" enctype="multipart/form-data">
            <p>
                Bitte wählen Sie genau ein Bild der Sehenswürdigkeit, welches Sie hochladen wollen.
            </p>
            <input type="file" name="fileToUpload" id="fileToUpload"><br/><br/>
            <p>
                Geben Sie hier die GPS-Koordinaten ein.
            </p>
            <label for="latitude">
                Latitude: 
                <input id="latitude" type="text" name="latitude">
            </label>
            <label for="longitude">
                Longitude: 
                <input id="longitude" type="text" name="longitude">
            </label>
            <br/><br/><p>
                Geben Sie hier eine textliche Beschreibung ein.<br> Am besten schreiben Sie diese in einem Editor und kopieren diese anschließend hier herein.
            </p>
            <label for="info_text">
                Text: 
                <input id="info_text" type="text" name="info_text">
            </label>
            <br/><br/><p>
                Bitte senden Sie die Daten ab.
            </p>
            <input type="Submit" value="Absenden" />
        </form>
    </div>
</body>
</html>