import random
import time
from faker import Faker
import psycopg2
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime, timedelta

# Global Filename Tag
tag = "0-"
rep = "0_"

# Initialize Faker
faker = Faker()

# Variables
## Config
quiet = True
block = "10k"
N_WORKERS = 100

## Configuration for PostgreSQL database
pslq_config = {
    'dbname': 'defaultdb',
    'user': 'linus',
    'password': 'password',
    'host': '10.119.105.102',
    'port': 5678
}
crdb_config = {
    'dbname': 'defaultdb',
    'user': 'linus',
    'password': 'password',
    'host': '10.119.105.102',
    'port': 30017
}
db_config = crdb_config

class Group_1: # Generic :: Multithread
    def __init__(self):
        pass

    def run_students(self, vol_students):
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        with open(f"gen_queries/{block}/G1/{tag}{vol_students}_SearchStudent.sql", "a+") as f:
            # Query for a random student by name
            student_query = f"SELECT * FROM public.student WHERE username LIKE '%{faker.user_name()}%';"
            cursor.execute(student_query)

            # Write queries to file
            f.write(f"{student_query}\n")
        cursor.close()
        conn.close()

    def search_students(self):
        print("search_students")
        vol_students = 300
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Get number of students
            cursor.execute("SELECT COUNT(*) FROM public.student")
            vol_students = cursor.fetchone()[0]

            with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
                executor.map(self.run_students(vol_students), range(vol_students))
            
            # Close the connection
            cursor.close()
            conn.close()
                    
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def run_lecturers(self, vol_lecturers):
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        with open(f"gen_queries/{block}/G1/{tag}{vol_lecturers}_SearchLecturer.sql", "a+") as f:
            # Query for a random student by name
            lecturer_query = f"SELECT * FROM public.lecturer WHERE lecturer_name LIKE '%{faker.last_name()}%';"
            cursor.execute(lecturer_query)

            # Write queries to file
            f.write(f"{lecturer_query}\n")
        cursor.close()
        conn.close()

    def search_lecturers(self):
        print("search_lecturers")
        vol_lecturers = 100
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM public.lecturer")
            vol_lecturers = cursor.fetchone()[0]

            with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
                executor.map(self.run_lecturers(vol_lecturers), range(vol_lecturers))
            
            # Close the connection
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def run_courses(self, vol_courses):
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        with open(f"gen_queries/{block}/G1/{tag}{vol_courses}_SearchCourse.sql", "a+") as f:
            # Query for a random student by name
            course_query = f"SELECT * FROM public.student WHERE username LIKE '%{faker.first_name()}%';"
            cursor.execute(course_query)

            # Write queries to file
            f.write(f"{course_query}\n")
        cursor.close()
        conn.close()

    def search_courses(self):
        print("search_courses")
        vol_courses = 100
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM public.course")
            vol_courses = cursor.fetchone()[0]

            with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
                executor.map(self.run_courses(vol_courses), range(vol_courses))
            
            # Close the connection
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def run_curriculums(self, vol_curriculums):
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        with open(f"gen_queries/{block}/G1/{tag}{vol_curriculums}_SearchCurriculum.sql", "a+") as f:
            # Query for a random student by name
            curriculum_query = f"SELECT * FROM public.curriculum WHERE curriculum_name LIKE '%{faker.text(max_nb_chars=20).strip().split()[0]} {faker.text(max_nb_chars=20).strip().split()[0]}%';"
            cursor.execute(curriculum_query)

            # Write queries to file
            f.write(f"{curriculum_query}\n")
        cursor.close()
        conn.close()

    def search_curriculums(self):
        print("search_curriculums")
        vol_curriculums = 4
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM public.curriculum")
            vol_curriculums = max(cursor.fetchone()[0], vol_curriculums)

            with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
                executor.map(self.run_curriculums(vol_curriculums), range(vol_curriculums))
            
            # Close the connection
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")


