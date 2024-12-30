import random
from faker import Faker
import psycopg2

from datetime import datetime, timedelta

# Global Filename Tag
tag = "0-"
rep = "0_"

# Initialize Faker
faker = Faker()

# Configuration for PostgreSQL database
db_config = {
    'dbname': 'defaultdb',
    'user': 'linus',
    'password': 'password',
    'host': '10.119.105.102',
    'port': 5678
}

class Group_1:
    def __init__(self):
        pass

    def search_students():
        vol_students = 300
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Get number of students
            cursor.execute("SELECT COUNT(*) FROM public.student")
            vol_students = cursor.fetchall()

            with open(f"queries/{tag}{vol_students}_SearchStudent.sql", "a+") as f:
                for _ in range(vol_students):
                    # Query for a random student by name
                    student_query = f"SELECT * FROM public.student WHERE username LIKE '%{faker.user_name()}%';"
                    cursor.execute(student_query)

                    # Write queries to file
                    f.write(f"{student_query}\n")
            
            # Close the connection
            cursor.close()
            conn.close()
                    
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def search_lecturers():
        vol_lecturers = 100
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM public.lecturer")
            vol_lecturers = cursor.fetchall()

            
            with open(f"queries/{tag}{vol_lecturers}_SearchLecturer.sql", "a+") as f:
                for _ in range(vol_lecturers):
                    # Query for a random student by name
                    lecturer_query = f"SELECT * FROM public.lecturer WHERE lecturer_name LIKE '%{faker.last_name()}%';"
                    cursor.execute(lecturer_query)

                    # Write queries to file
                    f.write(f"{lecturer_query}\n")
            
            # Close the connection
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_courses():
        vol_courses = 100
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM public.course")
            vol_courses = cursor.fetchall()

            with open(f"queries/{tag}{vol_courses}_SearchCourse.sql", "a+") as f:
                for _ in range(vol_courses):
                    # Query for a random student by name
                    course_query = f"SELECT * FROM public.student WHERE username LIKE '%{faker.first_name()}%';"
                    cursor.execute(course_query)

                    # Write queries to file
                    f.write(f"{course_query}\n")
            
            # Close the connection
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_curriculums():
        vol_curriculums = 4
        try:
            # Connect to the database
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM public.curriculum")
            vol_curriculums = cursor.fetchall()

            with open(f"queries/{tag}{vol_curriculums}_SearchCurriculum.sql", "a+") as f:
                for _ in range(vol_curriculums):
                    # Query for a random student by name
                    curriculum_query = f"SELECT * FROM public.curriculum WHERE curriculum_name LIKE '%{faker.text(max_nb_chars=20).strip().split()[0]} {faker.text(max_nb_chars=20).strip().split()[0]}%';"
                    cursor.execute(curriculum_query)

                    # Write queries to file
                    f.write(f"{curriculum_query}\n")
            
            # Close the connection
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"An error occurred: {e}")


