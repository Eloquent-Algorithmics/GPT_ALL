
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


# Configure logging for the module
logging.basicConfig(
    filename='email_tools.log',
    level=logging.INFO,
    format='%(levelname)s:%(message)s'
)


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
        logging.info("Emails from line 48: %s", emails)
        return emails

    except HttpError as error:
        logging.error("An error occurred from line 52: %s", error)
        return []


async def gmail_send_message(gmail_service, **kwargs):
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
        logging.info("Message Id from line 79: %s", send_message["id"])
        return f"Message Id: {send_message['id']}"
    except HttpError as error:
        logging.error("An error occurred from line 83: %s", error)
        return f"An error occurred while sending the email: {error}"


async def gmail_delete_message(gmail_service, message_id):
    """Delete an email message by ID."""
    try:
        gmail_service.users().messages().delete(userId='me', id=message_id).execute()
    except HttpError as error:
        logging.error("An error occurred from line 91: %s", error)


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
    logging.info("Email body from line 107: %s", body)
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
        logging.info("Email body from line 120: %s", body)
        return body
    else:
        body = payload['body'].get('data', '')
        # Await the coroutine to get the decoded body
        logging.info("Email body from line 124: %s", body)
        return await _decode_base64(body)


async def _decode_base64(data, mime_type='text/plain'):
    """Decode base64-encoded data."""
    try:
        decoded_body_bytes = base64.urlsafe_b64decode(data)
        decoded_body = decoded_body_bytes.decode(errors='ignore')
    except binascii.Error as e:
        logging.error(
            "Error decoding base64-encoded data from line 134: %s", e
        )
        decoded_body = ''

    if mime_type == 'text/html':
        soup = BeautifulSoup(decoded_body, 'html.parser')
        return soup.get_text()
    else:
        logging
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
                    # Search for messages matching an object ID: `object_id:`
                    "object_id": {
                        "type": "string",
                        "description": "Searches for messages by object ID to filter returned emails.",
                    },
                    # Search for messages matching a query: `query:`
                    "query": {
                        "type": "string",
                        "description": "Search query to filter emails by: `query:`",
                    },
                    # Specify words in the subject line to search for:`subject:`
                    "subject": {
                        "type": "string",
                        "description": "Words in the subject line to filter by: `subject:`",
                    },
                    # Specify a recipient to search for: `to:`
                    "to": {
                        "type": "string",
                        "description": "Specify a recipient to filter by: `to:`",
                    },
                    # Specify the sender to search for: `from:`
                    "from": {
                        "type": "string",
                        "description": "Specify the sender to filter by: `from:`",
                    },
                    # Specify a recipient to filter: `cc:`
                    "cc": {
                        "type": "string",
                        "description": "Recipient to filter by `cc:`",
                    },
                    # Specify a recipient who received a copy: `bcc:`
                    "bcc": {
                        "type": "string",
                        "description": "Filter by recipient who received a copy to filter by `bcc:`",
                    },
                    # Search for messages that match multiple terms: `OR` or `{ }`
                    "OR": {
                        "type": "string",
                        "description": "Find messages that match multiple terms `OR` or `{ }`, Example: from:amy OR from:david, Example: {from:amy from:david}",
                    },
                    # Remove messages from the results `-`
                    "-": {
                        "type": "string",
                        "description": "Remove messages from your results `-`, Example: dinner -movie",
                    },
                    # Search messages with words near each other. Use the number to say how many words apart the words can be `AROUND`
                    "AROUND": {
                        "type": "string",
                        "description": "Find messages with words near each other. Use the number to say how many words apart the words can be, Example: holiday AROUND 10 vacation",
                    },
                    # Search for messages that have a certain label `label:`
                    "label": {
                        "type": "string",
                        "description": "Find messages that have a certain label, Example: label:friends",
                    },
                    # Search for messages that have a Google Drive, Docs, Sheets, Slides, Youtube Video, attachment, link, an icon of a certain color, or that have or don't have a label:
                    "has": {
                        "type": "string",
                        "description": "Search for messages that have an attachment `has:`, Example: has:attachment, has:drive, has:document, has:spreadsheet, has:presentation, has:youtube, has:yellow-star, has:blue-start, has:userlabels, has:nouserlabels",
                    },
                    # Search for messages that have attachments of a certain type `filename:`
                    "filename": {
                        "type": "string",
                        "description": "Messages that have attachments of a certain type `filename:`, Example: filename:pdf, filename:homework.txt",
                    },
                    # Search by email for delivered messages: `deliveredto:`
                    "deliveredto": {
                        "type": "string",
                        "description": "Search by email for delivered messages `deliveredto:`, Example: deliveredto:",
                    },
                    # Search for messages in a certain category: `category:`
                    "category": {
                        "type": "string",
                        "description": "Search for messages in a certain category `category:`, Example: category:primary, category:social, category:promotions, category:updates, category:forums, category:reservations, category:purchases",
                    },
                    # Search for messages larger than a certain size in bytes `size:` `larger:` `smaller:`
                    "size": {
                        "type": "string",
                        "description": "Messages larger than a certain size in bytes `size:` `larger:` `smaller:`, Example: size:1000000, larger:10M",
                    },
                    # Search for results that match a word exactly `+`
                    "+": {
                        "type": "string",
                        "description": "Search for results that match a word exactly `+`, Example: +unicorn",
                    },
                    # Search for messages with a certain message-id header `rfc822msgid:`
                    "rfc822msgid": {
                        "type": "string",
                        "description": "Search for messages with a certain message-id header `rfc822msgid:`, Example: rfc822msgid:200503292@example.com",
                    },
                    # Search for messages from a mailing list `list:`
                    "list": {
                        "type": "string",
                        "description": "Optional Messages from a mailing list `list:`, Example: list:info@example.com",
                    },
                    # Search for an exact word or phrase `""`
                    "": {
                        "type": "string",
                        "description": "Search for an exact word or phrase `""`, Example: \"dinner and movie tonight\"",
                    },
                    # Group multiple search terms together `( )`
                    "()": {
                        "type": "string",
                        "description": "Group multiple search terms together `( )`, Example: subject:(dinner movie)",
                    },
                    # Messages in any folder, including Spam and Trash `in:anywhere`
                    "in": {
                        "type": "string",
                        "description": "Messages in any folder, including Spam and Trash `in:anywhere`, Example: in:anywhere movie",
                    },
                    # Search for messages that are marked: `is:important` `is:starred`
                    "is": {
                        "type": "string",
                        "description": "Search for messages that are marked: `is:important` `is:starred`, Example: is:important",
                    },
                    # Search for messages sent during a certain time period `after:`
                    "after": {
                        "type": "string",
                        "description": "Search for messages sent during a certain time period `after:`, `before:`, `older:`, `newer:`. Example: after:2004/04/16",
                    },
                    # Search for messages older or newer than a time period using d (day), m (month), and y (year)
                    "older_than": {
                        "type": "string",
                        "description": "Search for messages older or newer than a time period using d (day), m (month), and y (year), Example: newer_than:2d",
                    },
                    # Search for messages older or newer than a time period using d (day), m (month), and y (year)
                    "newer_than": {
                        "type": "string",
                        "description": "Search for messages older or newer than a time period using d (day), m (month), and y (year), Example: newer_than:2d",
                    },
                    # The sort order applied to the results of the search `order_by:`
                    "order_by": {
                        "type": "string",
                        "description": "Optional order by field.",
                    },
                    # The sort direction applied to the results of the search `order_direction:`
                    "order_direction": {
                        "type": "string",
                        "description": "Optional order direction.",
                    },
                    # The number of results to return `limit:`
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
