
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
from bs4 import BeautifulSoup
from googleapiclient.errors import HttpError


async def gmail_read_message(gmail_service):
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

            snippet = body[:300] if body else 'N/A'
            emails.append(
                {
                    'id': message['id'], 'from': sender,
                    'subject': subject, 'snippet': snippet
                }
            )
        return emails

    except HttpError:
        return []


async def gmail_send_message(gmail_service, **kwargs):
    """Send an email message."""
    subject = kwargs.get('subject')
    body = kwargs.get('body')
    to = kwargs.get('to', os.getenv("GMAIL_ADDRESS"))
    from_email = os.getenv("GMAIL_ADDRESS")

    email_message = f"From: {from_email}\r\n"
    email_message += f"To: {to}\r\n"
    email_message += f"Subject: {subject}\r\n\r\n"
    email_message += body

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
        return f"An error occurred while sending the email: {error}"


async def gmail_delete_message(gmail_service, message_id):
    """Delete an email message by ID."""
    try:
        gmail_service.users().messages().delete(userId='me', id=message_id).execute()
    except HttpError:
        pass


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
            body += await _decode_base64(part_body, part['mimeType'])
        return body
    else:
        body = payload['body'].get('data', '')
        return await _decode_base64(body)


async def _decode_base64(data, mime_type='text/plain'):
    """Decode base64-encoded data."""
    try:
        decoded_body_bytes = base64.urlsafe_b64decode(data)
        decoded_body = decoded_body_bytes.decode(errors='ignore')
    except binascii.Error:
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
            "name": "gmail_read_message",
            "description": "Searches and retrieves emails from the users Gmail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_id": {
                        "type": "string",
                        "description": "Searches for messages by object ID to filter returned emails.",
                    },
                    "query": {
                        "type": "string",
                        "description": "Search query to filter emails by: `query:`",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Words in the subject line to filter by: `subject:`",
                    },
                    "to": {
                        "type": "string",
                        "description": "Specify a recipient to filter by: `to:`",
                    },
                    "from": {
                        "type": "string",
                        "description": "Specify the sender to filter by: `from:`",
                    },
                    "cc": {
                        "type": "string",
                        "description": "Recipient to filter by `cc:`",
                    },
                    "bcc": {
                        "type": "string",
                        "description": "Filter by recipient who received a copy to filter by `bcc:`",
                    },
                    "OR": {
                        "type": "string",
                        "description": "Find messages that match multiple terms `OR` or `{ }`, Example: from:amy OR from:david, Example: {from:amy from:david}",
                    },
                    "-": {
                        "type": "string",
                        "description": "Remove messages from your results `-`, Example: dinner -movie",
                    },
                    "AROUND": {
                        "type": "string",
                        "description": "Find messages with words near each other. Use the number to say how many words apart the words can be, Example: holiday AROUND 10 vacation",
                    },
                    "label": {
                        "type": "string",
                        "description": "Find messages that have a certain label, Example: label:friends",
                    },
                    "has": {
                        "type": "string",
                        "description": "Search for messages that have an attachment `has:`, Example: has:attachment, has:drive, has:document, has:spreadsheet, has:presentation, has:youtube, has:yellow-star, has:blue-start, has:userlabels, has:nouserlabels",
                    },
                    "filename": {
                        "type": "string",
                        "description": "Messages that have attachments of a certain type `filename:`, Example: filename:pdf, filename:homework.txt",
                    },
                    "deliveredto": {
                        "type": "string",
                        "description": "Search by email for delivered messages `deliveredto:`, Example: deliveredto:",
                    },
                    "category": {
                        "type": "string",
                        "description": "Search for messages in a certain category `category:`, Example: category:primary, category:social, category:promotions, category:updates, category:forums, category:reservations, category:purchases",
                    },
                    "size": {
                        "type": "string",
                        "description": "Messages larger than a certain size in bytes `size:` `larger:` `smaller:`, Example: size:1000000, larger:10M",
                    },
                    "+": {
                        "type": "string",
                        "description": "Search for results that match a word exactly `+`, Example: +unicorn",
                    },
                    "rfc822msgid": {
                        "type": "string",
                        "description": "Search for messages with a certain message-id header `rfc822msgid:`, Example: rfc822msgid:200503292@example.com",
                    },
                    "list": {
                        "type": "string",
                        "description": "Optional Messages from a mailing list `list:`, Example: list:info@example.com",
                    },
                    "": {
                        "type": "string",
                        "description": "Search for an exact word or phrase `""`, Example: \"dinner and movie tonight\"",
                    },
                    "()": {
                        "type": "string",
                        "description": "Group multiple search terms together `( )`, Example: subject:(dinner movie)",
                    },
                    "in": {
                        "type": "string",
                        "description": "Messages in any folder, including Spam and Trash `in:anywhere`, Example: in:anywhere movie",
                    },
                    "is": {
                        "type": "string",
                        "description": "Search for messages that are marked: `is:important` `is:starred`, Example: is:important",
                    },
                    "after": {
                        "type": "string",
                        "description": "Search for messages sent during a certain time period `after:`, `before:`, `older:`, `newer:`. Example: after:2004/04/16",
                    },
                    "older_than": {
                        "type": "string",
                        "description": "Search for messages older or newer than a time period using d (day), m (month), and y (year), Example: newer_than:2d",
                    },
                    "newer_than": {
                        "type": "string",
                        "description": "Search for messages older or newer than a time period using d (day), m (month), and y (year), Example: newer_than:2d",
                    },
                    "order_by": {
                        "type": "string",
                        "description": "Optional order by field.",
                    },
                    "order_direction": {
                        "type": "string",
                        "description": "Optional order direction.",
                    },
                    "fields": {
                        "type": "string",
                        "description": "Optional fields to return.",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gmail_send_message",
            "description": "Send an email message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from": {
                        "type": "string",
                        "description": "The sender of the email.",
                    },
                    "to": {
                        "type": "string",
                        "description": "The recipient of the email.",
                    },
                    "subject": {
                        "type": "string",
                        "description": "The subject of the email.",
                    },
                    "body": {
                        "type": "string",
                        "description": "The body of the email.",
                    },
                },
                "required": ["subject", "body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gmail_delete_message",
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
    "gmail_read_message": gmail_read_message,
    "gmail_send_message": gmail_send_message,
    "gmail_delete_message": gmail_delete_message,
}
