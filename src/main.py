from datetime import datetime, timedelta

from database.services.NotificationLogService.notificationLogService import NotificationLogService
from database.services.ContractDataService.contractDataService import ContractDataService
from database.db_connection import get_db_session

def main():
    try:
        session = get_db_session()
        notification_service = NotificationLogService(session)
        contract_service = ContractDataService(session)
        # Query all results
        unprocessed_results = notification_service.get_unprocessed_notifications()
        for row in unprocessed_results:
            unprocessed_contracts = contract_service.get_unprocessed_contracts(row.ContractId)
            for contract in unprocessed_contracts:
                expiration_date = contract.ExpirationDate
                doc_type = contract.DocType


                print(contract.ExpirationDate)
            
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_reminder_date(expiration_date: datetime, doc_type: str): 
    if doc_type == "contract":
        return expiration_date - timedelta(days=30)
    elif doc_type == "invoice":
        return expiration_date - timedelta(days=15) # 15 days before expiration
    elif doc_type == "invoice":
        return expiration_date - timedelta(days=15) # 15 days before expiration
    elif doc_type == "invoice":
        return expiration_date - timedelta(days=15) # 15 days before expiration
    
    else:
        return expiration_date


if __name__ == "__main__":
    main()

