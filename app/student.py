from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, student_id, name, enrolled_in=None):
        # Call the parent class's __init__ method using super().
        super().__init__(name)
        # Initialize an empty list called 'enrolled_course_ids' to store the IDs of courses.
        self.student_id = student_id
        self.enrolled_in = enrolled_in or [] 