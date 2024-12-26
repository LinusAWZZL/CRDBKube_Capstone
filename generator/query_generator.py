import random

def generate_data(total):
    # Initialize data storage
    user_data = {}
    class_data = {}
    schedule_data = []
    selected_class_data = []
    grades_data = []
    n = int(total / 82)
    count = 0
    # Step 1: Generate data for User table (no dependencies)
    for i in range(1, n):  # Generate a users
        count += 1
        uname = f'user{i}'
        password = f'pass{i}'
        user_data[uname] = (uname, password)

    # Step 2: Generate data for Class table (no dependencies)
    for i in range(1, n):  # Generate b classes
        count += 1
        class_code = f'C{i:03}'
        cname = f'Class{i}'
        sks = random.randint(2, 4)  # Random credit hours
        class_data[class_code] = (class_code, cname, sks)

    # Step 3: Generate data for Schedule table (dependent on Class)
    for i, class_code in enumerate(class_data):  # Use class_code from Class table
        for j in range(1, 3+2*i%2):  # Generate 3 b schedules
            count += 1
            t = random.randint(8,16)
            time_start = f"{t:02d}:00:00"
            time_end = f"{t+1:02d}:00:00"
            schedule_data.append((class_code, time_start, time_end))  # Use class_code

    # Step 4: Generate data for SelectedClass table (dependent on User and Class)
    for uname in user_data.keys(): # Generates 40 Grades and selected classes per student ## 80 a
        for semester in range(1,9): # Register classes for 8 semesters
            for class_code in random.sample(class_data.keys(), 5):  # Select 5 random classes
                count += 2
                selected_class_data.append((uname, class_code, semester))
                grade_number = random.randint(60, 100)
                grade_letter = assign_grade_letter(grade_number)
                grades_data.append((uname, class_code, semester, grade_number, grade_letter))

    print(count)
    # Return all generated data
    return user_data, class_data, schedule_data, selected_class_data, grades_data

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

def generate_import_queries():
    user_data, class_data, schedule_data, selected_class_data, grades_data = generate_data(10000)
    queries = []

    query_str = "INSERT INTO account (username, pass) VALUES \n"
    for user, data in user_data.items():
        query_str += f"('{user}', '{data[1]}'),\n"
    query_str = query_str[:-2] + ";"
    queries.append(query_str)

    query_str = "INSERT INTO course (class_code, class_name, sks) VALUES \n"
    for class_code, data in class_data.items():
        query_str += f"('{class_code}', '{data[1]}', {data[2]}),\n"
    query_str = query_str[:-2] + ";"
    queries.append(query_str)

    query_str = "INSERT INTO schedule (schedule_class, time_start, time_end) VALUES \n"
    for class_code, time_start, time_end in schedule_data:
        query_str += f"('{class_code}', '{time_start}', '{time_end}'),\n"
    query_str = query_str[:-2] + ";"
    queries.append(query_str)

    query_str = "INSERT INTO selected_class (sc_user, sc_class, semester) VALUES \n"
    for uname, class_code, semester in selected_class_data:
        query_str += f"('{uname}', '{class_code}', {semester}),\n"
    query_str = query_str[:-2] + ";"
    queries.append(query_str)

    query_str = "INSERT INTO grades (grade_user, grade_class, semester, grade_number, grade_letter) VALUES \n"
    for uname, class_code, semester, grade_number, grade_letter in grades_data:
        query_str += f"('{uname}', '{class_code}', {semester}, {grade_number}, '{grade_letter}'),\n"
    query_str = query_str[:-2] + ";"
    queries.append(query_str)

    return queries

def generate_insert_queries(total):
    user_data, class_data, schedule_data, selected_class_data, grades_data = generate_data(total)
    queries = []

    print(user_data)
    # Generate INSERT statements for User table
    for user, data in user_data.items():
        queries.append(f"INSERT INTO account (username, pass) VALUES (\'{user}\', \'{data[1]}\');")

    # Generate INSERT statements for Class table
    for class_code, data in class_data.items():
        queries.append(f"INSERT INTO course (class_code, class_name, sks) VALUES ('{class_code}', '{data[1]}', {data[2]});")

    # Generate INSERT statements for Schedule table
    for class_code, time_start, time_end in schedule_data:
        queries.append(f"INSERT INTO schedule (schedule_class, time_start, time_end) VALUES ('{class_code}', '{time_start}', '{time_end}');")

    # Generate INSERT statements for SelectedClass table
    for uname, class_code, semester in selected_class_data:
        queries.append(f"INSERT INTO selected_class (sc_user, sc_class, semester) VALUES ('{uname}', '{class_code}', {semester});")

    # Generate INSERT statements for Grades table
    for uname, class_code, semester, grade_number, grade_letter in grades_data:
        queries.append(f"INSERT INTO grades (user, class, semester, grade_number, grade_letter) VALUES ('{uname}', '{class_code}', {semester}, {grade_number}, '{grade_letter}');")

    return queries

# Generate and print the queries
if __name__ == "__main__":
    # generate_data(10000)
    sql_queries = generate_import_queries()
    for query in sql_queries:
        print(query)

        
            