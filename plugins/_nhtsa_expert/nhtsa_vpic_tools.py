
# !/usr/bin/env python
# coding: utf-8
# Filename: nhtsa_vpic_expert.py
# Path: plugins/_nhtsa_vpic_expert/nhtsa_vpic_expert.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/20
"""
This module defines the NHTSA vPIC Expert plugin.
"""

import requests
from plugins.plugin_base import PluginBase


class NHTSAVPICPlugin(PluginBase):
    """
    This class defines the NHTSA vPIC Expert plugin.
    """

    def __init__(self):
        # Initialize the plugin
        self.nhtsa_vpic_url = "https://vpic.nhtsa.dot.gov/api/"
        super().__init__()

    async def initialize(self):
        """
        Initialize the plugin.

        """
        # pass

    async def get_vehicle_details(self, vin):
        """Retrieve vehicle details by VIN."""
        endpoint = f"{self.nhtsa_vpic_url}vehicles/decodevin/{vin}?format=json"
        response = requests.get(endpoint, timeout=5)
        data = response.json()
        return data['Results']

    def get_tools(self):
        nhtsa_vpic_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_vehicle_details",
                    "description": "Retrieve details of a vehicle by VIN.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "vin": {
                                "type": "string",
                                "description": "Vehicle Identification Number",
                            },
                        },
                        "required": ["vin"],
                    },
                },
            },
        ]

        self.tools.extend(nhtsa_vpic_tools)

        available_functions = {
            "get_vehicle_details": self.get_vehicle_details,
        }

        return available_functions, self.tools
