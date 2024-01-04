
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

TOOL_API_KEY = os.getenv("NEWS_API_KEY")


async def get_articles_newsapi(api_key=TOOL_API_KEY, **kwargs) -> List:
    """
    Fetch news from NewsAPI based on query parameters
    """
    query_params = kwargs
    query_params["apiKey"] = api_key
    url = "https://newsapi.org/v2/everything"

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
                                    (article.get("content", "")[:1000] + "...")
                                    if article.get("content") else ""
                                ),
                                "source": article.get("source", {}).get("name", ""),
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


async def get_top_headlines_newsapi(api_key=TOOL_API_KEY, **kwargs) -> List:
    """
    Fetch news from NewsAPI based on query parameters
    """
    query_params = kwargs
    query_params["apiKey"] = api_key
    url = "https://newsapi.org/v2/everything"

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
                                "source": article.get("source", {}).get("name", ""),
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
            "name": "get_articles_newsapi",
            "description": "This function allows you to get news from the NewsAPI.org API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "q": {
                        "type": "string",
                        "description": "The search query to find news articles for. Surround phrases with quotes for exact match. Prepend words or phrases that must appear with a + symbol. Prepend words that must not appear with a - symbol. Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. The complete value for q must be URL-encoded. Max length is 500 characters.",
                    },
                    "searchin": {
                        "type": "string",
                        "description": "The fields to restrict your q search to. The possible options are: title, description, content. Multiple options can be specified by separating them with a comma. Default: all fields are searched.",
                        "enum": ["title", "description", "content"],
                        "default": ["title", "description", "content"],
                    },
                    "sources": {
                        "type": "string",
                        "description": "A comma-separated string of identifiers (maximum 20) for the news sources or blogs you want headlines from. Use the /sources endpoint to locate these programmatically. Note: you can't mix this param with the country or category params.",
                    },
                    "domains": {
                        "type": "string",
                        "description": "A comma-separated string of domains to restrict the search to.",
                    },
                    "excludeDomains": {
                        "type": "string",
                        "description": "A comma-separated string of domains to remove from the results.",
                    },
                    "from": {
                        "type": "string",
                        "description": "A date and optional time for the oldest article allowed. This should be in ISO 8601 format. Default: the oldest according to your plan.",
                    },
                    "to": {
                        "type": "string",
                        "description": "A date and optional time for the newest article allowed. This should be in ISO 8601 format. Default: the newest according to your plan.",
                    },
                    "language": {
                        "type": "string",
                        "description": "Language of News",
                        "enum": ["en", "es"],
                        "default": "en",
                    },
                    "sortBy": {
                        "type": "string",
                        "description": "The order to sort the articles in. Possible options: relevancy, popularity, publishedAt. Default: publishedAt.",
                        "enum": ["relevancy", "popularity", "publishedAt"],
                        "default": "publishedAt",
                    },
                    "pageSize": {
                        "type": "integer",
                        "description": "Page Size",
                        "default": 10,
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page Number",
                        "default": 1,
                    },
                },
                "required": ["q"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_headlines_newsapi",
            "description": "This function allows you to get news from the NewsAPI.org API.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category you want to get headlines for. Possible options: business entertainment general health science sports technology.",
                        "enum": ["business", "entertainment", "general", "health", "science", "sports", "technology"],
                        "default": "general",
                    },
                    "sources": {
                        "type": "string",
                        "description": "A comma-separated string of identifiers (maximum 20) for the news sources or blogs you want headlines from. Use the /sources endpoint to locate these programmatically. Note: you can't mix this param with the country or category params.",
                    },
                    "q": {
                        "type": "string",
                        "description": "The search query to find news articles for. Surround phrases with quotes for exact match. Prepend words or phrases that must appear with a + symbol. Prepend words that must not appear with a - symbol. Alternatively you can use the AND / OR / NOT keywords, and optionally group these with parenthesis. The complete value for q must be URL-encoded. Max length is 500 characters.",
                    },
                    "pageSize": {
                        "type": "integer",
                        "description": "Page Size",
                        "default": 5,
                    },
                    "page": {
                        "type": "integer",
                        "description": "Page Number",
                        "default": 1,
                    },
                },
                "required": ["q"],
            },
        },
    },
]

# Define the available functions outside the class
available_functions = {
    "get_articles_newsapi": get_articles_newsapi,
    "get_top_headlines_newsapi": get_top_headlines_newsapi,
}
