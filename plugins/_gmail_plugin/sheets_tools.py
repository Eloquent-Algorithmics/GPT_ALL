
# !/usr/bin/env python
# coding: utf-8
# Filename: sheets_tools.py
# Path: plugins/_gmail_plugin/sheets_tools.py

"""
This module contains the Google Sheets functions and tools.
"""

import logging
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(
    filename='sheets_tools.log',
    level=logging.INFO,
    format='%(levelname)s:%(message)s'
)


async def read_spreadsheet(sheets_service, spreadsheet_id, range_name):
    """
    Reads data from a specified range in a Google Sheet.
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
            logging.info("Data retrieved successfully.")
            return values
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return f"An error occurred while reading the sheet: {error}"


async def write_spreadsheet(sheets_service, spreadsheet_id, range_name, values):
    """
    Writes data to a specified range in a Google Sheet.
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

        logging.info("Data written successfully.")
        return result
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return f"An error occurred while writing to the sheet: {error}"


async def append_spreadsheet(sheets_service, spreadsheet_id, range_name, values):
    """
    Appends data to the end of a specified range in a Google Sheet.
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

        logging.info("Data appended successfully.")
        return result
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return f"An error occurred while appending to the sheet: {error}"


sheets_tools_list = [
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
                        "description": "The ID of the spreadsheet to write to.",
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The A1 notation of the range to write to.",
                    },
                    "values": {
                        "type": "array",
                        "description": "The data to write in the range.",
                    },
                },
                "required": ["spreadsheet_id", "range_name", "values"],
            },
        },
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
                        "description": "The ID of the spreadsheet to append to.",
                    },
                    "range_name": {
                        "type": "string",
                        "description": "The A1 notation of the range to append to.",
                    },
                    "values": {
                        "type": "array",
                        "description": "The data to append in the range.",
                    },
                },
                "required": ["spreadsheet_id", "range_name", "values"],
            },
        },
    },
]

available_functions = {
    "read_spreadsheet": read_spreadsheet,
    "write_spreadsheet": write_spreadsheet,
    "append_spreadsheet": append_spreadsheet,
}
