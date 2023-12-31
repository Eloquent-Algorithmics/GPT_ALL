
# !/usr/bin/env python
# coding: utf-8
# Filename: system_commands_base.py
# Path: plugins/_system_commands/system_commands_base.py

"""
This file contains the System Commands plugin class.
"""

from plugins._system_commands.system_commands_tools import (
    system_commands_tool_list,
    available_functions as system_commands_functions
)
from plugins.plugin_base import PluginBase


class SystemCommandsPlugin(PluginBase):
    """
    This class defines the System Commands plugin.
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
        # Load tools and functions from system_commands_tools.py
        self.tools.extend(system_commands_tool_list)
        self.available_functions.update(system_commands_functions)
