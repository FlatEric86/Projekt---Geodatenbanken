import PY_lib, os, shutil

DATA = os.listdir('C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/upload')
for fname in DATA:
    if fname.endswith('.txt'):
        txt_file_name = fname
        with open('C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/upload/' + fname) as fin:
            data = fin.readline().split('$$token$$')
    else:
        name     = fname.split('.')[0]
        img_name = fname


text_, lat, lon = data

lat = float(lat.replace(',', '.'))
lon = float(lon.replace(',', '.'))




sql_api_obj = PY_lib.PY_SQL_API()


# Prüfe ob alle Bedingungen zum einfügen in die Datenbank erfüllt sind
# ansonsten gib Fehler zurück an PHP skript



if sql_api_obj.is_to_near_or_equal_or_not_in_area(lat, lon, name) == False:
    sql_api_obj.insert_into_db((name, lat, lon, img_name, text_))

else:
    print(sql_api_obj.is_to_near_or_equal_or_not_in_area(lat, lon, name))


# Verschiebe die Bildatei in das Bildverzeichnis
temp_file = 'C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/upload/' + img_name
dest_path = 'C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/Bilder/' + img_name
shutil.move(temp_file, dest_path)

# lösche Datendatei aus dem uploadverzeichnis

os.remove('C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/upload/' + txt_file_name)