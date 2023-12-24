# Filename: my_plugin.py
# Path: plugins/_my_plugin/my_plugin.py

"""
This module defines the MyPlugin plugin.
"""
import os
import sys

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the directory to the Python path to ensure imports work
sys.path.insert(0, current_dir)

from my_tools import (
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

    def load_plugin_tools(self):
        """
        Load tools and functions from accompanying scripts.
        """
        # Load tools and functions from my_tools.py
        self.tools.extend(my_tool_list)
        self.available_functions.update(my_functions)
