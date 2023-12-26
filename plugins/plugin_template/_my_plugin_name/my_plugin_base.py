
# !/usr/bin/env python
# coding: utf-8
# Filename: my_plugin_base.py
# Path: plugins/template/_my_plugin/my_plugin.py

"""
This script defines any shared aspects of this tool class.
"""

from plugins.plugin_template._my_plugin_name.my_plugin_tools import (
    my_tool_list,
    available_functions as my_functions
)
from plugins.plugin_base import PluginBase


class MyPlugin(PluginBase):
    """
    This class defines the MyPlugin plugin.
    """
    async def initialize(self):
        """
        Initialize the plugin.
        """
        self.load_plugin_tools()

    async def load_plugin_tools(self):
        """
        Load tools and functions from accompanying scripts.
        """
        # Load tools and functions from my_tools.py
        self.tools.extend(my_tool_list)
        self.available_functions.update(my_functions)
