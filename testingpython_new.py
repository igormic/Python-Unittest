import csv
from datetime import datetime

students = [
    [1, "Maria", "Krawczyk", []],
    [2, "Krzysztof", "Krawczyk", []],
    [3, "Jan", "Krawczyk", []],
    [4, "Alojzy", "Kołodziejski", []],
]


def student_add(students, name, surname):
    new_id = students[-1][0] + 1 if students else 1
    students.append([new_id, name, surname, []])
    print(f"Added student: {new_id}, {name} {surname}")


def student_remove(students, student_id):
    for student in students:
        if student[0] == student_id:
            students.remove(student)
            print(f"Removed student: {student_id}, {student[1]} {student[2]}")
            return
    print(f"Student with ID {student_id} not found.")


def student_base_export(students, filename="students_list.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "surname", "attendance"])
        for student in students:
            attendance_data = ";".join(
                [f"{entry['date']}:{entry['status']}" for entry in student[3]]
            )
            writer.writerow([student[0], student[1], student[2], attendance_data])
    print(f"Student list exported to {filename}")


def student_base_import(filename="students_list.csv"):
    imported_students = []
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                attendance = []
                if row["attendance"]:
                    attendance = [
                        {
                            "date": entry.split(":")[0],
                            "status": entry.split(":")[1],
                        }
                        for entry in row["attendance"].split(";")
                    ]
                imported_students.append(
                    [int(row["id"]), row["name"], row["surname"], attendance]
                )
        print(f"Student list imported from {filename}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return imported_students


def mark_attendance(students, student_id, attendance, date_str=None):
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    for student in students:
        if student[0] == student_id:
            student[3].append({"date": date_str, "status": attendance})
            print(f"Attendance marked: {student_id} -> {attendance} ({date_str})")
            return
    print(f"Student with ID {student_id} not found.")


def display_students(students):
    print("\nStudent List:")
    for student in students:
        print(f"{student[0]} - {student[1]} {student[2]}")
        for entry in student[3]:
            print(f"  Date: {entry['date']} - Status: {entry['status']}")
    print()


def update_attendance(students, student_id, new_status, date_str):
    for student in students:
        if student[0] == student_id:
            for entry in student[3]:
                if entry["date"] == date_str:
                    entry["status"] = new_status
                    print(
                        f"Updated attendance: {student_id} -> {new_status} ({date_str})"
                    )
                    return
            print(f"No attendance record for {student_id} on {date_str}.")
            return
    print(f"Student with ID {student_id} not found.")


if __name__ == "__main__":
    student_base_export(students)
    students = student_base_import()
    student_add(students, "Anna", "Kowalska")
    mark_attendance(students, 1, "Present")
    mark_attendance(students, 2, "Absent", "2023-10-10")
    mark_attendance(students, 3, "Present", "2023-11-10")
    display_students(students)
    update_attendance(students, 2, "Present", "2023-10-10")
    update_attendance(students, 4, "Present", "2023-11-10")
    student_remove(students, 3)
    display_students(students)
    student_base_export(students)
