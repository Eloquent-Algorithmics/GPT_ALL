
# !/usr/bin/env python
# coding: utf-8
# Filename: google_search_tools.py
# Path: plugins/_google_search_plugin/google_search_tools.py

"""
Tools for interacting with Google Search API.
"""

import os
import asyncio
from typing import List
import aiohttp
import requests

TOOL_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")


def search_google_synchronous(query: str, num: [int] = 10, start: [int] = 1, fileType: [str] = None, lr: [str] = None, safe: [str] = "off") -> List:
    """
    Search Google and return results.

    :param query: The search query string.
    :param num: Number of search results to return.
    :param start: The first result to retrieve (starts at 1).
    :param fileType: Filter results to a specific file type.
    :param lr: Restricts search to documents written in a particular language.
    :param safe: Search safety level (e.g., off, medium, high).
    :return: A list of search results.
    """

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": TOOL_API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num,
        "start": start,
        "safe": safe,
    }

    # Add optional parameters if they are provided
    if fileType:
        params["fileType"] = fileType
    if lr:
        params["lr"] = lr

    try:
        res = requests.get(url, params=params, timeout=5)
        data = res.json()
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

    except requests.exceptions.RequestException:
        return []


async def search_google_asynchronous(query: str, num: [int] = 10, start: [int] = 1, fileType: [str] = None, lr: [str] = None, safe: [str] = "off") -> List:
    """
    Search Google and return results.

    :param query: The search query string.
    :param num: Number of search results to return.
    :param start: The first result to retrieve (starts at 1).
    :param fileType: Filter results to a specific file type.
    :param lr: Restricts search to documents written in a particular language.
    :param safe: Search safety level (e.g., off, medium, high).
    :return: A list of search results.
    """

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": TOOL_API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num,
        "start": start,
        "safe": safe,
    }

    if fileType:
        params["fileType"] = fileType
    if lr:
        params["lr"] = lr

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

        except (KeyError, TypeError):

            return []

        except asyncio.TimeoutError:
            return []

        except aiohttp.ClientError:
            return []


search_google_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_google_synchronous",
            "description": "This function allows you to use the Google custom search engine API synchronously.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query to perform the search on.",
                    },
                    "num": {
                        "type": "integer",
                        "description": "Number of search results to return.",
                    },
                    "start": {
                        "type": "integer",
                        "description": "The first result to retrieve (starts at 1).",
                    },
                    "fileType": {
                        "type": "string",
                        "description": "Filter results to a specific file type.",
                    },
                    "lr": {
                        "type": "string",
                        "description": "Restricts the search to documents written in a particular language.",
                    },
                    "safe": {
                        "type": "string",
                        "description": "Search safety level.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_google_asynchronous",
            "description": "This function allows you to use the Google custom search engine API asynchronously.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query to perform the search on.",
                    },
                    "num": {
                        "type": "integer",
                        "description": "Number of search results to return.",
                    },
                    "start": {
                        "type": "integer",
                        "description": "The first result to retrieve (starts at 1).",
                    },
                    "fileType": {
                        "type": "string",
                        "description": "Filter results to a specific file type.",
                    },
                    "lr": {
                        "type": "string",
                        "description": "Restricts the search to documents written in a particular language.",
                    },
                    "safe": {
                        "type": "string",
                        "description": "Search safety level.",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

available_functions = {
    "search_google_synchronous": search_google_synchronous,
    "search_google_asynchronous": search_google_asynchronous,
}
