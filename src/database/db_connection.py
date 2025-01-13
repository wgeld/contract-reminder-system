import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Establish and return a connection to the SQL Server database.
    """
    server = os.getenv("DB_SERVER")  # Replace with your server
    database = os.getenv("DB_NAME")  # Replace with your database
    username = os.getenv("DB_USER")  # Replace with your username
    password = os.getenv("DB_PASS")  # Replace with your password

    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise


