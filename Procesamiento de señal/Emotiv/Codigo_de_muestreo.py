# -*- coding: utf-8 -*-
"""
Editor de Spyder
"""            
from emokit.emotiv import Emotiv
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import time 
import csv

if __name__ == "__main__":
    #Constantes 
    tm = 1  #Tiempo de muestreo
    fs = 128.0      #Frecuencia de muestreo
    N = fs*tm     #Numero de muestras
    ct = 0        #Contador
    dt = []       #Vector de datos
    df = []
    fp = []
    data = []
    times = np.arange(0,tm,1/fs)
    with Emotiv(display_output=False, verbose=True) as headset:
        t1 = time.clock()
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
                
                #fp = fp.append(dic['AF3'][0])
                dt.append(dic)                
                ct+=1
            time.sleep(0.007)
        t2 = time.clock()
    print 't = ' + str(t2 - t1)
    print 1/fs
                
    
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
    print "ready"
    data.append([i[1] for i in dicx['AF3']])
    plt.figure()
    plt.plot(times,data)
    plt.grid()
    plt.show()
    



























"""
    for x in range(0, N-1):
        
        AF3[x]=dt[x]['AF3']['value']
        AF4=dt[x]['AF4']['value']
        F3=dt[x]['F3']['value']
        F4=dt[x]['F4']['value']
        F7=dt[x]['F7']['value']
        F8=dt[x]['F8']['value']
        FC5=dt[x]['FC5']['value']
        FC6=dt[x]['FC6']['value']
        O1=dt[x]['O1']['value']
        O2=dt[x]['O2']['value']
        P7=dt[x]['P7']['value']
        P8=dt[x]['P8']['value']
        T7=dt[x]['T7']['value']
        T8=dt[x]['T8']['value']  
    
                plt.hold(True)
                plt.plot(f3,'b')
                plt.plot(fc5,'r')
                plt.plot(af3,'g')
                plt.pause(0.05)
"""
