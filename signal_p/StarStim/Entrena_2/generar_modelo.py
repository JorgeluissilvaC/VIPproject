# -*- coding: utf-8 -*-
"""
Created on Thu Jul 06 17:44:44 2017

@author: User
"""

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
import time 
import numpy as np
import matplotlib.pylab as plt
from sklearn.model_selection import cross_val_score
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
from pylsl import StreamInlet, resolve_stream
from sklearn.naive_bayes import GaussianNB

def get_data_db(id_s):
    """importa los datos del dataset(.mat).
    """
    mat_contents = sio.loadmat(id_s)
    conc = mat_contents['conc']
    rel = mat_contents['rel']
    dim=len(rel.shape)
    if (dim==3):
        conc = np.transpose(conc, (2, 1, 0))
        rel = np.transpose(rel, (2, 1, 0))
        data_time = np.zeros((len(conc)*2, len(conc[0]), len(conc[0][0])))
        data_time[0:len(conc)] = conc
        data_time[len(conc)::] = rel
        
    if (dim ==2):
        data_time = np.zeros((2,len(conc), len(conc[0])))
        data_time[0:len(conc)] = conc
        data_time[len(conc)::] = rel
   # conc = np.reshape(conc, (len(conc)*5,8,2500))
   # rel = np.reshape(rel, (len(rel)*5,8,2500))
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
    dim = len(data.shape)
    ndata = np.zeros(np.shape(data))
    if (dim == 3):
        mean_v = np.mean(data, axis=2)
        for trial in range(0, len(data)):
            for electrode in range(0, len(data[trial])):
                # Señal original -  señal DC
                v_trial = (data[trial][electrode] - mean_v[trial][electrode])
                ndata[trial][electrode] = v_trial # guardamos señal sin DC
    
    elif (dim == 2):
        mean_v = np.mean(data, axis=1)
        for electrode in range(0, len(data)):
                # Señal original -  señal DC
                v_trial = (data[electrode] - mean_v[electrode])
                ndata[trial] = v_trial # guardamos señal sin DC
                
    return ndata, mean_v

def down_sampling(data, sc_v, div):
    """Reduce la frecuencia de muestreo de una señal.
    """
    dim = len(data.shape)
    if (dim == 3):
        if ((div % 2) != 0):
            sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc_v+1))
        else:
            sub_signals = np.zeros((len(data), len(data[0]), len(data[0][0])/sc_v))
    
        for trial in range(0, len(data)):
            for electrode in range(0, len(data[trial])):
                sub_signals[trial][electrode] = data[trial][electrode][::sc_v]
    
    elif (dim == 2):    
        if ((div % 2) != 0):
            sub_signals = np.zeros((len(data), len(data[0])/sc_v+1))
        else:
            sub_signals = np.zeros((len(data), len(data[0])/sc_v))
        for number in range(0, len(data)):
                sub_signals[number] = data[number][::sc_v]
        
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

#S_ID = raw_input("[!] Digite el identificador del sujeto: ")
S_ID="dayan0407"
DATA = get_data_db(S_ID)
[D_DC, m_v] = remove_dc(DATA) # Datos sin DC
Y = butter_filter(D_DC)
SCALE = 8
FS = 500/SCALE # esto es porque fue submuestreado a 2
DIV = 500.0/SCALE
SUB_SIGNAL = down_sampling(Y, int(SCALE), DIV)
TS = 1.0/FS
TIME = np.arange(0, len(D_DC[0][0]) * TS, TS)
F, T, S = signal.spectrogram(SUB_SIGNAL, fs=FS)
ff = SUB_SIGNAL.shape # Tamaño del array
dimen = len(ff)

if (dimen == 3):
    M_F = np.mean(S, axis=3) # Potencia promedio para cada frecuencia
    FEATS = np.reshape(M_F, (ff[0], M_F.shape[2]*ff[1]))

elif (dimen == 2):    
    M_F = np.mean(S, axis=2) # Potencia promedio para cada frecuencia
    FEATS = M_F
    FEATS = np.reshape(FEATS, (M_F.shape[0]*M_F.shape[1],1))
    FEATS = FEATS.T

LABELS = np.zeros((M_F.shape[0]))
LABELS[0:len(LABELS)/2] = 1
LABELS[len(LABELS)/2::] = 2

"""
Clasificación
"""
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
X_train_minmax = min_max_scaler.fit_transform(FEATS)

clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, X_train_minmax, LABELS, cv=10)
scores.mean()
print "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
scoremax = 0
n_feats = np.arange(len(FEATS[0]))
count = np.zeros(len(n_feats))
for i in range(0,100):
    lsvc = LinearSVC(C=1, penalty="l1", dual=False).fit(X_train_minmax, LABELS )
    #    print FEATS.shape
    model = SelectFromModel(lsvc, prefit=True)
    X_new = model.transform(X_train_minmax)
    #   print X_new.shape
    #scaler = preprocessing.MinMaxScaler(feature_range=(-1,1))
    X_train = (X_new)
    lsvc2 = LinearSVC(C=1,penalty="l1", dual=False)
    scores = cross_val_score(lsvc, X_train, LABELS, cv=10)
#    print "Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)
    ind = model.get_support(indices=True)
    ix = np.in1d(n_feats,ind)
    count[np.where(ix)] += 1
    if (scores.mean() > scoremax):
        scoremax = scores.mean()
        indm = ind
        
print "Accuracy: %0.2f " % (scoremax)
#np.save('ind'+S_ID+'prueba',indm)

r0_feats = np.flatnonzero(count)
r_feats = np.flatnonzero(count>50)
#%%
clf.fit(X_train_minmax[:,r_feats], LABELS)
S_ID="jor"
DATA = get_data_db(S_ID)
[D_DC, m_v] = remove_dc(DATA) # Datos sin DC
Y = butter_filter(D_DC)
SCALE = 8
FS = 500/SCALE # esto es porque fue submuestreado a 2
DIV = 500.0/SCALE
SUB_SIGNAL = down_sampling(Y, int(SCALE), DIV)
TS = 1.0/FS
TIME = np.arange(0, len(D_DC[0][0]) * TS, TS)
F, T, S = signal.spectrogram(SUB_SIGNAL, fs=FS)
ff = SUB_SIGNAL.shape # Tamaño del array
dimen = len(ff)

if (dimen == 3):
    M_F = np.mean(S, axis=3) # Potencia promedio para cada frecuencia
    FEATS = np.reshape(M_F, (ff[0], M_F.shape[2]*ff[1]))

elif (dimen == 2):    
    M_F = np.mean(S, axis=2) # Potencia promedio para cada frecuencia
    FEATS = M_F
    FEATS = np.reshape(FEATS, (M_F.shape[0]*M_F.shape[1],1))
    FEATS = FEATS.T

Feat = min_max_scaler.transform(FEATS)
Feat2 = Feat[:,r_feats]
cls = clf.predict(Feat2)
LAB = np.zeros((M_F.shape[0]))
LAB[0:len(LAB)/2] = 1
LAB[len(LAB)/2::] = 2
acc = clf.score(Feat2,LAB)
print str(acc)+' ultimo'
#%%