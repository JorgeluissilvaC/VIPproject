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

id_s='julian' #Digite el sujeto
test_type='all' #Digite el tripo de prueba

cnx = mysql.connector.connect(user =     'root',
                                  password = 'uniatlantico',
                                  host =     'vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                  database = 'vipdb')
cursor = cnx.cursor()
if test_type == 'all':
    get_data = ("SELECT test_type,electrode,F0,F08,F16,F24,F32,F4,F48,F56,F64,F72,F8,F88,F96,F104,F112,F12,F128"
                " FROM c_" + id_s+" where (electrode = '11.0')")
else:
    get_data = ("SELECT F0,F08,F16,F24,F32,F4,F48,F56,F64,F72,F8,F88,F96,F104,F112,F12,F128"
                " FROM c_" + id_s +" where (test_type = '"+test_type+"')")
cursor.execute(get_data)
data = np.array(cursor.fetchall())
cursor.close()
cnx.close()

data_clms = ['F0','F08','F16','F24','F32','F4',
             'F48','F56','F64','F72','F8','F88',
             'F96','F104','F112','F12','F128','electrode','test_type']

name = id_s + '.arff'
a = data.copy()
a[:,2::] = np.multiply(10**11,data[:,2::])
test_typed = a[:,0]
sensors = stats.zscore(data[:,1::])
data[:,0:-1] = sensors
data[:,-1] = test_typed
arff.dump(name, data, relation = "whatever", names = data_clms)
