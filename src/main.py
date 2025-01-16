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
            if row.IsReminderSent == 0 and row.ReminderDate <= datetime.now():
                unprocessed_contracts = contract_service.get_unprocessed_contracts(row.ContractId)
                for contract in unprocessed_contracts:
                    contract_type = contract.DocumentType
                    expiration_date = contract.ExpirationDate
                    contract_title = contract.Title
                    contract_vendor = contract.VendorName
                    reminder_date = generate_reminder_date(expiration_date, contract_type)
                    notification_service.set_reminder(reminder_date, row.NotificationId)
            
            
    except Exception as e:
        print(f"An error occurred: {e}")


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


