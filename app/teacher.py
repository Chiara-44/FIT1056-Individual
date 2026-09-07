from app.user import User

class TeacherUser(User):
    """Represents a teacher."""
    # Implement the TeacherUser class, inheriting from User.
    # It should have an additional 'speciality' attribute in its __init__.
    def __init__(self, teacher_id, name, speciality):
        super().__init__(name)
        self.teacher_id = teacher_id
        self.speciality = speciality

class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, course_id, name, instrument, teacher_id=None, 
                 enrolled_student_ids=None, lessons=None):
        self.course_id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        # Initialize two empty lists: 'enrolled_student_ids' and 'lessons' or allow to be filled
        self.enrolled_student_ids = enrolled_student_ids or []
        self.lessons = lessons or []   # list of dicts: {lesson_id, day, start_time, room}


    def lessons_on_day(self, day):
        """Returns this course's lesson dicts that fall on the given day."""
        return [lesson for lesson in self.lessons if lesson["day"] == day]