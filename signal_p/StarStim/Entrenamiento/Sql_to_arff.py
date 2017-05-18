# -*- coding: utf-8 -*-
import numpy as np
import arff #Install arff con pip
import mysql.connector
from scipy import stats
from ast import literal_eval
"""
Tipos de prueba:
  r - relajación 
  mra - mover la mano derecha
  mla - mover la mano izquierda
  mou - mover objeto hacia arriba
  mod - mover objeto hacia abajo
  all - todas las ateriores
"""

id_s='jorges' #Digite el sujeto
test_type='all' #Digite el tripo de prueba

cnx = mysql.connector.connect(user =     'root', 
                              password = '1234',
                              host =     'localhost',
                              database = 'Datos_temp')
cursor = cnx.cursor()
if test_type == 'all':
    
    get_data = ("SELECT test_type,electrode,F0,F15,F31,F46,F62,F78,F93,F10,F12,F14,F156,F17,F18,F20,F21,F23,F25"
                " FROM c_" + id_s)
    
    data_clms = ['F0','F15','F31','F46','F62','F78','F93','F10',
             'F12','F14','F156','F17','F18','F20','F21','F23','F25'
             ,'test_type','electrode']
    
elif test_type == 'time':
    get_data = ("SELECT test_type,e1,e2,e3,e4,e5,e6,e7,e8 FROM s_" +id_s)
    
    data_clms = ['e1','e2','e3','e4','e5','e6','e7','e8','test_type']
    
else:
    get_data = ("SELECT F0,F15,F31,F46,F62,F78,F93,F10,F12,F14,F156,F17,F18,F20,F21,F23,F25"
                " FROM c_" + id_s +" where (test_type = '"+test_type+"')")
    data_clms = ['F0','F15','F31','F46','F62','F78','F93','F10',
             'F12','F14','F156','F17','F18','F20','F21','F23','F25'
             ,'test_type','electrode']
    
cursor.execute(get_data)
data = np.array(cursor.fetchall())
cursor.close()
cnx.close()


name = id_s + '.arff'
if test_type == 'all':
    das= np.roll(data,-2)
else:
    das = np.roll(data,-1)
das = das.astype(np.float)
arff.dump(name, das, relation = "whatever", names = data_clms)
