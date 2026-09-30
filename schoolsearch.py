from dataclasses import dataclass
import time


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

            try:
                student = Student(
                    last_name=parts[0],
                    first_name=parts[1],
                    grade=int(parts[2]),
                    classroom=int(parts[3]),
                    bus=int(parts[4]),
                    teacher_last_name=parts[5],
                    teacher_first_name=parts[6]
                )
            except ValueError:
                continue

            students.append(student)

    return students


def save_students(filename: str, students: list[Student]):
    with open(filename, "w", encoding="utf-8") as file:
        for student in students:
            file.write(
                f"{student.last_name},"
                f"{student.first_name},"
                f"{student.grade},"
                f"{student.classroom},"
                f"{student.bus},"
                f"{student.teacher_last_name},"
                f"{student.teacher_first_name}\n"
            )


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


def delete_student(
    students: list[Student],
    last_name: str,
    first_name: str
) -> int:
    old_length = len(students)

    students[:] = [
        student
        for student in students
        if not (
            student.last_name == last_name
            and student.first_name == first_name
        )
    ]

    return old_length - len(students)


def update_student(
    students: list[Student],
    last_name: str,
    first_name: str
) -> bool:
    for student in students:
        if (
            student.last_name == last_name
            and student.first_name == first_name
        ):
            print("Enter new data.")

            new_last_name = input("Last name: ").strip().upper()
            new_first_name = input("First name: ").strip().upper()

            try:
                new_grade = int(input("Grade: ").strip())
                new_classroom = int(input("Classroom: ").strip())
                new_bus = int(input("Bus: ").strip())
            except ValueError:
                print("Grade, classroom and bus must be numbers.")
                return False

            new_teacher_last_name = (
                input("Teacher last name: ").strip().upper()
            )
            new_teacher_first_name = (
                input("Teacher first name: ").strip().upper()
            )

            student.last_name = new_last_name
            student.first_name = new_first_name
            student.grade = new_grade
            student.classroom = new_classroom
            student.bus = new_bus
            student.teacher_last_name = new_teacher_last_name
            student.teacher_first_name = new_teacher_first_name

            return True

    return False


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

        elif command.startswith("S:"):
            student_command = command[2:].strip()

            if student_command.upper().endswith(" B"):
                last_name = student_command[:-2].strip().upper()

                start = time.perf_counter()
                results = search_student(students, last_name)
                elapsed = time.perf_counter() - start

                if not results:
                    print("No students found.")
                else:
                    for student in results:
                        print(
                            f"{student.last_name} {student.first_name} - "
                            f"Bus: {student.bus}"
                        )

                print(f"Search time: {elapsed:.6f} seconds")

            else:
                last_name = student_command.upper()

                start = time.perf_counter()
                results = search_student(students, last_name)
                elapsed = time.perf_counter() - start

                if not results:
                    print("No students found.")
                else:
                    for student in results:
                        print(
                            f"{student.last_name} {student.first_name}, "
                            f"Grade: {student.grade}, "
                            f"Classroom: {student.classroom}, "
                            f"Teacher: {student.teacher_first_name} "
                            f"{student.teacher_last_name}"
                        )

                print(f"Search time: {elapsed:.6f} seconds")

        elif command.upper().startswith("T:"):
            last_name = command[2:].strip().upper()

            start_time = time.perf_counter()
            results = search_teacher(students, last_name)
            end_time = time.perf_counter()

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

            print(f"Search time: {end_time - start_time:.8f} seconds")

        elif command.upper().startswith("C:"):
            try:
                classroom = int(command[2:].strip())
            except ValueError:
                print("Invalid classroom number.")
                continue

            start_time = time.perf_counter()
            results = search_classroom(students, classroom)
            end_time = time.perf_counter()

            if not results:
                print("No students found.")
                continue

            print(f"Students in classroom {classroom}:")

            for student in results:
                print(
                    f"{student.last_name} {student.first_name} | "
                    f"Grade: {student.grade}"
                )

            print(f"Search time: {end_time - start_time:.8f} seconds")

        elif command.upper().startswith("B:"):
            try:
                bus = int(command[2:].strip())
            except ValueError:
                print("Invalid bus number.")
                continue

            start_time = time.perf_counter()
            results = search_bus(students, bus)
            end_time = time.perf_counter()

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

            print(f"Search time: {end_time - start_time:.8f} seconds")

        elif command.upper().startswith("D:"):
            data = command[2:].strip().split(",")

            if len(data) != 2:
                print("Use: D: LASTNAME,FIRSTNAME")
                continue

            last_name = data[0].strip().upper()
            first_name = data[1].strip().upper()

            deleted_count = delete_student(
                students,
                last_name,
                first_name
            )

            if deleted_count == 0:
                print("Student not found.")
            else:
                save_students("students.txt", students)
                print(f"Deleted students: {deleted_count}")

        elif command.upper().startswith("U:"):
            data = command[2:].strip().split(",")

            if len(data) != 2:
                print("Use: U: LASTNAME,FIRSTNAME")
                continue

            last_name = data[0].strip().upper()
            first_name = data[1].strip().upper()

            updated = update_student(
                students,
                last_name,
                first_name
            )

            if not updated:
                print("Student not found or invalid data.")
            else:
                save_students("students.txt", students)
                print("Student updated successfully.")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()