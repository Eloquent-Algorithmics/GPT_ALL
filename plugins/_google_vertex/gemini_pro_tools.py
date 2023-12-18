
# !/usr/bin/env python
# coding: utf-8
# Filename: gemini_pro_tools.py
# Path: plugins\_google_vertex\gemini_pro_tools.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17

"""
This file contains the code for the Gemini Pro Class.
"""

import os
import google.generativeai as genai
from plugins.plugin_base import PluginBase


# Configure the genai library with the API key from the .env file
api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    raise ValueError("GEMINI_API_KEY not set in the environment variables.")
genai.configure(api_key=api_key)

# Set up the model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
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


class GeminiProPlugin(PluginBase):
    """
    This class defines the Gemini Pro plugin.
    """

    def __init__(self):
        super().__init__()
        self.model = genai.GenerativeModel(model_name="gemini-pro",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)
        self.convo = self.model.start_chat(history=[])

    async def initialize(self):
        # If there's no initialization needed, you can simply pass
        pass

    async def ask_gemini_pro(self, question):
        """
        Ask Gemini Pro a question and return the response using ChatSession.
        """
        # Send the message to the chat session and get the response
        self.convo.send_message(question)
        response_text = self.convo.last.text

        # Return the response text instead of printing it
        return response_text

    def get_tools(self):
        # Define the tool for ask_gemini_pro function
        ask_gemini_pro_tool = {
            "type": "function",
            "function": {
                "name": "ask_gemini_pro",
                "description": "Ask Gemini Pro a question and print response.",
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
