import sqlite3
n = "0"
test_type = "relax"
list_of_dic = [{"AF3":(1,2),
          "AF4":(3,3),
          "F3":(2,4),
          "F4":(1,5),
          "F7":(6,6),
          "F8":(12,7),
          "FC5":(1,8),
          "FC6":(8,9),
          "T7":(9,10),
          "T8":(0,11),
          "P7":(1,12),
          "P8":(8,13),
          "O1":(0,14),
          "O2":(91,15)},
          {"AF3":(7,2),
          "AF4":(65,3),
          "F3":(45,4),
          "F4":(6,5),
          "F7":(1,6),
          "F8":(6,7),
          "FC5":(8,8),
          "FC6":(0,9),
          "T7":(9,10),
          "T8":(1,11),
          "P7":(44,12),
          "P8":(3,13),
          "O1":(23,14),
          "O2":(67,15)}]

conn = sqlite3.connect('database1.db') #connection object
c = conn.cursor()
# Create table
c.execute('''CREATE TABLE IF NOT EXISTS '''+"s"+n+'''
                (n_sample INTEGER PRIMARY KEY,
                test_type TEXT NOT NULL,
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
                O2 REAL NOT NULL)''')

for n_s in list_of_dic :
    sn = [0]*15
    sn[0] = test_type

    for key, value in n_s.iteritems():
        print(key+": "+str(value[0]))

        if key == "AF3":
            sn[1] = value[0]
        elif key == "AF4":
            sn[2] = value[0]
        elif key == "F3":
            sn[3] = value[0]
        elif key == "F4":
            sn[4] = value[0]
        elif key == "F7":
            sn[5] = value[0]
        elif key == "F8":
            sn[6] = value[0]
        elif key == "FC5":
            sn[7] = value[0]
        elif key == "FC6":
            sn[8] = value[0]
        elif key == "T7":
            sn[9] = value[0]
        elif key == "T8":
            sn[10] = value[0]
        elif key == "P7":
            sn[11] = value[0]
        elif key == "P8":
            sn[12] = value[0]
        elif key == "01":
            sn[13] = value[0]
        elif key == "02":
            sn[14] = value[0]
        print sn
    c.execute('''INSERT INTO '''+"s"+n+''' VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', sn)
    conn.commit()
conn.close()
print "[!]Table: '"+"s"+n+"' added/updated"