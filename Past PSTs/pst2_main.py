# pst2_main.py - The Persistent Application

import json
import datetime

DATA_FILE = "msms.json"
app_data = {} # This global dictionary will hold ALL our data.

# --- Core Persistence Engine ---
def load_data(path=DATA_FILE):
    """Loads all application data from a JSON file."""
    global app_data
    try:
        with open(path, 'r') as f:
            # Use json.load(f) to load the file's content into the global 'app_data' variable.
            app_data = json.load(f)
            print("Data loaded successfully.")
    except FileNotFoundError:
        print("Data file not found. Initializing with default structure.")
        # If the file doesn't exist, initialize 'app_data' with a default dictionary.
        # It should have keys like: "students", "teachers", "attendance", "next_student_id", "next_teacher_id".
        # The lists should be empty and the IDs should start at 1.
        app_data = {
            "students": [],
            "teachers": [],
            "attendance": [],
            "next_student_id": 1,
            "next_teacher_id": 1
        }

def save_data(path=DATA_FILE):
    """Saves all application data to a JSON file."""
    # Open the file at 'path' in write mode ('w').
    # Use json.dump() to write the global 'app_data' dictionary to the file.
    # Use the 'indent=4' argument in json.dump() to make the file readable.
    with open(path, 'w') as f:
        json.dump(app_data, f, indent=4)
    print("Data saved successfully.")

# --- Full CRUD for Core Data ---
# Note: We are now working with lists of dictionaries, not lists of objects.

def add_teacher(name, speciality):
    """Adds a teacher dictionary to the data store."""
    #Get the next teacher ID from app_data['next_teacher_id'].
    teacher_id = app_data['next_teacher_id']
    #Create a new teacher dictionary with 'id', 'name', and 'speciality' keys.
    new_teacher = {"teacher_id": teacher_id, "name": name, "speciality": speciality}
    #Append the new dictionary to the app_data['teachers'] list.
    app_data['teachers'].append(new_teacher)
    #Increment the 'next_teacher_id' in app_data.
    app_data['next_teacher_id'] += 1
    print(f"Core: Teacher '{name}' added.")

def update_teacher(teacher_id, **fields):
    """Finds a teacher by ID and updates their data with provided fields."""
    # Loop through the app_data['teachers'] list.
    for teacher in app_data['teachers']:
        # If a teacher's 'id' matches teacher_id:
        if teacher['teacher_id'] == teacher_id:
            # Use the .update() method on the teacher dictionary to apply the 'fields'.
            teacher.update(fields)
            print(f"Teacher {teacher_id} updated.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")

def remove_teacher(teacher_id):
    """Removes a teacher from the data store."""
    # Find the teacher dictionary in app_data['teacher'] with the matching ID.
    for teacher in app_data['teachers']:
    # If found, use the .remove() method on the list to delete it.
        if teacher['teacher_id'] == teacher_id:
            app_data['teachers'].remove(teacher)
            print(f"Teacher {teacher_id} deleted.")
            return
    print(f"Error: Teacher with ID {teacher_id} not found.")
    
def add_student(name, enrolled_in):
    """Adds a student dictionary to the data store."""
    #Get the next student ID from app_data['next_student_id'].
    student_id = app_data['next_student_id']
    #Create a new student dictionary with 'id', 'name', and 'speciality' keys.
    new_student = {"student_id": student_id, "name": name, "enrolled_in": [enrolled_in]}
    #Append the new dictionary to the app_data['students'] list.
    app_data['students'].append(new_student)
    #Increment the 'next_student_id' in app_data.
    app_data['next_student_id'] += 1
    print(f"Core: Student '{name}' added.")

def update_student(student_id, **fields):
    """Finds a student by ID and updates their data with provided fields."""
    # Loop through the app_data['students'] list.
    for student in app_data['students']:
        # If a student's 'id' matches student_id:
        if student['student_id'] == student_id:
            # Use the .update() method on the student dictionary to apply the 'fields'.
            student.update(fields)
            print(f"Student {student_id} updated.")
            return
    print(f"Error: Student with ID {student_id} not found.")

