
# !/usr/bin/env python
# coding: utf-8
# Filename: my_plugin.py
# Path: plugins/_gmail_plugin/gmail_base.py

"""
This module contains the GmailToolsPlugin class.
"""

import os
import functools
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from plugins._gmail_plugin.email_tools import (
    email_tools_list,
    available_functions as email_functions
)
from plugins._gmail_plugin.calendar_tools import (
    calendar_tools_list,
    available_functions as calendar_functions
)
from plugins.plugin_base import PluginBase


class GmailPlugin(PluginBase):
    """
    This class defines the GmailPlugin.
    """
    # If modifying these scopes, delete the file token.json.
    SCOPES = [
        "https://mail.google.com/",
        "https://www.googleapis.com/auth/calendar"
    ]

    def __init__(self):
        self.creds = None
        self._load_credentials()
        self.gmail_service = build("gmail", "v1", credentials=self.creds)
        self.calendar_service = build("calendar", "v3", credentials=self.creds)

        super().__init__()

    async def initialize(self):
        """
        Initialize the plugin.
        """
        await self.load_plugin_tools()

    async def load_plugin_tools(self):
        """
        Load tools and functions from accompanying scripts.
        """
        # Load tools and functions from email_tools.py
        self.tools.extend(email_tools_list)
        for func_name, func in email_functions.items():
            self.available_functions[func_name] = functools.partial(
                func,
                self.gmail_service
            )

        # Load tools and functions from calendar_tools.py
        self.tools.extend(calendar_tools_list)
        for func_name, func in calendar_functions.items():
            self.available_functions[func_name] = functools.partial(
                func,
                self.calendar_service
            )

    def _load_credentials(self):
        if os.path.exists("plugins/_gmail_plugin/token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "plugins/_gmail_plugin/token.json",
                self.SCOPES
            )
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(
                    {
                        "installed": {
                            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                            "client_secret": os.getenv(
                                "GOOGLE_CLIENT_SECRET"
                            ),
                            "redirect_uris": [
                                os.getenv("GOOGLE_REDIRECT_URI")
                            ],
                            "auth_uri": (
                                "https://accounts.google.com/o/oauth2/auth"
                            ),
                            "token_uri": (
                                "https://oauth2.googleapis.com/token"
                            ),
                        }
                    },
                    self.SCOPES,
                )
                self.creds = flow.run_local_server(port=0)
            with open(
                "plugins/_gmail_plugin/token.json",
                "w",
                encoding="utf-8"
            ) as token:
                token.write(self.creds.to_json())
