import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='s0'")
lock = c.fetchall()
print lock
c.execute("SELECT MAX(n_trial) FROM s0")
n = c.fetchall()
print n[0][0]
conn.close()
