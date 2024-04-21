import sqlite3
conn = sqlite3.connect("leaf.db")
print("opened database successfully")
conn.execute("CREATE TABLE feedback(farmername TEXT,mobilenumber NUMBER,title TEXT,description TEXT)")
conn.execute("CREATE TABLE adminlogin (amail varchar,apassword varchar)")
conn.execute("CREATE TABLE signup (uname varchar,uphone varchar,username varchar,upassword varchar)")
print("table created successfully")
conn.close()