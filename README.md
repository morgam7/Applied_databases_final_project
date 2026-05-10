# Applied Databases Project

This is the repository for my final project for the Applied Databases module of the Higher Diploma in Science in Data Analytics at ATU Galway-Mayo.

The focus of this project is to create a Python command-line application that connects to both a MySQL database and a Neo4j graph database. The application is based on a conference management system and allows the user to view, add, and query conference data.

## Author

Marcella Morgan

## Project Overview

This project is a Python application called `main.py`.

The application uses two databases:

- A MySQL database called `appdbproj`
- A Neo4j database containing attendee connection data

The MySQL database stores the main conference management data, including companies, attendees, rooms, sessions, and registrations.

The Neo4j database stores `CONNECTED_TO` relationships between attendees. These relationships are used to show which attendees are connected to each other. The direction of the relationship is treated as unimportant in the application.

The project was designed to meet the brief by including:

- A Python menu-driven application
- A connection to a MySQL database
- A connection to a Neo4j graph database
- SQL queries across related MySQL tables
- Cypher queries across Neo4j attendee relationships
- Input validation and error handling
- The ability to add a new attendee to MySQL
- The ability to add a new attendee connection in Neo4j
- A room display feature using data loaded when the application starts

## Technologies Used

- Python
- MySQL
- Neo4j
- Cypher
- SQL
- MySQL Connector for Python
- Neo4j Python Driver
- Visual Studio Code
- Git and GitHub

## Project Setup

The project is intended to run on the Applied Databases virtual machine.

The databases are assumed to have already been imported into the VM before running the Python application.

The required database files are:

- `appdbproj.sql.txt`
- `appdbprojNeo4j.json`

The MySQL file creates the `appdbproj` database. This contains the tables used for the conference management data.

The Neo4j file contains the Cypher statements used to create attendee nodes and `CONNECTED_TO` relationships in Neo4j.

## Database Requirements

## MySQL

The MySQL database should be called:

`appdbproj`

It should contain the following tables:

- `company`
- `attendee`
- `room`
- `session`
- `registration`

The SQL file used to create the database is:

`appdbproj.sql.txt`

## Neo4j

The Neo4j database contains attendee nodes and `CONNECTED_TO` relationships.

The Neo4j file supplied for the project is:

`appdbprojNeo4j.json`

Although the file has a `.json` extension, it contains Cypher statements that are run in Neo4j.

The application connects to Neo4j using:

`bolt://localhost:7687`

On the VM used for development, the Neo4j username was:

`neo4j`

and the password was:

`neo4jneo4j`

If the password is different on another machine, the password variable at the top of `main.py` should be updated.

## Running the Application

To run the project, open a terminal in the project folder and run:

`python main.py`

On the VM used for development, Python was available through Anaconda, so the application could also be run using:

`& "C:\ProgramData\anaconda3\python.exe" main.py`

Before running the application, MySQL and Neo4j should both be running, and the required databases should already be imported.

## Project Structure

Applied_databases_final_project-main/

- `main.py`
- `appdbproj.sql.txt`
- `appdbprojNeo4j.json`
- `requirements.txt`
- `README.md`
- `GitLink.txt`

## Main File

### `main.py`

This is the main Python application file.

It contains:

- Database connection settings
- MySQL connection code
- Neo4j connection code
- Helper functions
- The main menu loop
- Code for each menu option
- Input validation
- Error handling
- Closing of database connections

## Menu Options

The application displays a command-line menu with the following options:

- `1 - View Speakers & Sessions`
- `2 - View Attendees by Company`
- `3 - Add New Attendee`
- `4 - View Connected Attendees`
- `5 - Add Attendee Connection`
- `6 - View Rooms`
- `x - Exit Application`

## Functionality

### 1 - View Speakers & Sessions

The user enters a speaker name, or part of a speaker name.

The application searches the MySQL `session` table and displays:

- Speaker name
- Session title
- Room name

If no speaker matches the search string, a message is displayed and the user is returned to the main menu.

### 2 - View Attendees by Company

The user enters a company ID.

The application validates that the company ID is numeric and greater than zero. It then checks whether the company exists in the MySQL database.

If the company exists, the application displays attendee and session details for attendees from that company, including:

- Attendee name
- Attendee date of birth
- Session title
- Speaker name
- Session date
- Room name

If the company does not exist, or if there are no attendees from that company for any sessions, an appropriate message is displayed.

### 3 - Add New Attendee

The user enters details for a new attendee:

- Attendee ID
- Name
- Date of birth
- Gender
- Company ID

The application checks whether:

- The attendee ID already exists
- The gender is valid
- The company ID exists
- The date of birth is in the correct format

If the details are valid, the attendee is added to the MySQL `attendee` table.

