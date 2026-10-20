# tests/test_schedule_manager.py
import pytest
import os
import csv
from app.schedule import ScheduleManager

# A pytest fixture creates a clean environment for each test function.
@pytest.fixture
def fresh_manager():
    """Creates a fresh ScheduleManager instance using a temporary test data file."""
    test_file = "test_data.json"
    # ARRANGE: Ensure no old test file exists.
    if os.path.exists(test_file):
        os.remove(test_file)
    return ScheduleManager(data_path=test_file)

# --- Teachers ---

def test_add_teacher(fresh_manager):
    '''Tests if teacher can be added'''
    fresh_manager.add_teacher("Barkly", "Piano")
    assert len(fresh_manager.teachers) == 1
    assert fresh_manager.teachers[0].name == "Barkly"
    assert fresh_manager.teachers[0].speciality == "Piano"

def test_update_teacher(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Piano")

    result = fresh_manager.update_teacher(2, name="Barklay")
    assert result == False
    result = fresh_manager.update_teacher(1, name="Barklay")
    assert result == True
    assert len(fresh_manager.teachers) == 1
    assert fresh_manager.teachers[0].name == "Barklay"
    assert fresh_manager.teachers[0].speciality == "Piano"


def test_remove_teacher(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Piano")

    result = fresh_manager.remove_teacher(2)
    assert result == False
    result = fresh_manager.remove_teacher(1)
    assert result == True
    assert len(fresh_manager.teachers) == 0


# ---Students

def test_add_student(fresh_manager):
    '''Tests if student can be added'''
    fresh_manager.add_student("Emanuel", ["101"])
    assert len(fresh_manager.students) == 1
    assert fresh_manager.students[0].name == "Emanuel"
    assert fresh_manager.students[0].enrolled_in == ["101"]

def test_update_student(fresh_manager):
    fresh_manager.add_student("Emanuel", ["101"])

    result = fresh_manager.update_student(2, name="Emanuela")
    assert result == False
    result = fresh_manager.update_student(1, name="Emanuela")
    assert result == True
    assert len(fresh_manager.students) == 1
    assert fresh_manager.students[0].name == "Emanuela"
    assert fresh_manager.students[0].enrolled_in == ["101"]

def test_remove_student(fresh_manager):
    fresh_manager.add_student("Emanuel", ["101"])

    result = fresh_manager.remove_student(2)
    assert result == False
    result = fresh_manager.remove_student(1)
    assert result == True
    assert len(fresh_manager.students) == 0


# --- other functions ---

def test_list_students(fresh_manager):
    result = fresh_manager.list_students()
    assert result == False

    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_student("Chiara", ["103"])

    result = fresh_manager.list_students()
    assert result[0].name == "Emanuel"
    assert result[0].enrolled_in == ["101"]
    assert result[1].name == "Chiara"
    assert result[1].enrolled_in == ["103"]
    assert len(result) == 2


def test_list_teachers(fresh_manager):
    result = fresh_manager.list_teachers()
    assert result == False

    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_teacher("Heatly", "Piano")

    result = fresh_manager.list_teachers()
    assert result[0].name == "Barkly"
    assert result[0].speciality == "Guitar"
    assert result[1].name == "Heatly"
    assert result[1].speciality == "Piano"
    assert len(result) == 2

def test_find_students(fresh_manager):
    result = fresh_manager.find_students("chi")
    assert result == False

    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_student("Chiara", ["103"])
    result = fresh_manager.find_students("chi")
    assert result[0].name == "Chiara"
    assert result[0].enrolled_in == ["103"]
    assert len(result) == 1

def test_find_teachers(fresh_manager):
    result = fresh_manager.find_teachers("bar")
    assert result == False

    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_teacher("heatly", "Piano")
    result = fresh_manager.find_teachers("bar")
    assert result[0].name == "Barkly"
    assert result[0].speciality == "Guitar"
    assert len(result) == 1

def test_find_student_by_id(fresh_manager):
    result = fresh_manager.find_student_by_id(1)
    assert result == None

    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_student("Chiara", ["103"])
    result = fresh_manager.find_student_by_id(1)
    assert result.student_id == 1
    assert result.name == "Emanuel"
    assert result.enrolled_in == ["101"]

def test_find_teacher_by_id(fresh_manager):
    result = fresh_manager.find_teacher_by_id(1)
    assert result == None

    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_teacher("heatly", "Piano")
    result = fresh_manager.find_teacher_by_id(1)
    assert result.teacher_id == 1
    assert result.name == "Barkly"
    assert result.speciality == "Guitar"

def test_front_desk_lookup(fresh_manager):
    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_student("Chiara", ["103"])
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_teacher("heatly", "Piano")

    result = fresh_manager.front_desk_lookup("barkly")
    assert result[0][0].teacher_id == 1
    assert result[0][0].name == "Barkly"
    assert result[0][0].speciality == "Guitar"
    assert len(result) == 1

def test_print_student_card(fresh_manager):
    fresh_manager.add_student("Emanuel", "101")

    filename, data = fresh_manager.print_student_card(1)
    assert filename == "1_card.txt"
    assert data == (
    "========================\n"
    "MUSIC SCHOOL ID BADGE\n"
    "========================\n"
    "ID: 1\n"
    "Name: Emanuel\n"
    "Enrolled In: 1, 0, 1"
)
    valid = fresh_manager.print_student_card(2)
    assert valid == None

def test_add_course(fresh_manager):
    # adding
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])

    assert len(fresh_manager.courses) == 1
    assert fresh_manager.courses[0].course_id == "101"
    assert fresh_manager.courses[0].name == "Guitar Basics"
    assert fresh_manager.courses[0].instrument == "Guitar"
    assert fresh_manager.courses[0].teacher_id == 1
    assert fresh_manager.courses[0].enrolled_student_ids == [1]

    # course id already exists
    valid = fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    assert valid == 101

    # teacher id not found
    valid = fresh_manager.add_course("102", "Guitar Basics", "Guitar", 2)
    assert valid == 102

