def search_students(conn, search_term):
    cursor = conn.cursor()

    search_query = """
    SELECT * FROM students
    WHERE name ILIKE %s OR registration_number ILIKE %s OR program_enrolled ILIKE %s
    """
    search_value = f"%{search_term}%"

    cursor.execute(search_query, (search_value, search_value, search_value))
    results = cursor.fetchall()

    cursor.close()
    return results