class Group_2(): # Lecturer Generic
    n_lecturers = 100

    def __init__(self):
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM public.lecturer")
        self.n_lecturers = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

    def run(self):
        for i in range(self.n_lecturers):
            self.transaction(i)

    def transaction(loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Get a random lecturer
            cursor.execute("SELECT lecturer_name FROM public.lecturer ORDER BY RANDOM() LIMIT 1;")
            lecturer_name = cursor.fetchone()[0]

            with open(f"queries/{tag}{rep}G2_LecturerTransaction{loop}.sql", "a+") as sf:
                sf.write(f"BEGIN ;\n")

                cursor.execute("SELECT lecturer_code FROM public.lecturer WHERE lecturer_name = %s LIMIT 1;", (lecturer_name))
                lecturer_code = cursor.fetchone()[0]
                sf.write(f"SELECT lecturer_code FROM public.lecturer WHERE lecturer_name = {lecturer_name}\n")

                # Get lecturer course offering
                query = f"""
                    SELECT co.co_name, co.semester, MAX(co.semester) AS current_semester, lecturer.lecturer_name
                    FROM public.lecturer
                    JOIN public.course_offering co ON lecturer.lecturer_code = co.class_lecturer
                    WHERE lecturer.lecturer_name = {lecturer_name};
                    """
                cursor.execute(query)
                sf.write(f"{query}\n")
                current_semester = cursor.fetchone()[2]

                # Get lecturer schedule
                query = f"""
                    SELECT s.schedule_class, s.time_start, s.time_end
                    FROM public.lecturer l
                    JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
                    JOIN public.schedule s ON co.co_name = s.schedule_class
                    WHERE l.lecturer_code = '{lecturer_code}'
                    AND co.semester = {current_semester}
                    ORDER BY s.created, s.schedule_class;
                    """
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


class Group_3(): # Student Generic
    n_students = 300

    def __init__(self):
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM public.student")
        self.n_students = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

    def run(self):
        for i in range(self.n_students):
            self.transaction(i)

    def transaction(loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Pick a random student and their password
            cursor.execute("SELECT username, pass FROM public.student ORDER BY RANDOM() LIMIT 1;")
            student_data = cursor.fetchone()
            student_username, student_password = student_data

            with open(f"queries/{tag}{rep}G3_StudentTransaction_{loop}.sql", "a+") as sf:
                sf.write("BEGIN;\n")

                # Get the student's code
                cursor.execute("SELECT student_code FROM public.student WHERE username = %s, pass = %s;", (student_username, student_password))
                student_code = cursor.fetchone()[0]
                sf.write(f"SELECT student_code FROM public.student WHERE username = {student_username}, pass = {student_password};\n")

                # Get student course registration
                query = f"""
                    SELECT cr.course_code, cr.semester, cr.grade_number, cr.grade_letter
                    FROM public.student s
                    JOIN public.course_registration cr ON s.student_code = cr.student_code
                    WHERE s.student_code = '{student_code}'
                    ORDER BY cr.semester;
                """
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get student's passed SKS and grades
                query = f"""
                    SELECT SUM(c.sks) AS total_sks, AVG(cr.grade_number) AS average_grade
                    FROM public.student s
                    JOIN public.course_registration cr ON s.student_code = cr.student_code
                    JOIN public.course c ON c.course_code = cr.course_code
                    WHERE s.student_code = '{student_code}'
                    AND cr.course_passed = true;
                """
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
            print(f"Transaction {loop} completed and saved to file.")
        except Exception as e:
            print(f"An error occurred during transaction {loop}: {e}")


class Group_4(): # New Semester Insertion
    def __init__(self, loop):
        self.loop = loop
    
    def run(self):
        for i in range(self.loop):
            self.new_courses(i)
            self.new_lecturers(i)
            self.new_students(i)
            self.new_offerings(i)

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
                            VALUES ({course_code}, {course_name}, {sks}, {course_curriculum}, null);
                            """

                    try:
                        cur.execute(query)

                        with open(f"queries/{tag}{rep}{loop}_InsertCourses.sql", "a+") as sf:
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
                            VALUES ({lecturer_code}, {lecturer_name});
                            """
                            
                    try:
                        cur.execute(query)

                        with open(f"queries/{tag}{rep}{loop}_InsertLecturers.sql", "a+") as sf:
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
                            VALUES ({student_code}, {username}, {password});
                            """

                    try:
                        cur.execute(query)
                        
                        with open(f"queries/{tag}{rep}{loop}_InsertStudents.sql", "a+") as sf:
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
                            VALUES ({co_name}, {semester}, {co_course}, {class_lecturer});
                            """
                    
                    for i in range(2):
                        time_start = datetime(2024, 1, 1, random.randint(8, 16), 0, 0)
                        time_end = time_start + timedelta(minutes=50 * random.randint(1, 3))

                        query += f"""
                                INSERT INTO schedule (schedule_class, semester, schedule_course, time_start, time_end) 
                                VALUES ({co_name}, {semester}, {co_course}, {time_start}, {time_end});
                                """
                    
                    query += "COMMIT ;"

                    try:
                        cur.execute(query)
                        
                        with open(f"queries/{tag}{rep}{loop}_InsertOfferings.sql", "a+") as sf:
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


class Group_5(): # IRS / SIAK WAR
    n_students = 300
    semester = 8

    def __init__(self):
        self.semester = random.randint(1,12)
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM public.student")
        self.n_students = cursor.fetchall()

        cursor.execute("DELETE FROM course_registration WHERE semester = %s",(self.semester))

        # Close the connection
        cursor.close()
        conn.close()

    def run(self):
        for i in range(self.n_students):
            self.transaction(i)

    def transaction(self, loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Pick a random student and their password
            cursor.execute("SELECT username, pass FROM public.student ORDER BY RANDOM() LIMIT 1;")
            student_data = cursor.fetchone()
            student_username, student_password = student_data

            with open(f"queries/{tag}{rep}G5_StudentRegistration_{loop}.sql", "a+") as sf:
                sf.write("BEGIN;\n")

                # Student login
                query = f"""
                    SELECT s.student_code
                    FROM public.student s
                    WHERE s.username = '{student_username}'
                    AND s.pass = '{student_password}';
                """
                cursor.execute(query)
                student_code = cursor.fetchone()[0]
                sf.write(f"{query}\n")

                # Get available courses
                query = f"""
                    SELECT co.co_id, co.semester, co.co_name, l.lecturer_name
                    FROM public.course_offering co
                    JOIN public.lecturer l ON cr.class_lecturer = l.lecturer_code
                    WHERE co.semester = {self.semester};
                """
                cursor.execute(query)
                offerings = cursor.fetchall()
                sf.write(f"{query}\n")

                # Register to offerings
                registered = []
                query = f"""
                        INSERT INTO public.course_registration (student_code, semester, course_code, course_name)
                        """
                for _ in range(random.randint(3,6)):
                    offering = random.choice(offerings)
                    while (self.semester, offering[0], offering[2]) in registered:
                        offering = random.choice(offerings)
                    query += f"""
                        VALUES ('{student_code}', {self.semester}, '{offering[0]}', '{offering[2]}'),
                    """
                    id = (self.semester, offering[0], offering[2])
                    registered.append(id)
                query = query[-1] + ";"
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get student course registration
                query = f"""
                    SELECT cr.cr_id, cr.course_name, s.student_code, l.lecturer_name
                    FROM public.student s
                    JOIN public.course_registration cr ON s.student_code = cr.student_code
                    JOIN public.course_offering co ON cr.cr_id = co.co_id
                    JOIN public.lecturer l ON co.class_lecturer = l.lecturer_code
                    WHERE s.student_code = '{student_code}'
                    AND cr.semester = {self.semester};
                """
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
                        AND course_name = '{registration[1]}';
                    """
                    id = (self.semester, offering[0], offering[2])
                    registered.remove(id)
                    cursor.execute(query)
                    sf.write(f"{query}\n")

                # Add courses
                registered_codes = {reg[0] for reg in registered}
                new_courses = [off for off in offerings if off[0] not in registered_codes]
                query = f"""
                        INSERT INTO public.course_registration (student_code, semester, course_code, course_name)
                        VALUES
                        """
                for _ in range(min(random.randint(1, 4), len(new_courses))):
                    new_course = random.choice(new_courses)
                    query += f"""
                            ('{student_code}', {loop}, '{new_course[0]}', '{new_course[2]}'),
                            """
                query = query[-1] + ";"
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
                    AND s.semester = {self.semester};
                """
                cursor.execute(query)
                sf.write(f"{query}\n")

                sf.write("END;\n")

            cursor.close()
            conn.close()
            print(f"Transaction {loop} completed and saved to file.")
        except Exception as e:
            print(f"An error occurred during transaction {loop}: {e}")


class Group_6(): # Grading
    n_lecturers = 100
    semester = 8

    def __init__(self):
        self.semester = random.randint(1,12)
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM public.lecturer")
        self.n_lecturers = cursor.fetchall()

        cursor.execute("""UPDATE course_offering 
                       SET grade_letter = NULL, grade_number = NULL, course_passed = FALSE
                       WHERE semester = %s""", (self.semester))

        # Close the connection
        cursor.close()
        conn.close()

    def run(self):
        for i in range(self.n_lecturers):
            self.transaction(i)
    
    def transaction(self, loop):
        try:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            # Pick a random lecturer
            cursor.execute("SELECT lecturer_name FROM public.lecturer ORDER BY RANDOM() LIMIT 1;")
            lecturer_name = cursor.fetchone()[0]

            # Open a file to save the transaction queries
            with open(f"queries/{tag}{rep}G6_LecturerTransaction_{loop}.sql", "a+") as sf:
                sf.write("BEGIN;\n")

                # Pick a random lecturer code
                cursor.execute("SELECT lecturer_code FROM public.lecturer WHERE lecturer_name = %s LIMIT 1;", (lecturer_name))
                lecturer_code = cursor.fetchone()[0]

                # Get Lecturer Current Course Offering
                query = f"""
                    SELECT co.course_id, co.semester, co.co_name
                    FROM public.lecturer l
                    JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
                    WHERE l.lecturer_code = '{lecturer_code}'
                    AND co.semester = {self.semester};
                """
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get Lecturer Current Course Students Grades
                query = f"""
                    SELECT st.student_code, st.username, cr.grade_letter, cr.grade_number, cr.course_passed
                    FROM public.lecturer l
                    JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
                    JOIN public.course_registration cr ON co.course_id = cr.course_code
                    JOIN public.student st ON cr.student_code = st.student_code
                    WHERE l.lecturer_code = '{lecturer_code}'
                    AND co.semester = {self.semester};
                """
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
                        SELECT co.course_id
                        FROM public.course_offering co
                        JOIN public.lecturer l ON co.class_lecturer = l.lecturer_code
                        WHERE l.lecturer_code = '{lecturer_code}'
                        AND co.semester = {self.semester}
                    )
                    AND grade_letter IS NULL;
                """
                cursor.execute(query)
                sf.write(f"{query}\n")

                # Get Class Average
                query = f"""
                    SELECT co.course_id, AVG(cr.grade_number) AS avg_grade
                    FROM public.lecturer l
                    JOIN public.course_offering co ON l.lecturer_code = co.class_lecturer
                    JOIN public.course_registration cr ON co.course_id = cr.course_code
                    WHERE l.lecturer_code = '{lecturer_code}'
                    AND co.semester = {self.semester}
                    GROUP BY co.course_id;
                """
                cursor.execute(query)
                sf.write(f"{query}\n")

                sf.write("END;\n")

            cursor.close()
            conn.commit()
            conn.close()
            print(f"Lecturer transaction {loop} completed and saved to file.")
        except Exception as e:
            print(f"An error occurred during lecturer transaction {loop}: {e}")

''' class Group_7(): # FAULT In another file
     def __init__(self):
         pass
    
     def run(self):
         pass'''

class Group_8(): # EXPENSIVE
    most_costly = ""
    usable_costly = ""

    def __init__(self):
        self.most_costly = """SELECT s.student_code, s.username, cr.grade, co.course_code, co.course_name, l.lecturer_name, SUM(c.sks) AS total_sks, AVG(cr.grade) AS average_grade  
                           FROM student s 
                           JOIN course_registration cr ON s.student_code = cr.student_code 
                           JOIN course_offering co ON cr.course_id = co.course_id 
                           JOIN lecturer l ON co.lecturer_code = l.lecturer_code  
                           JOIN course c ON co.course_code = c.course_code 
                           WHERE cr.course_passed = true 
                           GROUP BY s.student_code, s.username, cr.grade, co.course_code, co.course_name, l.lecturer_name 
                           ORDER BY total_sks DESC, average_grade DESC;"""
        
        self.usable_costly = """SELECT s.student_code, s.username, SUM(c.sks) AS total_sks, AVG(cr.grade_number) AS average_grade, curr.curriculum_year, curr.curriculum_name  
                            FROM student s 
                            JOIN course_registration cr 
                                ON s.student_code = cr.student_code 
                            JOIN course_offering co 
                                ON cr.course_code = co.co_course AND cr.semester = co.semester 
                            JOIN course c 
                                ON co.co_course = c.course_code 
                            JOIN curriculum curr 
                                ON c.course_curriculum = curr.curriculum_year 
                            JOIN (
                                SELECT curriculum_year, mode() WITHIN GROUP (ORDER BY course_name) AS most_common_course_name
                                FROM course
                                GROUP BY curriculum_year
                            ) mc 
                                ON c.course_curriculum = mc.curriculum_year 
                            WHERE cr.course_passed = true 
                            GROUP BY s.student_code, s.username, curr.curriculum_year, curr.curriculum_name 
                            ORDER BY total_sks DESC, average_grade DESC;"""

    def run(self):
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(self.most_costly) 
        cursor.execute(self.usable_costly)

        # Write queries to file
        with open(f"queries/MostCostly.sql", "w") as f:
            f.write(f"{self.most_costly}\n")
            f.write(f"{self.usable_costly}\n")
        
        # Close the connection
        cursor.close()
        conn.close()

def test_1():
    group = Group_1()
    print("Test 1 start")
    group.search_students()
    group.search_lecturers()
    group.search_courses()
    group.search_curriculums()
    print("Test 1 done")

def test_2():
    group = Group_2()
    print("Test 2 start")
    group.run()
    print("Test 2 done")

def test_3():
    group = Group_3()
    print("Test 3 start")
    group.run()
    print("Test 3 done")

def test_4():
    group = Group_4()
    print("Test 4 start")
    group.run()
    print("Test 4 done")

def test_5():
    group = Group_5()
    print("Test 5 start")
    group.run()
    print("Test 5 done")

def test_6():
    group = Group_6()
    print("Test 6 start")
    group.run()
    print("Test 6 done")

'''def test_7():
    group = Group_7()
    print("Test 7 start")
    group.run()
    print("Test 7 done")'''

def test_8():
    group = Group_8()
    print("Test 8 start")
    group.run()
    print("Test 8 done")

if __name__ == "__main__":
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    # test_7()
    test_8()