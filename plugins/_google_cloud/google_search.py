"""
This module defines the Google Search plugin.
"""

# !/usr/bin/env python
# coding: utf-8
# Filename: google_search.py
# Path: plugins\_google_cloud\google_search.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17

import os
import asyncio
from typing import List
import aiohttp
from rich.console import Console
from plugins.plugin_base import PluginBase

# Create a Console object
console = Console()


# Create the GoogleSearchPlugin class
class GoogleSearchPlugin(PluginBase):
    """
    This class defines the Google Search plugin.
    """

    def __init__(self):

        """
        Initialize the GoogleSearchPlugin class.

        """
        # Get the API key and CSE ID from environment variables
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key is None:
            raise ValueError("GOOGLE_API_KEY not set")

        google_cse_id = os.getenv("GOOGLE_CSE_ID")
        if google_cse_id is None:
            raise ValueError("GOOGLE_CSE_ID not set")

        super().__init__()

        # Set the API key and CSE ID as instance attributes
        self.api_key = google_api_key
        self.cse_id = google_cse_id

    async def initialize(self):
        # Initialization code if needed
        pass

    async def search_google(self, query: str) -> List:

        """
        Search Google and return results.
        """

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query,
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params, timeout=5) as res:
                    data = await res.json()
                    results = []
                    if data.get("items"):
                        for item in data["items"]:
                            results.append(
                                {
                                    "title": item["title"],
                                    "description": item["snippet"],
                                    "link": item["link"],
                                }
                            )
                    return results

            except (KeyError, TypeError) as error:
                console.print(f"An error occurred: {error}")
                return []
            except asyncio.TimeoutError as error:
                console.print(f"Timeout error occurred: {error}")
                return []
            except aiohttp.ClientError as error:
                console.print(f"Client error occurred: {error}")
                return []

    def get_tools(self):
        search_google_tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_google",
                    "description": "Search Google and return results.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "query perform the search on.",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

        self.tools.extend(search_google_tools)

        available_functions = {
            "search_google": self.search_google,
        }

        return available_functions, self.tools
