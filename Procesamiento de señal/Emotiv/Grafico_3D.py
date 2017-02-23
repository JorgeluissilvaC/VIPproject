# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Jorge Luis Silva C
"""
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


fs = 10e3
N = 1e5
amp = 2 * np.sqrt(2)
noise_power = 0.001 * fs / 2
time = np.arange(N) / fs
freq = np.linspace(1e3, 2e3, N)
x = amp * np.sin(2*np.pi*freq*time)
x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)

"""
t=100
fs=160
N=fs*t
time = np.linspace(0, t, N)
freq = 500
amp=1
x = amp * np.sin(2*np.pi*freq*time)
"""
#plt.plot(time,x)

f, t, Sxx = signal.spectrogram(x, fs, window=('tukey',0.25))
plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
