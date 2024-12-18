import unittest
from datetime import datetime

from testingpython_new import (
    mark_attendance,
    student_add,
    student_base_import,
    student_remove,
    update_attendance,
)


class TestStudentManager(unittest.TestCase):
    def setUp(self):
        self.sample_students = [
            [1, "Maria", "Krawczyk", []],
            [2, "Krzysztof", "Krawczyk", []],
            [3, "Jan", "Krawczyk", []],
            [4, "Alojzy", "Kołodziejski", []],
        ]

    def test_student_add(self):
        initial_count = len(self.sample_students)
        student_add(self.sample_students, "Anna", "Nowak")
        self.assertEqual(len(self.sample_students), initial_count + 1)
        self.assertEqual(self.sample_students[-1][1], "Anna")
        self.assertEqual(self.sample_students[-1][2], "Nowak")

    def test_student_remove(self):
        initial_count = len(self.sample_students)
        student_remove(self.sample_students, 1)
        self.assertEqual(len(self.sample_students), initial_count - 1)

        student_remove(self.sample_students, 99)
        self.assertEqual(len(self.sample_students), initial_count - 1)

    def test_mark_attendance(self):
        date_today = datetime.now().strftime("%Y-%m-%d")
        mark_attendance(self.sample_students, 1, "Present")

        self.assertEqual(len(self.sample_students[0][3]), 1)
        self.assertEqual(
            self.sample_students[0][3][0],
            {"date": date_today, "status": "Present"},
        )

    def test_update_attendance(self):
        mark_attendance(self.sample_students, 2, "Absent", "2023-10-10")
        update_attendance(self.sample_students, 2, "Present", "2023-10-10")

        self.assertEqual(
            self.sample_students[1][3][0],
            {"date": "2023-10-10", "status": "Present"},
        )

    def test_import_nonexistent_file(self):
        imported_students = student_base_import("nonexistent_file.csv")
        self.assertEqual(imported_students, [])


if __name__ == "__main__":
    unittest.main()
