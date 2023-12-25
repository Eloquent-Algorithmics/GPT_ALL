
# !/usr/bin/env python
# coding: utf-8
# Filename: nhtsa_vpic_tools.py
# Path: plugins/_nhtsa_plugin/nhtsa_vpic_tools.py

"""
This module defines the NHTSA vPIC VIN tools.
"""

import requests


async def get_vehicle_details(vin):
    """Retrieve vehicle details by VIN."""
    endpoint = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
    response = requests.get(endpoint, timeout=5)
    data = response.json()
    return data['Results']


nhtsa_vpic_tool_list = [
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


available_functions = {
    "get_vehicle_details": get_vehicle_details,
}
