
# !/usr/bin/env python
# coding: utf-8
# Filename: drive_tools.py
# Path: plugins/_gmail_plugin/drive_tools.py

"""
This module contains the Google Drive functions and tools.
"""

import os
import logging
import io
import re
import spacy
from googleapiclient.discovery import build
from googleapiclient.http import (
    MediaIoBaseUpload,
)
from plugins._gmail_plugin.errors import FolderNotFoundError

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Configure a separate logger for the Google Drive functions and tools
drive_tools_logger = logging.getLogger('gDrive_Tools')
drive_tools_logger.setLevel(logging.INFO)

# Create a log directory if it doesn't exist
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up the file handler to write logs to a file in the plugin's log directory
log_file_path = os.path.join(log_directory, 'drive_tools.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(
    logging.Formatter('%(levelname)s - %(message)s')
)
drive_tools_logger.addHandler(file_handler)


# Entity extraction functions using spaCy
def extract_file_names(text):
    """
    Extract file names from user input using spaCy.
    """
    doc = nlp(text)
    file_names = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
    drive_tools_logger.info(
        "Extracted file names from line 49: %s", file_names
    )
    return file_names


def extract_mime_types(text):
    """
    Extract MIME types from user input using spaCy.
    """
    doc = nlp(text)
    mime_types = [ent.text for ent in doc.ents if ent.label_ == "PRODUCT"]
    drive_tools_logger.info(
        "Extracted MIME types from line 61: %s", mime_types
    )
    return mime_types


def extract_folder_names(text):
    """
    Extract folder names from user input using spaCy.
    """
    doc = nlp(text)
    folder_names = [
        ent.text for ent in doc.ents if ent.label_ in (
            "ORG", "GPE", "LOC", "FAC"
        )
    ]
    drive_tools_logger.info(
        "Extracted folder names from line 78: %s", folder_names
    )
    return folder_names


def extract_file_id(text):
    """
    Extract a file ID-like pattern from user input using regular expressions.
    """
    # This is a simple regex pattern
    pattern = r'([a-zA-Z0-9-_]{25,})'
    matches = re.findall(pattern, text)
    drive_tools_logger.info(
        "Extracted file ID line 91: %s", matches
    )
    return matches


def extract_local_paths(text):
    """
    Extract local paths from user input using spaCy and/or regular expressions.
    """
    # Assuming local paths may be mentioned as entities of type 'ORG' or 'FAC'
    doc = nlp(text)
    local_paths = [
        ent.text for ent in doc.ents if ent.label_ in ("ORG", "FAC")
    ]

    # Alternatively, use regex to match a pattern for file paths
    pattern = r'([a-zA-Z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]*)'
    local_paths.extend(re.findall(pattern, text))
    drive_tools_logger.info(
        "Extracted local paths from line 110: %s", local_paths
    )
    return local_paths


def build_drive_service(credentials):
    """Builds the Google Drive service."""
    return build('drive', 'v3', credentials=credentials)


async def upload_file(drive_service, user_input):
    """
    Upload or update a file to Google Drive based on user input.
    """
    try:
        # Extract information from user input
        file_names = extract_file_names(user_input)
        mime_types = extract_mime_types(user_input)
        folder_names = extract_folder_names(user_input)

        # For simplicity, taking the first extracted file name and MIME type
        title = file_names[0] if file_names else 'Untitled'
        mime_type = mime_types[0] if mime_types else 'text/plain'
        folder_name = folder_names[0] if folder_names else 'My Drive'

        # Here you should define how you get the actual content to upload
        content = user_input

        file_metadata = {'name': title}
        media = MediaIoBaseUpload(
            io.BytesIO(content.encode()), mimetype=mime_type
        )

        # If the folder_name is not 'My Drive', find the folder ID
        if folder_name != 'My Drive':
            # Search for the folder to get its ID
            folder_id = 'GPT_ALL'
            file_metadata['parents'] = [folder_id]

        file = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()
        drive_tools_logger.info(
            "Uploaded/Updated file from line 153: %s", title
        )
        return f"Uploaded/Updated file with ID: {file.get('id')}"

    except IOError as e:
        drive_tools_logger.error("An error occurred from line 157: %s", e)
        return f"An error occurred while uploading the file: {e}"


