
# !/usr/bin/env python
# coding: utf-8
# Filename: nhtsa_vic_expert.py
# Path: plugins\_nhtsa_expert\nhtsa_vic_expert.py

"""
This module defines the NHTSA vPic Vehicle Data plugin.
"""
import os
import sys
# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the directory to the Python path to ensure imports work
sys.path.insert(0, current_dir)

from nhtsa_vpic_tools import (
    nhtsa_vpic_tool_list,
    available_functions as nhtsa_vpic_functions
)
from plugins.plugin_base import PluginBase


class NHTSAVPICPlugin(PluginBase):
    """
    This class defines the NHTSA vPic Vehicle Data plugin.
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
        # Load tools and functions from nhtsa_vpic_tools.py
        self.tools.extend(nhtsa_vpic_tool_list)
        self.available_functions.update(nhtsa_vpic_functions)
