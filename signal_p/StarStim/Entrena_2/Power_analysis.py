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
import scipy.io as sio
import numpy as np
import matplotlib.pylab as plt
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
#from sklearn import decomposition
from sklearn import svm
from sklearn.metrics import confusion_matrix


def get_data_db(id_s):
    """importa los datos del dataset(.mat).
    """
    mat_contents = sio.loadmat(id_s)
    conc = mat_contents['conc']
    rel = mat_contents['rel']
    conc = np.transpose(conc, (2, 1, 0))
    rel = np.transpose(rel, (2, 1, 0))
   # conc = np.reshape(conc, (len(conc)*5,8,2500))
   # rel = np.reshape(rel, (len(rel)*5,8,2500))
    data_time = np.zeros((len(conc)*2, len(conc[0]), len(conc[0][0])))
    data_time[0:len(conc)] = conc
    data_time[len(conc)::] = rel
    return data_time


def butter_filter(data, highcut=25, fqc=500, order=6):
    """Filtro pasabajas.
    """
    nyq = 0.5*fqc
    high = highcut/nyq
    [b_c, a_c] = signal.butter(order, high, btype='low')
    filt_sig = signal.lfilter(b_c, a_c, data)
    return filt_sig

def remove_dc(data):
    """ Remueve el DC de una señal.
    """
    ndata = np.zeros(np.shape(data))
    mean_v = np.mean(data, axis=2)
    for trial in range(0, len(data)):
        for electrode in range(0, len(data[trial])):
            # Señal original -  señal DC
            v_trial = (data[trial][electrode] - mean_v[trial][electrode])
            ndata[trial][electrode] = v_trial # guardamos señal sin DC
    return ndata, mean_v

def down_sampling(data, sc_v, div):
    """Reduce la frecuencia de muestreo de una señal.
    """
    if ((div % 2) != 0):
        sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc_v+1))
    else:
        sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc_v))

    for trial in range(0, len(data)):
        for electrode in range(0, len(data[trial])):
            sub_signals[trial][electrode] = data[trial][electrode][::sc_v]
    return sub_signals

def artifact_regression(data, reference):
    """Remueve los artifacts de una señal usando regresión. """
    reference = np.transpose(np.matrix(reference))
    data = np.transpose(np.matrix(data))
    op1 = (np.transpose(reference)*reference)/int(reference.shape[0]-1)
    op2 = (np.transpose(reference)*data)/int(data.shape[0]-1)
    coeff, _, _, _ = np.linalg.lstsq(op1, op2)
    data = data - reference*coeff
    data = np.transpose(data)
    return data

def power(data):
    power = (sum(np.abs(data)**2))/len(data)
    return power

S_ID = raw_input("[!] Digite el identificador del sujeto: ")

DATA = get_data_db(S_ID)
[D_DC, m_v] = remove_dc(DATA) # Datos sin DC
Y = butter_filter(D_DC)
SCALE = 8
FS = 500/SCALE # esto es porque fue submuestreado a 2
DIV = 500.0/SCALE
SUB_SIGNAL = down_sampling(Y, int(SCALE), DIV)

TS = 1.0/FS
TIME = np.arange(0, len(D_DC[0][0]) * TS, TS)
F, T, S = signal.spectrogram(SUB_SIGNAL, fs=FS,nfft=256, nperseg=200, noverlap=100)
ff = SUB_SIGNAL.shape # Tamaño del array
frang = ((F>=8)*(F<=12))#+((F>=16)*(F<=31))
M_F = np.mean(S[:,:,frang,:], axis=3) # Potencia promedio para cada frecuencia
FEATS = np.reshape(M_F, (ff[0]*ff[1], M_F.shape[2]))
LABELS = np.zeros((ff[0]*ff[1]))
LABELS[0:len(LABELS)/2] = 1
LABELS[len(LABELS)/2::] = 2
"""D.O. & T.C. """
min_max_scaler = preprocessing.MinMaxScaler()
X_train_minmax = min_max_scaler.fit_transform(FEATS)

"""
pca = decomposition.PCA(n_components=len(feat))
pca.fit(feat)
V = pca.components_
"""
clf = svm.SVC(kernel='linear', C=1)
#scores = cross_val_score(clf, X_train_minmax, LABELS, cv=8)
#scores.mean()
#print "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
clf.fit(X_train_minmax, LABELS)

#el = np.array(np.arange(0,8))
#potmed = S[:,:,(F>=8)*(F<=12),:] # Potencia entre 8-12 Hz
#potmed1 = np.mean(np.mean(potmed[0:len(potmed)/2], axis = 2), axis=0)
#potmed2 = np.mean(np.mean(potmed[len(potmed)/2::], axis = 2), axis=0)
#plt.close('all')
#for i in range(0,8):
#    plt.figure(i)
#    plt.plot(T,potmed1[i].T,'r', label="der")
#    plt.plot(T,potmed2[i].T, 'b', label="izq")
#    plt.legend(bbox_to_anchor=(1.05, 1), loc=1, borderaxespad=0.)
#    plt.show()
#    pass
#
S_ID = 'julian200602'

DATA = get_data_db(S_ID)
[D_DC, m_v] = remove_dc(DATA) # Datos sin DC
Y = butter_filter(D_DC)
SCALE = 8
FS = 500/SCALE # esto es porque fue submuestreado a 2
DIV = 500.0/SCALE
SUB_SIGNAL = down_sampling(Y, int(SCALE), DIV)

TS = 1.0/FS
TIME = np.arange(0, len(D_DC[0][0]) * TS, TS)
F, T, S1 = signal.spectrogram(SUB_SIGNAL, fs=FS,nfft=256, nperseg=200, noverlap=100)
ff = SUB_SIGNAL.shape # Tamaño del array
#frang = ((F>=8)*(F<=12))#+((F>=16)*(F<=31))
M_F = np.mean(S1[:,:,frang,:], axis=3) # Potencia promedio para cada frecuencia
feat = np.reshape(M_F, (ff[0]*ff[1], M_F.shape[2]))
X_test = min_max_scaler.fit_transform(feat)
output = clf.predict(X_test)

conf = confusion_matrix(LABELS, output)
print conf