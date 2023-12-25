# !/usr/bin/env python
# coding: utf-8
# Filename: plugin_base.py
# Path: plugins/plugin_base.py

"""
Base class for the plugins.
"""


class PluginBase:
    """
    Plugin Base Class.
    """
    def __init__(self, **kwargs):
        self.tools = []
        self.available_functions = {}
        self.__dict__.update(kwargs)

    async def initialize(self):
        """
        Initialize the plugin.
        """
        raise NotImplementedError

    def load_plugin_tools(self):
        """
        Load tools and functions from accompanying scripts.
        """
        raise NotImplementedError

    def get_tools(self):
        """
        Get the tools.
        """
        return self.tools

    def get_available_functions(self):
        """
        Get the available functions.
        """
        return self.available_functions
