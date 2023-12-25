# Filename: my_tools.py
# Path: plugins/_my_plugin/my_tools.py

"""
Tools for interacting with an external API.
"""

import os
import logging
from typing import List
import aiohttp

# Define the default URL and API key as constants at the top of the file
TOOL_URL = os.getenv("MY_API_URL", "https://api.example.com/v1")
TOOL_API_KEY = os.getenv("MY_API_KEY")


async def get_data_from_my_api(url=TOOL_URL, api_key=TOOL_API_KEY, **kwargs) -> List:
    """
    Fetch data from the external API based on query parameters.
    """
    query_params = kwargs
    query_params["apiKey"] = api_key

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=query_params, timeout=5) as res:
                data = await res.json()
                items = []
                # Process the data and populate the items list
                # ...
                return items

        except aiohttp.ServerTimeoutError as server_timeout_error:
            logging.error(
                "Server timeout error occurred: %s",
                server_timeout_error
            )
        except aiohttp.ClientConnectionError as connection_error:
            logging.error(
                "Connection error occurred: %s",
                connection_error
            )
        except aiohttp.ClientPayloadError as payload_error:
            logging.error(
                "Client payload error occurred: %s",
                payload_error
            )
        except aiohttp.ClientResponseError as response_error:
            logging.error(
                "Client response error occurred: %s",
                response_error
            )
        # Return an empty list in case of any exception
        return []


my_tool_list = [
    {
        "type": "function",
        "function": {
            "name": "get_data_from_my_api",
            "description": "Get data from the external API function",
            "parameters": {
                "type": "object",
                "properties": {
                    # Define the parameters for your API function
                },
                "required": [],  # Specify required parameters if any
            },
        },
    }
]

available_functions = {
    "get_data_from_my_api": get_data_from_my_api,
}
