# Import necessary modules
import psycopg2
import datetime
import credentials
from flask import Flask, request, jsonify
from db_connection import create_connection
from table_creation import create_students_table
from data_insertion import insert_student_data
from data_retrieval import search_students
from data_modification import update_student_data, delete_student_data
from data_sorting import sort_by_name, sort_by_date_of_birth, filter_by_program


# Create the Flask application
app = Flask(__name__)

# Define the Flask routes and their corresponding functionality


@app.route('/')
def home():
    return "Welcome to the Marticulation Registration Number System!"


@app.route('/register', methods=['POST'])
def register():
    # Get the data from the request
    data = request.get_json()
    name = data['name']
    date_of_birth = data['date_of_birth']
    program_enrolled = data['program_enrolled']
    registration_number = data['registration_number']

    # Perform the registration logic
    # Establish a connection to the database
    conn = psycopg2.connect(database=credentials.database,
                            user=credentials.user,
                            password=credentials.password,
                            host=credentials.host,
                            port=credentials.port)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to insert the data into the students table
    insert_query = "INSERT INTO students (name, date_of_birth, program_enrolled, registration_number) VALUES (%s, %s, %s, %s)"

    # Execute the SQL query with the provided data
    cursor.execute(insert_query, (name, date_of_birth,
                   program_enrolled, registration_number))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Return a response
    return jsonify({'message': 'Registration successful'})


@app.route('/search', methods=['GET'])
def search():
    # Get the search term from the request query parameters
    search_term = request.args.get('term')

    # Establish a connection to the database
    conn = psycopg2.connect(database=credentials.database,
                            user=credentials.user,
                            password=credentials.password,
                            host=credentials.host,
                            port=credentials.port)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to search for students based on the provided term
    search_query = "SELECT * FROM students WHERE name LIKE %s"

    # Execute the SQL query with the provided search term
    cursor.execute(search_query, ('%' + search_term + '%',))

    # Fetch all the results from the executed query
    search_results = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Return a response
    return jsonify({'results': search_results})


# Modify the student record
@app.route('/modify', methods=['PUT'])
def modify():
    # Get the data from the request
    data = request.get_json()
    student_id = data['student_id']
    new_name = data['new_name']
    new_program = data['new_program']

    # Establish a connection to the database
    conn = psycopg2.connect(database=credentials.database,
                            user=credentials.user,
                            password=credentials.password,
                            host=credentials.host,
                            port=credentials.port)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to update the student record
    update_query = "UPDATE students SET name = %s, program_enrolled = %s WHERE student_id = %s"

    # Execute the SQL query with the provided data
    cursor.execute(update_query, (new_name, new_program, student_id))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Return a response
    return jsonify({'message': 'Student record modified successfully'})

# Delete the student record


@app.route('/delete', methods=['DELETE'])
def delete():
    # Get the data from the request
    data = request.get_json()
    student_id = data['student_id']

    # Establish a connection to the database
    conn = psycopg2.connect(database=credentials.database,
                            user=credentials.user,
                            password=credentials.password,
                            host=credentials.host,
                            port=credentials.port)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to delete the student record
    delete_query = "DELETE FROM students WHERE student_id = %s"

    # Execute the SQL query with the provided student ID
    cursor.execute(delete_query, (student_id,))

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Return a response
    return jsonify({'message': 'Student record deleted successfully'})

# Sorting and filtering student records


@app.route('/sort', methods=['GET'])
def sort():
    # Get the sort option from the request query parameters
    sort_option = request.args.get('option')

    # Establish a connection to the database
    conn = psycopg2.connect(database=credentials.database,
                            user=credentials.user,
                            password=credentials.password,
                            host=credentials.host,
                            port=credentials.port)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    if sort_option == 'name':
        # Construct the SQL query to sort by name
        sort_query = "SELECT * FROM students ORDER BY name"
    elif sort_option == 'dob':
        # Construct the SQL query to sort by date of birth
        sort_query = "SELECT * FROM students ORDER BY date_of_birth"
    else:
        # Invalid sort option
        return jsonify({'message': 'Invalid sort option'})

    # Execute the SQL query for sorting
    cursor.execute(sort_query)

    # Fetch all the results from the executed query
    sorted_results = cursor.fetchall()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    # Return a response
    return jsonify({'results': sorted_results})


# Establish the database connection
conn = create_connection()

# Create the students table
create_students_table(conn)

# Prompt the user for student information
name = input("Enter student name: ")
date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
program_enrolled = input("Enter program enrolled: ")
registration_number = input("Enter registration number: ")

# Validate date of birth format
try:
    datetime.datetime.strptime(date_of_birth, "%Y-%m-%d")
except ValueError:
    print("Invalid date of birth format. Please enter the date in the format YYYY-MM-DD.")
    conn.close()
    exit()

# Validate registration number uniqueness
cursor = conn.cursor()
check_registration_query = "SELECT COUNT(*) FROM students WHERE registration_number = %s"
cursor.execute(check_registration_query, (registration_number,))
result = cursor.fetchone()

if result[0] > 0:
    print("Registration number already exists. Please enter a unique registration number.")
    conn.close()
    exit()

# Validate field lengths
max_name_length = 50
max_program_length = 50
max_registration_length = 20

if len(name) > max_name_length:
    print(
        f"Name exceeds the maximum allowed length of {max_name_length} characters.")
    conn.close()
    exit()

if len(program_enrolled) > max_program_length:
    print(
        f"Program enrolled exceeds the maximum allowed length of {max_program_length} characters.")
    conn.close()
    exit()

if len(registration_number) > max_registration_length:
    print(
        f"Registration number exceeds the maximum allowed length of {max_registration_length} characters.")
    conn.close()
    exit()

# Insert data into the students table
insert_student_data(conn, name, date_of_birth,
                    program_enrolled, registration_number)

# Prompt the user for searching
search_choice = input("Do you want to search for a student? (y/n): ")

if search_choice.lower() == "y":
    search_term = input("Enter the search term: ")
    search_results = search_students(conn, search_term)
    print("Search Results:")
    for result in search_results:
        print(result)

# Modify or delete student data
modification_choice = input(
    "Do you want to modify or delete a student record? (m/d/n): ")

if modification_choice.lower() == "m":
    student_id = input("Enter the student ID to modify: ")
    new_name = input("Enter the new name: ")
    new_program = input("Enter the new program: ")
    update_student_data(conn, student_id, new_name, new_program)
    print("Student record modified successfully.")
elif modification_choice.lower() == "d":
    student_id = input("Enter the student ID to delete: ")
    delete_student_data(conn, student_id)
    print("Student record deleted successfully.")
else:
    print("No modification or deletion performed.")

# Prompt the user for sorting or filtering
sort_filter_choice = input(
    "Do you want to sort or filter student records? (s/f/n): ")

if sort_filter_choice.lower() == "s":
    sort_option = input("Enter the sort option (name/dob): ")
    if sort_option.lower() == "name":
        sorted_results = sort_by_name(conn)
        print("Sorted Results:")
        for result in sorted_results:
            print(result)
    elif sort_option.lower() == "dob":
        sorted_results = sort_by_date_of_birth(conn)
        print("Sorted Results:")
        for result in sorted_results:
            print(result)
    else:
        print("Invalid sort option.")
elif sort_filter_choice.lower() == "f":
    program = input("Enter the program name to filter: ")
    filtered_results = filter_by_program(conn, program)
    print("Filtered Results:")
    for result in filtered_results:
        print(result)
else:
    print("No sorting or filtering performed.")


# Close the database connection
conn.close()


# Run the Flask application
if __name__ == '__main__':
    app.run(port=5001)
