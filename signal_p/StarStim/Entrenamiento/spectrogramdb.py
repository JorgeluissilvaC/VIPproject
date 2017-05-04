# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author:Julián Sibaja García, 
        Karolay Ardila Salazar,
        Dayán Mendez Vasquez,
        Jorge Silva Correa,

Tipos de prueba:
  r - relajación 
  mrh - mover la mano derecha
  mlh - mover la mano izquierda
  mou - mover objeto hacia arriba
  mod - mover objeto hacia abajo

"""
from scipy import signal
import numpy as np
import copy
import mysql.connector

def getDataFromDB(id_s, test_type):
    """Get all the trials of some subject(id_s) of some test(type_test)
    Input Arguments
        id_s: Subject identifier
        test_type: The type o test, it can be:
            r   - Relaxation
            mrh - Move right arm
            mlh - Move left arm
            mou - Move object up
            mod - Move object down
    Output
        [e1,e2,e3,e4,e5,e6,e7,e8]: List of list of electrode values with the structure:
        electrode = [[data of trial 0],[data of trial 1],...,[data of trial N]]
        
    For examle if you call data = getDataFromDB(id_s, test_type)
    and you try to get data[i][j], then you will get the data for the i electrode
    and the j trial.
    """
    print("Hola mama")
    cnx = mysql.connector.connect(user =     'root', 
                                  password = 'uniatlantico',
                                  host =     'vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                  database = 'vipdb')
    print("Hola mama2")
    cursor = cnx.cursor()
    cursor.execute("select n_trial,e1,e2,e3,e4,e5,e6,e7,e8 from "+"s_"+id_s+" WHERE (test_type = "+str(test_type)+")")
    #cursor.execute("SELECT n_trial,e1,e2,e3,e4,e5,e6,e7,e8 FROM vipdb.s_dayanST WHERE (test_type = 'mrh')")
    data = np.array(cursor.fetchall())
       # NB : you won't get an IntegrityError when reading    
    #for row in cursor:
    #    print(row)

    print("Hola mama3")
    cursor.close()
    cnx.close()
    e1 = []
    for i in range(0,int(data[-1][0])+1):
        e1.append([])
    e2 = copy.deepcopy(e1)
    e3 = copy.deepcopy(e1)
    e4 = copy.deepcopy(e1)
    e5 = copy.deepcopy(e1)
    e6 = copy.deepcopy(e1)
    e7 = copy.deepcopy(e1)
    e8 = copy.deepcopy(e1)

    for row in data:
        i = int(row[0])
        e1[i].append(row[1])
        e2[i].append(row[2])
        e3[i].append(row[3])
        e4[i].append(row[4])
        e5[i].append(row[5])
        e6[i].append(row[6])
        e7[i].append(row[7])
        e8[i].append(row[8])

    return [e1,e2,e3,e4,e5,e6,e7,e8]

def saveDataDB(sn_m):
    #conn = sqlite3.connect('database.db') #connection object
    #c = conn.cursor()
    cnx = mysql.connector.connect(user =     'root', 
                                  password = 'uniatlantico',
                                  host =     'vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                  database = 'vipdb')
    cursor = cnx.cursor()
    # Create table   
    add_table = (
            "CREATE TABLE IF NOT EXISTS `c_"+id_s+"` ("
            "  `n_sample` int(11) NOT NULL AUTO_INCREMENT,"
            "  `electrode` int(11) NOT NULL,"
            "  `test_type` int(11) NOT NULL,"
            "  `n_trial` int(11) NOT NULL,"
            "   `e1` REAL NOT NULL,"
            "   `e2` REAL NOT NULL,"
            "   `e3` REAL NOT NULL,"
            "   `e4` REAL NOT NULL,"
            "   `e5` REAL NOT NULL,"
            "   `e6` REAL NOT NULL,"
            "   `e7` REAL NOT NULL,"
            "   `e8` REAL NOT NULL,"
            "  PRIMARY KEY (`n_sample`)"
            ") ENGINE=InnoDB")
    cursor.execute(add_table)
    
    add_data = ("INSERT INTO c_"+id_s+
                "(electrode,test_type,n_trial,e1,e2,e3,e4,e5,e6,e7,e8)"
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)")
    #print sn_m
    cursor.executemany(add_data,sn_m)
    cnx.commit()
    cursor.close()
    cnx.close()
    print "[!]Table 'c_"+id_s+"' added/updated"
    
def butter_filter(data,lowcut = 3, highcut = 13,fs = 500, order = 6): # Filter
    nyq = 0.5*fs
    high = highcut/nyq
    b, a = signal.butter(order, high, btype ='low')
    y = signal.lfilter(b, a, data)
    return y

def removeDC(data):
    for electrode in range(0,len(data)):
        for trial in range(0,len(data[electrode])):

            v_trial = (data[electrode][trial] - np.mean(data[electrode][trial])) # Señal sin media y escalada a voltaje
            data[electrode][trial] = v_trial # Señal filtrada
    return data

def downSampling(data, scale,fs):
    if int(fs % 2):
        sub_signals = np.zeros((len(data), len(data[0]),len(data[0][0])/scale+1))
    else:
        sub_signals = np.zeros((len(data), len(data[0]),len(data[0][0])/scale))
        
    for electrode in range(0,len(data)):
        for trial in range(0,len(data[electrode])):
            sub_signals[electrode][trial] = data[electrode][trial][::scale]
    return sub_signals


test_types = ["r","mrh","mlh","mou","mod"]
id_s = raw_input("[!] Digite el identificador del sujeto: ")
while True:
    test_type = raw_input('''[!] Digite el tipo de experimento: 
  mrh - mover la mano derecha (se guardara con el id = 0 en la BD)
  mlh - mover la mano izquierda (se guardara con el id = 1 en la BD)
  mou - mover objeto hacia arriba (se guardara con el id = 2 en la BD)
  mod - mover objeto hacia abajo (se guardara con el id = 3 en la BD)
  r   - relajación  (se guardara con el id = 4 en la BD)
  => ''')
    
    if not(test_type in test_types):
        print("[X] El identificador no se encuentra, por favor ingrese uno válido")
    else:
        break
if (test_type == "mrh"):
    test_type=0
elif (test_type == "mlh"):
    test_type=1
elif (test_type == "mou"):
    test_type=2
elif (test_type == "mod"):
    test_type=3
elif (test_type == "r"):
    test_type=4
    
data = getDataFromDB(id_s, test_type)
tt=np.linspace(0, len(data[0][0])/500, num=len(data[0][0]))
Y=butter_filter(data[0][0])

scale= 10.0
Fs = 500/scale # esto es porque fue submuestreado a 2
data = removeDC(data)
sub_signals = downSampling(data,int(scale),Fs)

ts = 1.0/Fs
time = np.arange(0,len(data[0][0]) * ts,ts)
f, t, S = signal.spectrogram(sub_signals[0][0], fs=Fs, nperseg=32,nfft=32,noverlap=10)
ff = sub_signals.shape # Tamaño del array
Sxx = np.zeros((ff[0]*ff[1],len(f)+3))
i=0
for electrode in range(0,len(sub_signals)):
    for trial in range(0,len(sub_signals[electrode])):
        x = sub_signals[electrode][trial]
        _, _, S = signal.spectrogram(x, fs=Fs, nperseg=32,nfft=32,noverlap=10)
        Sxx[i,0:3] =[electrode+1,test_type,trial]
        Sxx[i,3::] = np.mean(S,axis=1)
        i+=1

#saveDataDB(Sxx.tolist())