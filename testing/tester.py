import random
import string
import psycopg2
import selector

try:
    import cPickle as pickle
except ImportError:  # Python 3.x
    import pickle

from datetime import datetime, timedelta

# Database connection setup
def connect_db(target):
    if target == 'postgres':
        return psycopg2.connect(
            dbname="defaultdb",
            user="tester",
            # password="tester",
            host="localhost",
            port="5432"
        )
    else:
        return psycopg2.connect(
            dbname="defaultdb",
            user="tester",
            # password="tester",
            host="localhost",
            port="5432"
        )

def assign_grade_letter(grade_number):
    """Assign a grade letter based on the given grading pattern."""
    if 85 <= grade_number:
        return 'A '
    elif 80 <= grade_number < 85:
        return 'A-'
    elif 75 <= grade_number < 80:
        return 'B+'
    elif 70 <= grade_number < 75:
        return 'B '
    elif 65 <= grade_number < 70:
        return 'B-'
    elif 60 <= grade_number < 65:
        return 'C+'
    elif 55 <= grade_number < 60:
        return 'C '
    elif 40 <= grade_number < 55:
        return 'D '
    else:
        return 'E '

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def generate_entries(x100, is_import):
    queries = []
    count = 0

    # Generate queries for the curriculum table
    if is_import:
        count += 3
        query = "INSERT INTO curriculum (curriculum_name, curriculum_year) VALUES \n"
        for value in generated_data["curriculums"]:
            query += f"('{value[0]}', {value[1]}),\n"
        query = query[:-2]+";\n"
        queries.append(query)

    # Generate queries for lecturers
    temp = 0
    if not is_import:
        temp = 3
    for i in range(47 + temp):
        lecturer_name = f"Lecturer_{i+1}"
        lecturer_code = f"{random_string(10)}{i:08}"  # max len 20
        generated_data["lecturers"][lecturer_code] = (lecturer_name, lecturer_code)
        if not is_import:
            queries.append(f"INSERT INTO lecturer (lecturer_name, lecturer_code) VALUES ('{lecturer_name}', '{lecturer_code}');")
        count += 1
    if is_import:
        query = "INSERT INTO lecturer (lecturer_name, lecturer_code) VALUES \n"
        for value in generated_data["lecturers"].values():
            query += f"('{value[0]}', '{value[1]}'),\n"
        query = query[:-2]+";\n"
        queries.append(query)

    # Generate data for the course table
    for i in range(x100 * 50):
        course_name = f"Course_{i+1}"
        sks = random.randint(2, 6)
        prerequisite = None
        course_curriculum = generated_data["curriculums"][random.randint(0, len(generated_data["curriculums"]) - 1)][0]
        course_code = f"{random_string(2)}{i:08}"  # max len 10
        generated_data["courses"][course_code] = (course_name, sks, prerequisite, course_curriculum, course_code)
        if not is_import:
            queries.append(f"INSERT INTO course (course_name, sks, prerequisite, course_curriculum, course_code) VALUES ('{course_name}', {sks}, {prerequisite}, '{course_curriculum}', '{course_code}');")
        count += 1
    if is_import:
        query = "INSERT INTO course (course_name, sks, prerequisite, course_curriculum, course_code) VALUES \n"
        for value in generated_data["courses"].values():
            query += f"('{value[0]}', {value[1]}, {value[2]}, '{value[3]}', '{value[4]}'),\n"
        query = query[:-2]+";\n"
        queries.append(query)

    # Generate data for students
    for i in range(x100 * 150):
        username = f"student_{i+1}"
        password = random_string(10)
        student_code = f"ST{i+1:07}"  # max len 10
        generated_data["students"][student_code] = (username, password, student_code)
        if not is_import:
            queries.append(f"INSERT INTO student (username, pass, student_code) VALUES ('{username}', '{password}', '{student_code}');")
        count += 1
    if is_import:
        query = "INSERT INTO student (username, pass, student_code) VALUES \n"
        for value in generated_data["students"].values():
            query += f"('{value[0]}', '{value[1]}', '{value[2]}'),\n"
        query = query[:-2]+";\n"
        queries.append(query)

    # Generate data for course offerings and schedules
    for i in range(x100 * 200):
        co_name = f"Offering_{i+1}"
        class_lecturer = random.choice([l[1] for l in generated_data["lecturers"].keys()])
        semester = random.randint(1, 12)
        co_course = random.choice(list(generated_data["courses"].keys()))
        generated_data["course_offerings"][f"{co_course}, {semester}, {co_name}"] = (co_name, class_lecturer, semester, co_course)
        if not is_import:
            queries.append(f"INSERT INTO course_offering (co_name, class_lecturer, semester, co_course) VALUES ('{co_name}', '{class_lecturer}', {semester}, '{co_course}');")
        count += 1

        for j in range(2):
            time_start = datetime(2024, 1, 1, random.randint(8, 16), 0, 0)
            time_end = time_start + timedelta(minutes=50 * random.randint(1, 3))
            generated_data["schedules"].append((co_name, semester, co_course, time_start, time_end))
            if not is_import:
                queries.append(f"INSERT INTO schedule (schedule_class, semester, schedule_course, time_start, time_end) VALUES ('{co_name}', {semester}, '{co_course}', '{time_start}', '{time_end}');")
            count += 1
    if is_import:
        query = "INSERT INTO course_offering (co_name, class_lecturer, semester, co_course) VALUES \n"
        for value in generated_data["course_offerings"].values():
            query += f"('{value[0]}', '{value[1]}', {value[2]}, '{value[3]}'),\n"
        query = query[:-2]+";\n"
        queries.append(query)

        query = "INSERT INTO schedule (schedule_class, semester, schedule_course, time_start, time_end) VALUES \n"
        for value in generated_data["schedules"]:
            query += f"('{value[0]}', {value[1]}, '{value[2]}', '{value[3]}', '{value[4]}'),\n"
        query = query[:-2] + ";\n"
        queries.append(query)

    # Generate data for course registrations
    for i in range(x100 * 200 - 50):
        student_code = random.choice(list(generated_data["students"].keys()))
        offering = random.choice(list(generated_data["course_offerings"].values()))
        while f"{student_code}, {offering[2]}, {offering[3]}" in generated_data["registrations"]:
            offering = random.choice(list(generated_data["course_offerings"].values()))
        semester = offering[2]
        course_code = offering[3]
        course_name = offering[0]
        if semester <= 8:
            grade_number = random.randint(50, 100)
            grade_letter = assign_grade_letter(grade_number)
        else:
            grade_number = 0
            grade_letter = '-'
        course_passed = grade_number >= 55
        generated_data["registrations"][f"{student_code}, {semester}, {course_code}"] = (student_code, semester, course_code, course_name, grade_number, grade_letter, course_passed)
        if not is_import:
            queries.append(f"INSERT INTO course_registration (student_code, semester, course_code, course_name, grade_number, grade_letter, course_passed) VALUES ('{student_code}', {semester}, '{course_code}', '{course_name}', {grade_number}, '{grade_letter}', {course_passed});")
        count += 1
    if is_import:
        query = "INSERT INTO course_registration (student_code, semester, course_code, course_name, grade_number, grade_letter, course_passed) VALUES \n"
        for value in generated_data["registrations"].values():
            query += f"('{value[0]}', {value[1]}, '{value[2]}', '{value[3]}', {value[4]}, '{value[5]}', {value[6]}),\n"
        query = query[:-2]+";\n"
        queries.append(query)

    print(count)
    return queries

