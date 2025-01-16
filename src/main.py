import asyncio
from datetime import datetime, timedelta, date
from database.services.NotificationLogService.notificationLogService import NotificationLogService
from database.services.ContractDataService.contractDataService import ContractDataService
from database.db_connection import get_db_session

def process_contracts():
    try:
        session = get_db_session()
        notification_service = NotificationLogService(session)
        contract_service = ContractDataService(session)
        # Query all results
        unprocessed_results = notification_service.get_unprocessed_notifications()
        for row in unprocessed_results:
            unprocessed_contracts = contract_service.get_unprocessed_contracts(row.ContractId)
            for contract in unprocessed_contracts:
                contract_type = contract.DocumentType
                expiration_date = contract.ExpirationDate
                reminder_date = generate_reminder_date(expiration_date, contract_type)
                notification_service.set_reminder(reminder_date, row.NotificationId)
            
    except Exception as e:
        print(f"An error occurred: {e}")

def send_reminders():
    try:
        session = get_db_session()
        notification_service = NotificationLogService(session)
        contract_service = ContractDataService(session)
        unprocessed_results = notification_service.get_unprocessed_emails()
        for row in unprocessed_results:
            # Convert datetime.now() to datetime object and strip time component if needed
            current_time = datetime.now()
            reminder_date = row.ReminderDate
            
            # Ensure both are datetime objects for comparison
            if isinstance(reminder_date, date):
                reminder_date = datetime.combine(reminder_date, datetime.min.time())
            
            if row.IsReminderSent == 0 and reminder_date <= current_time:
                unprocessed_contracts = contract_service.get_unprocessed_contracts(row.ContractId)
                for contract in unprocessed_contracts:
                    contract_type = contract.DocumentType
                    expiration_date = contract.ExpirationDate
                    contract_title = contract.Title
                    contract_vendor = contract.VendorName
                    contract_manager = contract.ContractManager
                    contract_summary = contract.ContractSummary

                    print(contract)
                    
    except Exception as e:
        print(f"An error occurred: {e}")

#TODO: Must set actual contract types
def generate_reminder_date(expiration_date: datetime, contract_type: str): 
    
    if contract_type == "Purchase Order":
        reminder_date = expiration_date - timedelta(days=30)
        return reminder_date
    elif contract_type == "NDA":
        reminder_date = expiration_date - timedelta(days=15) # 15 days before expiration
        return reminder_date
    elif contract_type == "Consulting Agreement":
        reminder_date = expiration_date - timedelta(days=15) # 15 days before expiration
        return reminder_date
    elif contract_type == "Type B":
        reminder_date = expiration_date - timedelta(days=15) # 15 days before expiration
        return reminder_date
    else:
        return expiration_date - timedelta(days=30)


if __name__ == "__main__":
    process_contracts()
    send_reminders()


