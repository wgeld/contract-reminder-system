from database.db_connection import get_db_connection

def query_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT TOP 10 * FROM [wcfMgmt_test].[dbo].[wcfMgmtEquipments]")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
