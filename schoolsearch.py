
from dataclasses import dataclass
import time


@dataclass
class Student:
    last_name: str
    first_name: str
    grade: int
    classroom: int
    bus: int


@dataclass
class Teacher:
    last_name: str
    first_name: str
    classroom: int


def load_students(filename):
    students = []

    with open(filename, "r", encoding="utf-8-sig") as file:
        for line in file:
            parts = [p.strip() for p in line.strip().split(",")]

            if not line.strip() or len(parts) != 5:
                continue

            try:
                students.append(Student(
                    parts[0], parts[1], int(parts[2]),
                    int(parts[3]), int(parts[4])
                ))
            except ValueError:
                continue

    return students


def load_teachers(filename):
    teachers = []

    with open(filename, "r", encoding="utf-8-sig") as file:
        for line in file:
            parts = [p.strip() for p in line.strip().split(",")]

            if not line.strip() or len(parts) != 3:
                continue

            try:
                teachers.append(Teacher(
                    parts[0], parts[1], int(parts[2])
                ))
            except ValueError:
                continue

    return teachers


def save_students(filename, students):
    with open(filename, "w", encoding="utf-8") as file:
        for s in students:
            file.write(
                f"{s.last_name}, {s.first_name}, {s.grade}, "
                f"{s.classroom}, {s.bus}\n"
            )


def search_student(students, last_name):
    return [
        s for s in students
        if s.last_name.casefold() == last_name.casefold()
    ]


def search_teacher(students, teachers, last_name):
    rooms = {
        t.classroom for t in teachers
        if t.last_name.casefold() == last_name.casefold()
    }

    return [s for s in students if s.classroom in rooms]


def search_classroom(students, classroom):
    return [s for s in students if s.classroom == classroom]


def search_bus(students, bus):
    return [s for s in students if s.bus == bus]


def search_grade(students, grade):
    return [s for s in students if s.grade == grade]


def teachers_in_classroom(teachers, classroom):
    return [t for t in teachers if t.classroom == classroom]


def teachers_for_grade(students, teachers, grade):
    rooms = {
        s.classroom for s in students if s.grade == grade
    }

    result = []
    seen = set()

    for t in teachers:
        key = (t.last_name, t.first_name, t.classroom)

        if t.classroom in rooms and key not in seen:
            result.append(t)
            seen.add(key)

    return result


def delete_student(students, last_name, first_name):
    old_length = len(students)

    students[:] = [
        s for s in students
        if not (
            s.last_name.casefold() == last_name.casefold()
            and s.first_name.casefold() == first_name.casefold()
        )
    ]

    return old_length - len(students)


def update_student(students, last_name, first_name):
    for s in students:
        if (
            s.last_name.casefold() == last_name.casefold()
            and s.first_name.casefold() == first_name.casefold()
        ):
            new_last = input("Last name: ").strip()
            new_first = input("First name: ").strip()

            try:
                new_grade = int(input("Grade: "))
                new_classroom = int(input("Classroom: "))
                new_bus = int(input("Bus: "))
            except ValueError:
                print("Invalid numeric data.")
                return False

            s.last_name = new_last
            s.first_name = new_first
            s.grade = new_grade
            s.classroom = new_classroom
            s.bus = new_bus

            return True

    return False


def teacher_for_student(teachers, student):
    return [
        t for t in teachers
        if t.classroom == student.classroom
    ]


def main():
    try:
        students = load_students("list.txt")
        teachers = load_teachers("teachers.txt")
    except OSError as error:
        print(f"Cannot open data file: {error}")
        return

    while True:
        try:
            command = input().strip()
        except EOFError:
            print("bye!")
            break

        upper = command.upper()

        if upper in ("Q", "QUIT"):
            print("bye!")
            break

        # Видалення учня
        if upper.startswith("D:"):
            parts = command[2:].strip().split(",", 1)

            if len(parts) != 2:
                continue

            count = delete_student(
                students, parts[0].strip(), parts[1].strip()
            )

            if count:
                save_students("list.txt", students)

            continue

        # Оновлення учня
        if upper.startswith("U:"):
            parts = command[2:].strip().split(",", 1)

            if len(parts) != 2:
                continue

            if update_student(
                students, parts[0].strip(), parts[1].strip()
            ):
                save_students("list.txt", students)

            continue

        start = time.perf_counter()
        results = []
        formatter = None

        try:
            # C: 104 T — учителі певного кабінету
            if upper.startswith("C:") and upper.endswith(" T"):
                classroom = int(command[2:-2].strip())
                results = teachers_in_classroom(
                    teachers, classroom
                )
                formatter = lambda t: (
                    f"{t.last_name}, {t.first_name}"
                )

            # G: 6 T — учителі, які навчають учнів цього рівня
            elif upper.startswith("G:") and upper.endswith(" T"):
                grade = int(command[2:-2].strip())
                results = teachers_for_grade(
                    students, teachers, grade
                )
                formatter = lambda t: (
                    f"{t.last_name}, {t.first_name}"
                )

            # S: SMITH B — автобус учня
            elif upper.startswith("S:") and upper.endswith(" B"):
                name = command[2:-2].strip()
                results = search_student(students, name)
                formatter = lambda s: (
                    f"{s.last_name}, {s.first_name}, {s.bus}"
                )

            # S: SMITH — кабінет та вчитель учня
            elif upper.startswith("S:"):
                name = command[2:].strip()
                results = search_student(students, name)

                def formatter(s):
                    teachers_found = teacher_for_student(
                        teachers, s
                    )

                    if teachers_found:
                        t = teachers_found[0]
                        return (
                            f"{s.last_name}, {s.first_name}, "
                            f"{s.grade}, {s.classroom}, "
                            f"{t.last_name}, {t.first_name}"
                        )

                    return (
                        f"{s.last_name}, {s.first_name}, "
                        f"{s.grade}, {s.classroom}"
                    )

            # T: NIBLER — учні вчителя
            elif upper.startswith("T:"):
                name = command[2:].strip()
                results = search_teacher(
                    students, teachers, name
                )
                formatter = lambda s: (
                    f"{s.last_name}, {s.first_name}"
                )

            # C: 104 — учні кабінету
            elif upper.startswith("C:"):
                classroom = int(command[2:].strip())
                results = search_classroom(students, classroom)
                formatter = lambda s: (
                    f"{s.last_name}, {s.first_name}"
                )

            # B: 53 — учні автобуса
            elif upper.startswith("B:"):
                bus = int(command[2:].strip())
                results = search_bus(students, bus)
                formatter = lambda s: (
                    f"{s.last_name}, {s.first_name}"
                )

            # G: 6 — учні певного рівня
            elif upper.startswith("G:"):
                grade = int(command[2:].strip())
                results = search_grade(students, grade)
                formatter = lambda s: (
                    f"{s.last_name}, {s.first_name}"
                )

            else:
                continue

        except ValueError:
            continue

        # Вимірюємо час пошуку та виводимо результат
        for item in results:
            print(formatter(item))

        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"{elapsed_ms:.0f}ms")


if __name__ == "__main__":
    main()
