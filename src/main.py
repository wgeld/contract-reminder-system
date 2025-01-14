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
                print(contract.ExpirationDate)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

