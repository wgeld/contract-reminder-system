import pyodbc
import os

def get_db_connection():
    """
    Establish and return a connection to the SQL Server database.
    """
    server = os.getenv("DB_SERVER", "localhost")  # Replace with your server
    database = os.getenv("DB_NAME", "ContractsDB")  # Replace with your database
    username = os.getenv("DB_USER", "sa")  # Replace with your username
    password = os.getenv("DB_PASS", "password")  # Replace with your password

    connection_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER=SQL_Dev1901;"
        f"DATABASE=wcfMgmt_test;"
        f"UID=wcf_app;"
        f"PWD=wcfapp;"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise
