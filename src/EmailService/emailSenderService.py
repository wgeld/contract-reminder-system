import msal
import requests
from typing import Dict, Any

# Configuration

#DO NOT PUSH IDS TO GITHUB UNLESS IN .ENV
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
TENANT_ID = "your-tenant-id"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

def get_access_token() -> str:
    """
    Get access token from Microsoft Graph API
    Returns:
        str: Access token if successful, raises exception if failed
    """
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    
    result = app.acquire_token_for_client(scopes=SCOPES)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Failed to acquire token: {result.get('error_description')}")

def send_contract_email(
    recipient_email: str,
    sender_email: str,
    contract_info: Dict[str, Any],
    subject: str = None,
    body_template: str = None
) -> bool:
    """
    Send an email with contract information using Microsoft Graph API
    
    Args:
        recipient_email (str): Email address of the recipient
        sender_email (str): Email address of the sender
        contract_info (dict): Dictionary containing contract information
        subject (str, optional): Custom email subject. Defaults to None
        body_template (str, optional): Custom email body template. Defaults to None
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        access_token = get_access_token()
        
        # Default subject and body if not provided
        if not subject:
            subject = f"Contract Information: {contract_info.get('contract_id', 'N/A')}"
            
        if not body_template:
            body_template = f"""
Contract Details:
Contract ID: {contract_info.get('contract_id', 'N/A')}
Contract Type: {contract_info.get('contract_type', 'N/A')}
Start Date: {contract_info.get('start_date', 'N/A')}
End Date: {contract_info.get('end_date', 'N/A')}

Please review the contract information above.
"""

        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "Text",
                    "content": body_template
                },
                "toRecipients": [
                    {"emailAddress": {"address": recipient_email}}
                ]
            }
        }

        response = requests.post(
            f"https://graph.microsoft.com/v1.0/users/{sender_email}/sendMail",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json=email_data
        )

        if response.status_code == 202:
            print("Email sent successfully!")
            return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False