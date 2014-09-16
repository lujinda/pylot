import sqlite3

conn=sqlite3.connect("temp.db")
curs=conn.cursor()
query="INSERT INTO Contacts VALUES(?,?)"

while True:
    line=raw_input().strip()
    if not line:break
    vals=line.split()
    curs.execute(query,vals)

conn.commit()
conn.close()

