# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author:Julián Sibaja García, 
        Karolay Ardila Salazar,
        Dayán Mendez Vasquez,
        Jorge Silva Correa,

Tipos de prueba:
  r - relajación 
  mra - mover la mano derecha
  mla - mover la mano izquierda
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
            mra - Move right arm
            mla - Move left arm
            mou - Move object up
            mod - Move object down
    Output
        [AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8]: List of list of electrode values with the structure:
        electrode = [[data of trial 0],[data of trial 1],...,[data of trial N]]
        
    For examle if you call data = getDataFromDB(id_s, test_type)
    and you try to get data[i][j], then you will get the data for the i electrode
    and the j trial.
    """
    cnx = mysql.connector.connect(user =     'root', 
                                  password = 'uniatlantico',
                                  host =     'vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                  database = 'vipdb')
    cursor = cnx.cursor()
    cursor.execute('''select n_trial,AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8 from '''+"s_"+id_s+" where (test_type = '"+test_type+"')")
    data = np.array(cursor.fetchall())
    cursor.close()
    cnx.close()

    AF3 = []
    for i in range(0,int(data[-1][0])+1):
        AF3.append([])
    AF4 = copy.deepcopy(AF3)
    F3 = copy.deepcopy(AF3)
    F4 = copy.deepcopy(AF3)
    F7 = copy.deepcopy(AF3)
    F8 = copy.deepcopy(AF3)
    FC5 = copy.deepcopy(AF3)
    FC6 = copy.deepcopy(AF3)
    T7 = copy.deepcopy(AF3)
    T8 = copy.deepcopy(AF3)
    P7 = copy.deepcopy(AF3)
    P8 = copy.deepcopy(AF3)

    for row in data:
        i = int(row[0])
        AF3[i].append(row[1])
        AF4[i].append(row[2])
        F3[i].append(row[3])
        F4[i].append(row[4])
        F7[i].append(row[5])
        F8[i].append(row[6])
        FC5[i].append(row[7])
        FC6[i].append(row[8])
        T7[i].append(row[9])
        T8[i].append(row[10])
        P7[i].append(row[11])
        P8[i].append(row[12])

    return [AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8]

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
            "   `F0` REAL NOT NULL,"
            "   `F08` REAL NOT NULL,"
            "   `F16` REAL NOT NULL,"
            "   `F24` REAL NOT NULL,"
            "   `F32` REAL NOT NULL,"
            "   `F4` REAL NOT NULL,"
            "   `F48` REAL NOT NULL,"
            "   `F56` REAL NOT NULL,"
            "   `F64` REAL NOT NULL,"
            "   `F72` REAL NOT NULL,"
            "   `F8` REAL NOT NULL,"
            "   `F88` REAL NOT NULL,"
            "   `F96` REAL NOT NULL,"
            "   `F104` REAL NOT NULL,"
            "   `F112` REAL NOT NULL,"
            "   `F12` REAL NOT NULL,"
            "   `F128` REAL NOT NULL,"
            "  PRIMARY KEY (`n_sample`)"
            ") ENGINE=InnoDB")
    cursor.execute(add_table)
    
    add_data = ("INSERT INTO c_"+id_s+
                "(electrode,test_type,n_trial,F0,F08,F16,F24,F32,F4,F48,F56,F64,F72,F8,F88,F96,F104,F112,F12,F128)"
                "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    #print sn_m
    cursor.executemany(add_data,sn_m)
    cnx.commit()
    cursor.close()
    cnx.close()
    print "[!]Table 'c_"+id_s+"' added/updated"
    
def butter_filter(data,lowcut = 3, highcut = 13,fs = 128, order = 6): # Filter
    nyq = 0.5*fs
    high = highcut/nyq
    b, a = signal.butter(order, high, btype ='low')
    y = signal.lfilter(b, a, data)
    return y

def removeDC(data):
    for electrode in range(0,len(data)):
        for trial in range(0,len(data[electrode])):

            v_trial = (data[electrode][trial] - np.mean(data[electrode][trial]))*(0.51*10**-6) # Señal sin media y escalada a voltaje
            data[electrode][trial] = butter_filter(v_trial) # Señal filtrada
    return data

def downSampling(data, scale):
    if (scale % 2):
        sub_signals = np.zeros((len(data), len(data[0]),len(data[0][0])/scale+1))
    else:
        sub_signals = np.zeros((len(data), len(data[0]),len(data[0][0])/scale))
        
    for electrode in range(0,len(data)):
        for trial in range(0,len(data[electrode])):
            sub_signals[electrode][trial] = data[electrode][trial][::scale]
    return sub_signals


test_types = ["r","mra","mla","mou","mod"]
id_s = raw_input("[!] Digite el identificador del sujeto: ")
while True:
    test_type = raw_input('''[!] Digite el tipo de experimento: 
  mra - mover la mano derecha (se guardara con el id = 0 en la BD)
  mla - mover la mano izquierda (se guardara con el id = 1 en la BD)
  mou - mover objeto hacia arriba (se guardara con el id = 2 en la BD)
  mod - mover objeto hacia abajo (se guardara con el id = 3 en la BD)
  r   - relajación  (se guardara con el id = 4 en la BD)
  => ''')
    if not(test_type in test_types):
        print("[X] El identificador no se encuentra, por favor ingrese uno válido")
    else:
        break

data = getDataFromDB(id_s, test_type)
tt=np.linspace(0, len(data[0][0])/128, num=len(data[0][0]))
Y=butter_filter(data[0][0])

if (test_type == "mra"):
    test_type=0
elif (test_type == "mla"):
    test_type=1
elif (test_type == "mou"):
    test_type=2
elif (test_type == "mod"):
    test_type=3
elif (test_type == "r"):
    test_type=4

data = removeDC(data)
sub_signals = downSampling(data,5)

Fs = 128.0/5 # esto es porque fue submuestreado a 2
ts = 1/Fs
time = np.arange(0,len(data[0][0]) * ts,ts)
f, t, S = signal.spectrogram(sub_signals[0][0], fs=Fs, nperseg=32,nfft=32,noverlap=10)
ff = sub_signals.shape # Tamaño del array
Sxx = np.zeros((ff[0]*ff[1],len(f)+3))
i=0
for electrode in range(0,len(sub_signals)):
    for trial in range(0,len(sub_signals[electrode])):
        x = sub_signals[electrode][trial]
        _, _, S = signal.spectrogram(x, fs=Fs, nperseg=32,nfft=32,noverlap=10)
        Sxx[i,0:3] =[electrode,test_type,trial]
        Sxx[i,3::] = np.mean(S,axis=1)
        i+=1

#saveDataDB(Sxx.tolist())