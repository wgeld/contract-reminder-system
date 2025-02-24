import logging
from datetime import datetime, timedelta
from database.services.notificationLogService import NotificationLogService
from database.services.contractDataService import ContractDataService
from database.services.reminderHistoryService import ReminderHistoryService
from database.services.contractTypeService import ContractTypeService
from database.db_connection import get_db_session
from emailSenderService import send_contract_email

def process_contracts():
    try:
        session = get_db_session()
        notification_service = NotificationLogService(session)
        contract_service = ContractDataService(session)
        reminder_history_service = ReminderHistoryService(session)
        # Query all results
        unprocessed_results = notification_service.get_unprocessed_notifications()
        for row in unprocessed_results:
            unprocessed_contracts = contract_service.get_unprocessed_contracts(row.ContractId)
            for contract in unprocessed_contracts:
                reminder_date = generate_reminder_date(contract.ExpirationDate, contract.ContractTypeId)
                reminder_history_service.set_reminder(reminder_date, contract.ContractId)
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_reminder_date(expiration_date: datetime, contract_type_id: int): 
    session = get_db_session()
    contract_type_service = ContractTypeService(session)
    days_before_expiration = contract_type_service.get_contract_type_days_before_reminder(contract_type_id)
    reminder_date = expiration_date - timedelta(days=days_before_expiration)
    return reminder_date

def send_reminders():
    try:
        session = get_db_session()
        contract_service = ContractDataService(session)
        reminder_history_service = ReminderHistoryService(session)
        contract_type_service = ContractTypeService(session)

        unprocessed_results = reminder_history_service.get_unprocessed_emails()

        for row in unprocessed_results:
            reminder_date = row.ReminderDate
            current_time = datetime.now().date()
            if row.IsReminderSent == 0 and reminder_date <= current_time:
                unprocessed_contracts = contract_service.get_unprocessed_contracts(row.ContractID)
                for contract in unprocessed_contracts:
                    contract_type = contract_type_service.get_contract_type(contract.ContractTypeId)
                    # Prepare contract information
                    contract_info = {
                        "contract_id": contract.ContractId,
                        "contract_type": contract_type.ContractType,
                        "end_date": contract.ExpirationDate.strftime("%Y-%m-%d") if contract.ExpirationDate else "N/A",
                        "title": contract.Title, 
                        "manager": contract_type.ContractOwner,
                        "vendor": contract.VendorName,
                        "summary": contract.ContractSummary,
                        "contract_type_id": contract.ContractTypeId
                    }

                    # Create custom email subject and body
                    subject = f"Contract Expiration Reminder: {contract.Title}"
                    body_template = f"""
                    Dear {contract_type.ContractOwner},

                    This is a reminder about the following contract that requires your attention:

                    Contract Title: {contract.Title}
                    Contract ID: {contract.ContractId}
                    Vendor: {contract.VendorName}
                    Contract Type: {contract_type.ContractType}
                    Expiration Date: {contract.ExpirationDate.strftime("%Y-%m-%d")}

                    Contract Summary:
                    {contract.ContractSummary}

                    Please review this contract and take necessary actions before the expiration date.

                    Best regards,
                    Contract Management System
                """
                    # Send the email
                    email_sent = send_contract_email(
                        recipient_email=contract_type.ContractOwnerEmail,
                        sender_email="automation@wgeld.org",  
                        contract_info=contract_info,
                        subject=subject,
                        body_template=body_template
                    )
                    if email_sent:
                        reminder_history_service.mark_email_as_sent(row.ReminderId)
                        print(f"Email sent successfully to {contract_type.ContractManager} for contract {contract.Title}")
                        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    logging.basicConfig(filename="script.log", level=logging.INFO)
    try:
        process_contracts()
        send_reminders()
    except Exception as e:
        logging.error(f"Error: {e}")


