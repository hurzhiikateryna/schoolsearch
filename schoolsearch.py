from dataclasses import dataclass


@dataclass
class Student:
    last_name: str
    first_name: str
    grade: int
    classroom: int
    bus: int
    teacher_last_name: str
    teacher_first_name: str


def load_students(filename: str) -> list[Student]:
    students = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split(",")

            if len(parts) != 7:
                continue

            student = Student(
                last_name=parts[0],
                first_name=parts[1],
                grade=int(parts[2]),
                classroom=int(parts[3]),
                bus=int(parts[4]),
                teacher_last_name=parts[5],
                teacher_first_name=parts[6]
            )

            students.append(student)

    return students


def search_student(students: list[Student], last_name: str) -> list[Student]:
    return [
        student
        for student in students
        if student.last_name == last_name
    ]


def search_teacher(students: list[Student], last_name: str) -> list[Student]:
    return [
        student
        for student in students
        if student.teacher_last_name == last_name
    ]


def search_classroom(students: list[Student], classroom: int) -> list[Student]:
    return [
        student
        for student in students
        if student.classroom == classroom
    ]


def search_bus(students: list[Student], bus: int) -> list[Student]:
    return [
        student
        for student in students
        if student.bus == bus
    ]


def main():
    students = load_students("students.txt")

    print("Schoolsearch")
    print(f"Loaded students: {len(students)}")
    print("Enter a command or Q to quit.")

    while True:
        command = input("> ").strip()

        if command.upper() == "Q":
            print("Goodbye!")
            break

        elif command.upper().startswith("S:"):
            last_name = command[2:].strip().upper()

            results = search_student(students, last_name)

            if not results:
                print("Student not found.")
                continue

            for student in results:
                print(
                    f"{student.last_name} {student.first_name} | "
                    f"Grade: {student.grade} | "
                    f"Classroom: {student.classroom} | "
                    f"Teacher: {student.teacher_last_name} "
                    f"{student.teacher_first_name}"
                )

        elif command.upper().startswith("T:"):
            last_name = command[2:].strip().upper()

            results = search_teacher(students, last_name)

            if not results:
                print("Teacher not found.")
                continue

            print(f"Students of teacher {last_name}:")

            for student in results:
                print(
                    f"{student.last_name} {student.first_name} | "
                    f"Grade: {student.grade} | "
                    f"Classroom: {student.classroom}"
                )

        elif command.upper().startswith("C:"):
            try:
                classroom = int(command[2:].strip())
            except ValueError:
                print("Invalid classroom number.")
                continue

            results = search_classroom(students, classroom)

            if not results:
                print("No students found.")
                continue

            print(f"Students in classroom {classroom}:")

            for student in results:
                print(
                    f"{student.last_name} {student.first_name} | "
                    f"Grade: {student.grade}"
                )

        elif command.upper().startswith("B:"):
            try:
                bus = int(command[2:].strip())
            except ValueError:
                print("Invalid bus number.")
                continue

            results = search_bus(students, bus)

            if not results:
                print("No students found.")
                continue

            print(f"Students on bus {bus}:")

            for student in results:
                print(
                    f"{student.last_name} {student.first_name} | "
                    f"Grade: {student.grade} | "
                    f"Classroom: {student.classroom}"
                )

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()