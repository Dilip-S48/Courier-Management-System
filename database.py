import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',       # Change to your host
            database='courier_db',  # The database created with setup.sql
            user='root',            # Change to your MySQL username
            password='dilipmysql'     # Change to your MySQL password
        )
        if connection.is_connected():
            print("Successfully connected to the database")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, params=None):
    """Execute a single query."""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        print("Query executed successfully")
        return cursor
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def fetch_all(connection, query, params=None):
    """Fetch all records from a query."""
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        records = cursor.fetchall()
        return records
    except Error as e:
        print(f"The error '{e}' occurred")
        return []

def fetch_one(connection, query, params=None):
    """Fetch a single record from a query."""
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        record = cursor.fetchone()
        return record
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

if __name__ == '__main__':
    # This allows you to test the connection directly
    conn = create_connection()
    if conn:
        conn.close()
        print("Database connection closed.")