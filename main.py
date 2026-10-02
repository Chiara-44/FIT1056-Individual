# main.py - The View Layer
from app.schedule import ScheduleManager
from gui.main_dashboard import launch

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    lessons = manager.get_lessons_for_day(day)

    if not lessons:
        print("No lessons scheduled for this day.")
        return

    for course, lesson in lessons:
        teacher = manager.find_teacher_by_id(course.teacher_id)
        teacher_name = teacher.name if teacher else "Unassigned"
        print(f"  {lesson['start_time']} - {course.name} ({course.instrument}) "
              f"- Teacher: {teacher_name} - Room: {lesson['room']}")


def student_menu(manager):
    while True:
        print("\n--- Student Management ---")
        print("1. Register New Student")
        print("2. Update Student Info")
        print("3. Remove Student")
        print("4. List All Students")
        print("b. Back to Main Menu")
        # print_student_card removed - now on main menu

        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter name of new student: ")
            raw = input("Enter class ID(s) to enroll in (comma-separated, e.g. 101,102): ")
            enrolled_in = [int(c.strip()) for c in raw.split(",") if c.strip()]
            manager.add_student(name, enrolled_in)
        elif choice == '2':
            student_id = int(input("Enter student ID to update: "))
            raw = input("Enter new class ID(s), comma-separated: ")
            new_enrol = [int(c.strip()) for c in raw.split(",") if c.strip()]
            manager.update_student(student_id, enrolled_in=new_enrol)
        elif choice == '3':
            student_id = int(input("Enter student ID to remove: "))
            manager.remove_student(student_id)
        elif choice == '4':
            manager.list_students()
        elif choice.lower() == 'b':
            break
        else:
            print("Invalid choice.")

def teacher_menu(manager):
    while True:
        print("\n--- Teacher Management ---")
        print("1. Register New Teacher")
        print("2. Update Teacher Info")
        print("3. Remove Teacher")
        print("4. List All Teachers")
        print("b. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == '1':
            name = input("Enter name of new teacher: ")
            speciality = input("Enter speciality: ")
            manager.add_teacher(name, speciality)
        elif choice == '2':
            teacher_id = int(input("Enter teacher ID to update: "))
            new_speciality = input("Enter new speciality: ")
            manager.update_teacher(teacher_id, speciality=new_speciality)
        elif choice == '3':
            teacher_id = int(input("Enter teacher ID to remove: "))
            manager.remove_teacher(teacher_id)
        elif choice == '4':
            manager.list_teachers()
        elif choice.lower() == 'b':
            break
        else:
            print("Invalid choice.")

def course_menu(manager):
    while True:
        print("\n--- Course Management ---")
        print("1. Add New Course")
        print("2. Add Lesson to Course")
        print("3. Switch Student's Course")
        print("b. Back to Main Menu")
        # check_in removed - now on main menu

        choice = input("Enter choice: ")

        if choice == '1':
            course_id = int(input("Enter new course ID: "))
            name = input("Enter course name: ")
            instrument = input("Enter instrument: ")
            teacher_id = input("Enter teacher ID (or leave blank): ")
            teacher_id = int(teacher_id) if teacher_id else None
            manager.add_course(course_id, name, instrument, teacher_id)
        elif choice == '2':
            course_id = int(input("Enter course ID: "))
            day = input("Enter day: ")
            start_time = input("Enter start time (e.g. 16:00): ")
            room = input("Enter room: ")
            manager.add_lesson_to_course(course_id, day, start_time, room)
        elif choice == '3':
            student_id = int(input("Enter student ID: "))
            from_course_id = int(input("Enter current course ID: "))
            to_course_id = int(input("Enter new course ID: "))
            manager.switch_student_course(student_id, from_course_id, to_course_id)
        elif choice.lower() == 'b':
            break
        else:
            print("Invalid choice.")

def other_menu(manager):
    while True:
        print("\n--- Other ---")
        print("1. Lookup Student or Teacher")
        print("b. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == '1':
            term = input("Enter search term: ")
            manager.front_desk_lookup(term)
        elif choice.lower() == 'b':
            break
        else:
            print("Invalid choice.")



def main():
    # """Main function to run the MSMS application."""
    # manager = ScheduleManager()  # Create ONE instance of the application brain.
    # manager._load_data()

    launch()


    # while True:
    #     print("\n===== MSMS v3 (Object-Oriented) =====")
    #     print("1. Check-in Student")
    #     print("2. Print Student Card")
    #     print("3. Student Management")
    #     print("4. Teacher Management")
    #     print("5. Course Management")
    #     print("6. Daily Roster")
    #     print("7. Other")
    #     print("q. Quit")

    #     choice = input("Enter choice: ")

    #     if choice == '1':
    #         student_id = int(input("Enter student ID: "))
    #         course_id = int(input("Enter course ID: "))
    #         manager.check_in(student_id, course_id)
    #     elif choice == '2':
    #         student_id = int(input("Enter student ID: "))
    #         manager.print_student_card(student_id)
    #     elif choice == '3':
    #         student_menu(manager)
    #     elif choice == '4':
    #         teacher_menu(manager)
    #     elif choice == '5':
    #         course_menu(manager)
    #     elif choice == '6':
    #         day = input("Enter day (e.g., Monday): ")
    #         front_desk_daily_roster(manager, day)
    #     elif choice == '7':
    #         other_menu(manager)
    #     elif choice.lower() == 'q':
    #         print("Goodbye.")
    #         break
    #     else:
    #         print("Invalid choice.")



if __name__ == "__main__":
    main()
        