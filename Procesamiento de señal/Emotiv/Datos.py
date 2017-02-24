# -*- coding: utf-8 -*-
"""
Editor de Spyder
"""            
from emokit.emotiv import Emotiv

if __name__ == "__main__":
    #Constantes 
    tm=5        #Tiempo de muestreo
    fs=128      #Frecuencia de muestreo
    N=fs*tm     #Numero de muestras
    ct=0        #Contador
    dt=[]       #Vector de datos

    with Emotiv(display_output=False, verbose=True) as headset:
        while ct < N:
            packet = headset.dequeue()
            if packet is not None:
                dt.append(packet.sensors)
                ct+=1
                pass   
            
    print "ready"
"""
    ldic =dt
    dicx = ldic[0].copy()
    for key,value in dicx.iteritems():
        	dicx[key] = []
            
    for i in ldic:
        	for key, value in i.iteritems():
        		value = i[key]['value']
        		quality = i[key]['quality']
        		dicx[key].append((quality,value))
        		pass
    """
   
    
    


































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
