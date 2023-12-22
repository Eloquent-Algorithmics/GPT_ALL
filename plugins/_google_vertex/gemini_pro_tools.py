
# Filename: gemini_pro_tools.py
# Path: plugins\_google_vertex\gemini_pro_tools.py
"""
This module defines the Gemini Pro Tools.
"""
import os
import google.generativeai as genai
from plugins.plugin_base import PluginBase


class GeminiProToolsPlugin(PluginBase):
    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key is None:
            raise ValueError("GEMINI_API_KEY not set in the environment variables.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(model_name="gemini-pro", generation_config=self.default_generation_config(), safety_settings=self.default_safety_settings())
        self.convo = self.model.start_chat(history=[])

        super().__init__()

    async def initialize(self):
        pass

    def default_generation_config(self):
        return {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

    def default_safety_settings(self):
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

    async def ask_gemini_pro(self, question, generation_config=None, safety_settings=None):
        if generation_config is None:
            generation_config = self.default_generation_config()
        if safety_settings is None:
            safety_settings = self.default_safety_settings()
        self.model.configure(generation_config=generation_config, safety_settings=safety_settings)
        self.convo.send_message(question)
        response_text = self.convo.last.text
        return response_text

    def get_tools(self):
        gemini_pro_tools = [
            {
                "type": "function",
                "function": {
                    "name": "ask_gemini_pro",
                    "description": "Ask Gemini Pro a question and get a response.",
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
            },
        ]

        self.tools.extend(gemini_pro_tools)

        available_functions = {
            "ask_gemini_pro": self.ask_gemini_pro,
        }

        return available_functions, self.tools
