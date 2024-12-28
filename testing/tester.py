import psycopg2
from concurrent.futures import ThreadPoolExecutor

# Database configuration
db_config = {
    "dbname": "your_db",
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": 5432,
}

# Load queries from file
with open("queries.sql", "r") as f:
    queries = f.read().split(";")  # Split by semicolon to get individual queries

# Function to execute a single query
def execute_query(query):
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        cur.close()
        conn.close()
        return f"Executed: {query[:30]}..."  # Log the query for debugging
    except Exception as e:
        return f"Error with query {query[:30]}: {str(e)}"

# Execute queries concurrently
with ThreadPoolExecutor(max_workers=300) as executor:  # Adjust 'max_workers' as needed
    results = list(executor.map(execute_query, queries))

# Print results
for result in results:
    print(result)
