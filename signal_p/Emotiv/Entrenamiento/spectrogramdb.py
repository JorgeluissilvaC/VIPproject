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
    Output
        [AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8]: List of list of electrode values with the structure:
        electrode = [[data of trial 0],[data of trial 1],...,[data of trial N]]
        
    For examle if you call data = getDataFromDB(id_s, test_type)
    and you try to get data[i][j], then you will get the data for the i electrode
    and the j trial.
    """
    conn = sqlite3.connect('database.db') #connection object
    c = conn.cursor()
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

    return [AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8]


def butter_filter(data,lowcut = 0, highcut = 13,fs = 128, order = 6): # Filter
    nyq = 0.5*fs;
    low = lowcut/nyq
    high = highcut/nyq
    b, a = signal.butter(order, [low,high], btype ='band')
    y = signal.lfilter(b, a, data)
    #f, pxx = signal.welch(y, fs)  
    #max_value = np.amax(pxx)
    return y

def removeDC(data):
    for electrode in range(0,len(data)):
        for trial in range(0,len(data[electrode])):

            v_trial = (data[electrode][trial] - np.mean(data[electrode][trial]))*(0.51*10**-6) # Señal sin media y escalada a voltaje
            data[electrode][trial] = butter_filter(v_trial) # Señal filtrada
    return data

def downSampling(data, scale):
    sub_signals = np.zeros((len(data), len(data[0]),len(data[0][0])/2))

    for electrode in range(0,len(data)):
        for trial in range(0,len(data[electrode])):
            sub_signals[electrode][trial] = data[electrode][trial][::scale]
    return sub_signals


test_types = ["r","mra","mla","mou","mod"]
id_s = raw_input("[!] Digite el identificador del sujeto: ")
while True:
    test_type = raw_input('''[!] Digite el tipo de experimento: 
  r - relajación 
  mra - mover la mano derecha
  mla - mover la mano izquierda
  mou - mover objeto hacia arriba
  mod - mover objeto hacia abajo
  => ''')
    if not(test_type in test_types):
        print("[X] El identificador no se encuentra, por favor ingrese uno válido")
    else:
        break

data = getDataFromDB(id_s, test_type)
data = removeDC(data)
sub_signals = downSampling(data,2)

Fs = 128.0/2 # esto es porque fue submuestreado a 2
ts = 1/Fs
time = np.arange(0,len(data[0][0]) * ts,ts)
S, f, t, _ = plt.specgram(sub_signals[0][0], NFFT=int(Fs), Fs=Fs, noverlap=int(Fs/2))
print len(S)
print "longitud de t: "+str(len(t))
print t
print "longitud de f: "+str(len(f))
print f
print len()
Sxx = np.zeros((len(sub_signals), len(sub_signals[0]),len(S[1])))


for electrode in range(0,len(sub_signals)):
    for trial in range(0,len(sub_signals[electrode])):
        x = sub_signals[electrode][trial]
        #print(Sxx)
        S, _, _, _ = plt.specgram(sub_signals[0][0], NFFT=int(Fs), Fs=Fs, noverlap=int(Fs/2))
        Sxx[electrode][trial]= S[1]


#print len(Sxx[0][0])
#print Sxx[0][0]

print "done"

