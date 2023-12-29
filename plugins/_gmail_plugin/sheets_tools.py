
# !/usr/bin/env python
# coding: utf-8
# Filename: sheets_tools.py
# Path: plugins/_gmail_plugin/sheets_tools.py

"""
This module contains the Google Sheets functions and tools.
"""

import logging
import re
import spacy
from spacy.matcher import Matcher
from googleapiclient.errors import HttpError

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define patterns for matching intents
matcher = Matcher(nlp.vocab)
matcher.add("READ_INTENT", [[{"LOWER": "read"}]])
matcher.add("WRITE_INTENT", [[{"LOWER": "write"}]])
matcher.add("APPEND_INTENT", [[{"LOWER": "append"}]])


# Function to determine the user's intent
def determine_intent(text):
    """
    This function determines the user's intent based on the input text.
    """
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]
        if rule_id == "READ_INTENT":
            return "read_spreadsheet"
        elif rule_id == "WRITE_INTENT":
            return "write_spreadsheet"
        elif rule_id == "APPEND_INTENT":
            return "append_spreadsheet"
    return None


# Function to extract entities like spreadsheet name and range
def extract_entities(text):
    """
    This function extracts entities like spreadsheet name and range from input.
    """
    doc = nlp(text)
    # Define your logic to extract entities like spreadsheet name and range
    spreadsheet_name = None
    range_name = None
    for ent in doc.ents:
        if ent.label_ == "ORG":
            spreadsheet_name = ent.text
        elif ent.label_ == "DATE":
            range_name = ent.text
        elif ent.label_ == "MONEY":
            range_name = ent.text
        elif ent.label_ == "PERCENT":
            range_name = ent.text
        elif ent.label_ == "CARDINAL":
            range_name = ent.text
        elif ent.label_ == "QUANTITY":
            range_name = ent.text
        elif ent.label_ == "ORDINAL":
            range_name = ent.text
        elif ent.label_ == "TIME":
            range_name = ent.text
        elif ent.label_ == "LOC":
            range_name = ent.text
        elif ent.label_ == "GPE":
            range_name = ent.text
        elif ent.label_ == "PERSON":
            range_name = ent.text
        elif ent.label_ == "NORP":
            range_name = ent.text
        elif ent.label_ == "PRODUCT":
            range_name = ent.text
        elif ent.label_ == "EVENT":
            range_name = ent.text
        elif ent.label_ == "WORK_OF_ART":
            range_name = ent.text
        elif ent.label_ == "LANGUAGE":
            range_name = ent.text
        elif ent.label_ == "LAW":
            range_name = ent.text
        elif ent.label_ == "FAC":
            range_name = ent.text

    # Add more conditions to extract other entities
    logging.info("Entities extracted: %s, %s", spreadsheet_name, range_name)
    return spreadsheet_name, range_name


# Main function to process user input
async def process_user_input(sheets_service, user_input):
    """
    This function processes the user input and calls the appropriate function.
    """
    intent = determine_intent(user_input)
    spreadsheet_name, range_name = extract_entities(user_input)

    # Convert the spreadsheet name to an ID
    spreadsheet_id = await get_spreadsheet_id_by_name(sheets_service, spreadsheet_name)
    if not spreadsheet_id:
        return f"Spreadsheet named '{spreadsheet_name}' not found."

    # Extract values from the user input
    values = extract_values(user_input)

    # Based on the intent, call the appropriate function
    if intent == "read_spreadsheet":
        return await read_spreadsheet(
            sheets_service,
            spreadsheet_id,
            range_name
        )
    elif intent == "write_spreadsheet":
        return await write_spreadsheet(
            sheets_service,
            spreadsheet_id,
            range_name,
            values
        )
    elif intent == "append_spreadsheet":
        return await append_spreadsheet(
            sheets_service,
            spreadsheet_id,
            range_name,
            values
        )
    else:
        return "I'm not sure what you want to do?"


async def read_spreadsheet(sheets_service, spreadsheet_id, range_name):
    """
    Reads data from a specified range in a Google Sheet.

    Note: This function uses the Google Sheets API. For more information, see:
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get

    """
    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        values = result.get('values', [])

        if not values:
            logging.info("No data found.")
            return "No data found."
        else:
            logging.info("Data retrieved successfully.%s", values)
            return values
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return f"An error occurred while reading the sheet: {error}"


