
# !/usr/bin/env python
# coding: utf-8
# Filename: accuweather_base.py
# Path: plugins/_accuweather_plugin/accuweather_base.py

"""
This is the Accuweather plugin Base class.
"""

import os
import functools
from plugins.plugin_base import PluginBase
from plugins._accuweather_plugin.accuweather_tools import (
    accu_weather_tools,
    available_functions as accuweather_functions,
)


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

        super().__init__()

        self.api_key = accuweather_api_key
        self.base_url = accuweather_base_url

    async def initialize(self):
        await self.load_plugin_tools()

    async def load_plugin_tools(self):
        """
        Load tools and functions from accompanying scripts.
        """
        self.tools.extend(accu_weather_tools)
        for func_name, func in accuweather_functions.items():
            # Bind the AccuWeather API key and base URL to the functions
            self.available_functions[func_name] = functools.partial(
                func,
                api_key=self.api_key,
                base_url=self.base_url
            )
