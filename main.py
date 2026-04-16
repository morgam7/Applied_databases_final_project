import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R!barules4evu",
    database="appdbproj"
)

print("Connected")

cursor = conn.cursor()
cursor.execute("SHOW TABLES")

for table in cursor:
    print(table)

cursor.close()
conn.close()