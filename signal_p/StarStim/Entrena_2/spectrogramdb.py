# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Julián Sibaja García,
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
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn import decomposition
from sklearn import svm

def getDataFromDB(id_s):
    mat_contents = sio.loadmat(id_s)
    conc = mat_contents['conc']
    rel = mat_contents['rel']
    conc = np.transpose(conc, (2, 1, 0))
    rel = np.transpose(rel, (2, 1, 0))
    data_time = np.zeros((len(conc)*2,len(conc[0]),len(conc[0][0])))
    data_time[0:len(conc)] = conc
    data_time[len(conc)::] = rel          
    return data_time


def butter_filter(data, lowcut=3, highcut=25, fs=500, order=6): # Filter
    nyq = 0.5*fs
    high = highcut/nyq
    [b, a] = signal.butter(order, high, btype='low')
    y = signal.lfilter(b, a, data)
    return y

def removeDC(data):
    ndata = np.zeros(np.shape(data))
    mean_v = np.mean(data, axis=2)
    for trial in range(0, len(data)):
        for electrode in range(0, len(data[trial])):
            # Señal original -  señal DC
            v_trial = (data[trial][electrode] - mean_v[trial][electrode])
            ndata[trial][electrode] = v_trial # guardamos señal sin DC
    return ndata

def downSampling(data, sc, Fs):
    if int(Fs % 2):
        sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc+1))
    else:
        sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc))

    for trial in range(0, len(data)):
        for electrode in range(0, len(data[trial])):
            sub_signals[trial][electrode] = data[trial][electrode][::sc]
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

id_s = raw_input("[!] Digite el identificador del sujeto: ")

datac = getDataFromDB(id_s)
data = removeDC(datac)
Y=butter_filter(data)
scale= 10
Fs = 500/scale # esto es porque fue submuestreado a 2
sub_signals = downSampling(Y,int(scale),Fs)

ts = 1.0/Fs
time = np.arange(0,len(data[0][0]) * ts,ts)
f, t, S = signal.spectrogram(sub_signals, fs=Fs)
ff = sub_signals.shape # Tamaño del array
m_f = np.mean(S, axis = 3) # Potencia promedio para cada frecuencia
feat = np.reshape(m_f, (ff[0]*ff[1],m_f.shape[2]))
label = np.zeros((ff[0]*ff[1]))
label[0:len(label)/2] = 1
label[len(label)/2::] = 2

"""
Clasificación 
"""      
min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(feat)

"""
pca = decomposition.PCA(n_components=len(feat))
pca.fit(feat)
V = pca.components_
"""
clf = clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, X_train_minmax, label, cv=10)
scores.mean()
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

