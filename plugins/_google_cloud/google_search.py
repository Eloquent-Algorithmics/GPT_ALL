
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
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        if GOOGLE_API_KEY is None:
            raise ValueError("GOOGLE_API_KEY not set")

        GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
        if GOOGLE_CSE_ID is None:
            raise ValueError("GOOGLE_CSE_ID not set")

        super().__init__(
            GOOGLE_API_KEY=GOOGLE_API_KEY,
            GOOGLE_CSE_ID=GOOGLE_CSE_ID,
        )

    async def initialize(self):
        # Initialization code if needed
        pass

    async def search_google(self, query: str) -> List:
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
                                "description": "The query to perform the search on.",
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
