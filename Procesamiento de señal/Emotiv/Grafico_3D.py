# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 22:08:35 2017

@author: Jorge Luis Silva C
"""
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
pi=3.1316

fs = 10e3
N = 1e5
amp = 20
noise_power = 0.0000000001*fs/2
time = np.arange(N) / fs
freq = np.linspace(1e3, 2e3, N)
x = amp * np.sin(2*np.pi*freq*time)
#x += np.random.normal(scale=np.sqrt(noise_power), size=time.shape)
"""q
dt=[]
x=np.arange(-2*pi,2*pi,0.1)
y=np.sin(x)
for x in range(0,100):
    dt.append(y)
"""
plt.plot(time,x)
"""
f, t, Sxx = signal.spectrogram(x, fs)

plt.pcolormesh(t, f, Sxx)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
"""