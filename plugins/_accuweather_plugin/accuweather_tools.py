
# !/usr/bin/env python
# coding: utf-8
# Filename: accuweather_tools.py
# Path: plugins/_accuweather_plugin/accuweather_tools.py

"""
This file contains the AccuWeather plugins functions and tools.

The free AccuWeather API key is limited to 50 calls per day and is limited to
5 days of Daily Forecasts, 12 hours of Hourly Forecasts, and 5 days of Indices.

See https://developer.accuweather.com/ for more information.

"""

import json
import aiohttp
import spacy

nlp = spacy.load("en_core_web_md")


def extract_location(user_input):
    """
    This function extracts the location from the user input.

    It uses the spaCy library to extract the location from the user input.

    """
    doc = nlp(user_input)
    locations = [
        ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")
    ]
    return locations


async def get_location_key(api_key, base_url, location_name):
    """
    This function gets the location key for the given location name.

    If no location provided or an empty string passed, defaults to Atlanta.

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
    params = {"apikey": api_key, "details": "true", "metric": "false"}
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
                    "humidity": (
                        current_conditions["RelativeHumidity"]
                    ),
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
            return json.dumps({error, "Failed to fetch weather data"})
        except ValueError as error:
            return json.dumps({error, "An unexpected error occurred"})


async def get_one_hour_weather_forecast(api_key, base_url, location: str = "Atlanta"):
    """
    This function gets the hourly forecast weather for the given location.

    If no location provided or an empty string passed, defaults to Atlanta.
    """

    if not location:
        location = "Atlanta"

    location = location.strip('"')

    location_key = await get_location_key(api_key, base_url, location)
    if not location_key:
        return json.dumps(
            {"error": "Failed to find location key for provided location"}
        )

    url = f"{base_url}/forecasts/v1/hourly/1hour/{location_key}"
    params = {"apikey": api_key, "details": "true", "metric": "false"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                forecast = data[0] if data and isinstance(data, list) else {}
                weather_info = {
                    "DateTime": forecast.get("DateTime"),
                    "WeatherIcon": forecast.get("WeatherIcon"),
                    "IconPhrase": forecast.get("IconPhrase"),
                    "HasPrecipitation": forecast.get("HasPrecipitation"),
                    "PrecipitationType": forecast.get("PrecipitationType"),
                    "PrecipitationIntensity": forecast.get("PrecipitationIntensity"),
                    "IsDaylight": forecast.get("IsDaylight"),
                    "Temperature": forecast.get("Temperature"),
                    "RealFeelTemperature": forecast.get("RealFeelTemperature"),
                    "RealFeelTemperatureShade": forecast.get("RealFeelTemperatureShade"),
                    "WetBulbTemperature": forecast.get("WetBulbTemperature"),
                    "WetBulbGlobeTemperature": forecast.get("WetBulbGlobeTemperature"),
                    "DewPoint": forecast.get("DewPoint"),
                    "Wind": forecast.get("Wind"),
                    "WindGust": forecast.get("WindGust"),
                    "RelativeHumidity": forecast.get("RelativeHumidity"),
                    "Visibility": forecast.get("Visibility"),
                    "Ceiling": forecast.get("Ceiling"),
                    "UVIndex": forecast.get("UVIndex"),
                    "UVIndexText": forecast.get("UVIndexText"),
                    "PrecipitationProbability": forecast.get("PrecipitationProbability"),
                    "RainProbability": forecast.get("RainProbability"),
                    "SnowProbability": forecast.get("SnowProbability"),
                    "IceProbability": forecast.get("IceProbability"),
                    "TotalLiquid": forecast.get("TotalLiquid"),
                    "Rain": forecast.get("Rain"),
                    "Snow": forecast.get("Snow"),
                    "Ice": forecast.get("Ice"),
                    "CloudCover": forecast.get("CloudCover"),
                    "Evapotranspiration": forecast.get("Evapotranspiration"),
                    "SolarIrradiance": forecast.get("SolarIrradiance"),
                }
                return json.dumps(weather_info)

        except aiohttp.ClientError as e:
            return json.dumps({"error": str(e)})
        except ValueError as error:
            return json.dumps({error, "An unexpected error occurred"})


async def get_twelve_hour_weather_forecast(api_key, base_url, location: str = "Atlanta"):
    """
    This function gets the twelve hour hourly forecast weather for the given location.

    If no location provided or an empty string passed, defaults to Atlanta.

    """
    if not location:
        location = "Atlanta"

    location = location.strip('"')

    location_key = await get_location_key(api_key, base_url, location)
    if not location_key:
        return json.dumps(
            {"error": "Failed to find location key for provided location"}
        )

    url = f"{base_url}/forecasts/v1/hourly/12hour/{location_key}"
    params = {"apikey": api_key, "details": "true", "metric": "false"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                if not data or not isinstance(data, list):
                    return json.dumps(
                        {"error": "Invalid forecast data format"}
                    )
                # Process each forecast in the list
                forecasts_info = []
                for forecast in data:
                    weather_info = {
                        "DateTime": forecast.get("DateTime"),
                        "WeatherIcon": forecast.get("WeatherIcon"),
                        "IconPhrase": forecast.get("IconPhrase"),
                        "HasPrecipitation": forecast.get("HasPrecipitation"),
                        "IsDaylight": forecast.get("IsDaylight"),
                        "Temperature": forecast.get("Temperature"),
                        "RealFeelTemperature": forecast.get("RealFeelTemperature"),
                        "RealFeelTemperatureShade": forecast.get("RealFeelTemperatureShade"),
                        "WetBulbTemperature": forecast.get("WetBulbTemperature"),
                        "WetBulbGlobeTemperature": forecast.get("WetBulbGlobeTemperature"),
                        "DewPoint": forecast.get("DewPoint"),
                        "Wind": forecast.get("Wind"),
                        "WindGust": forecast.get("WindGust"),
                        "RelativeHumidity": forecast.get("RelativeHumidity"),
                        "Visibility": forecast.get("Visibility"),
                        "Ceiling": forecast.get("Ceiling"),
                        "UVIndex": forecast.get("UVIndex"),
                        "UVIndexText": forecast.get("UVIndexText"),
                        "PrecipitationProbability": forecast.get("PrecipitationProbability"),
                        "RainProbability": forecast.get("RainProbability"),
                        "SnowProbability": forecast.get("SnowProbability"),
                        "IceProbability": forecast.get("IceProbability"),
                        "TotalLiquid": forecast.get("TotalLiquid"),
                        "Rain": forecast.get("Rain"),
                        "Snow": forecast.get("Snow"),
                        "Ice": forecast.get("Ice"),
                        "CloudCover": forecast.get("CloudCover"),
                        "Evapotranspiration": forecast.get("Evapotranspiration"),
                        "SolarIrradiance": forecast.get("SolarIrradiance"),
                    }
                    forecasts_info.append(weather_info)

                return json.dumps(forecasts_info)

        except aiohttp.ClientError as error:
            return json.dumps({error,"Failed to fetch weather data"})
        except ValueError as error:
            return json.dumps({error, "An unexpected error occurred"})


async def get_one_day_weather_forecast(api_key, base_url, location: str = "Atlanta"):
    """
    This function gets the one day forecast weather for the given location.

    If no location provided or an empty string passed, defaults to Atlanta.

    """
    if not location:
        location = "Atlanta"

    location = location.strip('"')

    location_key = await get_location_key(api_key, base_url, location)
    if not location_key:
        return json.dumps(
            {"error": "Failed to find location key for provided location"}
        )

    url = f"{base_url}/forecasts/v1/daily/1day/{location_key}"
    params = {"apikey": api_key, "details": "true", "metric": "false"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                weather_info = {
                    "Headline": data.get("Headline", {}),
                    "DailyForecasts": data.get("DailyForecasts", [])
                }
                return json.dumps(weather_info)

        except aiohttp.ClientError as error:
            return json.dumps({error, "Failed to fetch weather data"})
        except ValueError as error:
            return json.dumps({error, "An unexpected error occurred"})


async def get_five_day_weather_forecast(api_key, base_url, location: str = "Atlanta"):
    """
    This function gets the five day forecast weather for the given location.

    If no location provided or an empty string passed, defaults to Atlanta.

    """
    if not location:
        location = "Atlanta"

    location = location.strip('"')

    location_key = await get_location_key(api_key, base_url, location)
    if not location_key:
        return json.dumps(
            {"error": "Failed to find location key for provided location"}
        )

    url = f"{base_url}/forecasts/v1/daily/5day/{location_key}"
    params = {"apikey": api_key, "details": "true", "metric": "false"}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                weather_info = {
                    "Headline": data.get("Headline", {}),
                    "DailyForecasts": data.get("DailyForecasts", [])
                }
                return json.dumps(weather_info)

        except aiohttp.ClientError as error:
            return json.dumps({error, "Failed to fetch weather data"})
        except ValueError as error:
            return json.dumps({error, "An unexpected error occurred"})


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
        {
            "type": "function",
            "function": {
                "name": "get_one_day_weather_forecast",
                "description": "Get the 1 day forecast weather by City.",
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
        {
            "type": "function",
            "function": {
                "name": "get_five_day_weather_forecast",
                "description": "Get the 5 day forecast weather by City.",
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
        {
            "type": "function",
            "function": {
                "name": "get_one_hour_weather_forecast",
                "description": "Get the 1 hour forecast weather by City.",
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
        {
            "type": "function",
            "function": {
                "name": "get_twelve_hour_weather_forecast",
                "description": "Get the 12 hour forecast weather by City.",
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
    "get_one_hour_weather_forecast": get_one_hour_weather_forecast,
    "get_twelve_hour_weather_forecast": get_twelve_hour_weather_forecast,
    "get_one_day_weather_forecast": get_one_day_weather_forecast,
    "get_five_day_weather_forecast": get_five_day_weather_forecast,
}
