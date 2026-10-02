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
        self.next_lesson_id = 1
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
                self.next_lesson_id = data.get("next_lesson_id", 1)

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
            "next_lesson_id": self.next_lesson_id,
        }
        # Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def build_students(self, student_dicts):
        """Converts a list of raw student dictionaries into StudentUser objects."""
        students = []
        for student_dict in student_dicts:
            id = student_dict["student_id"]
            name = student_dict["name"]
            enrolled_in = student_dict.get("enrolled_in", [])
            students.append(StudentUser(id, name, enrolled_in))
        return students

    def build_teachers(self, teacher_dicts):
        """Converts a list of raw teacher dictionaries into TeacherUser objects."""
        teachers = []
        for teacher_dict in teacher_dicts:
            id = teacher_dict["teacher_id"]
            name = teacher_dict["name"]
            speciality = teacher_dict["speciality"]
            teachers.append(TeacherUser(id, name, speciality))
        return teachers

    def build_courses(self, course_dicts):
        """Converts a list of raw course dictionaries into Course objects."""
        courses = []
        for course_dict in course_dicts:
            course_id = course_dict["course_id"]
            name = course_dict["name"]
            instrument = course_dict["instrument"]
            teacher_id = course_dict.get("teacher_id")
            enrolled_student_ids = course_dict.get("enrolled_student_ids", [])
            lessons = course_dict.get("lessons", [])
            courses.append(Course(course_id, name, instrument, teacher_id,
                                enrolled_student_ids, lessons))
        return courses

    def add_teacher(self, name, speciality):
        """Adds a teacher dictionary to the data store."""
        #Create a new TeacherUser object with 'id', 'name', and 'speciality'
        teacher = TeacherUser(self.next_teacher_id, name, speciality)
        #Append the new object to the teachers list.
        self.teachers.append(teacher)
        #Increment the 'next_teacher_id'
        self.next_teacher_id += 1
        self._save_data()
        print(f"Core: Teacher '{name}' added.")

    def update_teacher(self, id, **fields):
        """Finds a teacher by ID and updates their data with provided fields."""
        # Loop through the teachers list.
        for teacher in self.teachers:
            # If a teacher's 'id' matches id:
            if teacher.teacher_id == id:
                # Update fields
                for key, value in fields.items():
                    setattr(teacher, key, value)
                print(f"Teacher {id} updated.")
                self._save_data()
                return True
        print(f"Error: Teacher with ID {id} not found.")
        return False

    def remove_teacher(self, id):
        """Removes a teacher from the data store."""
        # Find the teacher with the matching ID.
        for teacher in self.teachers:
        # If found, use the .remove() method on the list to delete it.
               if teacher.teacher_id == id:
                self.teachers.remove(teacher)
                print(f"Teacher {id} deleted.")
                self._save_data()
                return True
        print(f"Error: Teacher with ID {id} not found.")
        return False
        
    def add_student(self, name, enrolled_in):
        """enrolled_in should be a list of course IDs (ints) the student is enrolling in."""
        student = StudentUser(self.next_student_id, name, enrolled_in)
        self.students.append(student)

        for course_id in enrolled_in:
            course = self.find_course_by_id(course_id)
            if course:
                course.enrolled_student_ids.append(student.student_id)
            else:
                print(f"Warning: Course {course_id} not found — student enrolled in name only.")

        self.next_student_id += 1
        print(f"Core: Student '{name}' added.")
        self._save_data()
        return student

    def update_student(self, student_id, **fields):
        """Finds a student by ID and updates their data with provided fields.
        If 'enrolled_in' is being changed, also syncs the old/new courses' rosters."""
        for student in self.students:
            if student.student_id == student_id:

                if "enrolled_in" in fields:
                    old_courses = student.enrolled_in
                    new_courses = fields["enrolled_in"]

                    # Remove the student from courses they're leaving.
                    for course_id in old_courses:
                        if course_id not in new_courses:
                            course = self.find_course_by_id(course_id)
                            if course and student_id in course.enrolled_student_ids:
                                course.enrolled_student_ids.remove(student_id)

                    # Add the student to courses they're newly joining.
                    for course_id in new_courses:
                        if course_id not in old_courses:
                            course = self.find_course_by_id(course_id)
                            if course and student_id not in course.enrolled_student_ids:
                                course.enrolled_student_ids.append(student_id)

                for key, value in fields.items():
                    setattr(student, key, value)

                print(f"Student {student_id} updated.")
                self._save_data()
                return True
        print(f"Error: Student with ID {student_id} not found.")
        return False

    def remove_student(self, student_id):
        """Removes a student, and also removes them from every course's roster."""
        for student in self.students:
            if student.student_id == student_id:
                for course in self.courses:
                    if student_id in course.enrolled_student_ids:
                        course.enrolled_student_ids.remove(student_id)
                self.students.remove(student)
                print(f"Student {student_id} deleted.")
                self._save_data()
                return True
        print(f"Error: Student with ID {student_id} not found.")
        return False

    
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
            return False
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
    def find_student_by_id(self, id):
        """A new helper to find one student by their exact ID."""
        # Loop through students list. If a student's ID matches id, return the 
        # student object.
        for student in self.students:
            if student.student_id == id:
                return student
        # If the loop finishes without finding a match, return None.
        print("No Matches found")
        return None

    def find_teacher_by_id(self, id):
        for teacher in self.teachers:
            if teacher.teacher_id == id:
                return teacher
        return None

    def front_desk_lookup(self, term):
        """High-level function to search everything."""
        print(f"\n--- Performing lookup for '{term}' ---")
        self.find_students(term)
        self.find_teachers(term)


    def print_student_card(self, id):
        """Creates a text file badge for a student."""
        # Find the student
        student_to_print = None
        student_to_print = self.find_student_by_id(id)
        
        if student_to_print:
            # Create a filename, e.g., f"{id}_card.txt".
            filename = f"{id}_card.txt"
            # Open the file in write mode ('w').
            data = (
                # Write the student's details to the file in a nice format.
                "========================\n"
                "  MUSIC SCHOOL ID BADGE\n"
                "========================\n"
                "ID: {student_to_print.student_id}\n"
                "Name: {student_to_print.name}\n"
                "Enrolled In: {', '.join(str(c) for c in student_to_print.enrolled_in)}\n"
            )
            print(f"Printed student card to {filename}.")
            return(filename, data)
        else:
            print(f"Error: Could not print card, student {id} not found.")
            return None

    def check_in(self, id, course_id):
        """Records a student's attendance for a course after validation."""
        student = self.find_student_by_id(id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            print("Error: Check-in failed. Invalid Student or Course ID.")
            return False
            
        timestamp = datetime.datetime.now().isoformat()
        check_in_record = {"student_id": id, "course_id": course_id, "timestamp": timestamp}
        
        # This line will now work without causing an AttributeError.
        self.attendance_log.append(check_in_record)
        self._save_data() # Save the attendance log.
        print(f"Success: Student {student.name} checked into {course.name}.")
        return True

    def find_course_by_id(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def get_lessons_for_day(self, day):
        """Returns a list of (course, lesson) pairs scheduled on the given day."""
        result = []
        for course in self.courses:
            for lesson in course.lessons_on_day(day):
                result.append((course, lesson))
        return result

    def add_course(self, course_id, name, instrument, id=None):
        """Creates a new course with no students enrolled and no lessons yet."""
        # Validate course does not exist already
        if self.find_course_by_id(course_id) is not None:
            print(f"Error: Course ID {course_id} already exists.")
            return 101

        if self.find_teacher_by_id(id) is None:
           print(f"Error: teacher with ID {id} not found")
           return 102
            
        course = Course(course_id, name, instrument, id,
                        enrolled_student_ids=[], lessons=[])
        self.courses.append(course)
        print(f"Core: Course '{name}' added.")
        self._save_data()
        return True

    def add_lesson_to_course(self, course_id, day, start_time, room):
        """Adds a new lesson slot to an existing course."""
        course = self.find_course_by_id(course_id)
        if not course:
            print(f"Error: Course {course_id} not found.")
            return False

        lesson_id = self.next_lesson_id
        self.next_lesson_id += 1
        course.lessons.append({
            "lesson_id": lesson_id,
            "day": day,
            "start_time": start_time,
            "room": room,
        })
        self._save_data()
        print(f"Lesson added to '{course.name}' on {day} at {start_time}.")
        return lesson_id

        
    def switch_student_course(self, student_id, from_course_id, to_course_id):
        """Moves a student from one course to another, keeping both
        StudentUser.enrolled_in and Course.enrolled_student_ids in sync."""
        student = self.find_student_by_id(student_id)
        from_course = self.find_course_by_id(from_course_id)
        to_course = self.find_course_by_id(to_course_id)

        if not student:
            print(f"Error: Student {student_id} not found.")
            return False
        if not from_course or not to_course:
            print("Error: Invalid course ID(s).")
            return False
        if student_id not in from_course.enrolled_student_ids:
            print(f"Error: Student {student_id} is not enrolled in course {from_course_id}.")
            return False

        # Update the course rosters.
        from_course.enrolled_student_ids.remove(student_id)
        to_course.enrolled_student_ids.append(student_id)

        # Update the student's own record to match.
        if from_course_id in student.enrolled_in:
            student.enrolled_in.remove(from_course_id)
        if to_course_id not in student.enrolled_in:
            student.enrolled_in.append(to_course_id)

        self._save_data()
        print(f"Success: {student.name} switched from '{from_course.name}' to '{to_course.name}'.")
        return True

    def find_courses_by_instrument(self, instrument):
        """Returns all courses for an instrument (case-insensitive)."""
        return [c for c in self.courses
                if c.instrument.lower() == instrument.strip().lower()]

    def front_desk_daily_roster(self, day):
        """Displays a pretty table of all lessons on a given day."""
        # print(f"\n--- Daily Roster for {day} ---")
        lessons = self.get_lessons_for_day(day)

        if not lessons:
            print("No lessons scheduled for this day.")
            return

        rows = []
        for course, lesson in lessons:
            teacher = self.find_teacher_by_id(course.teacher_id)
            teacher_name = teacher.name if teacher else "Unassigned"
            # print(f"  {lesson['start_time']} - {course.name} ({course.instrument}) "
                # f"- Teacher: {teacher_name} - Room: {lesson['room']}")
            rows.append({"time": lesson['start_time'], "name": course.name, "instrument": course.instrument, 
                    "teacher": teacher_name, "room":lesson['room']})
        return rows