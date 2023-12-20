
# !/usr/bin/env python
# coding: utf-8
# Filename: gmail_tools.py
# Path: plugins/_google_api_client/gmail_tools.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/20

"""
This module contains the GmailToolsPlugin class.
"""

import os
import base64
import binascii
import datetime
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from plugins.plugin_base import PluginBase


class GmailToolsPlugin(PluginBase):
    """
    This class contains the GmailToolsPlugin class.
    """

    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://mail.google.com/", "https://www.googleapis.com/auth/calendar"]

    def __init__(self):
        self.creds = None
        self._load_credentials()
        self.gmail_service = build("gmail", "v1", credentials=self.creds)
        self.calendar_service = build("calendar", "v3", credentials=self.creds)

        super().__init__()

    async def initialize(self):
        # Initialization code if needed. If not, simply pass.
        pass

    def _load_credentials(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                            "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")],
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                        }
                    },
                    self.SCOPES,
                )
                self.creds = flow.run_local_server(port=0)
            with open("token.json", "w", encoding="utf-8") as token:
                token.write(self.creds.to_json())

    async def send_email(self, subject, body, to=None):
        if to is None:
            to = os.getenv("GMAIL_ADDRESS")
        message = {"subject": subject, "body": body, "to": to}
        self.create_message_and_send(message)

    async def create_message_and_send(self, message):
        to = message["to"]
        subject = message["subject"]
        body = message["body"]
        message = f"Subject: {subject}\n\n{body}"
        message_bytes = message.encode("utf-8")
        base64_bytes = base64.urlsafe_b64encode(message_bytes)
        base64_message = base64_bytes.decode("utf-8")

        raw_message = {"raw": base64_message}
        try:
            send_message = (
                self.gmail_service.users().messages().send(userId="me", body=raw_message).execute()
            )
            print(f"Message Id: {send_message['id']}")
        except HttpError as error:
            print(f"An error occurred: {error}")

    async def get_next_google_calendar_event(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"
        try:
            events_result = (
                self.calendar_service.events()
                .list(calendarId="primary", timeMin=now, maxResults=1, singleEvents=True, orderBy="startTime")
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                return "No upcoming events found."
            else:
                event = events[0]
                start = event["start"].get("dateTime", event["start"].get("date"))
                return f"Next event: {event['summary']} at {start}"
        except HttpError as error:
            print(f"An error occurred: {error}")
            return "An error occurred while retrieving events."

    async def delete_email(self, message_id):
        try:
            self.gmail_service.users().messages().delete(userId='me', id=message_id).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

    async def get_emails_google(self, user_object_id=None):
        try:
            results = self.gmail_service.users().messages().list(
                userId='me', labelIds=['INBOX'], maxResults=5).execute()
            messages = results.get('messages', [])

            emails = []
            for message in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me', id=message['id']).execute()

                sender, subject, body = self.extract_email_data(msg)

                snippet = body[:100] if body else 'N/A'
                emails.append({'id': message['id'], 'subject': subject,
                              'from': sender, 'snippet': snippet})
            return emails
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    async def extract_email_data(self, msg):
        headers = msg['payload']['headers']
        sender = ''
        subject = ''
        for header in headers:
            if header['name'].lower() == 'from':
                sender = header['value']
            elif header['name'].lower() == 'subject':
                subject = header['value']

        body = self._get_email_body(msg['payload'])
        return sender, subject, body

    async def _get_email_body(self, payload):
        if 'parts' in payload:
            parts = payload['parts']
            body = ''
            for part in parts:
                part_body = part['body'].get('data', '')
                body += self._decode_base64(part_body, part['mimeType'])
            return body
        else:
            body = payload['body'].get('data', '')
            return self._decode_base64(body)

    async def _decode_base64(self, data, mime_type='text/plain'):
        try:
            decoded_body_bytes = base64.urlsafe_b64decode(data)
            decoded_body = decoded_body_bytes.decode(errors='ignore')
        except binascii.Error as e:
            print(f"Error decoding base64-encoded data: {e}")
            decoded_body = ''

        if mime_type == 'text/html':
            soup = BeautifulSoup(decoded_body, 'html.parser')
            return soup.get_text()
        else:
            return decoded_body

    def get_tools(self):
        gmail_tools = [
            {
                "type": "function",
                "function": {
                    "name": "send_email",
                    "description": "Send an email message.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "subject": {
                                "type": "string",
                                "description": "The subject of the email.",
                            },
                            "body": {
                                "type": "string",
                                "description": "The body of the email.",
                            },
                            "to": {
                                "type": "string",
                                "description": "The recipient of the email.",
                            },
                        },
                        "required": ["subject", "body"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_next_google_calendar_event",
                    "description": "Get the next event from the Google Calendar.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_email",
                    "description": "Delete an email message by ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "message_id": {
                                "type": "string",
                                "description": "The ID of the email to delete.",
                            },
                        },
                        "required": ["message_id"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_emails_google",
                    "description": "Retrieve a list of emails from Gmail.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_object_id": {
                                "type": "string",
                                "description": "An optional user object ID to filter emails.",
                            },
                        },
                        "required": [],
                    },
                },
            },
        ]

        self.tools.extend(gmail_tools)

        available_functions = {
            "send_email": self.send_email,
            "get_next_google_calendar_event": self.get_next_google_calendar_event,
            "delete_email": self.delete_email,
            "get_emails_google": self.get_emails_google,
        }

        return available_functions, self.tools
