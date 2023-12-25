
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

    # Debug print
    logging.info(
        "Making request to Google CSE API with params: %s",
        params
    )

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=5) as res:
                data = await res.json()
                logging.info(
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
                # Log the results before returning
                logging.info("Search results: %s", results)
                return results

        except (KeyError, TypeError) as error:
            logging.error(
                "An error occurred: %s",
                error
            )
            return []

        except asyncio.TimeoutError as error:
            logging.error(
                "Timeout error occurred: %s",
                error
            )
            return []

        except aiohttp.ClientError as error:
            logging.error(
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
