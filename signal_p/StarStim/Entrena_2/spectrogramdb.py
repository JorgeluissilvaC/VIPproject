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
import scipy.io as sio
import matplotlib.pylab as plt 

def getDataFromDB(id_s):
    mat_contents = sio.loadmat(id_s)
    conc = mat_contents['conc']
    rel = mat_contents['rel']
    conc = np.transpose(conc,(2,0,1))
    rel = np.transpose(rel,(2,0,1))
    return conc,rel

    
def butter_filter(data,lowcut = 3, highcut = 25,fs = 500, order = 6): # Filter
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

def artifactRegression(data,reference):
    reference = np.transpose(np.matrix(reference))
    data = np.transpose(np.matrix(data))
    op1 = (np.transpose(reference)*reference)/int(reference.shape[0]-1)
    op2 = (np.transpose(reference)*data)/int(data.shape[0]-1)
    coeff,_,_,_=np.linalg.lstsq(op1,op2)
    data = data - reference*coeff
    data = np.transpose(data)
    return data


test_types = ["r","mrh","mlh","mou","mod"]
id_s = raw_input("[!] Digite el identificador del sujeto: ")

[datac, datar] = getDataFromDB(id_s)
# np.transpose(datac,(0,2,1)) #transponer el array
#tt=np.linspace(0, len(data[0][0])/500, num=len(data[0][0]))
Y=butter_filter(datac)
scale= 10
Fs = 500/scale # esto es porque fue submuestreado a 2

#
#data = removeDC(data)
#data = butter_filter(data)
#data_temp = np.zeros((len(data),len(data[0]),500*4))
#for electrode in range(0,len(data)):
#    for trial in range(0,len(data[0])):
#        data_temp[electrode][trial] = data[electrode][trial][1000:3000]
#
#data = data_temp
#"""
#tmpRef = np.zeros((2,len(data[0][0])))
#data_s = np.zeros((2,len(data[0][0])))
#tmp_data=np.zeros((2,len(data[0]),len(data[0][0])))
#for trial in range(0,len(data[0])):
#    tmpRef[0] = data[0][trial]
#    tmpRef[1] = data[1][trial]
#    data_s[0] = data[4][trial]
#    data_s[1] = data[5][trial]
#    tmp_data[:,trial,:] = artifactRegression(data_s,tmpRef)
#    
##sub_signals = downSampling(tmp_data,int(scale),Fs)
#"""
#sub_signals = downSampling(data,int(scale),Fs)
#
#ts = 1.0/Fs
#time = np.arange(0,len(data[0][0]) * ts,ts)
#f, t, S = signal.spectrogram(sub_signals[0][0], fs=Fs, nperseg=32,nfft=32,noverlap=10)
#ff = sub_signals.shape # Tamaño del array
#Sxx = np.zeros((ff[0]*ff[1],len(f)+3))
#i=0
#for electrode in range(0,len(sub_signals)):
#    for trial in range(0,len(sub_signals[electrode])):
#        x = sub_signals[electrode][trial]
#        _, _, S = signal.spectrogram(x, fs=Fs, nperseg=32,nfft=32,noverlap=10)
#        Sxx[i,0:3] =[electrode+1,test_type,trial]
#        Sxx[i,3::] = np.mean(S,axis=1)
#        i+=1
#
#saveDataDB(Sxx.tolist())