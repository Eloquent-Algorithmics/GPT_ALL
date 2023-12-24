
# !/usr/bin/env python
# coding: utf-8
# Filename: news_expert.py
# Path: plugins/_news_expert/news_expert.py

"""
This module defines the News Expert plugin.
"""
import os
import sys
# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the directory to the Python path to ensure imports work
sys.path.insert(0, current_dir)

from newsapi_tools import (
    newsorg_tool_list,
    available_functions as newsapi_functions
)
from nytimes_tools import (
    nytimes_tool_list,
    available_functions as nytimes_functions
)

from plugins.plugin_base import PluginBase


class NewsExpertPlugin(PluginBase):
    """
    This class defines the News Expert plugin.
    """
    async def initialize(self):
        """
        Initialize the plugin.
        """
        self.load_plugin_tools()

    def load_plugin_tools(self):
        """
        Load tools and functions from accompanying scripts.
        """
        # Load tools and functions from newsapi_tools.py
        self.tools.extend(newsorg_tool_list)
        self.available_functions.update(newsapi_functions)

        # Load tools and functions from nytimes_tools.py
        self.tools.extend(nytimes_tool_list)
        self.available_functions.update(nytimes_functions)
