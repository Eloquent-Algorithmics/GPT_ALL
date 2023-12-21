
# !/usr/bin/env python
# coding: utf-8
# Filename: news_expert.py
# Path: plugins\_news_expert\news_expert.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/20

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
        self.news_api_key = os.getenv("NEWS_API_KEY")
        if self.news_api_key is None:
            raise ValueError("NEWS_API_KEY not set")

        self.newsapi_org_url = os.getenv("NEWSAPI_ORG_URL")
        if self.newsapi_org_url is None:
            raise ValueError("NEWSAPI_ORG_URL not set")

        self.nyt_api_key = os.getenv("NYT_API_KEY")
        if self.nyt_api_key is None:
            raise ValueError("NYT_API_KEY not set")

        self.nyt_article_search_url = os.getenv("NYT_ARTICLE_SEARCH_URL")
        if self.nyt_article_search_url is None:
            raise ValueError("NYT_ARTICLE_SEARCH_URL not set")

        super().__init__()

    async def initialize(self):
        # Initialization code if needed
        pass

    async def get_all_news(self, **kwargs) -> List:
        """
        Returns news articles from NewsAPI.org and the New York Times API.

        """

        query_params = kwargs

        newsapi_news = await get_news_from_newsapi(
            self.newsapi_org_url, self.news_api_key, **query_params
        )
        nytimes_news = await get_news_from_nytimes(
            query_params["q"], self.nyt_article_search_url, self.nyt_api_key
        )

        return newsapi_news + nytimes_news

    def get_tools(self):
        news_anchor_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_all_news",
                    "description": "Aggregate news articles from NewsAPI.org and NYTimes.",
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
                                "description": "Date of oldest article.",
                            },
                            "to": {
                                "type": "string",
                                "description": "Today's date.",
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
                    "description": "Fetch news articles from NewsAPI.org API.",
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
                                "description": "Date of oldest article.",
                            },
                            "to": {
                                "type": "string",
                                "description": "Todays date.",
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
                    "description": "Fetch news from New York Times API.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Query for New York Times.",
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
            "get_news_from_newsapi": lambda **kwargs: get_news_from_newsapi(
                self.newsapi_org_url, self.news_api_key, **kwargs
            ),
            "get_news_from_nyt": lambda **kwargs: get_news_from_nytimes(
                kwargs["query"], self.nyt_api_key, self.nyt_article_search_url
            ),
        }

        return available_functions, self.tools