def remove_student(student_id):
    """Removes a student from the data store."""
    # Find the student dictionary in app_data['student'] with the matching ID.
    for student in app_data['students']:
    # If found, use the .remove() method on the list to delete it.
        if student['student_id'] == student_id:
            app_data['students'].remove(student)
            print(f"Student {student_id} deleted.")
            return
    print(f"Error: Student with ID {student_id} not found.")
    pass
 
def list_students():
    """Prints all students in the database."""
    print("\n--- Student List ---")
    if not app_data['students']:
        print("No students in the system.")
        return
    # Loop through student_db. For each student, print their ID, name, and their enrolled_in list.
    for student in app_data['students']:
        print(f"  ID: {student['student_id']}, Name: {student['name']}, Enrolled in: {student['enrolled_in']}")

def list_teachers():
    """Prints all teachers in the database."""
    # Implement the logic to list all teachers, similar to list_students().
    print("\n--- Teacher List ---")
    if not app_data['teachers']:
        print("No teachers in the system.")
        return
    for teacher in app_data['teachers']:
        print(f"  ID: {teacher['teacher_id']}, Name: {teacher['name']}, Speciality: {teacher['speciality']}")

def find_students(term):
    """Finds students by name."""
    print(f"\n--- Finding Students matching '{term}' ---")
    # Create an empty list to store results.
    matches_list = []
    # Loop through student_db. If the search 'term' (case-insensitive) is in the student's name,
    # add them to your results list.
    for student in app_data['students']:
        if term.lower() in student['name'].lower():
            matches_list.append(student)

    # After the loop, if the results list is empty, print "No match found."
    # Otherwise, print the details for each student in the results list.
    if not matches_list:
        print("No match found.")
    else:
        for student in matches_list:
            print(f"  ID: {student['student_id']}, Name: {student['name']}, Enrolled in: {student['enrolled_in']}")



def find_teachers(term):
    """Finds teachers by name or speciality."""
    print(f"\n--- Finding teachers matching '{term}' ---")
    # Implement this function similar to find_students, but check
    # for the term in BOTH the teacher's name AND their speciality.

    # Create an empty list to store results.
    matches_list = []
    # Loop through teacher_db. If the search 'term' (case-insensitive) is in the teacher's name or specialty,
    # add them to your results list.
    for teacher in app_data['teachers']:
        if (term.lower() in teacher['name'].lower()) or (term.lower() in teacher['speciality'].lower()):
            matches_list.append(teacher)

    # After the loop, if the results list is empty, print "No match found."
    # Otherwise, print the details for each student in the results list.
    if not matches_list:
        print("No match found.")
    else:
        for teacher in matches_list:
            print(f"  ID: {teacher['teacher_id']}, Name: {teacher['name']}, Speciality: {teacher['speciality']}")


# --- Front Desk Functions  ---
def find_student_by_id(student_id):
    """A new helper to find one student by their exact ID."""
    # Loop through student_db. If a student's ID matches student_id, return the student object.
    for student in app_data['students']:
        if student['student_id'] == student_id:
            return student
    # If the loop finishes without finding a match, return None.
    return None

def front_desk_lookup(term):
    """High-level function to search everything."""
    print(f"\n--- Performing lookup for '{term}' ---")
    find_students(term)
    find_teachers(term)

def check_in(student_id, course_id, timestamp=None):
    """Records a student's attendance for a course."""
    if timestamp is None:
        # Get the current time as a string using datetime.datetime.now().isoformat()
        timestamp = datetime.datetime.now().isoformat()
    
    # Create a check-in record dictionary.
    # It should contain 'student_id', 'course_id', and 'timestamp'.
    check_in_record = {
        "student_id": student_id,
        "course_id": course_id,
        "timestamp": timestamp
    }
    # Append this new record to the app_data['attendance'] list.
    app_data['attendance'].append(check_in_record)
    print(f"Receptionist: Student {student_id} checked into {course_id}.")

