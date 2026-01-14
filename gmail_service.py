import os
import pickle
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from utils import clean_text, classify_email, get_priority  # Make sure these exist in utils.py

# Gmail read-only scope
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_gmail_service():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_recent_emails(max_results=5):
    """
    Fetch recent emails from Gmail
    Returns list of (subject, body)
    """
    service = get_gmail_service()

    emails = []

    results = service.users().messages().list(
        userId="me",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    for msg in messages:
        message = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="full"
        ).execute()

        headers = message["payload"]["headers"]
        subject = ""
        body = ""

        for header in headers:
            if header["name"] == "Subject":
                subject = header["value"]

        payload = message["payload"]

        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    body = base64.urlsafe_b64decode(
                        part["body"]["data"]
                    ).decode("utf-8", errors="ignore")
        else:
            if "body" in payload and "data" in payload["body"]:
                body = base64.urlsafe_b64decode(
                    payload["body"]["data"]
                ).decode("utf-8", errors="ignore")

        emails.append({
            "subject": subject,
            "body": body,
            "id": msg["id"]  # <-- Gmail message ID for clickable link
        })

    return emails


def get_classified_emails(max_results=5):
    """
    Fetch recent emails and classify them
    Returns dict with categories as keys
    """
    result = {
        "INTERVIEW": [],
        "ONLINE JOB": [],
        "SOCIAL ADS": []
    }

    emails = fetch_recent_emails(max_results)

    for email in emails:
        text = clean_text(email["subject"] + " " + email["body"])
        category = classify_email(text)
        priority = get_priority(category)

        if category in result:
            result[category].append({
                "subject": email["subject"],
                "priority": priority,
                "id": email["id"]  # <-- add the Gmail ID here
            })

    return result
