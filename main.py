import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R!barules4evu",
    database="appdbproj"
)

print("Connected")
'''
cursor = conn.cursor()
cursor.execute("SHOW TABLES")

for table in cursor:
    print(table)

cursor.close()
conn.close()
'''

cursor = conn.cursor()

print("Conference Management")
print("---------------------")
print("Menu") 
print("----")
print("----")
print("1 - View Speakers & Sessions")
print("2 - View Attendees by Company")
print("3 - Add New Attendee")

choice = input("Choice:")

if choice == "1":

    input = (input("Enter speaker name :"))
    
    query = """
    SELECT speakerName 
    FROM session 
    WHERE speakerName LIKE %s
    """
    cursor.execute(query, ('%' + input + '%',))
    results = cursor.fetchall()

    for row in results:
        print(row)

else:
    print("Wrong choice")




cursor.close()
conn.close()

