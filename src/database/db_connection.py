import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

def get_db_engine():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    driver = os.getenv("DB_DRIVER").replace(" ", "+")

    connection_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"
    
    try:
        engine = create_engine(connection_url, echo=False)
        return engine
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

def get_db_session():
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()


