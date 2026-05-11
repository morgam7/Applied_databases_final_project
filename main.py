import mysql.connector
from datetime import datetime
from neo4j import GraphDatabase


# -----------------------------
# Database connection settings
# -----------------------------

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
MYSQL_DATABASE = "appdbproj"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4jneo4j"
NEO4J_DATABASE = "appdbprojNeo4j"


# -----------------------------
# Connect to MySQL and Neo4j
# -----------------------------

conn = mysql.connector.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

cursor = conn.cursor()

neo4j_driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

print("Connected to MySQL and Neo4j.")


# -----------------------------
# Load rooms once at program start
# This is needed because option 6 should not show rooms added after the app starts.
# -----------------------------

cursor.execute("""
SELECT roomID, roomName, capacity
FROM room
ORDER BY roomID
""")

rooms_cache = cursor.fetchall()


# -----------------------------
# Helper functions
# -----------------------------

def get_attendee_from_mysql(attendee_id):
    """Returns attendee ID and name from MySQL, or None if not found."""

    query = """
    SELECT attendeeID, attendeeName
    FROM attendee
    WHERE attendeeID = %s
    """

    cursor.execute(query, (attendee_id,))
    return cursor.fetchone()


def get_connected_attendees_from_neo4j(attendee_id):
    """Returns all attendees connected to the selected attendee in either direction."""

    query = """
    MATCH (a:Attendee {AttendeeID: $attendee_id})
    OPTIONAL MATCH (a)-[:CONNECTED_TO]-(connected:Attendee)
    RETURN 
        a.AttendeeID AS attendee_id,
        connected.AttendeeID AS connected_id
    ORDER BY connected.AttendeeID
    """

    with neo4j_driver.session() as session:
        result = session.run(query, attendee_id=attendee_id)
        return list(result)


def attendees_are_connected(attendee_id_1, attendee_id_2):
    """Checks whether two attendees are already connected in either direction."""

    query = """
    MATCH (a:Attendee {AttendeeID: $id1})
    MATCH (b:Attendee {AttendeeID: $id2})
    MATCH (a)-[r:CONNECTED_TO]-(b)
    RETURN count(r) AS relationship_count
    """

    with neo4j_driver.session() as session:
        result = session.run(query, id1=attendee_id_1, id2=attendee_id_2)
        record = result.single()

    return record["relationship_count"] > 0


def create_attendee_connection(attendee_id_1, attendee_id_2):
    """
    Creates Neo4j Attendee nodes if needed, then creates a CONNECTED_TO relationship.
    The attendee IDs have already been checked against MySQL before this function is called.
    """

    query = """
    MERGE (a:Attendee {AttendeeID: $id1})
    MERGE (b:Attendee {AttendeeID: $id2})
    MERGE (a)-[:CONNECTED_TO]->(b)
    """

    with neo4j_driver.session() as session:
        session.run(query, id1=attendee_id_1, id2=attendee_id_2)


def valid_date(date_text):
    """Checks that a date is in YYYY-MM-DD format."""

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# -----------------------------
# Main menu loop
# -----------------------------