async def write_spreadsheet(sheets_service, spreadsheet_id, range_name, values):
    """
    Writes data to a specified range in a Google Sheet.

    Note: This function uses the Google Sheets API. For more information, see:
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/update

    """
    try:
        body = {
            'values': values
        }
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        logging.info("Data written successfully.%s", result)
        return result
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return f"An error occurred while writing to the sheet: {error}"


async def append_spreadsheet(sheets_service, spreadsheet_id, range_name, values):
    """
    Appends data to the end of a specified range in a Google Sheet.

    Note: This function uses the Google Sheets API. For more information, see:
    https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append

    """
    try:
        body = {
            'values': values
        }
        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()

        logging.info("Data appended successfully.%s", result)
        return result
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return f"An error occurred while appending to the sheet: {error}"


async def get_spreadsheet_id_by_name(drive_service, spreadsheet_name):
    """
    Searches for a spreadsheet by name and returns its ID from Google Drive.

    Note: This function uses the Google Drive API.

    For more information, see:
    https://developers.google.com/drive/api/v3/search-files

    """
    try:
        # List all files of type 'spreadsheet' in the user's Google Drive
        response = drive_service.files().list(
            q="mimeType='application/vnd.google-apps.spreadsheet'",
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        files = response.get('files', [])

        # Normalize search term to lower case for case-insensitive comparison
        search_term = spreadsheet_name.lower()

        # Use regular expression to allow for partial matches and variations
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)

        # Search for a spreadsheet that contains the search term in its title
        for file in files:
            title = file.get('name', '').lower()
            if pattern.search(title):
                logging.info("Spreadsheet ID found: %s", file.get('id'))
                return file.get('id')
        return None
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return None


# Function to extract values to write or append from user input
def extract_values(user_input):
    """
    This function extracts values to write or append from the user input.
    Assuming the user input might be structured as follows:
    "In 'Budget', set 'January' 'Marketing' to 5000 and 'February' 'Sales' to 3000."
    """
    doc = nlp(user_input)

    # Placeholder for extracted values
    values = []

    # Assuming the pattern is "set 'Column' 'Row' to 'Value'"
    # We will look for this pattern using spaCy's dependency parsing
    for token in doc:
        if token.text.lower() == "set":
            # Find the column, row, and value following the "set" keyword
            column = None
            row = None
            value = None
            for child in token.children:
                # Check if the child is a noun
                if child.pos_ in ['NOUN', 'PROPN']:
                    if not column:
                        column = child.text
                    elif not row:
                        row = child.text
                # Check if the child is a number (which would be the value)
                elif child.pos_ == 'NUM':
                    value = child.text
                # Check for compound values (e.g., "5000" following "to")
                elif child.text.lower() == "to":
                    for grandchild in child.children:
                        if grandchild.pos_ == 'NUM':
                            value = grandchild.text

            # If we have found a column, row, and value, add it to the list
            if column and row and value:
                values.append({'column': column, 'row': row, 'value': value})

    sheet_values = []
    for item in values:
        # Convert the column and row into A1 notation if necessary
        a1_notation = f"{item['column']}{item['row']}"
        # Append the value for the corresponding cell
        sheet_values.append([a1_notation, item['value']])

    return sheet_values


# Define the list of functions that will be available to the user
sheets_tools_list = [
    {
        "type": "function",
        "function": {
            "name": "process_user_input",
            "description": "Process natural language input to perform actions on a Google Sheet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "The natural language input from the user describing the action to perform.",
                    },
                },
                "required": ["user_input"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_spreadsheet",
            "description": "Read data from a specified range in a Google Sheet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet to read from.",
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The A1 notation of the range to read.",
                    },
                },
                "required": ["spreadsheet_id", "range_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_spreadsheet",
            "description": "Write data to a specified range in a Google Sheet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet to write to."
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The A1 notation of the range to write to."
                    },
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "description": "The data to write in the range, as an array of arrays where each sub-array represents a row of data."
                    }
                },
                "required": ["spreadsheet_id", "range_name", "values"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "append_spreadsheet",
            "description": "Append data to the end of a specified range in a Google Sheet.",
            "parameters": {
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "The ID of the spreadsheet to append to."
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The A1 notation of the range to append to."
                    },
                    "values": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        },
                        "description": "The data to append in the range, as an array of arrays where each sub-array represents a row of data."
                    }
                },
                "required": ["spreadsheet_id", "range_name", "values"]
            }
        }
    },
]

available_functions = {
    "process_user_input": process_user_input,
    "read_spreadsheet": read_spreadsheet,
    "write_spreadsheet": write_spreadsheet,
    "append_spreadsheet": append_spreadsheet,
}
