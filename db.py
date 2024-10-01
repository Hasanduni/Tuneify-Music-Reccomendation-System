import mysql.connector

db_config = {
    'user': 'root',
    'password': 'user',
    'host': 'localhost',
    'database': 'user'  # Change to your database name
}

def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
