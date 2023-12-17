
# !/usr/bin/env python
# coding: utf-8
# Filename: gemini_pro_tools.py
# Path: plugins\_google_vertex\gemini_pro_tools.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17

"""
This file contains the code for the Gemini Pro Class.
"""

from vertexai.preview.generative_models import (
    GenerativeModel,
)
from plugins.plugin_base import PluginBase


# Define the Gemini Pro model
gemini_model = GenerativeModel("gemini-pro")
gemini_chat = gemini_model.start_chat(history=[])


class GeminiProPlugin(PluginBase):
    """
    This class defines the Gemini Pro plugin.
    """
    def __init__(self):
        super().__init__()

    async def initialize(self):
        # Initialization code if needed
        pass

    async def ask_gemini_pro(self, question):
        """
        Ask Gemini Pro a question and return the response using ChatSession.
        """
        # Send the message to the chat session and get the response
        response = gemini_chat.send_message(question)

        # Collect the response text
        response_text = ""
        for part in response.candidates[0].content.parts:
            response_text += part.text

        # Return the response text instead of printing it
        return response_text

    def get_tools(self):
        # Define the tool for ask_gemini_pro function
        ask_gemini_pro_tool = {
            "type": "function",
            "function": {
                "name": "ask_gemini_pro",
                "description": "Ask Gemini Pro a question and print the response.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The question to ask Gemini Pro.",
                        },
                    },
                    "required": ["question"],
                },
            },
        }
        self.tools.append(ask_gemini_pro_tool)

        # Add the ask_gemini_pro function to the available functions
        available_functions = {
            "ask_gemini_pro": self.ask_gemini_pro,
        }

        return available_functions, self.tools
