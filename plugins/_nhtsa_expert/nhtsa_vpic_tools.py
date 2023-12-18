# Filename: nhtsa_vpic_expert.py
# Path: plugins/_nhtsa_vpic_expert/nhtsa_vpic_expert.py

"""
This module defines the NHTSA vPIC Expert plugin.
"""

import os
import requests
from typing import List
from plugins.plugin_base import PluginBase


class NHTSAVPICPlugin(PluginBase):
    """
    This class defines the NHTSA vPIC Expert plugin.
    """

    def __init__(self):
        # Initialize the plugin
        self.NHTSA_VPIC_URL = "https://vpic.nhtsa.dot.gov/api/"
        super().__init__()

    async def initialize(self):
        """
        Initialize the plugin.
        This method can be used to perform any setup operations required by the plugin.
        If no initialization is needed, you can simply pass or provide a basic implementation.
        """
        pass  # If no initialization is needed, otherwise add initialization code here.

    async def get_vehicle_types(self):
        """Retrieve the list of vehicle types."""
        endpoint = f"{self.NHTSA_VPIC_URL}vehicles/GetVehicleTypesForMake/honda?format=json"
        response = requests.get(endpoint)
        data = response.json()
        return data['Results']

    async def get_vehicle_details(self, vin):
        """Retrieve vehicle details by VIN."""
        endpoint = f"{self.NHTSA_VPIC_URL}vehicles/decodevin/{vin}?format=json"
        response = requests.get(endpoint)
        data = response.json()
        return data['Results']

    def get_tools(self):
        nhtsa_vpic_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_vehicle_types",
                    "description": "Retrieve the list of vehicle types.",
                },
            },
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
            "get_vehicle_types": self.get_vehicle_types,
            "get_vehicle_details": self.get_vehicle_details,
        }

        return available_functions, self.tools