def print_student_card(student_id):
    """Creates a text file badge for a student."""
    # Find the student dictionary in app_data['students'].
    student_to_print = None
    for s in app_data['students']:
        if s['student_id'] == student_id:
            student_to_print = s
            break
    
    if student_to_print:
        # Create a filename, e.g., f"{student_id}_card.txt".
        filename = f"{student_id}_card.txt"
        # Open the file in write mode ('w').
        with open(filename, 'w') as f:
            # Write the student's details to the file in a nice format.
            f.write("========================\n")
            f.write(f"  MUSIC SCHOOL ID BADGE\n")
            f.write("========================\n")
            f.write(f"ID: {student_to_print['student_id']}\n")
            f.write(f"Name: {student_to_print['name']}\n")
            f.write(f"Enrolled In: {', '.join(student_to_print.get('enrolled_in', []))}\n")
        print(f"Printed student card to {filename}.")
    else:
        print(f"Error: Could not print card, student {student_id} not found.")


# --- Main Application Loop ---
def main():
    """Main function to run the MSMS application."""
    load_data() # Load all data from file at startup.

    while True:
        print("\n===== MSMS v2 (Persistent) =====")
        print("1. Check-in Student")
        print("2. Print Student Card")
        print("3. Register New Student")
        print("4. Update Student Info")
        print("5. Remove Student")
        print("6. Register New Teacher")
        print("7. Update Teacher Info")
        print("8. Remove Teacher")
        print("9. Lookup Student or Teacher")
        print("10. (Admin) List all Students")
        print("11. (Admin) List all Teachers")

        print("q. Quit and Save")
        
        choice = input("Enter your choice: ")
        
        made_change = False # A flag to track if we need to save
        if choice == '1':
            # Get student_id and course_id from user, then call check_in().
            student_id = input("Enter student ID to check in: ")
            course_id = input("Enter course ID: ")
            check_in(student_id, course_id)
            made_change = True
        elif choice == '2':
            # Get student_id, then call print_student_card().
            student_id = int(input("Enter student ID you wish to print a student card for: "))
            print_student_card(student_id)
            pass # No change made, so no save needed
        elif choice == '3':
            # Get name and what they will be enrolled in then call add_student().
            name = input("Enter name of new student: ")
            enrolled_in = input("Enter class to enroll new student in: ")
            add_student(name, enrolled_in)
            made_change = True
        elif choice == '4':
            # Get student_id and new details, then call update_student().
            # Example: update_student(1, enrolled_in="Advanced Piano")
            student_id = int(input("Enter student ID you wish to update: "))
            new_enrol = input("Enter new class to enroll in: ")
            update_student(student_id, enrolled_in=[new_enrol])
            made_change = True
        elif choice == '5':
            # Get student_id, then call remove_student().
            student_id = int(input("Enter student ID you wish to remove: "))
            remove_student(student_id)
            made_change = True
        elif choice == '6':
            # Get name and what their speciality then call add_teacher().
            name = input("Enter name of new teacher: ")
            speciality = input("Enter speciality of new teacher in: ")
            add_teacher(name, speciality)
            made_change = True
        elif choice == '7':
            # Get teacher_id and new details, then call update_teacher().
            # Example: update_teacher(1, speciality="Advanced Piano")
            teacher_id = int(input("Enter teacher ID you wish to update: "))
            new_specialty = input("Enter new specialty: ")
            update_teacher(teacher_id, speciality=new_specialty)
            made_change = True
        elif choice == '8':
            # Get teacher_id, then call remove_teacher().
            teacher_id = int(input("Enter teacher ID you wish to remove: "))
            remove_teacher(teacher_id)
            made_change = True
        elif choice == '9':
            # Prompt for a search term, then call front_desk_lookup.
            term = input("Enter search term: ")
            front_desk_lookup(term)
            pass # No change made, so no save needed
        elif choice == '10':
            #lists all students
            list_students()
            pass # No change made, so no save needed
        elif choice == '11':
            #lists all teachers
            list_teachers()
            pass # No change made, so no save needed
        elif choice.lower() == 'q':
            print("Saving final changes and exiting.")
            break
        else:
            print("Invalid choice.")
            
        if made_change:
            save_data() # Save the data immediately after any change.

    save_data() # One final save on exit.

# --- Program Start ---
if __name__ == "__main__":
    main()