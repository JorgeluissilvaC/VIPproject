# -*- coding: utf-8 -*-
import sqlite3
import numpy as np
import arff #Install arff con pip
import mysql.connector
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
test_type='r' #Digite el tripo de prueba 

cnx = mysql.connector.connect(user =     'root',
                                  password = 'uniatlantico',
                                  host =     'vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                  database = 'vipdb')
cursor = cnx.cursor()
if test_type == 'all':
    get_data = ("SELECT electrode,test_type,n_trial,F0,F08,F16,F24,F32,F4,F48,F56,F64,F72,F8,F88,F96,F104,F112,F12,F128"
                " FROM c_" + id_s)
else:
    get_data = ("SELECT electrode,n_trial,F0,F08,F16,F24,F32,F4,F48,F56,F64,F72,F8,F88,F96,F104,F112,F12,F128"
                " FROM c_" + id_s +" where (test_type = '"+test_type+"')")
cursor.execute(get_data)
data = np.array(cursor.fetchall())
cursor.close()
cnx.close()

data_clms = ['electrode','test_type','n_trial',
             'F0','F08','F16','F24','F32','F4',
             'F48','F56','F64','F72','F8','F88',
             'F96','F104','F112','F12','F128']

name = id_s + '.arff'
arff.dump(name, data, relation = "whatever", names = data_clms)
