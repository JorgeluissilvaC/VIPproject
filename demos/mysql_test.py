import mysql.connector

data = [[0, "r", 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,666,666,666],
        [1, "mra", 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,666,666]]


TABLES = {}
t_name = "unknown"
TABLES[t_name] = (
    "CREATE TABLE IF NOT EXISTS `"+t_name+"` ("
    "  `n_sample` int(11) NOT NULL AUTO_INCREMENT,"
    "  `n_trial` int(11) NOT NULL,"
    "  `test_type` varchar(14) NOT NULL,"
    "   `AF3` REAL NOT NULL,"
    "   `AF4` REAL NOT NULL,"
    "   `F3` REAL NOT NULL,"
    "   `F4` REAL NOT NULL,"
    "   `F7` REAL NOT NULL,"
    "   `F8` REAL NOT NULL,"
    "   `FC5` REAL NOT NULL,"
    "   `FC6` REAL NOT NULL,"
    "   `T7` REAL NOT NULL,"
    "   `T8` REAL NOT NULL,"
    "   `P7` REAL NOT NULL,"
    "   `P8` REAL NOT NULL,"
    "   `O1` REAL NOT NULL,"
    "   `O2` REAL NOT NULL,"
    "  PRIMARY KEY (`n_sample`)"
    ") ENGINE=InnoDB")

add_data = ("INSERT INTO "+t_name+
               "(n_trial,test_type,AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8,O1,O2) "
               "VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)")

cnx = mysql.connector.connect(user='root', password='uniatlantico',
                                host='vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                database='vipdb')
cursor = cnx.cursor()

### CREATE TABLE ###
#for name, ddl in TABLES.iteritems():
#    cursor.execute()

### INSERT DATA ###
cursor.executemany(add_data,data)

cnx.commit()
cursor.close()
cnx.close()
