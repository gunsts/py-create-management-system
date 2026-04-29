import dataclasses
import pickle


@dataclasses.dataclass
class Specialty:
    name: str
    number: int


@dataclasses.dataclass
class Student:
    first_name: str
    last_name: str
    birth_date: str
    average_mark: float
    has_scholarship: bool
    phone_number: str
    address: str


@dataclasses.dataclass
class Group:
    specialty: Specialty
    students: list[Student]
    course: str


def write_groups_information(groups: list[Group]) -> int:
    max_students = max(len(group.students) for group in groups)
    with open("groups.pickle", "w") as file:
        for group in groups:
            file.write(f"Specialty: {group.specialty.name}\n")
            file.write(f"Number: {group.specialty.number}\n")
            file.write(f"Course: {group.course}\n")
            file.write("Students:\n")
            for student in group.students:
                file.write(f"  - {student.first_name} {student.last_name}, "
                           f"Birth Date: {student.birth_date}, "
                           f"Average Mark: {student.average_mark}, "
                           f"Has Scholarship: \
                            {'Yes' if student.has_scholarship else 'No'}, "
                           f"Phone Number: {student.phone_number}, "
                           f"Address: {student.address}\n")
            file.write("\n")
    return max_students


def write_students_information(groups: list[Group]) -> int:
    total_students = sum(len(group.students) for group in groups)
    with open("students.pickle", "wb") as file:
        pickle.dump(groups, file)
    return total_students


def read_groups_information(filename: str) -> list[Group]:
    groups = []
    with open(filename, "r") as file:
        lines = file.readlines()
        current_group = None
        for line in lines:
            line = line.strip()
            if line.startswith("Specialty:"):
                if current_group is not None:
                    groups.append(current_group)
                specialty_info = line[len("Specialty: "):].split(" (")
                specialty_name = specialty_info[0]
                specialty_number = int(specialty_info[1][:-1])
                current_group = Group(Specialty(specialty_name,
                                                specialty_number), [], "")
            elif line.startswith("Course:"):
                if current_group is not None:
                    current_group.course = line[len("Course: "):]
            elif line.startswith("-"):
                student_info = line[2:].split(", ")
                first_name, last_name = student_info[0].split(" ")
                birth_date = student_info[1].split(": ")[1]
                average_mark = float(student_info[2].split(": ")[1])
                has_scholarship = student_info[3].split(": ")[1] == "Yes"
                phone_number = student_info[4].split(": ")[1]
                address = student_info[5].split(": ")[1]
                if current_group is not None:
                    current_group.students.append(Student(first_name,
                                                          last_name,
                                                          birth_date,
                                                          average_mark,
                                                          has_scholarship,
                                                          phone_number,
                                                          address))
        if current_group is not None:
            groups.append(current_group)
    return groups


def read_students_information(filename: str) -> list[Group]:
    with open(filename, "rb") as file:
        groups = pickle.load(file)
    return groups