async def download_file(drive_service, user_input, local_path):
    """
    Download a file from Google Drive by file name or folder name.
    """
    try:
        # Extract file and folder names from user input
        file_names = extract_file_names(user_input)
        folder_names = extract_folder_names(user_input)

        # Determine the file name and folder name (if any)
        file_name = file_names[0] if file_names else None
        folder_name = folder_names[0] if folder_names else None

        # If folder name is provided, find the folder ID
        folder_id = None
        if folder_name:
            folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
            folder_response = drive_service.files().list(
                q=folder_query, fields="files(id)"
            ).execute()
            folders = folder_response.get('files', [])
            if folders:
                folder_id = folders[0].get('id')

        # Search for the file by name
        file_query = f"name = '{file_name}'"
        if folder_id:
            file_query += f" and '{folder_id}' in parents"
        drive_tools_logger.info(
            "Downloaded file '%s' with ID: %s from line 188",
            file_name,
            file_id
        )
        return f"Downloaded file '{file_name}' to {local_path}"

    except IOError as e:
        drive_tools_logger.error(
            "An error occurred: %s from line 196", e, exc_info=True
        )
        return f"An error occurred while downloading the file: {e}"


async def list_files(drive_service, folder_name='My Drive', max_results=10):
    """
    List files in Google Drive within a specified folder.
    """
    try:
        # If folder_name is 'My Drive', use the special 'root' alias
        if folder_name == 'My Drive':
            folder_id = 'root'
        else:
            # Corrected query to search for a folder by name
            folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
            folder_response = drive_service.files().list(
                q=folder_query, fields="files(id, name)"
            ).execute()
            folders = folder_response.get('files', [])

            # If no folders found, raise a custom exception
            if not folders:
                drive_tools_logger.info(
                    "No folder found with the name '%s'.", folder_name
                )
                raise FolderNotFoundError(folder_name)

            # Assuming the first folder found is the one we want
            folder_id = folders[0].get('id')

        # Query to list files inside the folder
        query = f"'{folder_id}' in parents"
        response = drive_service.files().list(
            q=query, pageSize=max_results, fields="nextPageToken, files(id, name)"
        ).execute()
        files_info = response.get('files', [])

        # Format the file information into a string
        if files_info:
            file_list_str = "\n".join(
                f"{file['name']} (ID: {file['id']})" for file in files_info
            )
            drive_tools_logger.info(
                "Files in folder from line 243 '%s': %s",
                folder_name,
                file_list_str
            )
            return f"Files in folder '{folder_name}':\n{file_list_str}"
        else:
            return f"No files found in folder '{folder_name}'."

    except IOError as e:
        drive_tools_logger.error("An error occurred: %s", e)
        return f"An error occurred while listing the files: {e}"


def search_my_drive(drive_service):
    """
    Search all files and folders in 'My Drive'.
    :param drive_service: The authenticated Google Drive service instance.
    :return: List of files and folders in 'My Drive'.
    """
    try:
        files_info = list_files(drive_service, folder_name='My Drive')
        drive_tools_logger.info(
            "Files in 'My Drive' from line 255: %s", files_info
        )
        return files_info
    except Exception as e:
        print(f"An error occurred while searching 'My Drive': {e}")
        drive_tools_logger.error("An error occurred from line 271: %s", e)
        return []


drive_tools_list = [
    {
        "type": "function",
        "function": {
            "name": "upload_file",
            "description": "Upload or update a file to Google Drive based on user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "The user input containing file name, content, and other metadata.",
                    }
                },
                "required": ["user_input"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "download_file",
            "description": "Download a file from Google Drive based on user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "The user input containing the file ID and local path information.",
                    }
                },
                "required": ["user_input"],
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "upload_file",
            "description": "Upload or update a file to Google Drive based on user input.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_input": {
                        "type": "string",
                        "description": "The user input containing file name, content, and other metadata.",
                    }
                },
                "required": ["user_input"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a specified Google Drive folder. If 'folder_name' is 'My Drive', it lists files in 'My Drive', which is the top-level folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_name": {
                        "type": "string",
                        "description": "The name of the folder to list files from. Defaults to 'My Drive' (equivalent to 'My Drive') if not specified.",
                        "default": "My Drive"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "The maximum number of file results to retrieve. Defaults to 10 if not specified.",
                        "default": 10
                    }
                },
                "required": []
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_my_drive",
            "description": "Search all files and folders in 'My Drive'.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        },
    },
]

available_functions = {
    "upload_file": upload_file,
    "download_file": download_file,
    "list_files": list_files,
    "search_my_drive": search_my_drive,
}

# drive_tools_logger.info(f"Available functions: {available_functions}, {drive_tools_list}")
