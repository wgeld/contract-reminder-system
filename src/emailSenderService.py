import msal
import requests
from typing import Dict, Any
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENTSECRET = os.getenv("CLIENTSECRET")
TENANT_ID = os.getenv("TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]


def get_access_token() -> str:

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENTSECRET
    )
    
    result = app.acquire_token_for_client(scopes=SCOPES)
    
    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Failed to acquire token: {result.get('error_description')}")

"""    
Returns:
    bool: True if email sent successfully, False otherwise.
"""

def send_contract_email(
    recipient_email: str,
    sender_email: str,
    contract_info: Dict[str, Any],
    subject: str = None,
    body_template: str = None
) -> bool:

    try:
        access_token = get_access_token()
        
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
                    "contentType": "HTML",
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
            return True
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return False
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
