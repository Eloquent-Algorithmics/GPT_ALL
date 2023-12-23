# !/usr/bin/env python
# coding: utf-8
# Filename: news_expert.py
# Path: plugins\_news_expert\news_expert.py

"""
This contains the main module for the News Expert plugin.
"""
import os
import logging
import importlib.util
import inspect
from pathlib import Path
from plugins.plugin_base import PluginBase

# Configure logging to output to the console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def register_tools(cls):
    """
    Class decorator to register tools in the class attribute 'tools'.
    """
    logger.debug("Registering tools for class: %s", cls.__name__)
    for name, method in cls.__dict__.items():
        if callable(method) and hasattr(method, "tool_metadata"):
            cls.tools.append(method.tool_metadata)
            logger.debug("Registered tool: %s", name)
    return cls


def register_tool(func):
    """
    Decorator to add tool metadata to the function.
    """
    logger.debug("Registering tool: %s", func.__name__)
    func.tool_metadata = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__,
            "parameters": func.__annotations__,
            # Add more metadata if needed
        },
    }
    logger.debug("Registered tool metadata: %s", func.tool_metadata)
    return func


class NewsExpertPlugin(PluginBase):
    """
    This class contains the main module for the News Expert plugin.
    """
    # Class attribute to hold tool definitions
    tools = []
    available_functions = {}

    def __init__(self):
        logger.debug("Initializing NewsExpertPlugin")
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.newsapi_org_url = os.getenv("NEWSAPI_ORG_URL")
        self.nyt_api_key = os.getenv("NYT_API_KEY")
        self.nyt_article_search_url = os.getenv("NYT_ARTICLE_SEARCH_URL")

        if not all([self.news_api_key, self.newsapi_org_url, self.nyt_api_key, self.nyt_article_search_url]):
            logger.error("One or more required environment variables are not set")
            raise ValueError("One or more required environment variables are not set")

        super().__init__()

    async def initialize(self):
        logger.debug("Initializing tools for NewsExpertPlugin")
        # Dynamically load tools from the scripts in the same directory
        plugin_dir = Path(__file__).parent
        for file_path in plugin_dir.glob('*.py'):
            if file_path.name != 'news_expert.py':  # Skip the main plugin script
                logger.debug("Loading module from file: %s", file_path)
                spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                # Update available_functions with functions from the module
            for name, func in inspect.getmembers(module, inspect.isfunction):
                if hasattr(func, 'tool_metadata'):
                    self.tools.append(func.tool_metadata)  # Update the instance attribute
                    self.available_functions[name] = func
                    logger.debug("Loaded function: %s", name)

    def get_tools(self):
        # Return the dynamically loaded tools
        logger.debug("Returning available tools")
        return self.available_functions, self.tools

    @register_tool
    async def news_anchor(self, query: str) -> str:
        """
        Fetch and summarize news articles from all available sources based on the user's query.
        """
        logger.debug("Executing news_anchor with query: %s", query)
        news_articles = []
        # Assume get_news_from_newsapi and get_news_from_nyt are loaded and available
        if 'get_news_from_newsapi' in self.available_functions:
            logger.debug("Fetching news from newsapi.org")
            news_articles.extend(await self.available_functions['get_news_from_newsapi'](self.newsapi_org_url, self.news_api_key, q=query))
        if 'get_news_from_nyt' in self.available_functions:
            logger.debug("Fetching news from NYT")
            news_articles.extend(await self.available_functions['get_news_from_nyt'](query, self.nyt_article_search_url, self.nyt_api_key))

        # Summarize the gathered collection of articles
        summary = "Summary of articles:\n" + "\n".join([article['title'] for article in news_articles])
        logger.debug("Summary generated")
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

available_functions = {
    "news_anchor": NewsExpertPlugin.news_anchor
}

# Register the tools after defining all methods
NewsExpertPlugin = register_tools(NewsExpertPlugin)
logger.debug("Registered NewsExpertPlugin with tools")
