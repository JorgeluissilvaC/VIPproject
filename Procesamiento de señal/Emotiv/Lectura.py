# -*- coding: utf-8 -*-
"""
Editor de Spyder
"""            
import time
import matplotlib.pyplot as plt
from emokit.emotiv import Emotiv

if __name__ == "__main__":
    n=0
    f3=[]
    fc5=[]
    af3=[]
    with Emotiv(display_output=True, verbose=True) as headset:
        while True:
            packet = headset.dequeue()
            if packet is not None:
                f3.append(packet.sensors['F3']['value'])
                fc5.append(packet.sensors['FC5']['value'])
                af3.append(packet.sensors['AF3']['value'])
                plt.hold(True)
                plt.plot(f3,'b')
                plt.plot(fc5,'r')
                plt.plot(af3,'g')
                n+=1
                plt.pause(0.05)
                pass
            time.sleep(0.001)

   