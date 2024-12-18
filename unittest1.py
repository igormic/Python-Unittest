import unittest
import os
import csv
from datetime import datetime
from testingpython_new import (
    student_add,
    student_remove,
    student_base_export,
    student_base_import,
    mark_attendance,
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
        self.test_file = "students_list.csv"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_student_base_export(self):
        student_base_export(self.sample_students, self.test_file)
        self.assertTrue(os.path.exists(self.test_file))

        with open(self.test_file, "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        self.assertEqual(rows[0], ["id", "name", "surname", "attendance"])
        self.assertEqual(rows[1], ["1", "Maria", "Krawczyk", ""])
        self.assertEqual(len(rows), 5)

    def test_student_base_import(self):
        student_base_export(self.sample_students, self.test_file)
        imported_students = student_base_import(self.test_file)

        self.assertEqual(len(imported_students), len(self.sample_students))
        self.assertEqual(imported_students[0], self.sample_students[0])

    def test_student_add(self):
        initial_count = len(self.sample_students)
        student_add(self.sample_students, "Anna", "Kowalska")

        self.assertEqual(len(self.sample_students), initial_count + 1)
        self.assertEqual(self.sample_students[-1][1], "Anna")
        self.assertEqual(self.sample_students[-1][2], "Kowalska")
        self.assertEqual(self.sample_students[-1][0], 5)

    def test_student_remove(self):
        initial_count = len(self.sample_students)
        student_remove(self.sample_students, 3)

        self.assertEqual(len(self.sample_students), initial_count - 1)
        self.assertNotIn([3, "Jan", "Krawczyk", []], self.sample_students)

        student_remove(self.sample_students, 99)
        self.assertEqual(len(self.sample_students), initial_count - 1)

    def test_mark_attendance(self):
        date_today = datetime.now().strftime('%Y-%m-%d')
        mark_attendance(self.sample_students, 1, "Present")

        self.assertEqual(len(self.sample_students[0][3]), 1)
        self.assertEqual(self.sample_students[0][3][0], {"date": date_today, "status": "Present"})

    def test_update_attendance(self):
        mark_attendance(self.sample_students, 2, "Absent", "2023-10-10")
        update_attendance(self.sample_students, 2, "Present", "2023-10-10")

        self.assertEqual(self.sample_students[1][3][0]["status"], "Present")
        update_attendance(self.sample_students, 2, "Absent", "2023-11-11")

        self.assertEqual(len(self.sample_students[1][3]), 1)

    def test_import_nonexistent_file(self):
        imported_students = student_base_import("nonexistent_file.csv")
        self.assertEqual(imported_students, [])

if __name__ == "__main__":
    unittest.main()