class Group_2(): # Lecturer Generic :: Multithread
    n_lecturers = 1000

    def __init__(self):
        # # Connect to the database
        # conn = psycopg2.connect(**db_config)
        # cursor = conn.cursor()

        # cursor.execute("SELECT COUNT(*) FROM public.lecturer")
        # self.n_lecturers = cursor.fetchone()[0]

        # # Close the connection
        # cursor.close()
        # conn.close()

        pass

    def run(self):
        print("+", end="")
        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda loop: self.transaction(loop), range(self.n_lecturers))
        print("x")

    def transaction(self, loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Get a random lecturer
            cursor.execute("SELECT lecturer_name FROM public.lecturer ORDER BY RANDOM() LIMIT 1;")
            lecturer_name = cursor.fetchone()[0]
            # print(f"SELECT lecturer_code FROM public.lecturer WHERE lecturer_name = {lecturer_name};\n")

            with open(f"gen_queries/{block}/G2/{tag}{rep}LecturerTransaction{loop}.sql", "a+") as sf:
                sf.write(f"BEGIN ;\n")

                query = f"SELECT lecturer_code FROM public.lecturer WHERE lecturer_name = '{lecturer_name}' LIMIT 1;\n"
                cursor.execute(query)
                lecturer_code = cursor.fetchone()[0]
                sf.write(query)

                # Get lecturer course offering
                query = f"""
SELECT co.co_name, co.semester, co.co_course, lecturer.lecturer_name
FROM public.lecturer
JOIN public.course_offering co ON lecturer.lecturer_code = co.class_lecturer
WHERE lecturer.lecturer_name = '{lecturer_name}'
ORDER BY co.co_course;"""
                cursor.execute(query)
                sf.write(f"{query}\n")
                semesters = [1] + [t[1] for t in cursor.fetchall()] 
                current_semester = max(semesters)

                # Get lecturer schedule
                query = f"""
SELECT s.schedule_class, s.time_start, s.time_end
FROM public.lecturer l
JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
JOIN public.schedule s ON co.co_name = s.schedule_class
WHERE l.lecturer_code = '{lecturer_code}'
AND co.semester = {current_semester}
ORDER BY s.created, s.schedule_class;"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get lecturer students
                query = f"""
SELECT st.student_code, st.username, cr.course_code
FROM public.lecturer l
JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
JOIN public.course_registration cr ON co.co_course = cr.course_code
JOIN public.student st ON cr.student_code = st.student_code
WHERE l.lecturer_code = '{lecturer_code}'
AND co.semester = {current_semester}
ORDER BY st.created, st.student_code;
                    """
                cursor.execute(query)
                sf.write(f"{query}\n")

                sf.write(f"END ; \n")
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")


class Group_3(): # Student Generic :: Multithread
    n_students = 2000

    def __init__(self):
        # # Connect to the database
        # conn = psycopg2.connect(**db_config)
        # cursor = conn.cursor()

        # cursor.execute("SELECT COUNT(*) FROM public.student")
        # self.n_students = cursor.fetchone()[0]

        # # Close the connection
        # cursor.close()
        # conn.close()

        pass

    def run(self):
        print("+", end="")
        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda loop: self.transaction(loop), range(self.n_students))
        print("x")

    def transaction(self, loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Pick a random student and their password
            cursor.execute("SELECT username, pass FROM public.student ORDER BY RANDOM() LIMIT 1;")
            student_data = cursor.fetchone()
            student_username, student_password = student_data

            with open(f"gen_queries/{block}/G3/{tag}{rep}StudentTransaction_{loop}.sql", "a+") as sf:
                sf.write("BEGIN;\n")

                # Get the student's code
                cursor.execute("SELECT student_code FROM public.student WHERE username = %s AND pass = %s;", (student_username, student_password))
                student_code = cursor.fetchone()[0]
                sf.write(f"SELECT student_code FROM public.student WHERE username = {student_username} AND pass = {student_password};\n")

                # Get student course registration
                query = f"""
SELECT cr.course_code, cr.semester, cr.grade_number, cr.grade_letter
FROM public.student s
JOIN public.course_registration cr ON s.student_code = cr.student_code
WHERE s.student_code = '{student_code}'
ORDER BY cr.semester;"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get student's passed SKS and grades
                query = f"""
SELECT SUM(c.sks) AS total_sks, AVG(cr.grade_number) AS average_grade
FROM public.student s
JOIN public.course_registration cr ON s.student_code = cr.student_code
JOIN public.course c ON c.course_code = cr.course_code
WHERE s.student_code = '{student_code}'
AND cr.course_passed = true;"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get student's schedule for the latest semester
                query = f"""
SELECT s.schedule_class, s.time_start, s.time_end
FROM public.student st
JOIN public.course_registration cr ON st.student_code = cr.student_code
JOIN public.schedule s ON s.schedule_class = cr.course_code
WHERE st.student_code = '{student_code}'
AND s.semester = (
    SELECT MAX(cr.semester)
    FROM public.student st
    JOIN public.course_registration cr ON st.student_code = cr.student_code
    WHERE st.student_code = '{student_code}'
);
                """
                cursor.execute(query)
                sf.write(f"{query}\n")

                sf.write("END;\n")

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred during transaction {loop}: {e}")


class Group_4(): # New Semester Insertion
    def __init__(self, loop):
        self.loop = loop
    
    def run(self):
        print("+", end="")
        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda i: self.new_courses(i), range(self.loop))
        print("~", end="")

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda i: self.new_lecturers(i), range(self.loop))
        print("~", end="")

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda i: self.new_students(i), range(self.loop))
        print("~", end="")

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda i: self.new_offerings(i), range(self.loop))
        print("x")


    def new_courses(self, loop):
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            with conn.cursor() as cur:
                # Fetch available curriculums
                cur.execute("SELECT curriculum_year FROM public.curriculum;")
                curriculums = [row[0] for row in cur.fetchall()]

                for _ in range(10):
                    course_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
                    course_name = faker.catch_phrase()
                    sks = random.choice([2, 3, 4])
                    course_curriculum = random.choice(curriculums) if curriculums else None
                    # prerequisite = None if random.choice([True, False]) else ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

                    if not course_curriculum:
                        continue  # Skip if no curriculum is available

                    query = f"""
INSERT INTO public.course (course_code, course_name, sks, course_curriculum, prerequisite)
VALUES ('{course_code}', '{course_name}', {sks}, '{course_curriculum}', NULL);"""

                    try:
                        cur.execute(query)

                        with open(f"gen_queries/{block}/G4/{tag}{rep}InsertCourses_{loop}.sql", "a+") as sf:
                            sf.write(f"{query}\n")
                    except psycopg2.IntegrityError as e:
                        print("integrity error", e)
                        # conn.rollback()  # Handle duplicate primary key issues
                        continue
                    
                conn.commit()

            # Close the connection
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def new_lecturers(self, loop):
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            with conn.cursor() as cur:
                for _ in range(10):
                    lecturer_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=20))
                    lecturer_name = faker.name()

                    query = f"""
INSERT INTO public.lecturer (lecturer_code, lecturer_name)
VALUES ('{lecturer_code}', '{lecturer_name}');"""
                            
                    try:
                        cur.execute(query)

                        with open(f"gen_queries/{block}/G4/{tag}{rep}InsertLecturers_{loop}.sql", "a+") as sf:
                            sf.write(f"{query}\n")
                    except psycopg2.IntegrityError:
                        conn.rollback()  # Handle duplicate primary key issues
                        continue
                conn.commit()

            # Close the connection
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")
                
    def new_students(self, loop):
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            with conn.cursor() as cur:
                for _ in range(10):
                    student_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
                    username = faker.user_name()
                    password = faker.password()

                    query = f"""
INSERT INTO public.student (student_code, username, pass)
VALUES ('{student_code}', '{username}', '{password}');"""

                    try:
                        cur.execute(query)
                        
                        with open(f"gen_queries/{block}/G4/{tag}{rep}InsertStudents_{loop}.sql", "a+") as sf:
                            sf.write(f"{query}\n")
                    except psycopg2.IntegrityError:
                        conn.rollback()  # Handle duplicate primary key issues
                        continue
                conn.commit()

            # Close the connection
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def new_offerings(self, loop):
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            with conn.cursor() as cur:# Fetch available courses and lecturers
                cur.execute("SELECT course_code FROM public.course;")
                courses = [row[0] for row in cur.fetchall()]

                cur.execute("SELECT lecturer_code FROM public.lecturer;")
                lecturers = [row[0] for row in cur.fetchall()]
                for _ in range(10):
                    co_name = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))
                    semester = random.choice(range(1, 9))
                    co_course = random.choice(courses) if courses else None
                    class_lecturer = random.choice(lecturers) if lecturers else None

                    query = f"""
BEGIN ;
INSERT INTO public.course_offering (co_name, semester, co_course, class_lecturer)
VALUES ('{co_name}', {semester}, '{co_course}', '{class_lecturer}');"""
                    
                    for i in range(2):
                        time_start = datetime(2024, 1, 1, random.randint(8, 16), 0, 0)
                        time_end = time_start + timedelta(minutes=50 * random.randint(1, 3))

                        time_start = time_start.strptime(str(time_start), "%Y-%m-%d %H:%M:%S").time().isoformat()
                        time_end = time_end.strptime(str(time_end), "%Y-%m-%d %H:%M:%S").time().isoformat()

                        query += f"""INSERT INTO schedule (schedule_class, semester, schedule_course, time_start, time_end) 
VALUES ('{co_name}', {semester}, '{co_course}', '{time_start}', '{time_end}');
"""
                    
                    query += "END ;"

                    try:
                        cur.execute(query)
                        
                        with open(f"gen_queries/{block}/G4/{tag}{rep}InsertOfferings_{loop}.sql", "a+") as sf:
                            sf.write(f"{query}\n")
                    except psycopg2.IntegrityError:
                        conn.rollback()  # Handle duplicate primary key issues
                        continue
                conn.commit()

            # Close the connection
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")


class Group_5(): # IRS / SIAK WAR :: Multithread
    n_students = 200
    semester = 8

    def __init__(self):
        self.semester = random.randint(1,8)
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # cursor.execute("SELECT COUNT(*) FROM public.student")
        # self.n_students = cursor.fetchone()[0]

        query = f"DELETE FROM course_registration WHERE semester = {self.semester}"
        cursor.execute(query)

        # Close the connection
        cursor.close()
        conn.close()

    def run(self):
        print("+", end="")
        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda i: self.transaction(i), range(self.n_students))
        print("x")

    def transaction(self, loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Pick a random student and their password
            cursor.execute("SELECT username, pass FROM public.student ORDER BY RANDOM() LIMIT 1;")
            student_data = cursor.fetchone()
            student_username, student_password = student_data

            with open(f"gen_queries/{block}/G5/{tag}{rep}StudentRegistration_{loop}.sql", "a+") as sf:
                sf.write("BEGIN;\n")

                # Student login
                query = f"""
SELECT s.student_code
FROM public.student s
WHERE s.username = '{student_username}'
AND s.pass = '{student_password}';"""
                cursor.execute(query)
                student_code = cursor.fetchone()[0]
                student_code = str(student_code)
                sf.write(f"{query}\n")

                # Get available courses
                query = f"""
SELECT co.co_course, co.semester, co.co_name, l.lecturer_name
FROM public.course_offering co
JOIN public.lecturer l ON co.class_lecturer = l.lecturer_code
WHERE co.semester = {self.semester};"""
                cursor.execute(query)
                offerings = cursor.fetchall()
                sf.write(f"{query}\n")

                # Register to offerings
                registered = []
                query = f"""
INSERT INTO public.course_registration (student_code, semester, course_code, course_name) VALUES """
                for _ in range(random.randint(3,6)):
                    offering = random.choice(offerings)
                    while (self.semester, offering[0], offering[2]) in registered:
                        offering = random.choice(offerings)
                    query += f"""('{student_code}', {self.semester}, '{offering[0]}', '{offering[2]}'),\n"""
                    id = (self.semester, offering[0], offering[2])
                    registered.append(id)
                query = query[:-2] + ";"
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get student course registration
                query = f"""
SELECT cr.course_code, cr.course_name, s.student_code, l.lecturer_name
FROM public.student s
JOIN public.course_registration cr ON s.student_code = cr.student_code
JOIN public.course_offering co ON cr.course_code = co.co_course
JOIN public.lecturer l ON co.class_lecturer = l.lecturer_code
WHERE s.student_code = '{student_code}'
AND cr.semester = {self.semester};"""
                cursor.execute(query)
                sf.write(f"{query}\n")
                
                # Drop courses
                cursor.execute(query)
                sf.write(f"{query}\n")
                for _ in range(min(random.randint(1, len(registered)), max(len(registered) - 1, 0))):
                    registration = random.choice(registered)
                    query = f"""
DELETE FROM public.course_registration
WHERE student_code = '{student_code}'
AND semester = {self.semester}
AND course_code = '{registration[0]}'
AND course_name = '{registration[1]}';"""
                    
                    id = (self.semester, offering[0], offering[2])
                    if id in registered:
                        registered.remove(id)
                    cursor.execute(query)
                    sf.write(f"{query}\n")

                # Add courses
                registered_codes = {reg[0] for reg in registered}
                new_courses = [off for off in offerings if off[0] not in registered_codes]
                # print("start")
                query = f"""
INSERT INTO public.course_registration (student_code, semester, course_code, course_name)
VALUES """
                for _ in range(min(random.randint(1, 4), len(new_courses))):
                    new_course = random.choice(new_courses)
                    query += f"('{student_code}', {self.semester}, '{new_course[0]}', '{new_course[2]}'),\n"
                query = query[:-2] + ";"
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get student's schedule for the latest semester
                query = f"""
SELECT s.schedule_class, s.time_start, s.time_end
FROM public.student st
JOIN public.course_registration cr ON st.student_code = cr.student_code
JOIN public.schedule s ON s.schedule_course = cr.course_code
AND s.schedule_class = cr.course_name
WHERE st.student_code = '{student_code}'
AND s.semester = {self.semester};"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                sf.write("\nEND;\n")

            cursor.close()
            conn.close()
        except Exception as e:
            if not(quiet):
                print(f"An error occurred during transaction {loop}: {e} \n {query}")


class Group_6(): # Grading :: Multithread
    n_lecturers = 1000
    semester = 8

    def __init__(self):
        self.semester = random.randint(1,12)
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # cursor.execute("SELECT COUNT(*) FROM public.lecturer")
        # self.n_lecturers = cursor.fetchone()[0]

        query = f"""UPDATE course_registration
                    SET grade_letter = NULL, grade_number = NULL, course_passed = FALSE
                    WHERE semester = {self.semester}"""
        cursor.execute(query)

        # Close the connection
        cursor.close()
        conn.close()

    def run(self):
        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda i: self.transaction(i), range(self.n_lecturers))
    
    def transaction(self, loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Pick a random lecturer
            cursor.execute("SELECT lecturer_name FROM public.lecturer ORDER BY RANDOM() LIMIT 1;")
            lecturer_name = cursor.fetchone()[0]

            # Open a file to save the transaction queries
            with open(f"gen_queries/{block}/G6/{tag}{rep}LecturerTransaction_{loop}.sql", "a+") as sf:
                sf.write("BEGIN;\n")

                # Pick a random lecturer code
                query = f"SELECT lecturer_code FROM public.lecturer WHERE lecturer_name = '{lecturer_name}' LIMIT 1;"
                cursor.execute(query)
                lecturer_code = cursor.fetchone()[0]
                sf.write(f"{query}\n")

                # Get Lecturer Current Course Offering
                query = f"""
SELECT co.co_course, co.semester, co.co_name
FROM public.lecturer l
JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
WHERE l.lecturer_code = '{lecturer_code}'
AND co.semester = {self.semester};"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get Lecturer Current Course Students Grades
                query = f"""
SELECT st.student_code, st.username, cr.grade_letter, cr.grade_number, cr.course_passed
FROM public.lecturer l
JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
JOIN public.course_registration cr ON co.co_course = cr.course_code
JOIN public.student st ON cr.student_code = st.student_code
WHERE l.lecturer_code = '{lecturer_code}'
AND co.semester = {self.semester};"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Add Student Grades [Transaction] for all students with no grade
                query = f"""
UPDATE public.course_registration
SET grade_letter = CASE
    WHEN random() > 0.7 THEN 'A'
    WHEN random() > 0.6 THEN 'B'
    WHEN random() < 0.1 THEN 'E'
    ELSE 'C' END,
    course_passed = CASE
    WHEN grade_letter IN ('A', 'B', 'C') THEN true ELSE false END
WHERE course_code IN (
    SELECT co.co_course
    FROM public.course_offering co
    JOIN public.lecturer l ON co.class_lecturer = l.lecturer_code
    WHERE l.lecturer_code = '{lecturer_code}'
    AND co.semester = {self.semester}
)
AND grade_letter IS NULL;"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get Class Average
                query = f"""
SELECT co.co_course, AVG(cr.grade_number) AS avg_grade
FROM public.lecturer l
JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
JOIN public.course_registration cr ON co.co_course = cr.course_code
WHERE l.lecturer_code = '{lecturer_code}'
AND co.semester = {self.semester}
GROUP BY co.co_course;
"""
                cursor.execute(query)
                sf.write(f"{query}\n")

                sf.write("END;\n")

            cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"An error occurred during lecturer transaction {loop}: {e}")


''' class Group_7(): # FAULT
     def __init__(self):
         pass
    
     def run(self):
         pass'''


class Group_8(): # EXPENSIVE
    most_costly = ""
    usable_costly = ""

    def __init__(self):
        self.most_costly = """SELECT s.student_code, s.username, SUM(c.sks) AS total_sks, AVG(cr.grade_number) AS average_grade, l.lecturer_name, co.co_name, c.course_name, co.co_course  
FROM student s 
JOIN course_registration cr ON s.student_code = cr.student_code 
JOIN course_offering co ON cr.course_code = co.co_course 
JOIN lecturer l ON co.class_lecturer = l.lecturer_code  
JOIN course c ON co.co_course = c.course_code 
WHERE cr.course_passed = true 
GROUP BY s.student_code, s.username, co.co_course, c.course_name, co.co_name, l.lecturer_name 
ORDER BY total_sks DESC, average_grade DESC;
"""
        
        self.usable_costly = """WITH most_common_courses AS (
    SELECT 
        course_curriculum, 
        course_name,
        COUNT(*) AS course_count,
        ROW_NUMBER() OVER (PARTITION BY course_curriculum ORDER BY COUNT(*) DESC, course_name) AS row_num
    FROM course
    GROUP BY course_curriculum, course_name
)
SELECT 
    s.student_code, 
    s.username, 
    SUM(c.sks) AS total_sks, 
    AVG(cr.grade_number) AS average_grade, 
    curr.curriculum_year, 
    curr.curriculum_name,
    mc.course_name AS most_common_course_name
FROM student s
JOIN course_registration cr 
    ON s.student_code = cr.student_code
JOIN course_offering co 
    ON cr.course_code = co.co_course AND cr.semester = co.semester
JOIN course c 
    ON co.co_course = c.course_code
JOIN curriculum curr 
    ON c.course_curriculum = curr.curriculum_year
JOIN most_common_courses mc 
    ON c.course_curriculum = mc.course_curriculum 
    AND mc.row_num = 1  -- Get the most common course name per curriculum
WHERE cr.course_passed = true
GROUP BY s.student_code, s.username, curr.curriculum_year, curr.curriculum_name, mc.course_name
ORDER BY total_sks DESC, average_grade DESC;"""

    def run(self):
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(self.most_costly) 
        cursor.execute(self.usable_costly)

        # Write queries to file
        with open(f"gen_queries/{block}/MostCostly.sql", "w") as f:
            f.write(f"{self.most_costly}\n")
            f.write(f"{self.usable_costly}\n")
        
        # Close the connection
        cursor.close()
        conn.close()


def test_1():
    group = Group_1()
    start_time = time.time()
    print("Test 1 start")
    group.search_students()
    group.search_lecturers()
    group.search_courses()
    group.search_curriculums()
    execution_time = time.time() - start_time
    print(f"Test 1 done in {execution_time}")

    with open(f"time_results.txt", "a+") as f:
        f.write(f"g1 :: {execution_time}\n")

def test_2():
    group = Group_2()
    start_time = time.time()
    print("Test 2 start")
    group.run()
    execution_time = time.time() - start_time
    print(f"Test 2 done in {execution_time}")

    with open(f"time_results.txt", "a+") as f:
        f.write(f"g2 :: {execution_time}\n")

def test_3():
    group = Group_3()
    start_time = time.time()
    print("Test 3 start")
    group.run()
    execution_time = time.time() - start_time
    print(f"Test 3 done in {execution_time}")

    with open(f"time_results.txt", "a+") as f:
        f.write(f"g3 :: {execution_time}\n")

def test_4():
    group = Group_4(14)
    start_time = time.time()
    print("Test 4 start")
    group.run()
    execution_time = time.time() - start_time
    print(f"Test 4 done in {execution_time}")

    with open(f"time_results.txt", "a+") as f:
        f.write(f"g4 :: {execution_time}\n")

def test_5():
    group = Group_5()
    start_time = time.time()
    print("Test 5 start")
    group.run()
    execution_time = time.time() - start_time
    print(f"Test 5 done in {execution_time}")

    with open(f"time_results.txt", "a+") as f:
        f.write(f"g5 :: {execution_time}\n")

def test_6():
    group = Group_6()
    start_time = time.time()
    print("Test 6 start")
    group.run()
    execution_time = time.time() - start_time
    print(f"Test 6 done in {execution_time}")

    with open(f"time_results.txt", "a+") as f:
        f.write(f"g6 :: {execution_time}\n")

'''def test_7():
    group = Group_7()
    print("Test 7 start")
    group.run()
    print("Test 7 done")'''

def test_8():
    group = Group_8()
    start_time = time.time()
    print("Test 8 start")
    group.run()
    execution_time = time.time() - start_time
    print(f"Test 8 done in {execution_time}")

    with open(f"time_results.txt", "a+") as f:
        f.write(f"g8 :: {execution_time}\n")

def data_import():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("Importing Start")

    start_time = time.time()
    with open('queries/00setup/0_import.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        cursor.execute(sql_content)
        conn.commit()

    execution_time = time.time() - start_time
    print(f"Importing finished in {execution_time}")

    cursor.close()
    conn.close()
    with open(f"time_import.txt", "a+") as f:
        f.write(f"{execution_time}\n")

def statement(query):
    if query.strip():  # Skip empty statements
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

def in10k(mode):
    print("In10k Start")

    init_time = time.time()
    start_time = time.time()
    with open('queries/00setup/1_10k_1_curriculum.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} curriculum\n")

    start_time = time.time()
    with open('queries/00setup/1_10k_1_lecturer.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} lecturer\n")
    
    start_time = time.time()
    with open('queries/00setup/1_10k_1_student.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} student\n")

    start_time = time.time()
    with open('queries/00setup/1_10k_2_course.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} course\n")
    
    start_time = time.time()
    with open('queries/00setup/1_10k_3_course_offering.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} offering\n")

    start_time = time.time()
    with open('queries/00setup/1_10k_4_course_registration.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} registration\n")

    start_time = time.time()
    with open('queries/00setup/1_10k_4_schedule.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} schedule\n")

    print(f"Importing finished in {time.time() - init_time}")
    with open(f"time_in10k.txt", "a+") as f:
        f.write(f"{mode} total {time.time() - init_time}\n\n")
    cursor.close()
    conn.close()

def in500k(mode):
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    print("In500k Start")

    init_time = time.time()
    start_time = time.time()
    with open('queries/00setup/2_500k_1_curriculum.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} curriculum\n")

    start_time = time.time()
    with open('queries/00setup/2_500k_1_lecturer.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} lecturer\n")
    
    start_time = time.time()
    with open('queries/00setup/2_500k_1_student.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} student\n")

    start_time = time.time()
    with open('queries/00setup/2_500k_2_course.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} course\n")
    
    start_time = time.time()
    with open('queries/00setup/2_500k_3_course_offering.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} offering\n")

    start_time = time.time()
    with open('queries/00setup/2_500k_4_course_registration.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} registration\n")

    start_time = time.time()
    with open('queries/00setup/2_500k_4_schedule.sql', 'r') as sql_file:
        sql_content = sql_file.read()
        sql_statements = sql_content.split(';')

        with ThreadPoolExecutor(max_workers=N_WORKERS) as executor:
            executor.map(lambda statement: statement(conn, statement), sql_statements)

        # cursor.execute(sql_content)
        # conn.commit()
    execution_time = time.time() - start_time
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} {execution_time} schedule\n")

    print(f"Importing finished in {time.time() - init_time}")
    with open(f"time_in500k.txt", "a+") as f:
        f.write(f"{mode} total {time.time() - init_time}\n\n")
    cursor.close()
    conn.close()

def clean():
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("TRUNCATE course, course_offering, course_registration, curriculum, lecturer, schedule, student cascade;")
    conn.commit()

    cursor.close()
    conn.close()
    pass

if __name__ == "__main__":
    print("DB Connection Test")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # cursor.execute("SELECT COUNT(*) FROM public.student;")
        # print(cursor.fetchone()[0])
        cursor.execute("SELECT version();")
        print(cursor.fetchone()[0])

        cursor.close()
        conn.close()
        print("connection success")
    except:
        print("connection failed")

    print("\nClean Insert")
    # Data Insertion clean
    clean()
    data_import()
    clean()
    in10k("clean")
    clean()
    in500k("clean")
    clean()

    print("\nOperations")
    # Import
    print("=10k")
    data_import()
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    ## test_7()
    test_8()

    # In10k
    print("=20k")
    block = "20k"
    in10k("dirty")
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    ## test_7()
    test_8()

    # # In500k
    print("=500k")
    block = "520k"
    in500k("dirty")
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    # ## test_7()
    test_8()