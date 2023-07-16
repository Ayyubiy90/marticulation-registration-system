from db_connection import create_connection


def create_students_table(conn):
    cursor = conn.cursor()

    # Drop the existing "students" table if it exists
    drop_table_query = "DROP TABLE IF EXISTS students;"
    cursor.execute(drop_table_query)

    # Create the "students" table
    create_table_query = """
    CREATE TABLE students (
        student_id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        date_of_birth DATE,
        program_enrolled VARCHAR(50),
        registration_number VARCHAR(20) UNIQUE
    )
    """

    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
