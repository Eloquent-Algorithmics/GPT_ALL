
# !/usr/bin/env python
# coding: utf-8
# Filename: gemini_pro_base.py
# Path: plugins/_gemini_pro_plugin/gemini_pro_base.py

"""
This is the Gemini Pro Expert plugin.

This plugin is a wrapper around the Gemini Pro API.

"""

import os
import functools
import google.generativeai as genai
from plugins.plugin_base import PluginBase

from plugins._gemini_pro_plugin.gemini_pro_vision_tools import (
    gemini_pro_vision_tools,
    available_functions as gemini_pro_vision_functions
)
from plugins._gemini_pro_plugin.gemini_pro_tools import (
    gemini_pro_tools,
    available_functions as gemini_pro_functions
)


class GeminiProPlugin(PluginBase):
    """
    This is the Gemini Pro Expert plugin.

    This plugin is a wrapper around the Gemini Pro API.

    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key is None:
            raise ValueError("GEMINI_API_KEY not set in the .env file")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=self.default_generation_config(),
            safety_settings=self.default_safety_settings()
        )
        self.convo = self.model.start_chat(history=[])

        # Initialize the tools and available functions dictionaries
        self.tools = []
        self.available_functions = {}

        super().__init__()

    async def initialize(self):
        # Load tools and functions from gemini_pro_tools.py
        self.tools.extend(gemini_pro_tools)
        for func_name, func in gemini_pro_functions.items():
            # Bind the GeminiProPlugin instance to the function
            self.available_functions[func_name] = functools.partial(func, self)

        # Load tools and functions from gemini_pro_vision_tools.py
        self.tools.extend(gemini_pro_vision_tools)
        for func_name, func in gemini_pro_vision_functions.items():
            # Bind the GeminiProPlugin instance to the function
            self.available_functions[func_name] = functools.partial(func, self)

    def default_generation_config(self):
        """
        Returns the default generation config for the Gemini Pro API.

        This is the same as the default generation config for the
        Gemini Pro API, except that the max_output_tokens is set to 512
        instead of 256.
        """
        return {
            "temperature": 1,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 512,
        }

    def default_safety_settings(self):
        """
        Returns the default safety settings for the Gemini Pro API.

        This is the same as the default safety settings for the
        Gemini Pro API, except that the threshold for all categories
        is set to BLOCK_MEDIUM_AND_ABOVE instead of BLOCK_HIGH_AND_ABOVE.

        """
        return [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
