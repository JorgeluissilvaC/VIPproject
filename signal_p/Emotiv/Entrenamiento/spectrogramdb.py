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
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import json
import sqlite3
import copy


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
            all - All the tests
    Output
        AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8: List of senor values with the structure:
        sensor = [[data of trial 1],[data of trial 2],...,[data of trial N]]
    """
    conn = sqlite3.connect('database.db') #connection object
    c = conn.cursor()

    if test_type == "all" :
        c.execute('''select * from '''+"s_"+id_s)
    else:
        c.execute('''select n_trial,AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8 from '''+"s_"+id_s+" where (test_type = '"+test_type+"')")
    data = np.array(c.fetchall())
    conn.close()

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

    return AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8

def butter_bandpass_filter(data,lowcut = 0, highcut = 13,fs = 128, order = 6): # Filter
    nyq = 0.5*fs;
    low = lowcut/nyq
    high = highcut/nyq
    b, a = signal.butter(order, [low,high], btype ='band')
    y = signal.lfilter(b, a, data)
    #f, pxx = signal.welch(y, fs)  
    #max_value = np.amax(pxx)
    return y

def diezmado(data, n): # Función para diezmar fs/5
    pass


test_types = ["r","mra","mla","mou","mod"]
id_s = raw_input("[!] Digite el identificador del sujeto: ")
while True:
    test_type = raw_input('''[!] Digite el tipo de experimento: 
  r - relajación 
  mra - mover la mano derecha
  mla - mover la mano izquierda
  mou - mover objeto hacia arriba
  mod - mover objeto hacia abajo
  all - Todos los tipos
  => ''')
    if not(test_type in test_types):
        print("[X] El identificador no se encuentra, por favor ingrese uno válido")
    else:
        break

AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8 = getDataFromDB(id_s, test_type)

print len(AF3[1])

fs = 128.0
ts = 1/fs
time = np.arange(0,len(AF3[0]) * ts,ts)
"""
for key in lst:

  data[key] = (data[key] - np.mean(data[key]))*(0.51*10**-6) # Señal sin media y escalada a voltaje
  data[key] = butter_bandpass_filter(data[key]) # Señal filtrada
  #Data vs time 
  #plt.subplot(211)
  plt.plot(time,data[key])
  plt.ylabel('Sensor value [uV]')
  plt.xlabel('Time [sec]')
  plt.title(key)
  plt.grid()
  #Spectrogram 
  #plt.subplot(212)
  #f, t, Sxx, im = plt.specgram(data[key], NFFT=128, Fs=128,noverlap=100)
  plt.show()
  #savefig(key + '.png', dpi = 300)

"""
print "done"