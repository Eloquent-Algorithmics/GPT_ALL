# Filename: gemini_pro_vision_tools.py
# Path: plugins\_google_vertex\gemini_pro_vision_tools.py
"""
This module defines the Gemini Pro Vision Tools.
"""
import os
import base64
import google.generativeai as genai
from vertexai.preview.generative_models import (
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)
from plugins.plugin_base import PluginBase


class GeminiProVisionToolsPlugin(PluginBase):
    """
    This class defines the Gemini Pro Vision Tools plugin.
    """
    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key is None:
            raise ValueError("GEMINI_API_KEY not set in the .env variables.")

        genai.configure(api_key=self.api_key)

        super().__init__()

    async def initialize(self):
        pass

    async def ask_gemini_pro_vision(self, question, source_folder, specific_file_name):
        """
        Ask Gemini Pro Vision a question about a specific image file.

        Args:
            question: The question to ask.
            source_folder: The folder containing the image file.
            specific_file_name: The name of the image file.
        """
        # Set up the generation configuration
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }

        # Read the image file as bytes and encode it with base64
        image_path = os.path.join(source_folder, specific_file_name)

        # Read the image file as bytes and encode it with base64
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')

        # Create a Part object with the image data
        image_part = Part.from_data(data=encoded_image, mime_type="image/jpeg")

        # Set the safety settings to block harmful content
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH:
                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT:
                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
                HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        # Create a GenerativeModel object for the Gemini Pro Vision model
        model = genai.GenerativeModel(model_name="gemini-pro-vision",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

        # Make the request and stream the responses
        responses = model.generate_content(
            [image_part, question],
            stream=False,
        )
        for response in responses:
            if response.candidates:
                return response.candidates[0].content.parts[0].text
            else:
                return "No response candidates found."

    # Populate the tools list with the tools from this plugin
    def get_tools(self):

        gemini_pro_vision_tools = [
            {
                "type": "function",
                "function": {
                    "name": "ask_gemini_pro_vision",
                    "description": "Ask Gemini Pro Vision a question about a specific image or video file located in the 'uploads' folder.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "The question to ask Gemini Pro Vision model.",
                            },
                            "specific_file_name": {
                                "type": "string",
                                "description": "The name of the image or video file in the 'uploads' folder.",
                            },
                        },
                        "required": ["question", "specific_file_name"],
                    },
                },
            },
        ]

        self.tools.extend(gemini_pro_vision_tools)

        available_functions = {
            "ask_gemini_pro_vision": self.ask_gemini_pro_vision,
        }

        return available_functions, self.tools
