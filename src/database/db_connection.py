import pyodbc
import os

from dotenv import load_dotenv

load_dotenv()

def get_db_connection():

    server = os.getenv("DB_SERVER")  
    database = os.getenv("DB_NAME")  
    username = os.getenv("DB_USER")  
    password = os.getenv("DB_PASS")  
    driver = os.getenv("DB_DRIVER")

    connection_string = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
        f"Integrated Security=false;"
    )
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection failed: {e}")
        raise


