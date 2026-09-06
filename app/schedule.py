import json
import datetime
from app.student import StudentUser
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        self.next_student_id = 1
        self.next_teacher_id = 1
        self._load_data()

    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # Load students, teachers, and courses as before.
                self.students = self.build_students(data.get("students", []))
                self.teachers = self.build_teachers(data.get("teachers", []))
                self.courses = self.build_courses(data.get("courses", []))

                # Plain data - no object wrapping needed, so just pull it straight out.
                self.next_student_id = data.get("next_student_id", 1)
                self.next_teacher_id = data.get("next_teacher_id", 1)

                # Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't 
                # exist.
                self.attendance_log = data.get("attendance", [])
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.__dict__ for s in self.students],
            "teachers": [t.__dict__ for t in self.teachers],
            "courses": [c.__dict__ for c in self.courses],
            # Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            "next_student_id": self.next_student_id,
            "next_teacher_id": self.next_teacher_id,
        }
        # Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def build_students(self, student_dicts):
        """Converts a list of raw student dictionaries into StudentUser objects."""
        students = []
        for student_dict in student_dicts:
            student_id = student_dict["student_id"]
            name = student_dict["name"]
            enrolled_in = student_dict.get("enrolled_in", [])
            students.append(StudentUser(student_id, name, enrolled_in))
        return students

    def build_teachers(self, teacher_dicts):
        """Converts a list of raw teacher dictionaries into TeacherUser objects."""
        teachers = []
        for teacher_dict in teacher_dicts:
            teacher_id = teacher_dict["teacher_id"]
            name = teacher_dict["name"]
            speciality = teacher_dict["speciality"]
            teachers.append(TeacherUser(teacher_id, name, speciality))
        return teachers

    def build_courses(self, course_dicts):
        """Converts a list of raw course dictionaries into Course objects."""
        courses = []
        for course_dict in course_dicts:
            course_id = course_dict["course_id"]
            name = course_dict["name"]
            teacher_id = course_dict.get("teacher_id")
            courses.append(Course(course_id, name, teacher_id))
        return courses

    def add_teacher(self, name, speciality):
        """Adds a teacher dictionary to the data store."""
        #Create a new TeacherUser object with 'id', 'name', and 'speciality'
        teacher = TeacherUser(self.next_teacher_id, name, speciality)
        #Append the new object to the teachers list.
        self.teachers.append(teacher)
        #Increment the 'next_teacher_id'
        self.next_teacher_id += 1
        print(f"Core: Teacher '{name}' added.")

    def update_teacher(self, teacher_id, **fields):
        """Finds a teacher by ID and updates their data with provided fields."""
        # Loop through the teachers list.
        for teacher in self.teachers:
            # If a teacher's 'id' matches teacher_id:
            if teacher.teacher_id == teacher_id:
                # Update fields
                for key, value in fields.items():
                    setattr(teacher, key, value)
                print(f"Teacher {teacher_id} updated.")
                return
        print(f"Error: Teacher with ID {teacher_id} not found.")

    def remove_teacher(self, teacher_id):
        """Removes a teacher from the data store."""
        # Find the teacher with the matching ID.
        for teacher in self.teachers:
        # If found, use the .remove() method on the list to delete it.
               if teacher.teacher_id == teacher_id:
                self.teachers.remove(teacher)
                print(f"Teacher {teacher_id} deleted.")
                return
        print(f"Error: Teacher with ID {teacher_id} not found.")
        
    def add_student(self, name, enrolled_in):
        """Adds a student dictionary to the data store."""
        #Create a new StudentUser object with 'id', 'name', and a list of what they're 
        # enrolled in
        student = StudentUser(self.next_student_id, name, [enrolled_in])
        #Append the new object to the students list.
        self.students.append(student)
        #Increment the 'next_srudent_id'
        self.next_student_id += 1
        print(f"Core: Student '{name}' added.")

    def update_student(self, student_id, **fields):
        """Finds a student by ID and updates their data with provided fields."""
        # Loop through the students list.
        for student in self.students:
            # If a teacher's 'id' matches teacher_id:
            if student.student_id == student_id:
                # Update fields
                for key, value in fields.items():
                    setattr(student, key, value)
                print(f"Student {student_id} updated.")
                return
        print(f"Error: Student with ID {student_id} not found.")

    def remove_student(self, student_id):
        """Removes a student from the data store."""
        # Find the student with the matching ID.
        for student in self.students:
        # If found, use the .remove() method on the list to delete it.
           if student.student_id == student_id:
                self.students.remove(student)
                print(f"Student {student_id} deleted.")
                return
        print(f"Error: Student with ID {student_id} not found.")

    
    def list_students(self):
        """Prints all students in the database."""
        print("\n--- Student List ---")
        if not self.students:
            print("No students in the system.")
            return
        for student in self.students:
            print(f"  ID: {student.student_id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")

    def list_teachers(self):
        """Prints all teachers in the database."""
        # Implement the logic to list all teachers, similar to list_students().
        print("\n--- Teacher List ---")
        if not self.teachers:
            print("No teachers in the system.")
            return
        for teacher in self.teachers:
            print(f"  ID: {teacher.teacher_id}, Name: {teacher.name}, Speciality: {teacher.speciality}")

    def find_students(self, term):
        """Finds students by name."""
        print(f"\n--- Finding Students matching '{term}' ---")
        # Using list comprehension for less lines of code
        matches = [s for s in self.students if term.lower() in s.name.lower()]
        if not matches:
            print("No match found.")
        else:
            for student in matches:
                print(f"  ID: {student.student_id}, Name: {student.name}, Enrolled in: {student.enrolled_in}")
        return matches


    def find_teachers(self, term):
        """Finds teachers by name or speciality."""
        print(f"\n--- Finding teachers matching '{term}' ---")
        # Using list comprehension for less lines of code
        matches = [t for t in self.teachers
                if term.lower() in t.name.lower() or term.lower() in t.speciality.lower()]
        if not matches:
            print("No match found.")
        else:
            for teacher in matches:
                print(f"  ID: {teacher.teacher_id}, Name: {teacher.name}, Speciality: {teacher.speciality}")
        return matches

    # --- Front Desk Functions  ---
    def find_student_by_id(self, student_id):
        """A new helper to find one student by their exact ID."""
        # Loop through students list. If a student's ID matches student_id, return the 
        # student object.
        for student in self.students:
            if student.student_id == student_id:
                return student
        # If the loop finishes without finding a match, return None.
        print("No Matches found")
        return

    def front_desk_lookup(self, term):
        """High-level function to search everything."""
        print(f"\n--- Performing lookup for '{term}' ---")
        self.find_students(term)
        self.find_teachers(term)

    def check_in(self, student_id, course_id, timestamp=None):
        """Records a student's attendance for a course."""
        if timestamp is None:
            # Get the current time as a string using datetime.datetime.now().isoformat()
            timestamp = datetime.datetime.now().isoformat()
        
        # Create a check-in record dictionary and append this new record to the app_data['attendance'] list.
        self.attendance_log.append({"student_id": student_id, "course_id": course_id, "timestamp": timestamp})
        print(f"Receptionist: Student {student_id} checked into {course_id}.")

    def print_student_card(self, student_id):
        """Creates a text file badge for a student."""
        # Find the student
        student_to_print = None
        for s in self.students:
            if s.student_id == student_id:
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
                f.write(f"ID: {student_to_print.student_id}\n")
                f.write(f"Name: {student_to_print.name}\n")
                f.write(f"Enrolled In: {', '.join(student_to_print.enrolled_in)}\n")
            print(f"Printed student card to {filename}.")
        else:
            print(f"Error: Could not print card, student {student_id} not found.")
