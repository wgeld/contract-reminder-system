from reminders.reminder_service import query_database

def main():
    try:
        # Query all results
        results = query_database()
        print("All results:")
        for row in results:
            print(row)
        
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

