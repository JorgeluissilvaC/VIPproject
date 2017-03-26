# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
import arff #Install arff con pip
"""
Tipos de prueba:
  r - relajación 
  mra - mover la mano derecha
  mla - mover la mano izquierda
  mou - mover objeto hacia arriba
  mod - mover objeto hacia abajo
"""

id_s='jorge' #Digite el sujeto 
test_type='r' #Digite el tripo de prueba 

conn = sqlite3.connect('database.db') #connection object
c = conn.cursor()
c.execute('''select n_trial,AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8 from '''+"s_"+id_s+" where (test_type = '"+test_type+"')")
data = np.array(c.fetchall())
conn.close()

name = id_s + '.arff'
arff.dump(name, data, relation="whatever", names=['n_trial','AF3','AF4','F3','F4','F7','F8','FC5','FC6','T7','T8','P7','P8'])
