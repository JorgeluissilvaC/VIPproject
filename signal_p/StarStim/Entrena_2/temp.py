# -*- coding: utf-8 -*-
import mysql.connector
cnx = mysql.connector.connect(user =     'root', 
      password = '1234',
      host =     'localhost',
      database = 'Datos_temp')
cursor = cnx.cursor()
