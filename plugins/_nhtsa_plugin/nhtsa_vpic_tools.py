
# !/usr/bin/env python
# coding: utf-8
# Filename: nhtsa_vpic_tools.py
# Path: plugins/_nhtsa_plugin/nhtsa_vpic_tools.py

"""
This module defines the NHTSA vPIC VIN tools.
"""

import requests

def get_vehicle_details_by_vin_synchronous(vin):
    """Retrieve vehicle details by VIN."""
    endpoint = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
    response = requests.get(endpoint, timeout=5)
    data = response.json()
    return data['Results']


async def get_vehicle_details_by_vin_asynchronous(vin):
    """Retrieve vehicle details by VIN."""
    endpoint = f"https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/{vin}?format=json"
    response = requests.get(endpoint, timeout=5)
    data = response.json()
    return data['Results']


nhtsa_vpic_tool_list = [
    {
        "type": "function",
        "function": {
            "name": "get_vehicle_details_by_vin_synchronous",
            "description": "This function allows you to retrieve details of a vehicle by VIN from the NHTSA vPic API synchronously.",
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
    {
        "type": "function",
        "function": {
            "name": "get_vehicle_details_by_vin_asynchronous",
            "description": "This function allows you to retrieve details of a vehicle by VIN from the NHTSA vPic API asynchronously.",
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
    "get_vehicle_details_by_vin_synchronous": get_vehicle_details_by_vin_synchronous,
    "get_vehicle_details_by_vin_asynchronous": get_vehicle_details_by_vin_asynchronous,
}
