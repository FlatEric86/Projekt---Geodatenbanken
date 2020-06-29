import numpy as np
import utm
import mysql.connector

class PY_SQL_API:
    '''
    Die Klasse definiert die nötige Python-SQL-API zur Dateneingabe und Ausgabe
    in bzw. aus der SQL-Datenbank. Sie ist sehr hart programmiert was bestimmte
    Parameterwerte wie Datenbankenverbindungsparameter etc. angeht, da sich 
    diese weder in der Laufzeit noch wärend des gesamten Projektbestandes 
    ändern werden.
    '''

    def __init__(self):
        self.db = mysql.connector.connect(
        host='localhost',
        user='sql_api',
        password='db_koet_',
        database='koethen'
        )



    def is_to_near_or_equal_or_not_in_area(self, lat, lon, name):
        '''
        Die Methode prüft, ob die neue Sehenswürdigkeit bereits in der 
        Datenbank existiert. Das passiert sowohl über den Namen als auch 
        über die Koordinate. Wobei nicht auf Äquivalenz der Koordinate 
        sondern auf die Nähe geprüft wird. Zudem wird geprüft, ob sich
        die Sehenswürdigkeit außerhalb des validen Kartenbereichs befindet.
        Dieser Wurde als ein Radium um die Kirch nahe der Kartenmitte von
        0.005347 Koordinateneinheiten definiert.
        Eine weitere Abfrage prüft, ob der Name schon in der Datenbank 
        existiert.
        '''
        gps = np.array([lat, lon])

        # frage ab ob Koordinate im nicht erlaubeten Kartenbereich ist.
        # Wenn ja gib entsprechenden Fehler zurück.
        if np.linalg.norm(gps - np.array([51.751371, 11.973681])) > 0.005347:
            return 'err_not_in_area'

         
        table = self.get_table_from_db_as_list()
        for row in table:  
            gps_ref = np.array([row[1], row[2]])

            # frage ob der Name der Sehenswürdigkeit schon in der Datenbank 
            # existiert. Gib entsprechenden Fehlercode aus wenn wahr.
            if name == row[0]:
                return 'err_equal_data'
                 

            # frage ob die Sehenswürdigkeit zu nah an einer anderen befindet
            # Invalider Radius beträgt dabei 0.00008 Ordinateneinheiten
            if np.linalg.norm(gps - gps_ref) <= 0.00008:
                return 'err_equal_data'

        return False
             



    def insert_into_db(self, vals):
        '''
        Die Methode übergibt die ihr übergebenen Werte einer neuen
        Tabellenzeile an die Tabelle sehenswuerdigkeiten der Datenbank.
        '''

        dbcursor = self.db.cursor(buffered=True)
        sql_cmd  = "INSERT INTO items (name, lat, lon, img_names,\
                   text_info) VALUES (%s, %s, %s, %s, %s)"                     

        dbcursor.execute(sql_cmd, vals)
        self.db.commit()
        del dbcursor
        

    def get_table_from_db_as_list(self):
        '''
        Die Methode ruft die gesamte Tabelle <items> auf und gibt
        sie als list-Objekt zurück
        '''
        dbcursor = self.db.cursor(buffered=True)
        dbcursor.execute("select * from items")

        table = [list(item) for item in dbcursor.fetchall()]
        del dbcursor

        return table



    def get_number_of_rows(self):
        '''
        Die Methode gibt die Anzahl an Spaltes der Tabelle zurück
        '''
        return len(self.get_table_from_db_as_list())



    def get_row_by_name(self, name):
        '''
        Die Methode ruft die Zeile der Tabelle definiert durch den Namen
        der Sehenswürdigkeit ab und gibt die Zeile als list-Objekt zurücl
        '''
        dbcursor = self.db.cursor(buffered=True)
        dbcursor.execute("select * from items where name = "
                        + "'" 
                        + name 
                        + "'"
        )

        table = [item for item in dbcursor.fetchall()[0]]

        del dbcursor
        return table



    def del_row_by_name(self, name):
        '''
        Methode zum entfernen von Sehenswürdigkeiten aus der Datenbank
        '''
        dbcursor = self.db.cursor()
        sql = "delete from sehenswuerdigkeiten where name = " + "'" + name + "'" 
        dbcursor.execute(sql)
        self.db.commit()

        del dbcursor



# debug_obj = PY_SQL_API()
# print(debug_obj.get_row_by_name('bla'))




