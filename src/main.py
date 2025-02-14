from datetime import datetime, timedelta, date
from src.database.services.notificationLogService import NotificationLogService
from src.database.services.contractDataService import ContractDataService
from src.database.services.reminderHistoryService import ReminderHistoryService
from database.db_connection import get_db_session
from EmailService.emailSenderService import send_contract_email

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
                reminder_date = generate_reminder_date(contract.ExpirationDate, contract.ContractType)
                reminder_history_service.set_reminder(reminder_date, contract.ContractId)
            
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_reminder_date(expiration_date: datetime, contract_type: str): 
    # Define reminder days for each contract type
    reminder_days = {
        "Purchase Order": 30,
        "Consulting Agreement": 15,
        "Bids": 30,
        "Tree Trimming": 30,
        "Fiber General Services": 25,
        "Contractors": 30,
        "Gas General Services": 20,
        "Corrosion Control": 25,
        "Welding/Pipe Fitting": 30,
        "Leak Patrol": 20,
        "Plumbing": 30,
        "Materials": 30,
        "Phone Systems": 30,
        "Fiber Equipment": 30,
        "Networking": 30,
        "Office Supplies": 25,
        "General Services": 30,
        "Power": 30,
        "Electric Supply": 30,
        "Transmission": 30,
        "Capacity": 30,
        "Gas supply": 20,
        "Office Equipment": 30,
        "Printers": 30,
        "Computers": 30,
        "Laptops": 25
    }

    # Determine reminder days, default to 30 if not found
    days_before_expiration = reminder_days.get(contract_type, 30)
    reminder_date = expiration_date - timedelta(days=days_before_expiration)
    return reminder_date

def send_reminders():
    try:
        session = get_db_session()
        contract_service = ContractDataService(session)
        reminder_history_service = ReminderHistoryService(session)

        unprocessed_results = reminder_history_service.get_unprocessed_emails()

        for row in unprocessed_results:
            reminder_date = row.ReminderDate
            current_time = datetime.now().date()
            if row.IsReminderSent == 0 and reminder_date <= current_time:
                unprocessed_contracts = contract_service.get_unprocessed_contracts(row.ContractID)
                for contract in unprocessed_contracts:
                    # Prepare contract information
                    contract_info = {
                        "contract_id": contract.ContractId,
                        "contract_type": contract.ContractType,
                        "end_date": contract.ExpirationDate.strftime("%Y-%m-%d") if contract.ExpirationDate else "N/A",
                        "title": contract.Title, 
                        "manager": contract.ContractManager,
                        "vendor": contract.VendorName,
                        "summary": contract.ContractSummary
                    }

                    # Create custom email subject and body
                    subject = f"Contract Expiration Reminder: {contract.Title}"
                    body_template = f"""
                    Dear {contract.ContractManager},

                    This is a reminder about the following contract that requires your attention:

                    Contract Title: {contract.Title}
                    Contract ID: {contract.ContractId}
                    Vendor: {contract.VendorName}
                    Contract Type: {contract.ContractType}
                    Expiration Date: {contract.ExpirationDate.strftime("%Y-%m-%d")}

                    Contract Summary:
                    {contract.ContractSummary}

                    Please review this contract and take necessary actions before the expiration date.

                    Best regards,
                    Contract Management System
                """

                    # Send the email
                    email_sent = send_contract_email(
                        recipient_email="ddagostino@wgeld.org",  # Assuming ContractManager field contains email
                        sender_email="automation@wgeld.org",  # Replace with your sender email
                        contract_info=contract_info,
                        subject=subject,
                        body_template=body_template
                    )

                    # Update reminder status if email was sent successfully
                    if email_sent:
                        # reminder_history_service.mark_reminder_as_sent(row.ID)
                        print(f"Email sent successfully to {contract.ContractManager} for contract {contract.Title}")
                    
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    #process_contracts()
    send_reminders()


