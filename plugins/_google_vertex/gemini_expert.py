# Filename: gemini_pro_expert.py
# Path: plugins\_google_vertex\gemini_pro_expert.py
"""
This is the Gemini Pro Expert plugin.
"""
import os
import google.generativeai as genai
from plugins._google_vertex.gemini_pro_tools import GeminiProToolsPlugin
from plugins._google_vertex.gemini_pro_vision_tools import GeminiProVisionToolsPlugin
from plugins.plugin_base import PluginBase


class GeminiProExpertPlugin(PluginBase):

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key is None:
            raise ValueError("GEMINI_API_KEY not set in the environment variables.")

        genai.configure(api_key=self.api_key)

        self.model = genai.GenerativeModel(model_name="gemini-pro", generation_config=self.default_generation_config(), safety_settings=self.default_safety_settings())
        self.convo = self.model.start_chat(history=[])

        super().__init__()

    async def initialize(self):
        await self.gemini_pro_tools_plugin.initialize()
        await self.gemini_pro_vision_tools_plugin.initialize()

    async def handle_request(self, request):
        if 'image' in request:
            # Assuming 'image' in the request is the path to the image file
            # and 'question' is the question related to the image.
            source_folder, specific_file_name = os.path.split(request['image'])
            return await self.gemini_pro_vision_tools_plugin.ask_gemini_pro_vision(request['question'], source_folder, specific_file_name)
        else:
            return await self.gemini_pro_tools_plugin.ask_gemini_pro(request['question'])

    def get_tools(self):
        gemini_pro_tools = self.gemini_pro_tools_plugin.get_tools()
        gemini_pro_vision_tools = self.gemini_pro_vision_tools_plugin.get_tools()
        return gemini_pro_tools + gemini_pro_vision_tools

    def default_generation_config(self):
        return {
            "temperature": 1,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 512,
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

    async def ask_gemini_pro_expert(self, question, generation_config=None, safety_settings=None):

        if generation_config is None:
            generation_config = self.default_generation_config()
        if safety_settings is None:
            safety_settings = self.default_safety_settings()
        self.convo.send_message(question)
        response_text = self.convo.last.text
        return response_text

    def get_tools(self):

        gemini_pro_tools = self.gemini_pro_tools_plugin.get_tools()
        gemini_pro_vision_tools = self.gemini_pro_vision_tools_plugin.get_tools()

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "ask_gemini_pro_expert",
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
                    "returns": {
                        "type": "string",
                        "description": "The response from Gemini Pro.",
                    },
                },
            },
        ]

        self.tools.extend(tools)

        available_functions = {
            "ask_gemini_pro_expert": self.ask_gemini_pro_expert,
        }

        return available_functions, self.tools