def error(model_val, true_val):
    '''
    Erechnet den Fehler zwischen modelliertem Punkt und dem wahren Punkt
    auf basis der Norm des Richtungsvektors beider Punkte -> Abstandsnorm
    zwischen den beiden Punkten
    '''
    return np.linalg.norm(true_val - model_val)


def get_lamda_mu_and_opt_ref_point():
    '''
    Funktion zur Schätzung der beiden Skalare lambda und mue, sowie
    dem optimalen Referenzpunkt aus den Kalibrierungsdaten.
    ''' 
    X_UTM = []
    X_PXL = []

    # Lade die Kalibrierungsdaten und trenne sie auf in UTM-Koordinate
    # und Pixel-Koordinate. Konvertiere sie von string auf float und packe 
    # sie jeweils in die entsprechenden Listen X_UTM und X_PXL
    with open('C:/Users/Alex/XAMPP/htdocs/geodatenbanken_projekt/skripte/coord_transf.dat', 'r') as fin:
        i = 0
        for line in fin.readlines():
            # überspringe Datei-Header
            if i == 0:
                i += 1
                continue
            else:
                line = line.strip('\n').split(';')
                X_UTM.append(np.array([float(line[0])
                                      , float(line[1])])
                            )
                X_PXL.append(np.array([float(line[2])
                                      , float(line[3])])
                            )
                
         
    LAM = []
    MU  = []
    
    # iteriere über alle möglichen Punkt zu Punkt Beziehungen und 
    # berechne den lambda- sowie mue-Wert
    for i in range(len(X_UTM)):
        for j in range(len(X_UTM)):
            # überspringe den Fall wenn zwei Punkte identisch sind
            if i == j:
                continue
            else:
                delta_pxl_x = abs(X_PXL[i][0] - X_PXL[j][0])
                delta_utm_x = abs(X_UTM[i][0] - X_UTM[j][0])
                
                lam = delta_pxl_x / delta_utm_x
                         
                delta_pxl_y = abs(X_PXL[i][1] - X_PXL[j][1])
                delta_utm_y = abs(X_UTM[i][1] - X_UTM[j][1])
                
                mu = delta_pxl_y / delta_utm_y
     
                LAM.append(lam)
                MU.append(mu)
     
    lam = np.mean(LAM)
    mu  = np.mean(MU)
    
    
    
    # bereche optimalen Referenzpunkt 
    # Referenzpunkt ist dann optimal, wenn die Summe aller
    # quadrierten Fehler kleinstmöglich ist
    # Der Fehler ist der Abstand zwischen modellierten transformierten Punkt
    # und dem korrespondierenden Punkt aus der Kalibrierungsdatei
    
    tensor = np.array([[lam, 0], [0, -mu]])
    
    ERR = []
    for i in range(len(X_PXL)):
        err = []
        for j in range(len(X_PXL)):
            if i == j:
                continue
            else:
            
                shift_vec  = X_UTM[j] - X_UTM[i]
                ref_transf = X_PXL[i]
                
                model_point = np.dot(tensor, shift_vec) + ref_transf
                
                mod_err = error(model_point, X_PXL[j])
                
                # print(80*'~')
                # print('Modell: ', model_point)
                # print('Wahrer: ', X_PXL[j])
                # print(mod_err)
                
                err.append(mod_err**2)
                
        ERR.append(sum(err))
                
                
    # die berechneten optimalen Referenzpunkte            
    ref_x_pxl = X_PXL[ERR.index(min(ERR))]   
    ref_x_utm = X_UTM[ERR.index(min(ERR))]
                

    return tensor, ref_x_utm, ref_x_pxl
   
 
def UTM_to_PXL(x_utm):
    '''
    Funktion zum Transformieren der UTM-Koordinaten in Pixel-Koordinaten
    '''    
    lam_mu_tensor, ref_x_utm, ref_x_pxl = get_lamda_mu_and_opt_ref_point()   

    vec = np.dot(lam_mu_tensor, (x_utm - ref_x_utm)) + ref_x_pxl

    return int(round(vec[0])), int(round(vec[1]))
    
    

def GPS_to_PXL(lat, lon):
    '''
    Funktion zum Transformieren der GPS-Koordinaten in Pixel-Koordinaten,
    auf Basis der Funktion UTM_to_PXL(). 
    '''
 
    x = utm.from_latlon(lat, lon)[0]
    y = utm.from_latlon(lat, lon)[1]
    
    x_vec = np.array([x, y])
    
    return UTM_to_PXL(x_vec)
    
    
    