# !/usr/bin/env python
# coding: utf-8
# Filename: plugin_base.py
# Path: plugins/plugin_base.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/18

"""Base class for plugins."""


# plugin_base.py
class PluginBase:
    """
    Base class for plugins.
    """
    def __init__(self, **kwargs):
        self.tools = []
        self.__dict__.update(kwargs)

    async def initialize(self):
        """
        Initialize the plugin.
        """
        raise NotImplementedError

    def get_tools(self):
        """
        Get the tools.
        """
        return self.tools
