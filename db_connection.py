import psycopg2

def create_connection():
    # Replace the placeholders with your PostgreSQL credentials
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="postgres",
        password="AbdullahAbdurazaq@1234567890",
        database="marticulation_system"
    )
    return conn