def generate_select():
    pass

if __name__ == "__main__":
    generated_data = {
        "curriculums": [("curriculum_2012", 2012), ("curriculum_2016", 2016), ("curriculum_2020", 2020)],
        "lecturers": {},
        "courses": {},
        "students": {},
        "course_offerings": {},
        "schedules": [],
        "registrations": {}
    }

    with open('import.p', 'rb') as fp:
        data = pickle.load(fp)
    sql_queries = generate_entries(10, True)
    with open("Import.sql", "w") as f:
        f.write("\n".join(sql_queries))
    with open('import.p', 'wb') as fp:
        pickle.dump(generated_data, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open('10k.p', 'rb') as fp:
        data = pickle.load(fp)
    sql_queries = generate_entries(10, False)
    with open("In10k.sql", "w") as f:
        f.write("\n".join(sql_queries))
    with open('10k.p', 'wb') as fp:
        pickle.dump(generated_data, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open('500k.p', 'rb') as fp:
        data = pickle.load(fp)
    sql_queries = generate_entries(500, False)
    with open("In500k.sql", "w") as f:
        f.write("\n".join(sql_queries))
    with open('500k.p', 'wb') as fp:
        pickle.dump(generated_data, fp, protocol=pickle.HIGHEST_PROTOCOL)

    with open('1m.p', 'rb') as fp:
        data = pickle.load(fp)
    sql_queries = generate_entries(1000, False)
    with open("In1m.sql", "w") as f:
        f.write("\n".join(sql_queries))
    with open('1m.p', 'wb') as fp:
        pickle.dump(generated_data, fp, protocol=pickle.HIGHEST_PROTOCOL)


# Execute queries concurrently
# with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust 'max_workers' as needed
#     results = list(executor.map(execute_query, queries))
