# !/usr/bin/env python
# coding: utf-8
# Filename: accuweather_tools.py
# Path: plugins/_accuweather_plugin/accuweather_tools.py

"""
This file contains the AccuWeather tools.
"""

import logging
import json
import aiohttp
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_location(user_input):
    """
    This function extracts the location from the user input.
    """
    doc = nlp(user_input)
    locations = [
        ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")
    ]
    return locations


async def get_location_key(api_key, base_url, location_name):
    """
    This function gets the location key for the given location name.
    """
    url = f"{base_url}/locations/v1/cities/search"
    params = {"apikey": api_key, "q": location_name}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            response.raise_for_status()
            locations = await response.json()
            if locations:
                return locations[0]["Key"]
            else:
                return None


async def get_current_weather(api_key, base_url, location: str = "Atlanta"):
    """
    This function gets the current weather for the given location.

    If no location provided or an empty string passed, defaults to Atlanta.
    """

    # Check if the location is an empty string and set it to the default
    if not location:
        location = "Atlanta"

    # Strip any extra quotes from the location string
    location = location.strip('"')

    location_key = await get_location_key(api_key, base_url, location)
    if not location_key:
        return json.dumps(
            {"error": "Failed to find location key for provided location"}
        )

    url = f"{base_url}/currentconditions/v1/{location_key}"
    params = {"apikey": api_key, "details": "true"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                current_conditions = data[0]
                weather_info = {
                    "weather_text": (
                        current_conditions["WeatherText"]
                    ),
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
                    "uv_index": (
                        current_conditions["UVIndex"]
                    ),
                    "cloud_cover": (
                        current_conditions["CloudCover"]
                    ),
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
            logging.error("HTTP error occurred: %s", error)
            return json.dumps({"error": "Failed to fetch weather data"})
        except ValueError as error:
            logging.error("An error occurred: %s", error)
            return json.dumps({"error": "An unexpected error occurred"})


accu_weather_tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather by City.",
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

available_functions = {
    "get_current_weather": get_current_weather,
}
