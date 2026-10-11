import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",       
    "user": "root",           
    "password": "root",  
    "database": "user_management_db"
}


def get_connection():
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None


def test_connection():
    conn = get_connection()
    if conn:
        print("✅ Successfully connected to MySQL database!")
        conn.close()
    else:
        print("❌ Failed to connect. Check your DB_CONFIG credentials.")


if __name__ == "__main__":
    test_connection()
