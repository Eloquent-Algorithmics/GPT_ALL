
# !/usr/bin/env python
# coding: utf-8
# Filename: nytimes_tools.py
# Path: plugins\_news_expert\nytimes_tools.py

"""
This module contains functions to fetch
news articles from New York Times API based on a query.
"""
from typing import List
import aiohttp


async def get_news_from_nytimes(
        query: str,
        url: str,
        nyt_api_key: str
) -> List:
    """
    This function fetches news articles from New York Times based on a query.
    :param query: The search query for the New York Times API
    :param url: The URL for the New York Times API
    :param nyt_api_key: The API key for the New York Times API
    :return: A list of news articles
    """
    # Define the parameters for the request
    params = {
        "q": query,
        "api-key": nyt_api_key,
    }

    # Make the request to the New York Times API
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as res:
                res.raise_for_status()
                data = await res.json()
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
                return nyt_news
        except ValueError as error:
            print(f"Failed to fetch news from NYT: {error}")
            return []


# Define the tool metadata for this function
get_news_from_nytimes_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_news_from_nyt",
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
    },
]

# Define the available functions in this module
available_functions = {
    "get_news_from_nyt": get_news_from_nytimes,
}
