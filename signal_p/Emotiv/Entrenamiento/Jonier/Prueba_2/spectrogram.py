# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Karolay Ardila Salazar :v
"""
from scipy import signal
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import json

def butter_bandpass_filter(data,lowcut=8, highcut=12,fs=128, order=6):
	nyq = 0.5*fs;
	low = lowcut/nyq
	high= highcut/nyq
	b, a = signal.butter(order, [low,high], btype ='band')
	y = signal.lfilter(b, a, data)
#	f, pxx = signal.welch(y, fs)  
#	max_value = np.amax(pxx)
	return y

with open('relajacion1.json', 'r') as fp:
#with open('concentration1.json', 'r') as fp:
	data = json.load(fp)

fs = 128.0
ts = 1/fs
time = np.arange(0,len(data['AF3']) * ts,ts)
lst = ['AF3','AF4','F3','F4','F7','F8','FC5','FC6','T7','T8','P7','P8','O1','O2',]
index = list(xrange(len(data['AF3'])))

k = 1
while k == 1:
	for key in lst:
		for i in index: 
			data[key][i] = data[key][i][1]

		data[key] = butter_bandpass_filter(data[key])
		#Data vs time 
		plt.figure()
		plt.subplot(211)
		plt.plot(time,data[key])
		plt.ylabel('Sensor value')
		plt.xlabel('Time [sec]')
		plt.title(key)
		plt.grid()

		#Spectrogram 
		plt.subplot(212)
		Pxx, freq, bins, im = plt.specgram(data[key], NFFT=150, Fs=128,noverlap=50)
		plt.show()
		#savefig(key + '.png', dpi = 300)
	k = 0


"""
#Example of a signal

pi = np.pi
ph = 0
amp = 10
freq = 200
time = 1
fs = 1000
ts = 1.0/fs
time = np.arange(0,time,ts)
y = np.sin(2*pi*freq*time+ph)
"""