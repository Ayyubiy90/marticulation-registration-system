def update_student_data(conn, student_id, new_name, new_program):
    cursor = conn.cursor()

    update_query = """
    UPDATE students
    SET name = %s, program_enrolled = %s
    WHERE student_id = %s
    """

    cursor.execute(update_query, (new_name, new_program, student_id))
    conn.commit()
    cursor.close()


def delete_student_data(conn, student_id):
    cursor = conn.cursor()

    delete_query = """
    DELETE FROM students
    WHERE student_id = %s
    """

    cursor.execute(delete_query, (student_id,))
    conn.commit()
    cursor.close()
