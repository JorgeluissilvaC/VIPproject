# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:46:14 2017

@author: User
"""
dt=[]
qu=[]
dtt=[]
quu=[]
d=packet.sensors
for key, value in d.iteritems():
    dt.append(packet.sensors[key]['value'])
    qu.append(packet.sensors[key]['quality'])
    
    dt=[]
    qu=[]
    pass