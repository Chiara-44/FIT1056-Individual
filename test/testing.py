import unittest
from app.schedule import add_student, students

class TestMSMS(unittest.TestCase):
    def test_add_student_twice(self):
        add_student()