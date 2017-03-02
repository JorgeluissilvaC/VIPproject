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
    data = [i[1] for i in dicx['AF3']]
    plt.figure()
    plt.plot(times,data)
    plt.grid()
    plt.show()

    w = csv.writer(open("output.csv", "w"))
    for key, val in dicx.items():
        w.writerow([key, val])
    karo = {}
    for key, val in csv.reader(open("output.csv")):
        karo[key] = val