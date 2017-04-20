# -*- coding: utf-8 -*-
"""
Editor de Spyder
Graficas de las señales obtenidas con el emotiv
de los electrodos F3 FC5 AF3 
"""            
import time
import matplotlib.pyplot as plt #Librería para las gráficas
from emokit.emotiv import Emotiv #Librería Emokit 

if __name__ == "__main__":
    n=0 # Se podría usar para limitar el while
    f3=[] # Declarar lista para F3
    fc5=[] # Declarar lista para FC5
    af3=[] # Declarar lista para AF3
    af4=[]
    f4=[]
    f7=[]
    f8=[]
    fc6=[]
    t7=[]
    t8=[]
    p7=[]
    p8=[]
    with Emotiv(display_output=False, verbose=True) as headset:
        while True:
            packet = headset.dequeue()
            if packet is not None:

                while len(f3)< 650:
                    f3.append((packet.sensors['F3']['value'])+7000)
                    fc5.append((packet.sensors['FC5']['value']+6000))
                    af3.append(packet.sensors['AF3']['value'])
                    af4.append(packet.sensors['AF4']['value'])
                    f4.append(packet.sensors['F4']['value'])
                    f7.append(packet.sensors['F7']['value'])
                    f8.append(packet.sensors['F8']['value'])
                    fc6.append(packet.sensors['FC6']['value'])
                    t7.append(packet.sensors['T7']['value'])
                    t8.append(packet.sensors['T8']['value'])
                    p7.append(packet.sensors['P7']['value'])
                    p8.append(packet.sensors['P8']['value'])
                    time.sleep(0.0078125)

 
                g1= time.clock()
                plt.hold(True)        
                """
                ,fc5,'g',af3,'b',af4,'b',f4,'b',f7,'b',f8,'b',fc6,'b',t7,'b',t8,'b',p7,'b',p8,'b'
                """
                plt.plot(f3,'#FF530D')
                g2= time.clock()  
                hy=g2-g1
                print(hy)                
                plt.pause(0.0000000000000000000000000000000000000000005)               
                del f3[0]
                del fc5[0]
                del af3[0]
                del af4[0]
                del f4[0]
                del f7[0]
                del f8[0]
                del fc6[0]
                del t7[0]
                del t8[0]
                del p7[0]
                del p8[0]
                #time.sleep(0.0000000000000000000000000000000000000000005)
                pass
                plt.cla()
            #time.sleep(0.001)

   
