# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Jorge Luis Silva C
"""
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
pi=np.pi
"""
fs = 10e3
N = 1e5
amp = 20
noise_power = 0.0000000001*fs/2
time = np.arange(N) / fs
freq = np.linspace(1e3, 2e3, N)
x = amp * np.sin(2*np.pi*freq*time)
#x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
"""
ph=0
amp=1
freq=100
time=1
fs=10000
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
