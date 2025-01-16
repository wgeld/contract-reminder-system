import msal
import requests

# Configuration
CLIENT_ID = "your-client-id"
CLIENT_SECRET = "your-client-secret"
TENANT_ID = "your-tenant-id"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]

# Create a confidential client application
app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET
)

# Acquire a token for the application
result = app.acquire_token_for_client(scopes=SCOPES)

if "access_token" in result:
    print("Token acquired successfully!")
    access_token = result["access_token"]
else:
    print(f"Failed to acquire token: {result.get('error_description')}")

# Define the email
email_data = {
    "message": {
        "subject": "Hello from Microsoft Graph",
        "body": {
            "contentType": "Text",
            "content": "This email was sent using the Microsoft Graph API!"
        },
        "toRecipients": [
            {"emailAddress": {"address": "recipient@example.com"}}
        ]
    }
}

# Send the email
response = requests.post(
    "https://graph.microsoft.com/v1.0/users/sender@example.com/sendMail",
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    },
    json=email_data
)

if response.status_code == 202:
    print("Email sent successfully!")
else:
    print(f"Error: {response.status_code}, {response.text}")