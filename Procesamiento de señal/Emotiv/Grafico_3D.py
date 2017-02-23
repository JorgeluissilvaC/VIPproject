# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Jorge Luis Silva C
"""
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
pi=np.pi
ph=0
amp=10
freq=200
time=1
fs=1000
ts=1.0/fs
time=np.arange(0,time,ts)
y=np.sin(2*pi*freq*time+ph)
#Primera gráfica 
plt.figure()
plt.plot(time,y)
plt.grid()
plt.show()
#Segunda gráfica 

#Tercera gráfica 
plt.figure()
f, t, Sxx = signal.spectrogram(y, fs,window=('tukey', 0.1))
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar()
plt.show()
