
# !/usr/bin/env python
# coding: utf-8
# Filename: nhtsa_vpic_base.py
# Path: plugins/_nhtsa_plugin/nhtsa_vic_base.py

"""
This module defines the NHTSA vPic Vehicle Data plugin.
"""

from plugins._nhtsa_plugin.nhtsa_vpic_tools import (
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