def test_add_lesson_to_course(fresh_manager):
    # adding
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_lesson_to_course("101", "Monday", "10:00", "Room A")

    assert len(fresh_manager.courses[0].lessons) == 1
    assert fresh_manager.courses[0].lessons[0]["lesson_id"] == 1
    assert fresh_manager.courses[0].lessons[0]["day"] == "Monday"
    assert fresh_manager.courses[0].lessons[0]["start_time"] == "10:00"
    assert fresh_manager.courses[0].lessons[0]["room"] == "Room A"

    # course does not exist
    result  = fresh_manager.add_lesson_to_course("102", "Monday", "10:00", "Room A")
    assert result == False

def test_check_in(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])

    fresh_manager.check_in(1, "101")
    assert fresh_manager.attendance_log[0]["student_id"] == 1
    assert fresh_manager.attendance_log[0]["course_id"] == "101"
    assert len(fresh_manager.attendance_log) == 1

def test_find_course_by_id(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])

    result = fresh_manager.find_course_by_id("101")
    assert result.course_id == "101"
    assert result.name == "Guitar Basics"
    assert result.instrument == "Guitar"
    assert result.teacher_id == 1
    assert result.enrolled_student_ids == [1]

def test_get_lessons_for_day(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_course("102", "Advanced Guitar", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_lesson_to_course("101", "Monday", "10:00", "Room A")
    fresh_manager.add_lesson_to_course("102", "Monday", "12:00", "Room B")

    result = fresh_manager.get_lessons_for_day("Monday")
    assert len(result) == 2

    course, lesson = result[0]
    assert course.course_id == "101"
    assert lesson["day"] == "Monday"
    assert lesson["start_time"] == "10:00"
    assert lesson["room"] == "Room A"

    course, lesson = result[1]
    assert course.course_id == "102"
    assert lesson["start_time"] == "12:00"


# --- new tests ---

def test_check_in_invalid(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])

    # student does not exist
    result = fresh_manager.check_in(2, "101")
    assert result == False
    # course does not exist
    result = fresh_manager.check_in(1, "102")
    assert result == False
    assert len(fresh_manager.attendance_log) == 0

def test_update_student_courses(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_course("102", "Advanced Guitar", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])

    result = fresh_manager.update_student(1, enrolled_in=["102"])
    assert result == True
    assert fresh_manager.students[0].enrolled_in == ["102"]
    assert fresh_manager.courses[0].enrolled_student_ids == []
    assert fresh_manager.courses[1].enrolled_student_ids == [1]

def test_remove_student_from_courses(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])

    fresh_manager.remove_student(1)
    assert fresh_manager.courses[0].enrolled_student_ids == []

