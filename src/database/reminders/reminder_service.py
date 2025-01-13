from src.database.db_connection import get_db_connection

def get_reminders():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reminders")
    return cursor.fetchall()