import os
from datetime import datetime

def generate_sql_script(table_name, primary_key_column, conflicting_values, output_dir="sql_scripts"):
    """
    Generates an SQL script to test primary key conflict and rollback for a specified table.

    Args:
        table_name (str): Name of the table.
        primary_key_column (str): Primary key column for the table.
        conflicting_values (list): List of values to use for intentional conflicts.
        output_dir (str): Directory to save the generated scripts.

    Returns:
        str: Path to the generated SQL script file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/test_{table_name}_conflict_{timestamp}.sql"

    with open(filename, "w") as file:
        file.write("-- Begin the transaction\n")
        file.write("BEGIN;\n\n")

        # Insert the first valid record
        file.write(f"-- Insert a valid record\n")
        file.write(f"INSERT INTO {table_name} ({primary_key_column}) VALUES ('{conflicting_values[0]}');\n\n")

        # Insert a conflicting record
        file.write(f"-- Intentional primary key conflict\n")
        file.write(f"INSERT INTO {table_name} ({primary_key_column}) VALUES ('{conflicting_values[1]}');\n\n")

        # Optional error check
        file.write("-- If the above insert doesn't raise an error, explicitly throw one (for testing)\n")
        file.write("DO $$ BEGIN\n")
        file.write(f"    IF NOT EXISTS (\n")
        file.write(f"        SELECT 1 FROM {table_name} WHERE {primary_key_column} = '{conflicting_values[1]}'\n")
        file.write(f"    ) THEN\n")
        file.write(f"        RAISE EXCEPTION 'Expected primary key conflict, but it did not occur.';\n")
        file.write("    END IF;\n")
        file.write("END $$;\n\n")

        # Rollback the transaction
        file.write("-- Rollback to undo all inserts in this transaction\n")
        file.write("ROLLBACK;\n\n")

        # Verify rollback
        file.write(f"-- Verify rollback\n")
        file.write(f"SELECT * FROM {table_name} WHERE {primary_key_column} = '{conflicting_values[1]}';\n")

    return filename

# Example usage
def main():
    table_name = "public.student"
    primary_key_column = "student_code"
    conflicting_values = ["S123456789", "S123456789"]

    script_path = generate_sql_script(table_name, primary_key_column, conflicting_values)
    print(f"SQL script generated: {script_path}")

if __name__ == "__main__":
    main()
