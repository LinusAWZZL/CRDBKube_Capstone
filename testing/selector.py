import random

class QueryGenerator:
    def __init__(self):
        pass

    def lecturer_queries(self, lecturer_code, semester):
        return {
            "lectures": f"SELECT course_offering " +
                        f"FROM course_offering " +
                        f"WHERE lecturer_code = '{lecturer_code}' " +
                        f"AND semester = {semester};",

            "schedule": f"SELECT schedule " +
                        f"FROM schedule " +
                        f"JOIN course_offering ON schedule.course_id = course_offering.course_id " +
                        f"WHERE course_offering.lecturer_code = '{lecturer_code}' " +
                        f"AND semester = {semester} " +
                        f"ORDER BY schedule.created;",

            "students_in_courses": f"SELECT student.student_code, student.username " +
                                   f"FROM student " +
                                   f"JOIN course_registration ON student.student_code = course_registration.student_code " +
                                   f"JOIN course_offering ON course_registration.course_id = course_offering.course_id " +
                                   f"WHERE course_offering.lecturer_code = '{lecturer_code}' " +
                                   f"AND course_offering.semester = {semester} " +
                                   f"GROUP BY course_offering.course_id;"
        }

    def student_queries(self, student_code):
        return {
            "course_registration": f"SELECT course_registration " +
                                   f"FROM course_registration " +
                                   f"WHERE student_code = '{student_code}' " +
                                   f"ORDER BY semester;",

            "sks_and_grades": f"SELECT SUM(course.sks) AS total_sks, AVG(course_registration.grade) AS average_grade " +
                              f"FROM course " +
                              f"JOIN course_registration ON course.course_code = course_registration.course_code " +
                              f"WHERE course_registration.student_code = '{student_code}' " +
                              f"AND course_registration.course_passed = true;",

            "schedule": f"SELECT schedule " +
                        f"FROM schedule " +
                        f"JOIN course_registration ON schedule.course_id = course_registration.course_id " +
                        f"WHERE course_registration.student_code = '{student_code}' " +
                        f"AND schedule.semester = (SELECT MAX(semester) FROM course_registration);"
        }

    def registration_queries(self, student_code, semester):
        return {
            "register_course": f"INSERT INTO course_registration (student_code, semester) " +
                               f"VALUES ('{student_code}', '{semester}');",

            "update_registration": f"UPDATE course_registration "
                                   f"SET grade_number = {random.randint(0, 100)} "
                                   f"WHERE student_code = '{student_code}' "
                                   f"AND semester = {semester};"
        }

    def grading_queries(self, lecturer_code, semester):
        return {
            "students_in_courses": f"SELECT student.student_code, student.username " +
                                   f"FROM student " +
                                   f"JOIN course_registration ON student.student_code = course_registration.student_code " +
                                   f"JOIN course_offering ON course_registration.course_id = course_offering.course_id " +
                                   f"WHERE course_offering.lecturer_code = '{lecturer_code}' " +
                                   f"AND course_offering.semester = {semester};",

            "update_grades_random": f"UPDATE course_registration " +
                                    f"  SET grade_letter = CASE " +
                                    f"  WHEN random() > 0.7 THEN 'A' " +
                                    f"  WHEN random() > 0.6 THEN 'B' " +
                                    f"  WHEN random() < 0.1 THEN 'E' " +
                                    f"  ELSE 'C' END, " +
                                    f"  course_passed = CASE " +
                                    f"  WHEN grade_letter IN ('A', 'B', 'C') THEN true ELSE false END " +
                                    f"WHERE course_id IN (" +
                                    f"  SELECT course_id " +
                                    f"  FROM course_offering " +
                                    f"  WHERE lecturer_code = '{lecturer_code}' " +
                                    f"  AND semester = {semester}" +
                                    f");",

            "average_grades": f"SELECT course_offering.course_id, AVG(course_registration.grade) AS avg_grade " +
                              f"FROM course_offering " +
                              f"JOIN course_registration ON course_offering.course_id = course_registration.course_id " +
                              f"WHERE course_offering.lecturer_code = '{lecturer_code}' " +
                              f"AND course_offering.semester = {semester} " +
                              f"GROUP BY course_offering.course_id;"
        }

    def complex_query(self):
        return {
            "most_costly": f"SELECT s.student_code, s.username, cr.grade, co.course_code, co.course_name, l.lecturer_name, SUM(c.sks) AS total_sks, AVG(cr.grade) AS average_grade " +
                           f"FROM student s " +
                           f"JOIN course_registration cr ON s.student_code = cr.student_code " +
                           f"JOIN course_offering co ON cr.course_id = co.course_id " +
                           f"JOIN lecturer l ON co.lecturer_code = l.lecturer_code " +
                           f"JOIN course c ON co.course_code = c.course_code " +
                           f"WHERE cr.course_passed = true " +
                           f"GROUP BY s.student_code, s.username, cr.grade, co.course_code, co.course_name, l.lecturer_name " +
                           f"ORDER BY total_sks DESC, average_grade DESC;"
        }

def read_file(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Example Usage:
if __name__ == "__main__":
    generator = QueryGenerator()

    # Read student codes, lecturer codes, and course codes from files
    student_names = read_file("NamesStudents.txt")
    lecturer_names = read_file("NamesLecturers.txt")
    course_names = read_file("NamesCourses.txt")

    # Generate queries for each student
    for student_code in student_codes:
        student_queries = generator.student_queries(student_code)
        print(f"Student Queries for {student_code}: \n", student_queries)

    # Generate queries for each lecturer
    semester = random.randint(1, 8)
    for lecturer_code in lecturer_codes:
        lecturer_queries = generator.lecturer_queries(lecturer_code, semester)
        print(f"Lecturer Queries for {lecturer_code}: \n", lecturer_queries)

    # Generate queries for each course (if needed)
    for course_code in course_codes:
        print(f"Placeholder for course-specific queries for {course_code}")


