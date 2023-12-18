
# !/usr/bin/env python
# coding: utf-8
# Filename: news_expert.py
# Path: plugins\_news_expert\news_expert.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17

"""
This module defines the News Expert plugin.
"""

import os
from typing import List
from plugins.plugin_base import PluginBase


# Import the functions from the newsapi_tools and nytimes_tools modules
from plugins._news_expert.newsapi_tools import get_news_from_newsapi
from plugins._news_expert.nytimes_tools import get_news_from_nytimes


class NewsExpertPlugin(PluginBase):
    """
    This class defines the News Expert plugin.
    """

    def __init__(self):

        # Initialize the plugin
        self.NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        if self.NEWS_API_KEY is None:
            raise ValueError("NEWS_API_KEY not set")

        self.NEWSAPI_ORG_URL = os.getenv("NEWSAPI_ORG_URL")
        if self.NEWSAPI_ORG_URL is None:
            raise ValueError("NEWSAPI_ORG_URL not set")

        self.NYT_API_KEY = os.getenv("NYT_API_KEY")
        if self.NYT_API_KEY is None:
            raise ValueError("NYT_API_KEY not set")

        self.NYT_ARTICLE_SEARCH_URL = os.getenv("NYT_ARTICLE_SEARCH_URL")
        if self.NYT_ARTICLE_SEARCH_URL is None:
            raise ValueError("NYT_ARTICLE_SEARCH_URL not set")

        super().__init__()

    async def initialize(self):
        # Initialization code if needed
        pass

    async def get_all_news(self, **kwargs) -> List:
        
        query_params = kwargs

        newsapi_news = await get_news_from_newsapi(self.NEWSAPI_ORG_URL, self.NEWS_API_KEY, **query_params)
        nytimes_news = await get_news_from_nytimes(query_params["q"], self.NYT_API_KEY, self.NYT_ARTICLE_SEARCH_URL)

        return newsapi_news + nytimes_news

    def get_tools(self):
        news_anchor_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_all_news",
                    "description": "Aggregate news articles from NewsAPI.org and the New York Times API.",
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
                            "page": {
                                "type": "integer",
                                "description": "Page Number",
                                "default": 1,
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
            {
                "type": "function",
                "function": {
                    "name": "get_news_from_newsapi",
                    "description": "Fetch news articles from NewsAPI.org API based on a query.",
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
            {
                "type": "function",
                "function": {
                    "name": "get_news_from_nyt",
                    "description": "Fetch news from New York Times API based on a query.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query for the New York Times API.",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
        ]

        self.tools.extend(news_anchor_tools)

        available_functions = {
            "get_all_news": self.get_all_news,
            "get_news_from_newsapi": lambda **kwargs: get_news_from_newsapi(self.NEWSAPI_ORG_URL, self.NEWS_API_KEY, **kwargs),
            "get_news_from_nyt": lambda **kwargs: get_news_from_nytimes(kwargs["query"], self.NYT_API_KEY, self.NYT_ARTICLE_SEARCH_URL),
        }

        return available_functions, self.tools