### 4 - View Connected Attendees

The user enters an attendee ID.

The application checks the Neo4j database for an `Attendee` node with that ID and finds all attendees with a `CONNECTED_TO` relationship in either direction.

The application then uses MySQL to get the names of the attendees, because the Neo4j database stores attendee IDs while the MySQL database stores attendee names.

If the attendee exists in MySQL but not in Neo4j, the attendee name is shown with the message:

`No connections`

If the attendee does not exist in either database, an error message is displayed and the user is asked to enter another attendee ID.

### 5 - Add Attendee Connection

The user enters two attendee IDs.

The application checks that:

- Both IDs are numeric
- The two IDs are not the same
- Both attendees exist in the MySQL database
- The attendees are not already connected in Neo4j

If the checks pass, the application creates any missing Neo4j attendee node and adds a `CONNECTED_TO` relationship between the two attendees.

The relationship is checked in both directions, because the direction of `CONNECTED_TO` is not important for this project.

### 6 - View Rooms

The application displays all rooms from the MySQL `room` table.

The room data is loaded once when the application starts. This means that any rooms manually added to MySQL after the program starts will not appear until the application is exited and restarted. This matches the project specification.

### x - Exit Application

This option exits the application and closes the database connections.

## Database Design

## MySQL Database

The MySQL database is called `appdbproj`.

It contains the following tables:

### `company`

Stores company details.

Example fields:

- `companyID`
- `companyName`
- `industry`

### `attendee`

Stores attendee details.

Example fields:

- `attendeeID`
- `attendeeName`
- `attendeeDOB`
- `attendeeGender`
- `attendeeCompanyID`

### `room`

Stores room details.

Example fields:

- `roomID`
- `roomName`
- `capacity`

### `session`

Stores conference session details.

Example fields:

- `sessionID`
- `sessionTitle`
- `speakerName`
- `sessionDate`
- `roomID`

### `registration`

Stores which attendees are registered for which sessions.

Example fields:

- `registrationID`
- `attendeeID`
- `sessionID`
- `registeredAt`

## Neo4j Database

The Neo4j database stores attendee connection data.

Each attendee node has an `AttendeeID` property.

Example node:

`(:Attendee {AttendeeID: 101})`

Attendees may be linked by a `CONNECTED_TO` relationship.

Example relationship:

`(:Attendee {AttendeeID: 101})-[:CONNECTED_TO]->(:Attendee {AttendeeID: 109})`

The application treats this relationship as undirected, so connections are searched using:

`(a)-[:CONNECTED_TO]-(connected)`

rather than only checking one direction.

## Input Validation and Error Handling

The application includes validation for the main user input conditions described in the project brief.

Examples include:

- Non-numeric company IDs
- Non-existent company IDs
- Existing attendee IDs when adding a new attendee
- Invalid gender values
- Invalid attendee IDs
- Non-existent attendee IDs
- Attempts to connect an attendee to themselves
- Attempts to create a duplicate attendee connection

Database errors are caught where appropriate and displayed to the user.

## Highlights and Challenges

### Working with Two Databases

A key part of the project was using both MySQL and Neo4j in the same Python application. MySQL stores the structured conference data, while Neo4j stores the graph-based attendee connections.

### Combining MySQL and Neo4j Data

For the connected attendee features, the application uses Neo4j to find connections and MySQL to retrieve attendee names. This means the program combines data from both databases using attendee IDs.

### Directionless Relationships

The `CONNECTED_TO` relationship in Neo4j is treated as directionless for this project. The Cypher queries use an undirected relationship pattern so that connections are found regardless of which direction the relationship was originally created in.

### Room Caching

The rooms are loaded when the application starts and stored in memory. This was done to meet the requirement that rooms manually added after option 6 is first chosen should not appear until the application is restarted.

### Menu-Based Application Structure

The project is organised as a command-line menu application. Helper functions are used for repeated tasks such as retrieving attendees from MySQL, checking Neo4j connections, and creating new relationships.

## Limitations

The application assumes that the MySQL and Neo4j databases have already been imported and are running before the program starts.

The database connection settings are stored at the top of `main.py`. If the database username, password, or Neo4j password is different on another machine, these values may need to be updated.

The application is intended as a college project to demonstrate Python, SQL, MySQL, Neo4j, Cypher, and working with two different database systems.

## References

I used the module lecture notes, class materials, and the project specification as a guide when completing this project.

I also used the following documentation and references:

- [MySQL Documentation](https://dev.mysql.com/doc/)
- [MySQL Connector/Python Documentation](https://dev.mysql.com/doc/connector-python/en/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Neo4j Python Driver Manual](https://neo4j.com/docs/python-manual/current/)
- [Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Python Documentation](https://docs.python.org/3/)
