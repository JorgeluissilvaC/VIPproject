# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 09:29:32 2017

@author: Mendez Vasquez
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Julián Sibaja García,
	   Karolay Ardila Salazar,
	   Dayán Mendez Vasquez,
	   Jorge Silva Correa,
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
import math

def butter_filter(data, highcut=30, fqc=500, order=6):
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
	if (dim == 2):
		mean_v = np.mean(data, axis=1)
		for electrode in range(0, len(data[0])):
			# Señal original -  señal DC
			v_trial = (data[electrode] - mean_v[electrode])
			ndata[electrode] = v_trial # guardamos señal sin DC
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

def car_data(data):
	dim = len(data.shape)
	ndata = np.zeros(np.shape(data))
	if (dim==3):
		for trial in range(0,len(data)):
			mean_v = np.mean(data[trial],axis=0)
			mean_e= data[trial] - mean_v
			ndata[trial] = mean_e
	if (dim==2):
		mean_v = np.mean(data,axis=0)
		ndata = data - mean_v
	return ndata

def getDataExt(id_s):
	"""importa los datos del dataset.--------------------------------------
	"""
	mat_contents = sio.loadmat(id_s)
	der = mat_contents['der']
	izq = mat_contents['izq']
	dim=len(izq.shape)
	if (dim==3):
		der = np.transpose(der, (2, 1, 0))
		izq = np.transpose(izq, (2, 1, 0))
		data_time = np.zeros((len(der)*2, len(der[0]), len(der[0][0])))
		data_time[0:len(der)] = der
		data_time[len(der)::] = izq
	if (dim ==2):
		data_time = np.zeros((2,len(der), len(der[0])))
		data_time[0:len(der)] = der
		data_time[len(der)::] = izq

	LABELS = np.zeros((data_time.shape[0]))
	LABELS[0:len(LABELS)/2] = 1
	LABELS[len(LABELS)/2::] = 2
	return data_time, LABELS