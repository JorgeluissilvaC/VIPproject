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
import sqlite
#with open('relajacion1.json', 'r') as fp:
#  data = json.load(fp)

conn = sqlite3.connect('database1.db') #connection object
c = conn.cursor()
c.execute('''select * from '''+"s"+n)
print("hi")
data = c.fetchall()
for row in data:


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
    f, t, Sxx = signal.spectrogram(data[key], fs, window=('tukey', 0.1))
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
  #plt.show()
    savefig(key + '.png', dpi = 300)
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