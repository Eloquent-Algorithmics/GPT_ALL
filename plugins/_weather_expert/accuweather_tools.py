
# !/usr/bin/env python
# coding: utf-8
#
# Filename: accuweather_tools.py
# Path: plugins\_weather_expert\accuweather_tools.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17

"""
This file contains the AccuWeather tools.
"""

import os
import json
import aiohttp
import spacy
from rich.console import Console
from plugins.plugin_base import PluginBase

console = Console()

nlp = spacy.load("en_core_web_sm")


# AccuWeatherPlugin classS
class AccuWeatherPlugin(PluginBase):
    """
    This class defines the AccuWeather plugin.
    """

    def __init__(self):
        accuweather_api_key = os.getenv("ACCUWEATHER_API_KEY")
        if accuweather_api_key is None:
            raise ValueError("ACCUWEATHER_API_KEY not set")

        accuweather_base_url = os.getenv("ACCUWEATHER_BASE_URL")
        if accuweather_base_url is None:
            raise ValueError("ACCUWEATHER_BASE_URL not set")

        super().__init__(
            ACCUWEATHER_API_KEY=accuweather_api_key,
            ACCUWEATHER_BASE_URL=accuweather_base_url,
        )

        self.api_key = accuweather_api_key
        self.base_url = accuweather_base_url

    async def initialize(self):
        # Initialization code if needed
        pass

    def extract_location(self, user_input):
        """
        This function extracts the location from the user input.
        """
        doc = nlp(user_input)
        locations = [
            ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")
        ]
        return locations

    async def get_location_key(self, location_name):
        """
        This function gets the location key for the given location name.
        """
        url = f"{self.base_url}/locations/v1/cities/search"
        params = {"apikey": self.api_key, "q": location_name}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                locations = await response.json()
                if locations:
                    return locations[0]["Key"]
                else:
                    return None

    async def get_current_weather(self, location: str = "Atlanta"):
        """
        This function gets the current weather for the given location.

        If no location provided or an empty string passed, defaults to Atlanta.

        """

        # Check if the location is an empty string and set it to the default
        if not location:
            location = "Atlanta"

        location_key = await self.get_location_key(location)
        if not location_key:
            return json.dumps(
                {"error": "Failed to find location key for provided location"}
            )

        url = f"{self.base_url}/currentconditions/v1/{location_key}"
        params = {"apikey": self.api_key, "details": "true"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()
                    current_conditions = data[0]
                    weather_info = {
                        "weather_text": (current_conditions["WeatherText"]),
                        "temperature": (
                            current_conditions["Temperature"]["Imperial"]["Value"]
                        ),
                        "humidity": current_conditions["RelativeHumidity"],
                        "wind_speed": (
                            current_conditions["Wind"]["Speed"]["Imperial"]["Value"]
                        ),
                        "wind_direction": (
                            current_conditions["Wind"]["Direction"]["Localized"]
                        ),
                        "wind_direction_degrees": (
                            current_conditions["Wind"]["Direction"]["Degrees"]
                        ),
                        "uv_index": (current_conditions["UVIndex"]),
                        "cloud_cover": (current_conditions["CloudCover"]),
                        "pressure": (
                            current_conditions["Pressure"]["Imperial"]["Value"]
                        ),
                        "visibility": (
                            current_conditions["Visibility"]["Imperial"]["Value"]
                        ),
                        "precipitation": (
                            current_conditions["Precip1hr"]["Imperial"]["Value"]
                        ),
                        "observation_time": (
                            current_conditions["LocalObservationDateTime"]
                        ),
                    }
                    return json.dumps(weather_info)
            except aiohttp.ClientError as error:
                console.print(f"HTTP error occurred: {error}")
                return json.dumps({"error": "Failed to fetch weather data"})
            except ValueError as error:
                console.print(f"An error occurred: {error}")
                return json.dumps({"error": "An unexpected error occurred"})

    def get_tools(self):
        accu_weather_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "Get the current weather in a location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city, e.g. Atlanta.",
                            },
                        },
                        "required": ["location"],
                    },
                },
            },
        ]

        self.tools.extend(accu_weather_tools)

        available_functions = {
            "get_current_weather": self.get_current_weather,
        }

        return available_functions, self.tools
