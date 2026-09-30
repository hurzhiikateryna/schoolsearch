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


def main():
    students = load_students("students.txt")

    print(f"Loaded students: {len(students)}")


if __name__ == "__main__":
    main()