def sort_by_name(conn):
    cursor = conn.cursor()

    sort_query = """
    SELECT * FROM students
    ORDER BY name
    """

    cursor.execute(sort_query)
    results = cursor.fetchall()

    cursor.close()
    return results


def sort_by_date_of_birth(conn):
    cursor = conn.cursor()

    sort_query = """
    SELECT * FROM students
    ORDER BY date_of_birth
    """

    cursor.execute(sort_query)
    results = cursor.fetchall()

    cursor.close()
    return results


def filter_by_program(conn, program):
    cursor = conn.cursor()

    filter_query = """
    SELECT * FROM students
    WHERE program_enrolled = %s
    """

    cursor.execute(filter_query, (program,))
    results = cursor.fetchall()

    cursor.close()
    return results
