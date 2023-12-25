
# !/usr/bin/env python
# coding: utf-8
# Filename: newsapi_tools.py
# Path: plugins/_news_plugin/newsapi_tools.py

"""
Tools for interacting with NewsAPI.org API.
register for an API key @ https://newsapi.org/
"""

import os
import logging
from typing import List
import aiohttp
from rich.console import Console

console = Console()

TOOL_URL = os.getenv("NEWSAPI_URL", "https://newsapi.org/v2/everything")
TOOL_API_KEY = os.getenv("NEWS_API_KEY")


async def get_news_from_newsapi(url=TOOL_URL, api_key=TOOL_API_KEY, **kwargs) -> List:
    """
    Fetch news from NewsAPI based on query parameters
    """
    query_params = kwargs
    query_params["apiKey"] = api_key

    # Debug print
    logging.info("Making request to NewsAPI with params: %s", query_params)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=query_params, timeout=5) as res:
                data = await res.json()
                logging.info("Received response from NewsAPI: %s", data)
                news = []
                articles = data.get("articles")
                if articles:
                    for article in articles:
                        news.append(
                            {
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "snippet": (
                                    (article.get("content", "")[:500] + "...")
                                    if article.get("content") else ""
                                ),
                                "link": article.get("url", "")
                            }
                        )
                elif data.get("status") == "error":
                    # Handle the case where the API returns an error
                    error_message = data.get('message', 'Unknown error')
                    logging.debug(
                        "NewsAPI.org returned an error: %s",
                        error_message
                    )
                    return []
                else:
                    logging.debug("Error fetching news: Status %s", res.status)
                    return []  # Return an empty list if the status is not 200

                # Log the results before returning
                logging.info("News: %s", news)
                return news

        except aiohttp.ServerTimeoutError as server_timeout_error:
            logging.debug(
                "Server timeout error occurred: %s",
                server_timeout_error
            )
        except aiohttp.ClientConnectionError as connection_error:
            logging.debug(
                "Connection error occurred: %s",
                connection_error
            )
        except aiohttp.ClientPayloadError as payload_error:
            logging.debug(
                "Client payload error occurred: %s",
                payload_error
            )
        except aiohttp.ClientResponseError as response_error:
            logging.debug(
                "Client response error occurred: %s",
                response_error
            )
        # Return an empty list in case of any exception
        return []


# Define the tool list outside the class
newsorg_tool_list = [
    {
        "type": "function",
        "function": {
            "name": "get_news_from_newsapi",
            "description": "Get news from NewsAPI.org API function",
            "parameters": {
                "type": "object",
                "properties": {
                    "q": {
                        "type": "string",
                        "description": "Query to return news stories",
                    },
                    "language": {
                        "type": "string",
                        "description": "Language of News",
                        "enum": ["en", "es"],
                        "default": "en",
                    },
                    "pageSize": {
                        "type": "integer",
                        "description": "Page Size",
                        "default": 10,
                    },
                    "from": {
                        "type": "string",
                        "description": "Optional Date of oldest article.",
                    },
                    "to": {
                        "type": "string",
                        "description": "Optional Date of newest article.",
                    },
                },
                "required": ["q"],
            },
        },
    }

]

# Define the available functions outside the class
available_functions = {
    "get_news_from_newsapi": get_news_from_newsapi,
}
