# PST - Chiara Gillam - 33117810

## History
PST1 adds a few key core funcitonalities to the MSMS system.

PST2 adds a persistence model to the app and adds new functionalities such as the ability to print student cards, a full CRUD system and a check in list

PST3 rebuilds the project with a professional Object-Oriented (OOP) design

PST4 Replace the text console with a modern Graphical User
Interface (GUI).

## The persistence data model and object oriented data structure
All application data is stored in a single JSON file (data/msms.json), organized under five top-level keys:

**students** — a list of student records, each storing a student ID, name, and the list of courses they're enrolled in.

**teachers** — a list of teacher records, each storing a teacher ID, name, and speciality.

**courses** — a list of course records, each storing a course ID, name, instrument, assigned teacher ID, enrolled student IDs, and a list of scheduled lessons (day, time, room).

**attendance** — a list of check-in records, each capturing a student ID, course ID, and a timestamp of when the check-in occurred.

**next_student_id**, **next_teacher_id**, **next_lesson_id** — counters used to auto-assign the next available ID when a new student, teacher, or lesson is created, so IDs are never reused or duplicated.

On startup, ScheduleManager reads this file and rebuilds the raw dictionaries into StudentUser, TeacherUser, and Course objects. On every change, it converts these objects back into dictionaries and writes the full file back to disk, so the JSON file always reflects the current in-memory state.


## Core Helper Functions in schedule.py
These are the core functions that help the program run.
The app provides the ability to Create, Read, Update, and Delete all student, teacher, and course instances (CRUD).
 
***build_students, build_teachers, build_courses*** - Convert the raw dictionaries loaded from the JSON file into `StudentUser`, `TeacherUser`, and `Course` objects respectively, so the rest of the program can work with objects instead of plain dicts.
 
***add_teacher*** - Takes name and specialty as arguments and creates a new teacher, adding it to the database.
 
***update_teacher*** - Takes teacher ID and a key value dict pair for any field you want to edit for a given teacher.
 
***remove_teacher*** - Takes teacher ID and removes teacher with that ID from the database.
 
***add_student*** - Takes name and a list of course IDs to enrol in as arguments and creates a new student, adding it to the database. Also updates the enrolled course(s) so their rosters include the new student.
 
***update_student*** - Takes student ID and a key value dict pair for any field you want to edit for a given student. If enrolment is being changed, also syncs the old and new courses' rosters to match.
 
***remove_student*** - Takes student ID and removes student with that ID from the database, and removes them from every course roster they were part of.
 
***list_students*** - Prints all students in the database.
 
***list_teachers*** - Prints all teachers in the database.
 
***find_students*** - Takes a key word and finds students by name. Function is case insensitive and will match any substring.
 
***find_teachers*** - Takes a key word and finds teacher by name or specialty. Function is case insensitive and will match any substring.
 
***add_course*** - Takes a course ID, name, instrument, and optionally a teacher ID and creates a new course with no students enrolled and no lessons scheduled yet.
 
***add_lesson_to_course*** - Takes a course ID, day, start time, and room, and adds a new lesson slot to an existing course's schedule.
 
***switch_student_course*** - Takes a student ID and two course IDs (the course they're leaving and the course they're joining) and moves the student between them, keeping both the student's own record and both courses' rosters in sync.

***find_courses_by_instrument*** - Returns all courses for an instrument (case-insensitive).
 
***def front_desk_daily_roster(self, day)*** - Returns all lessons on a given day.

## Front Desk Functions
 
***find_student_by_id*** - Takes a student ID and finds one student by their exact ID.
 
***find_teacher_by_id*** - Takes a teacher ID and finds one teacher by their exact ID.
 
***find_course_by_id*** - Takes a course ID and finds one course by its exact ID.
 
***get_lessons_for_day*** - Takes a day of the week and returns every scheduled lesson that falls on it, paired with its course.
 
***front_desk_lookup*** - Takes a key word and finds teachers by name or specialty and any students names that match. Function is case insensitive and will match any substring.
 
***check_in*** - Takes a student ID and a course ID and records a student's attendance for a course, after validating that both exist.
 
***print_student_card*** - Takes a student ID and creates a text file badge for that student.


## Project Structure
 
```
app/
  user.py        - base User class
  student.py     - StudentUser class (inherits from User)
  teacher.py     - TeacherUser and Course classes
  schedule.py    - ScheduleManager: the controller layer described above
data/
  msms.json      - persistent data store
gui/
  course_pages.py   - code for how the course page looks and works in the gui
  main_dashboard.py - Streamlit setup and how navigation of site works
  roster_pages.py   - code for how the roster page looks and works in the gui
  student_pages.py  - code for how the student page looks and works in the gui
  teacher_pages.py  - code for how the teacher page looks and works in the gui

main.py           - the view layer: menu loop and user interaction
```
 
## Menu Overview

```
├── Student Management
│   ├── Find a Student by Name
│   ├── Register New Student
│   ├── Update Student Info
│   ├── Remove Student
│   ├── All Students
├── Teacher Management
│   ├── Find a Teacher by Name or Specialty
│   ├── Register New Teacher
│   ├── Update Teacher Info
│   ├── Remove Teacher
│   ├── All Teachers
│   └── b. Back to Main Menu
├── Course Management
│   ├── Add New Course
│   ├── Add Lesson to Course
|── Daily Roster
│   ├── Daily Roster
│   ├── Student Check in
|── Payments
│   ├── To be implemented in PST5


```



## Main Application
The main.py application launches the streamlit site that is defined in main_dashboard.py. The application then reads from the msms.json and constructs the necessary structs from it to be stored in working memory. The navigation menu is simple to follow and for each class there are CRUD options to edit Students, Teachers and Courses. The full navigation stack is described above. Each option guides the user to input the arguments needed to fulfil that function. The program saves changes immediately after any change is made, rather than waiting until the user quits.

## Running the application
The application is designed to run in python 3.14. running the application is as simple as executing the following command at the directory root:
```
streamlit run main.py
```
 The GUI can be seen in a browser at http://localhost:8501/
