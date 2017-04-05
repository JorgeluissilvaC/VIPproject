import sqlite3
import mysql.connector

conn = sqlite3.connect('database.db') #connection object
c = conn.cursor()
t_name = "s_julian"
c.execute('''select * from '''+t_name)
data = c.fetchall()
conn.close()


TABLES = {}

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
    "   `O2` REAL NOT NULL)"
    "  PRIMARY KEY (`n_sample`)"
    ") ENGINE=InnoDB")
add_data = ("INSERT INTO "+t_name+
               "(n_sample,n_trial,test_type,AF3,AF4,F3,F4,F7,F8,FC5,FC6,T7,T8,P7,P8) "
               "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)")

try:
  cnx = mysql.connector.connect(user='root', password='uniatlantico',
                                host='vipdb.cd4eqkinbht7.us-west-2.rds.amazonaws.com',
                                database='vipdb')
  cursor = cnx.cursor()
  for name, ddl in TABLES.iteritems():
    try:
        print("Creating table "+str(name))
        cursor.executemany(add_data,data)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()
