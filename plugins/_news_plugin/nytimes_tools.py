
# !/usr/bin/env python
# coding: utf-8
# Filename: nytimes_tools.py
# Path: plugins/_news_plugin/nytimes_tools.py

"""
This script contains the functions, tools, and available tools lists
to fetch articles from New York Times.
"""

import os
import logging
from typing import List
import aiohttp
from rich.console import Console

# Initialize the rich console
console = Console()

# Define the APIs URL and API key
TOOL_URL = os.getenv("NYT_ARTICLE_SEARCH_URL")
TOOL_API_KEY = os.getenv("NYT_API_KEY")


async def get_news_from_nytimes(query: str, api_key=TOOL_API_KEY, url=TOOL_URL) -> List:
    """
    Asynchronously fetches news articles from the New York Times API based on a search query.

    Args:
    - api_key (str): The API key used for authenticating with the New York Times API.
    - query (str): The search query string to find articles related to.
    - url (str): The base URL of the New York Times API.

    Returns:
    - List[Dict[str, str]]: A list of dictionaries, where each dictionary 
    - contains information about a news article, including 'title', 'description', 'snippet', and 'link'.
    """
    # Define the parameters for the request
    params = {
        "q": query,
        "api-key": api_key,
    }

    # Make the request to the New York Times API
    async with aiohttp.ClientSession() as session:
        try:
            logging.debug("Calling to NYTimes API with query: %s", query)
            async with session.get(url, params=params) as res:
                res.raise_for_status()
                data = await res.json()
                logging.debug("Response from NYTimes API: %s", data)
                nyt_news = []
                for doc in data["response"]["docs"]:
                    nyt_news.append(
                        {
                            "title": doc["headline"]["main"],
                            "description": doc["abstract"],
                            "snippet": doc["lead_paragraph"],
                            "link": doc["web_url"],
                        }
                    )
                logging.debug("Processed news articles: %s", nyt_news)
                return nyt_news

        # Handle exceptions
        except aiohttp.ServerTimeoutError as server_timeout_error:
            logging.debug(
                "Server timeout error occurred: %s", server_timeout_error
            )
        except aiohttp.ClientConnectionError as connection_error:
            logging.debug(
                "Connection error occurred: %s", connection_error
            )
        except aiohttp.ClientPayloadError as payload_error:
            logging.debug(
                "Client payload error occurred: %s", payload_error
            )
        except aiohttp.ClientResponseError as response_error:
            logging.debug(
                "Client response error occurred: %s", response_error
            )
        # Return an empty list in case of any exception
        return []


nytimes_tool_list = [
    {
        "type": "function",
        "function": {
            "name": "get_news_from_nytimes",
            "description": "Fetch news from New York Times based on a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The New York Times search query.",
                    },
                },
                "required": ["query"],
            },
        },
    }
]

available_functions = {
    "get_news_from_nytimes": get_news_from_nytimes,
}
