import random
from faker import Faker
import psycopg2

# Initialize Faker
faker = Faker()

# Function to generate search queries in PostgreSQL format
def generate_search_queries(n):
    # Separate files for each category
    student_queries = []
    lecturer_queries = []
    course_queries = []

    for _ in range(n):
        # Query for a random student by name
        student_query = f"SELECT * FROM public.student WHERE username LIKE '%{faker.first_name()}%';"
        student_queries.append(student_query)

        # Query for a random lecturer by name
        lecturer_query = f"SELECT * FROM public.lecturer WHERE lecturer_name LIKE '%{faker.last_name()}%';"
        lecturer_queries.append(lecturer_query)

        # Query for a random course by name
        course_query = f"SELECT * FROM public.course WHERE course_name LIKE '%{faker.text(max_nb_chars=20).strip().split()[0]}%';"
        course_queries.append(course_query)

    # Write queries to separate files
    with open(f"queries/{n}_SearchStudent.sql", "w") as f:
        for query in student_queries:
            f.write(f"{query}\n")

    with open(f"queries/{n}_SearchLecturer.sql", "w") as f:
        for query in lecturer_queries:
            f.write(f"{query}\n")

    with open(f"queries/{n}_SearchCourse.sql", "w") as f:
        for query in course_queries:
            f.write(f"{query}\n")

    return student_queries + lecturer_queries + course_queries

# Function to execute the queries
def execute_queries(queries, db_config):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        for query in queries:
            cursor.execute(query)
            results = cursor.fetchall()
            print(f"Results for query: {query}")
            for row in results:
                print(row)

        # Close the connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to fetch names from the database and append them to files
def fetch_and_save_names(n, db_config):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Fetch and append student names
        cursor.execute("SELECT username FROM public.student ORDER BY RANDOM() LIMIT %s;", (n,))
        students = cursor.fetchall()
        with open(f"queries/{n}_NamesStudents.txt", "w") as f:
            for student in students:
                f.write(f"{student[0]}\n")

        # Fetch and append lecturer names
        cursor.execute("SELECT lecturer_name FROM public.lecturer ORDER BY RANDOM() LIMIT %s;", (n,))
        lecturers = cursor.fetchall()
        with open(f"queries/{n}_NamesLecturers.txt", "w") as f:
            for lecturer in lecturers:
                f.write(f"{lecturer[0]}\n")

        # Fetch and append course names
        cursor.execute("SELECT course_name FROM public.course ORDER BY RANDOM() LIMIT %s;", (n,))
        courses = cursor.fetchall()
        with open(f"queries/{n}_NamesCourses.txt", "w") as f:
            for course in courses:
                f.write(f"{course[0]}\n")

        # Close the connection
        cursor.close()
        conn.close()
        print("Names have been appended to files.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Configuration for PostgreSQL database
db_config = {
    'dbname': 'defaultdb',
    'user': 'linus',
    'password': 'password',
    'host': '10.119.105.102',
    'port': 5678
}

# Generate and run N search queries
N = 1000  # Change this number to control the number of search queries per type
queries = generate_search_queries(N)
execute_queries(queries, db_config)

# Fetch names and append them to files
fetch_and_save_names(N, db_config)
