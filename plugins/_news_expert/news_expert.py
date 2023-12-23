
# !/usr/bin/env python
# coding: utf-8
# Filename: news_expert.py
# Path: plugins\_news_expert\news_expert.py

"""
This contains the main module for the News Expert plugin.
"""
import os
import importlib.util
import inspect
from pathlib import Path
from plugins.plugin_base import PluginBase


def register_tools(cls):
    """
    Class decorator to register tools in the class attribute 'tools'.
    """
    for name, method in cls.__dict__.items():
        if callable(method) and hasattr(method, "tool_metadata"):
            cls.tools.append(method.tool_metadata)
    return cls


def register_tool(func):
    """
    Decorator to add tool metadata to the function.
    """
    func.tool_metadata = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": func.__annotations__,
            # Add more metadata if needed
        },
    }
    return func


class NewsExpertPlugin(PluginBase):
    """
    This class contains the main module for the News Expert plugin.
    """
    # Class attribute to hold tool definitions
    tools = []
    available_functions = {}

    def __init__(self):
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.newsapi_org_url = os.getenv("NEWSAPI_ORG_URL")
        self.nyt_api_key = os.getenv("NYT_API_KEY")
        self.nyt_article_search_url = os.getenv("NYT_ARTICLE_SEARCH_URL")

        if not all([self.news_api_key, self.newsapi_org_url, self.nyt_api_key, self.nyt_article_search_url]):
            raise ValueError("One or more required environment variables are not set")

        super().__init__()

    async def initialize(self):
        # Dynamically load tools from the scripts in the same directory
        plugin_dir = Path(__file__).parent
        for file_path in plugin_dir.glob('*.py'):
            if file_path.name != 'news_expert.py':  # Skip the main plugin script
                spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # Update available_functions with functions from the module
                for name, func in inspect.getmembers(module, inspect.isfunction):
                    if hasattr(func, 'tool_metadata'):
                        self.tools.append(func.tool_metadata)
                        self.available_functions[name] = func

    def get_tools(self):
        # Return the dynamically loaded tools
        return self.available_functions, self.tools

    async def news_anchor(self, query: str) -> str:
        """
        Fetch and summarize news articles from all available sources based on the user's query.
        """
        news_articles = []
        # Assume get_news_from_newsapi and get_news_from_nyt are loaded and available
        if 'get_news_from_newsapi' in self.available_functions:
            news_articles.extend(await self.available_functions['get_news_from_newsapi'](self.newsapi_org_url, self.news_api_key, q=query))
        if 'get_news_from_nyt' in self.available_functions:
            news_articles.extend(await self.available_functions['get_news_from_nyt'](query, self.nyt_article_search_url, self.nyt_api_key))

        # Summarize the articles (this is a placeholder, you'll need to implement the summarization logic)
        summary = "Summary of articles:\n" + "\n".join([article['title'] for article in news_articles])
        return summary


# Define the tool metadata for the news_anchor method
NewsExpertPlugin.news_anchor.tool_metadata = {
    "type": "function",
    "function": {
        "name": "news_anchor",
        "description": "Fetch and summarize news articles from all available sources based on the user's query.",
        "parameters": {
            "query": {
                "type": "string",
                "description": "The search query for news articles.",
            },
        },
    },
}

# Register the tools after defining all methods
NewsExpertPlugin = register_tools(NewsExpertPlugin)
