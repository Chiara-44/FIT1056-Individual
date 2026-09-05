# PST - Chiara Gillam - 33117810

## History
PST1 adds a few key core funcitonalities to the MSMS system.

PST2 adds a persistence model to the app and adds new functionalities such as the ability to print student cards, a full CRUD system and a check in list


## The new persistence data model
The program uses a JSON file to store data across app launches.

There are 5 dictionary items storing different data saved in the MSMS.JSON file 
 
The ***"students"*** key stores a list of students. Each student entry is a dictionary storing three values, Student ID, name and what instrument classes they are enrolled in

The ***"teachers"*** key stores a list of teachers. Each teacher entry is a dictionary storing three values,name, teacher ID and specialty 

The ***"attendence"*** key stores a list of each check-in that has been recorded. It contains a dictionary with student_id course_id and timestamp of when they checked in.

The last two are the next student IDs available for teachers and students.


## Core Helper Functions
These are the core functions that help the program run
The app provides the ability to Create, read, update, and delete all student and teacher instances (CRUD).


***add_teacher*** - Takes name and specialty as arguments and creates a teacher list of dicts and adds it to the database.

***update_teacher*** - takes teacher ID and a key value dict pair for any field you want to edit for a given teacher.

***remove_teacher*** - takes teacher ID and removes teacher with that ID from the database.

***add_student*** - Takes name and what to enrol in as arguments and creates a student list of dicts and adds it to the database.


***update_student*** - takes student ID and a key value dict pair for any field you want to edit for a given student.

***remove_student*** - takes student ID and removes student with that ID from the database.

***list_students*** - Prints all students in the database.

***list_teachers*** - Prints all teachers in the database.

***find_students*** - Takes a key word and finds students by name. Function is case insensitive and will match any substring.

***find_teachers*** - Takes a key word and finds teacher by name or specialty. Function is case insensitive and will match any substring.


## Front Desk Functions 

***find_student_by_id*** - Takes a student ID and finds one student by their exact ID. 

***front_desk_lookup*** - Takes a key word and finds teachers by name or specialty and any students names that match. Function is case insensitive and will match any substring.

***check_in*** - Takes a student ID and creates a text file badge for a student.

***print_student_card*** - Takes a student ID, course ID and optionally a timestamp and records a student's attendance for a course.




## Main Application
The main application starts off by loading in the data from the JSON file. It is a for loop with a main menu. it gives 11 options to pick from. This includes checking in a student, Printing a student card, registering a new student, updating an existing student, removing a student, registering a new teacher, updating an existing teacher, removing a teacher, student and teacher lookup, listing all students, listing all teachers, with an option to quit the program when finished. Each option will then guide the user to input the arguments needed to fulfill those function. The program will save changes if there are any made and will save before quitting as well.

## Running the application
The application is designed to run in python 3.14. running the application is as simple as executing the pst2_main.py file and the GUI can be seen in the terminal. Interacting with the GUI is done through the terminal as well.