while True:
    print()
    print("Conference Management")
    print("---------------------")
    print("Menu")
    print("----")
    print("1 - View Speakers & Sessions")
    print("2 - View Attendees by Company")
    print("3 - Add New Attendee")
    print("4 - View Connected Attendees")
    print("5 - Add Attendee Connection")
    print("6 - View Rooms")
    print("x - Exit Application")

    choice = input("Choice: ").strip()


    # -----------------------------
    # Option 1: View speakers and their sessions
    # -----------------------------

    if choice == "1":
        speaker = input("Enter speaker name: ").strip()

        query = """
        SELECT s.speakerName, s.sessionTitle, r.roomName
        FROM session s
        JOIN room r
            ON s.roomID = r.roomID
        WHERE s.speakerName LIKE %s
        ORDER BY s.speakerName, s.sessionTitle
        """

        cursor.execute(query, ("%" + speaker + "%",))
        results = cursor.fetchall()

        if not results:
            print()
            print("Session Details")
            print("-------------------")
            print("No speakers found with that name.")
        else:
            print()
            print(f"Session Details For {speaker}")
            print("-------------------")

            for row in results:
                print(f"Speaker: {row[0]}")
                print(f"Session: {row[1]}")
                print(f"Room: {row[2]}")
                print()


    # -----------------------------
    # Option 2: View attendees by company
    # -----------------------------

    elif choice == "2":

        while True:
            company_id = input("Enter Company ID: ").strip()

            if not company_id.isdigit() or int(company_id) <= 0:
                print()
                print("Company Search Error")
                print("-------------------")
                print("***ERROR*** Invalid company ID.")
                continue

            company_id = int(company_id)

            check_query = """
            SELECT companyID, companyName
            FROM company
            WHERE companyID = %s
            """

            cursor.execute(check_query, (company_id,))
            company = cursor.fetchone()

            if company is None:
                print()
                print("Company Search Error")
                print("-------------------")
                print(f"Company with ID {company_id} does not exist.")
                continue

            company_name = company[1]

            query = """
            SELECT 
                a.attendeeName,
                a.attendeeDOB,
                s.sessionTitle,
                s.speakerName,
                s.sessionDate,
                r.roomName
            FROM attendee a
            JOIN registration reg
                ON a.attendeeID = reg.attendeeID
            JOIN session s
                ON s.sessionID = reg.sessionID
            JOIN room r
                ON r.roomID = s.roomID
            WHERE a.attendeeCompanyID = %s
            ORDER BY a.attendeeName, s.sessionDate
            """

            cursor.execute(query, (company_id,))
            results = cursor.fetchall()

            print()
            print(f"Attendees for {company_name}")
            print("-------------------")

            if len(results) == 0:
                print("No attendees registered for any sessions.")
            else:
                for row in results:
                    print(f"Attendee: {row[0]}")
                    print(f"DOB: {row[1]}")
                    print(f"Session: {row[2]}")
                    print(f"Speaker: {row[3]}")
                    print(f"Date: {row[4]}")
                    print(f"Room: {row[5]}")
                    print()

            break


    # -----------------------------
    # Option 3: Add a new attendee
    # -----------------------------

    elif choice == "3":

        valid = True

        print()
        print("Add New Attendee")
        print("----------------")

        attendeeID = input("Attendee ID: ").strip()
        name = input("Name: ").strip()
        dob = input("DOB YYYY-MM-DD: ").strip()
        gender = input("Gender: ").strip().capitalize()
        companyID = input("Company ID: ").strip()

        if not attendeeID.isdigit() or int(attendeeID) <= 0:
            print()
            print("Attendee Entry Error")
            print("-------------------")
            print("***ERROR*** Invalid attendee ID.")
            valid = False
        else:
            attendeeID = int(attendeeID)

        if not companyID.isdigit() or int(companyID) <= 0:
            print()
            print("Attendee Entry Error")
            print("-------------------")
            print("***ERROR*** Invalid company ID.")
            valid = False
        else:
            companyID = int(companyID)

        if not valid_date(dob):
            print()
            print("Attendee Entry Error")
            print("-------------------")
            print("***ERROR*** DOB must be in YYYY-MM-DD format.")
            valid = False

        if gender not in ["Male", "Female"]:
            print()
            print("Attendee Entry Error")
            print("-------------------")
            print("***ERROR*** Gender must be Male or Female.")
            valid = False

        if valid:
            check_attendee_query = """
            SELECT attendeeID
            FROM attendee
            WHERE attendeeID = %s
            """

            cursor.execute(check_attendee_query, (attendeeID,))
            attendee_result = cursor.fetchone()

            if attendee_result is not None:
                print()
                print("Attendee Entry Error")
                print("-------------------")
                print(f"***ERROR*** Attendee ID {attendeeID} already exists.")
                valid = False

            check_company_query = """
            SELECT companyID
            FROM company
            WHERE companyID = %s
            """

            cursor.execute(check_company_query, (companyID,))
            company_result = cursor.fetchone()

            if company_result is None:
                print()
                print("Attendee Entry Error")
                print("-------------------")
                print(f"***ERROR*** Company ID {companyID} does not exist.")
                valid = False

        if valid:
            insert_query = """
            INSERT INTO attendee
            (attendeeID, attendeeName, attendeeDOB, attendeeGender, attendeeCompanyID)
            VALUES (%s, %s, %s, %s, %s)
            """

            try:
                cursor.execute(insert_query, (attendeeID, name, dob, gender, companyID))
                conn.commit()

                print()
                print("Attendee Added")
                print("-------------------")
                print(f"Attendee ID: {attendeeID}")
                print(f"Name: {name}")
                print(f"DOB: {dob}")
                print(f"Gender: {gender}")
                print(f"Company ID: {companyID}")

            except mysql.connector.Error as err:
                print()
                print("Attendee Entry Error")
                print("-------------------")
                print(f"***ERROR*** ({err.errno}, \"{err.msg}\")")


    # -----------------------------
    # Option 4: View connected attendees
    # -----------------------------

    elif choice == "4":

        while True:
            attendee_id = input("Enter Attendee ID: ").strip()

            if not attendee_id.isdigit():
                print()
                print("***ERROR*** Invalid attendee ID.")
                continue

            attendee_id = int(attendee_id)

            records = get_connected_attendees_from_neo4j(attendee_id)

            if records:
                mysql_attendee = get_attendee_from_mysql(attendee_id)

                if mysql_attendee is not None:
                    attendee_name = mysql_attendee[1]
                else:
                    attendee_name = "Unknown"

                print()
                print(f"Connected Attendees For {attendee_name}")
                print("-------------------")
                print(f"Attendee ID: {attendee_id}")
                print()

                connections_found = False

                for record in records:
                    connected_id = record["connected_id"]

                    if connected_id is not None:
                        connected_attendee = get_attendee_from_mysql(connected_id)

                        if connected_attendee is not None:
                            connected_name = connected_attendee[1]
                        else:
                            connected_name = "Unknown"

                        print(f"Connected Attendee ID: {connected_id}")
                        print(f"Connected Attendee Name: {connected_name}")
                        print()
                        connections_found = True

                if not connections_found:
                    print("No connections")

                break

            mysql_attendee = get_attendee_from_mysql(attendee_id)

            if mysql_attendee is not None:
                print()
                print(f"Connected Attendees For {mysql_attendee[1]}")
                print("-------------------")
                print(f"Attendee ID: {mysql_attendee[0]}")
                print("No connections")
                break

            print()
            print("***ERROR*** Attendee does not exist.")
            


    # -----------------------------
    # Option 5: Add attendee connection
    # -----------------------------

    elif choice == "5":

        while True:
            attendee_id_1 = input("Enter Attendee 1 ID: ").strip()
            attendee_id_2 = input("Enter Attendee 2 ID: ").strip()

            if not attendee_id_1.isdigit() or not attendee_id_2.isdigit():
                print()
                print("***ERROR*** Attendee IDs must be numeric.")
                continue

            attendee_id_1 = int(attendee_id_1)
            attendee_id_2 = int(attendee_id_2)

            if attendee_id_1 == attendee_id_2:
                print()
                print("***ERROR*** An attendee cannot be connected to themselves.")
                continue

            attendee_1 = get_attendee_from_mysql(attendee_id_1)
            attendee_2 = get_attendee_from_mysql(attendee_id_2)

            if attendee_1 is None or attendee_2 is None:
                print()
                print("***ERROR*** One or both attendee IDs do not exist.")
                continue

            if attendees_are_connected(attendee_id_1, attendee_id_2):
                print()
                print("***ERROR*** These attendees are already connected.")
                continue

            create_attendee_connection(attendee_id_1, attendee_id_2)

            print()
            print(f"{attendee_1[1]} is now connected to {attendee_2[1]}.")
            break


    # -----------------------------
    # Option 6: View rooms
    # -----------------------------

    elif choice == "6":

        print()
        print("Room Details")
        print("-------------------")

        for room in rooms_cache:
            print(f"Room ID: {room[0]}")
            print(f"Room Name: {room[1]}")
            print(f"Capacity: {room[2]}")
            print()


    # -----------------------------
    # Exit application
    # -----------------------------

    elif choice.lower() == "x":
        print()
        print("Exit Application")
        print("-------------------")
        print("Exiting application.")
        break


    # -----------------------------
    # Anything else: show menu again
    # -----------------------------

    else:
        print()
        print("Menu Error")
        print("-------------------")
        print("***ERROR*** Invalid menu choice.")


# -----------------------------
# Close database connections
# -----------------------------

cursor.close()
conn.close()
neo4j_driver.close()