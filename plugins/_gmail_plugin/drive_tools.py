# !/usr/bin/env python
# coding: utf-8
# Filename: drive_tools.py
# Path: plugins/_gmail_plugin/drive_tools.py

"""
This module contains the Google Drive functions and tools.
"""

import io
import re
import spacy
from googleapiclient.discovery import build
from googleapiclient.http import (
    MediaIoBaseUpload,
    MediaFileUpload,
)

nlp = spacy.load("en_core_web_sm")


def extract_file_names(text):
    """
    Extract file names from user input using spaCy.
    """
    doc = nlp(text)
    file_names = [ent.text for ent in doc.ents if ent.label_ == "WORK_OF_ART"]
    return file_names


def extract_mime_types(text):
    """
    Extract MIME types from user input using spaCy.
    """
    doc = nlp(text)
    mime_types = [ent.text for ent in doc.ents if ent.label_ == "PRODUCT"]
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
    return folder_names


def extract_file_id(text):
    """
    Extract a file ID-like pattern from user input using regular expressions.
    """
    pattern = r'([a-zA-Z0-9-_]{25,})'
    matches = re.findall(pattern, text)
    return matches


def extract_local_paths(text):
    """
    Extract local paths from user input using spaCy and/or regular expressions.
    """
    doc = nlp(text)
    local_paths = [
        ent.text for ent in doc.ents if ent.label_ in ("ORG", "FAC")
    ]

    pattern = r'([a-zA-Z]:\\(?:[^\\\/:*?"<>|\r\n]+\\)*[^\\\/:*?"<>|\r\n]*)'
    local_paths.extend(re.findall(pattern, text))

    return local_paths


def build_drive_service(credentials):
    """Builds the Google Drive service."""
    return build('drive', 'v3', credentials=credentials)


async def upload_file(drive_service, user_input):
    """
    Upload or update a file to Google Drive based on user input.
    """
    try:
        file_names = extract_file_names(user_input)
        mime_types = extract_mime_types(user_input)
        folder_names = extract_folder_names(user_input)

        title = file_names[0] if file_names else 'Untitled'
        mime_type = mime_types[0] if mime_types else 'text/plain'
        folder_name = folder_names[0] if folder_names else 'root'

        content = user_input

        file_metadata = {'name': title}
        media = MediaIoBaseUpload(
            io.BytesIO(content.encode()), mimetype=mime_type
        )

        if folder_name != 'root':
            folder_id = 'GPT_ALL'
            file_metadata['parents'] = [folder_id]

        file = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()

        return f"Uploaded/Updated file with ID: {file.get('id')}"

    except Exception as e:
        return f"An error occurred while uploading the file: {e}"


async def download_file(drive_service, user_input, local_path):
    """
    Download a file from Google Drive by file name or folder name.
    """
    try:
        file_names = extract_file_names(user_input)
        folder_names = extract_folder_names(user_input)

        file_name = file_names[0] if file_names else None
        folder_name = folder_names[0] if folder_names else None

        folder_id = None
        if folder_name:
            folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
            folder_response = drive_service.files().list(q=folder_query, fields="files(id)").execute()
            folders = folder_response.get('files', [])
            if folders:
                folder_id = folders[0].get('id')

        return f"Downloaded file '{file_name}' to {local_path}"

    except Exception as e:
        return f"An error occurred while downloading the file: {e}"


async def list_files(drive_service, folder_name='root', max_results=10):
    """
    List files in Google Drive within a specified folder.
    """
    try:
        folder_query = f"name = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
        folder_response = drive_service.files().list(
            q=folder_query, fields="files(id, name)"
        ).execute()
        folders = folder_response.get('files', [])

        if not folders:
            return []

        folder_id = folders[0].get('id')

        query = "'%s' in parents" % folder_id
        response = drive_service.files().list(
            q=query, pageSize=max_results, fields="nextPageToken, files(id, name)"
        ).execute()
        files_info = [
            {'name': file.get('name'), 'id': file.get('id')} for file in response.get('files', [])
        ]

        return files_info

    except Exception as e:
        return f"An error occurred while listing the files: {e}"


async def create_folder(drive_service, folder_name, parent_id='root'):
    """
    Create a new folder in Google Drive.
    """
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')


async def search_files(drive_service, query):
    """
    Search for files and folders in Google Drive.
    """
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    return items


async def share_file(drive_service, file_id, user_email, role='reader'):
    """
    Share a file or folder with a user.
    """
    user_permission = {
        'type': 'user',
        'role': role,
        'emailAddress': user_email
    }
    drive_service.permissions().create(
        fileId=file_id,
        body=user_permission,
        fields='id'
    ).execute()


async def move_file(drive_service, file_id, folder_id):
    """
    Move a file or folder to a different folder.
    """
    file = drive_service.files().get(fileId=file_id, fields='parents').execute()
    previous_parents = ",".join(file.get('parents'))
    file = drive_service.files().update(
        fileId=file_id,
        addParents=folder_id,
        removeParents=previous_parents,
        fields='id, parents'
    ).execute()


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
            "name": "list_files",
            "description": "List files in a specified Google Drive folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_name": {
                        "type": "string",
                        "description": "The name of the folder to list files from. Defaults to 'root' if not specified.",
                        "default": "root"
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
            "name": "create_folder",
            "description": "Create a new folder in Google Drive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "folder_name": {
                        "type": "string",
                        "description": "The name of the folder to create.",
                    },
                    "parent_id": {
                        "type": "string",
                        "description": "The ID of the parent folder. Defaults to 'root' if not specified.",
                        "default": "root"
                    }
                },
                "required": ["folder_name"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_files",
            "description": "Search for files and folders in Google Drive.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to use.",
                    }
                },
                "required": ["query"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "share_file",
            "description": "Share a file or folder with a user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "The ID of the file or folder to share.",
                    },
                    "user_email": {
                        "type": "string",
                        "description": "The email address of the user to share with.",
                    },
                    "role": {
                        "type": "string",
                        "description": "The role to grant to the user. Defaults to 'reader' if not specified.",
                        "default": "reader"
                    }
                },
                "required": ["file_id", "user_email"]
            }
        },
    },
    {
        "type": "function",
        "function": {
            "name": "move_file",
            "description": "Move a file or folder to a different folder.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_id": {
                        "type": "string",
                        "description": "The ID of the file or folder to move.",
                    },
                    "folder_id": {
                        "type": "string",
                        "description": "The ID of the folder to move the file or folder to.",
                    }
                },
                "required": ["file_id", "folder_id"]
            }
        },
    }
]

available_functions = {
    "upload_file": upload_file,
    "download_file": download_file,
    "list_files": list_files,
    "create_folder": create_folder,
    "search_files": search_files,
    "share_file": share_file,
    "move_file": move_file,
}
