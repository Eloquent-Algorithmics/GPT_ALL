
# !/usr/bin/env python
# coding: utf-8
# Filename: drive_tools.py
# Path: plugins/_gmail_plugin/errors.py

"""
This module contains custom exceptions for the Gmail plugin.
"""


class FolderNotFoundError(Exception):
    """Exception raised when a folder is not found in Google Drive."""
    def __init__(self, folder_name, message="Folder not found"):
        self.folder_name = folder_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}: {self.folder_name}"
