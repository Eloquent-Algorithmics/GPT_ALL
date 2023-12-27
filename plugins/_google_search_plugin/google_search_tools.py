
# !/usr/bin/env python
# coding: utf-8
# Filename: google_search_tools.py
# Path: plugins/_google_search_plugin/google_search_tools.py

"""
Tools for interacting with Google Search API.
"""

import os
import logging
import asyncio
from typing import List
import aiohttp

TOOL_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Configure a separate logger for the Google Search plugin
google_search_logger = logging.getLogger('GoogleSearchPlugin')
google_search_logger.setLevel(logging.INFO)

# Create a log directory if it doesn't exist
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up the file handler to write logs to a file in the plugin's log directory
log_file_path = os.path.join(log_directory, 'google_search.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(
    logging.Formatter('%(name)s - %(levelname)s - %(message)s')
)
google_search_logger.addHandler(file_handler)


async def search_google(query: str) -> List:
    """
    Search Google and return results.
    """

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": TOOL_API_KEY,
        "cx": CSE_ID,
        "q": query,
    }

    google_search_logger.info(
        "Making request to Google CSE API with params: %s",
        params
    )

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=5) as res:
                data = await res.json()
                google_search_logger.info(
                    "Received response from Google CSE API: %s",
                    data
                )
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
                # Log the results before returning using the plugin-specific logger
                google_search_logger.info("Search results: %s", results)
                return results

        except (KeyError, TypeError) as error:
            google_search_logger.error(
                "An error occurred: %s",
                error
            )
            return []

        except asyncio.TimeoutError as error:
            google_search_logger.error(
                "Timeout error occurred: %s",
                error
            )
            return []

        except aiohttp.ClientError as error:
            google_search_logger.error(
                "Client error occurred: %s",
                error
            )
            return []


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

available_functions = {
    "search_google": search_google,
}
