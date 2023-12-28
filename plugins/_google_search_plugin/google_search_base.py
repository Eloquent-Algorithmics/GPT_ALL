
# !/usr/bin/env python
# coding: utf-8
# Filename: google_search_base.py
# Path: plugins/_google_search_plugin/google_search_base.py

"""
This module defines the Google Search plugin.
"""

import logging
from plugins.plugin_base import PluginBase

from plugins._google_search_plugin.google_search_tools import (
    search_google_tools,
    available_functions as google_functions
)


# Create the GoogleSearchPlugin class
class GoogleSearchPlugin(PluginBase):
    """
    This class defines the Google Search plugin.
    """

    def __init__(self):
        super().__init__()
        # Define a logger for this plugin
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    async def initialize(self):
        """
        Initialize the plugin.
        """
        self.load_plugin_tools()

    def load_plugin_tools(self):
        """
        Load tools and functions from accompanying scripts.
        """
        # Load tools and functions from google_search_tools.py
        self.tools.extend(search_google_tools)
        self.available_functions.update(google_functions)
