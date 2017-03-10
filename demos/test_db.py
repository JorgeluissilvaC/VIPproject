import sqlite3

list_of_dic = [["AF3":(1,2),
          "AF4":(1,3),
          "F3":(1,4),
          "F4":(1,5),
          "F7":(1,6),
          "F8":(1,7),
          "FC5":(1,8),
          "FC6":(1,9),
          "T7":(1,10),
          "T8":(1,11),
          "P7":(1,12),
          "P8":(1,13),
          "O1":(1,14),
          "O2":(1,15)],
          ["AF3":(1,2),
          "AF4":(1,3),
          "F3":(1,4),
          "F4":(1,5),
          "F7":(1,6),
          "F8":(1,7),
          "FC5":(1,8),
          "FC6":(1,9),
          "T7":(1,10),
          "T8":(1,11),
          "P7":(1,12),
          "P8":(1,13),
          "O1":(1,14),
          "O2":(1,15)]]

conn = sqlite3.connect('database1.db') #connection object
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE '''+n+"_"+self.na_me+'''
	(n_sample INTEGER PRIMARY KEY,
          AF3 REAL NOT NULL,
          AF4 REAL NOT NULL,
          F3 REAL NOT NULL,
          F4 REAL NOT NULL,
          F7 REAL NOT NULL,
          F8 REAL NOT NULL,
          FC5 REAL NOT NULL,
          FC6 REAL NOT NULL,
          T7 REAL NOT NULL,
          T8 REAL NOT NULL,
          P7 REAL NOT NULL,
          P8 REAL NOT NULL,
          O1 REAL NOT NULL,
          O2 REAL NOT NULL,)''')

for n in list_of_dic :
	sn = [0]*14
	for key, value in n.iteritems():
		if key == "AF3":
			sn[0] = value[0]
		elif key == "AF4":
					sn[1] = value[0]
		elif key == "F3":
			sn[2] = value[0]
		elif key == "F4":
			sn[3] = value[0]
		elif key == "F7":
			sn[4] = value[0]
		elif key == "F8":
			sn[5] = value[0]
		elif key == "FC5":
			sn[6] = value[0]
		elif key == "FC6":
			sn[7] = value[0]
		elif key == "T7":
			sn[8] = value[0]
		elif key == "T8":
			sn[9] = value[0]
		elif key == "P7":
			sn[10] = value[0]
		elif key == "P8":
			sn[11] = value[0]
		elif key == "01":
			sn[12] = value[0]
		elif key == "02":
			sn[13] = value[0]
	c.execute = ('''INSERT INTO '''+n+"_"+self.na_me+''' VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', sn)
	conn.commit()
conn.close()
print "new table: '"+n+"_"+self.na_me+"' in the db"