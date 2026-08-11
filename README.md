# PST - Chiara Gillam - 33117810

## PST1 
PST1 adds a few key core funcitonalities to the MSMS system.

### Data Models and In-Memory Databases 
There are two classes for storing data. A teacher class and a Student class. 

**Student class** - Stores three data types, Student ID, name and what instrument classes they are enrolled in. It is initialised with only a name and ID 

**Teacher class**  - Stores three data types, name, teacher ID and specialty. It is initialised with all three

There is a list for storing class instances for each class and global variables for what the next id for each is.


### Core Helper Functions
These are the core functions that help the program run

***add_teacher*** - Takes name and specialty as arguments and creates a teacher object and adds it to the database.

***list_students*** - Prints all students in the database.

***list_teachers*** - Prints all teachers in the database.

***find_students*** - Takes a key word and finds students by name. Function is case insensitive and will match any substring.

***find_teachers*** - Takes a key word and finds teacher by name or specialty. Function is case insensitive and will match any substring.

### Front Desk Functions 

***find_student_by_id*** - Takes a student ID and finds one student by their exact ID. 

**front_desk_register*** - Takes a name and instrument and registers and enrols them.

***front_desk_enrol*** - Takes a student ID and instrument and enrols an existing student in a course.

***front_desk_lookup*** - Takes a key word and finds teachers by name or specialty and any students names that match. Function is case insensitive and will match any substring.

### Main Application
The main application is a for loop with a main menu. it gives six options to pick from. The include registering new students, enrolling existing ones into classes, looking up either students or teachers, and viewing full lists of all students or all teachers for administrative purposes, with an option to quit the program when finished. Each option will then guide the user to input the arguments needed to fulfill those function.

### Running the application
The application is designed to run in python 3.14. running the application is as simple as executing the MSMS.py file and the GUI can be seen in the terminal. Interacting with the GUI is done through the terminal as well.