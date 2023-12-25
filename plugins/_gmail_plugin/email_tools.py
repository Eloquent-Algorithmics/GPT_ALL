
# !/usr/bin/env python
# coding: utf-8
# Filename: email_tools.py
# Path: plugins/_gmail_plugin/email_tools.py
"""
This module contains the Gmail Email functions and tools.
"""
import os
import base64
import binascii
import logging
from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError


async def read_email(gmail_service):
    """Retrieve a list of emails from Gmail."""
    try:
        results = gmail_service.users().messages().list(
            userId='me', labelIds=['INBOX'], maxResults=5).execute()
        messages = results.get('messages', [])

        emails = []
        for message in messages:
            msg = gmail_service.users().messages().get(
                userId='me', id=message['id']).execute()

            sender, subject, body = await extract_email_data(msg)

            snippet = body[:100] if body else 'N/A'
            emails.append(
                {
                    'id': message['id'], 'subject': subject,
                    'from': sender, 'snippet': snippet
                }
            )
        return emails

    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return []


async def send_email(gmail_service, **kwargs):
    """Send an email message."""
    subject = kwargs.get('subject')
    body = kwargs.get('body')
    to = kwargs.get('to', os.getenv("GMAIL_ADDRESS"))
    from_email = os.getenv("GMAIL_ADDRESS")

    # Create the email message with proper headers
    email_message = f"From: {from_email}\r\n"
    email_message += f"To: {to}\r\n"
    email_message += f"Subject: {subject}\r\n\r\n"
    email_message += body

    # Encode the message in base64url format
    message_bytes = email_message.encode("utf-8")
    base64_bytes = base64.urlsafe_b64encode(message_bytes)
    base64_message = base64_bytes.decode("utf-8")

    raw_message = {"raw": base64_message}
    try:
        send_message = (
            gmail_service.users().messages().send(userId="me", body=raw_message).execute()
        )
        return f"Message Id: {send_message['id']}"
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return f"An error occurred while sending the email: {error}"


async def delete_email(gmail_service, message_id):
    """Delete an email message by ID."""
    try:
        gmail_service.users().messages().delete(userId='me', id=message_id).execute()
    except HttpError as error:
        logging.error("An error occurred: %s", error)


async def extract_email_data(msg):
    """Extract the sender, subject, and body from an email message."""
    headers = msg['payload']['headers']
    sender = ''
    subject = ''
    for header in headers:
        if header['name'].lower() == 'from':
            sender = header['value']
        elif header['name'].lower() == 'subject':
            subject = header['value']

    body = await _get_email_body(msg['payload'])
    return sender, subject, body


async def _get_email_body(payload):
    """Get the body of an email message."""
    if 'parts' in payload:
        parts = payload['parts']
        body = ''
        for part in parts:
            part_body = part['body'].get('data', '')
            # Await the coroutine to get the decoded body
            body += await _decode_base64(part_body, part['mimeType'])
        return body
    else:
        body = payload['body'].get('data', '')
        # Await the coroutine to get the decoded body
        return await _decode_base64(body)


async def _decode_base64(data, mime_type='text/plain'):
    """Decode base64-encoded data."""
    try:
        decoded_body_bytes = base64.urlsafe_b64decode(data)
        decoded_body = decoded_body_bytes.decode(errors='ignore')
    except binascii.Error as e:
        logging.error("Error decoding base64-encoded data: %s", e)
        decoded_body = ''

    if mime_type == 'text/html':
        soup = BeautifulSoup(decoded_body, 'html.parser')
        return soup.get_text()
    else:
        return decoded_body


email_tools_list = [
    {
        "type": "function",
        "function": {
            "name": "read_email",
            "description": "Retrieve a list of emails from Gmail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_object_id": {
                        "type": "string",
                        "description": "Optional object ID to filter emails.",
                    },
                },
                "required": [],
            },
        },
    },
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
]

available_functions = {
    "read_email": read_email,
    "send_email": send_email,
    "delete_email": delete_email,
}