def test_switch_student_course(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_course("102", "Advanced Guitar", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])

    # student does not exist
    result = fresh_manager.switch_student_course(2, "101", "102")
    assert result == False
    # course does not exist
    result = fresh_manager.switch_student_course(1, "101", "103")
    assert result == False
    # student not in the course they're switching from
    result = fresh_manager.switch_student_course(1, "102", "101")
    assert result == False

    result = fresh_manager.switch_student_course(1, "101", "102")
    assert result == True
    assert fresh_manager.students[0].enrolled_in == ["102"]
    assert fresh_manager.courses[0].enrolled_student_ids == []
    assert fresh_manager.courses[1].enrolled_student_ids == [1]

def test_find_courses_by_instrument(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_teacher("Heatly", "Piano")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_course("102", "Advanced Guitar", "Guitar", 1)
    fresh_manager.add_course("201", "Piano Basics", "Piano", 2)

    result = fresh_manager.find_courses_by_instrument("guitar")
    assert len(result) == 2
    assert result[0].course_id == "101"
    assert result[1].course_id == "102"

    result = fresh_manager.find_courses_by_instrument("Drums")
    assert result == []

def test_front_desk_daily_roster(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_lesson_to_course("101", "Monday", "10:00", "Room A")

    # no lessons on this day
    result = fresh_manager.front_desk_daily_roster("Sunday")
    assert result == None

    result = fresh_manager.front_desk_daily_roster("Monday")
    assert len(result) == 1
    assert result[0]["time"] == "10:00"
    assert result[0]["name"] == "Guitar Basics"
    assert result[0]["instrument"] == "Guitar"
    assert result[0]["teacher"] == "Barkly"
    assert result[0]["room"] == "Room A"

    # teacher removed
    fresh_manager.remove_teacher(1)
    result = fresh_manager.front_desk_daily_roster("Monday")
    assert result[0]["teacher"] == "Unassigned"

def test_record_payment_and_history(fresh_manager):
    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_student("Chiara", ["103"])

    # student does not exist
    result = fresh_manager.record_payment(3, 100.00, "Credit Card")
    assert result == False

    result = fresh_manager.record_payment(1, 100.00, "Credit Card")
    assert result == True
    fresh_manager.record_payment(2, 50.00, "Cash")

    history = fresh_manager.get_payment_history(1)
    assert len(history) == 1
    assert history[0]['amount'] == 100.00
    assert history[0]['method'] == "Credit Card"

def test_get_payment_history_no_results(fresh_manager):
    fresh_manager.add_student("Emanuel", ["101"])

    history = fresh_manager.get_payment_history(1)
    assert history == []

def test_export_report(fresh_manager, tmp_path):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])
    out_file = tmp_path / "report.csv"

    # nothing to export yet
    result = fresh_manager.export_report("financial", out_file)
    assert result == False

    # unknown report kind
    with pytest.raises(ValueError):
        fresh_manager.export_report("payroll", out_file)

    fresh_manager.record_payment(1, 100.00, "Credit Card")
    result = fresh_manager.export_report("financial", out_file)
    assert result == True
    with open(out_file, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["student_id"] == "1"   # CSV gives everything back as strings
    assert rows[0]["method"] == "Credit Card"

    fresh_manager.check_in(1, "101")
    result = fresh_manager.export_report("attendance", out_file)
    assert result == True
    with open(out_file, newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["course_id"] == "101"

def test_save_and_load(fresh_manager):
    fresh_manager.add_teacher("Barkly", "Guitar")
    fresh_manager.add_course("101", "Guitar Basics", "Guitar", 1)
    fresh_manager.add_student("Emanuel", ["101"])
    fresh_manager.add_lesson_to_course("101", "Monday", "10:00", "Room A")
    fresh_manager.check_in(1, "101")
    fresh_manager.record_payment(1, 100.00, "Cash")

    # a new manager reading the same file should see everything
    reloaded = ScheduleManager(data_path=fresh_manager.data_path)
    assert reloaded.students[0].name == "Emanuel"
    assert reloaded.teachers[0].name == "Barkly"
    assert reloaded.courses[0].enrolled_student_ids == [1]
    assert len(reloaded.courses[0].lessons) == 1
    assert len(reloaded.attendance_log) == 1
    assert len(reloaded.finance_log) == 1
    assert reloaded.next_student_id == 2