from db_connection import create_connection


def insert_student_data(conn, name, date_of_birth, program_enrolled, registration_number):
    cursor = conn.cursor()

    insert_data_query = """
    INSERT INTO students (name, date_of_birth, program_enrolled, registration_number)
    VALUES (%s, %s, %s, %s)
    """
    data = (name, date_of_birth, program_enrolled, registration_number)

    cursor.execute(insert_data_query, data)
    conn.commit()
    cursor.close()
