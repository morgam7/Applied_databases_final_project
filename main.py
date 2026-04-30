import mysql.connector
from datetime import datetime

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

while True:
    print("Conference Management")
    print("---------------------")
    print("Menu")
    print("----")
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by Company")
    print("3 - Add New Attendee")
    print("4 - Exit")

    choice = input("Choice: ")

    if choice == "1":
        speaker = input("Enter speaker name: ")

        query = """
        SELECT speakerName, sessionTitle, roomID
        FROM session
        WHERE speakerName LIKE %s
        """

        cursor.execute(query, ('%' + speaker + '%',))
        results = cursor.fetchall()

        if not results:
            print("No speakers found with that name")
        else:
            for row in results:
                print(row)


    elif choice == "2":
        
        while True:
            company_id = input("Enter Company ID:")

            if not company_id.isdigit() or int(company_id) <= 0:
                continue

            check_query = """
                SELECT companyID, companyName 
                FROM company
                WHERE companyID = %s
            """

            cursor.execute(check_query, (company_id,))
            company = cursor.fetchone()

            if company is None:
                print(f"Company with ID {company_id} doesn't exist")
                continue
            
            company_name = company[1]

            query = """
                SELECT a.attendeeName, a.attendeeDOB, s.sessionTitle, s.speakerName, r.roomName
                FROM attendee a
                JOIN registration reg
                ON a.attendeeID = reg.attendeeID
                JOIN session s
                ON s.sessionID = reg.sessionID
                JOIN room r
                ON r.roomID = s.roomID
                WHERE a.attendeeCompanyID = %s
                """


            cursor.execute(query, (company_id,))
            results = cursor.fetchall()

            if len(results) == 0:
                print(f"{company_name} attendees.")
                print(f"No attendees found for {company_name}")
                continue
            else:
                for row in results:
                    print(row)

                break

    elif choice == "3":

        valid = True

        print("Add New Attendee :")
        print("----------------")

        attendeeID = input("Attendee ID : ")
        name = input("Name : ")
        dob = input("DOB : ")
        gender = input("Gender : ").lower()
        companyID = input("Company ID : ")


        # Check Attendee ID exists
        check_attendee_query = """
        SELECT attendeeID
        FROM attendee
        WHERE attendeeID = %s
        """

        cursor.execute(check_attendee_query, (attendeeID,))
        attendee_result = cursor.fetchone()

        if attendee_result is not None:
            print(f"***ERROR*** Atendee ID: {attendeeID} already exists.")
            valid = False


        # Check gender
        if gender not in ["male", "female"]:
            print("***ERROR*** Gender must be male/female")
            valid = False


        # Check company ID exists
        check_company_query = """
        SELECT companyID
        FROM company
        WHERE companyID = %s
        """

        cursor.execute(check_company_query, (companyID,))
        company_result = cursor.fetchone()

        if company_result is None:
            print(f"***ERROR*** Company ID: {companyID} does not exist.")
            valid = False



        # Only try to insert if the other checks passed
        # Only insert if all checks passed
        if valid:
            insert_query = """
            INSERT INTO attendee 
            (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s)
            """

            try:
                cursor.execute(insert_query, (attendeeID, name, dob, gender, companyID))
                conn.commit()

                print("New attendee added successfully.")

            except mysql.connector.Error as err:
                print(f"***ERROR*** {err}")
                #print(f"***ERROR*** ({err.errno}, \"{err.msg}\")")
        

            

    
    
    
    
    
    
    elif choice == "4":
        print("Goodbye")
        break

    else:
        print("Wrong choice")

'''
CREATE TABLE session (
    sessionID INT PRIMARY KEY,
    sessionTitle VARCHAR(150) NOT NULL,
    speakerName VARCHAR(100) NOT NULL,
    sessionDate DATE NOT NULL,
    roomID INT NOT NULL,
    FOREIGN KEY (roomID) REFERENCES room(roomID)
);
'''






cursor.close()
conn.close()

