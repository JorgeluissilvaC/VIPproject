# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 14:16:42 2017

@author: User
"""
from emokit.emotiv import Emotiv
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import time 

def GetDataO(tm):
    fs = 128.0      #Frecuencia de muestreo
    N = fs*tm     #Numero de muestras
    ct = 0        #Contador
    dt = []       #Vector de datos
    with Emotiv(display_output=False, verbose=True) as headset:
        while ct < N:
            packet = headset.dequeue()
            if packet is not None:
                # print packet.sensors
                # print "########################" 
                dic = {}
                
                for key, value in packet.sensors.iteritems():
                    value = packet.sensors[key]['value']
                    quality = packet.sensors[key]['quality']
                    dic[key] = (value,quality)                
                dt.append(dic)                
                ct+=1
            time.sleep(0.007)
    ldic = dt
    dicx = ldic[0].copy()
    for key,value in dicx.iteritems():
        dicx[key] = []
                
    for i in ldic:
        for key, value in i.iteritems():
            value = i[key][0]
            quality = i[key][1]
            dicx[key].append((quality,value))
            pass
    return dicx