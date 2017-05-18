# -*- coding: utf-8 -*-
import numpy as np
import arff #Install arff con pip
import mysql.connector
from scipy import stats
"""
Tipos de prueba:
  r - relajación 
  mra - mover la mano derecha
  mla - mover la mano izquierda
  mou - mover objeto hacia arriba
  mod - mover objeto hacia abajo
  all - todas las ateriores
"""

id_s='dayan' #Digite el sujeto
test_type='all' #Digite el tripo de prueba

cnx = mysql.connector.connect(user =     'root', 
                              password = '1234',
                              host =     'localhost',
                              database = 'Datos_temp')
cursor = cnx.cursor()
if test_type == 'all':
    
    get_data = ("SELECT test_type,electrode,F0,F15,F31,F46,F62,F78,F93,F10,F12,F14,F156,F17,F18,F20,F21,F23,F25"
                " FROM c_" + id_s)
    

    
else:
    get_data = ("SELECT F0,F15,F31,F46,F62,F78,F93,F10,F12,F14,F156,F17,F18,F20,F21,F23,F25"
                " FROM c_" + id_s +" where (test_type = '"+test_type+"')")
cursor.execute(get_data)
data = np.array(cursor.fetchall())
cursor.close()
cnx.close()

data_clms = ['F0','F15','F31','F46','F62','F78','F93','F10',
             'F12','F14','F156','F17','F18','F20','F21','F23','F25'
             ,'test_type','electrode']
name = id_s + '.arff'
das= np.roll(data,-2)
"""
a = data.copy()
a[:,2::] = np.multiply(10**11,data[:,2::])
test_typed = a[:,0]
sensors = stats.zscore(data[:,1::])
data[:,0:-1] = sensors
data[:,-1] = test_typed
print data
"""
arff.dump(name, das, relation = "whatever", names = data_clms)
