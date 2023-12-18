
# !/usr/bin/env python
# coding: utf-8
# Filename: newsapi_tools.py
# Path: plugins\_news_expert\newsapi_tools.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17

"""
Tools for interacting with NewsAPI.org

register for an API key @ https://newsapi.org/

"""
from typing import List
import aiohttp
from rich.console import Console

console = Console()


async def get_news_from_newsapi(url, api_key, **kwargs) -> List:
    """
    Fetch news from NewsAPI based on query parameters
    """
    query_params = kwargs
    query_params["apiKey"] = api_key

    # Debug print
    # console.print(f"Making request to NewsAPI with params: {query_params}")

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=query_params, timeout=5) as res:
                data = await res.json()
                # console.print(f"Received response from NewsAPI: {data}")
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
                    console.print(
                        f"NewsAPI.org returned an error: {error_message}"
                    )
                    return []
                else:
                    console.print(f"Error fetching news: Status {res.status}")
                    return []  # Return an empty list if the status is not 200
                return news

        except aiohttp.ServerTimeoutError as server_timeout_error:
            console.print(
                f"Server timeout error occurred: {server_timeout_error}"
            )
        except aiohttp.ClientConnectionError as connection_error:
            console.print(
                f"Connection error occurred: {connection_error}"
            )
        except aiohttp.ClientPayloadError as payload_error:
            console.print(
                f"Client payload error occurred: {payload_error}"
            )
        except aiohttp.ClientResponseError as response_error:
            console.print(
                f"Client response error occurred: {response_error}"
            )
        # Return an empty list in case of any exception
        return []


newsapi_tools = [
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
    },

]
