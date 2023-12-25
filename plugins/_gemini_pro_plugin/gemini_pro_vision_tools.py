# !/usr/bin/env python
# coding: utf-8
# Filename: gemini_pro_tools.py
# Path: plugins/_gemini_pro_vision_plugin/gemini_pro_vision_tools.py
"""
This module defines the Gemini Pro Vision Tools.
"""
import os
import logging
import base64
import google.generativeai as genai
from vertexai.preview.generative_models import Part, Image

source_folder = "uploads"


async def ask_gemini_pro_vision(self, question, specific_file_name) -> Image:
    """
    Ask Gemini Pro Vision a question about a specific image file.

    Args:
        question: The question to ask.
        specific_file_name: The name of the image file.
    """
    try:
        logging.debug(f"Received question: {question}, for file: {specific_file_name}")

        # Set up the generation configuration
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }

        # Read the image file as bytes and encode it with base64
        try:
            image_path = os.path.join(source_folder, specific_file_name)
            logging.debug(f"Reading image from path: {image_path}")

            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
        except FileNotFoundError:
            logging.error(f"File not found: {image_path}")
            return "File not found."
        except PermissionError:
            logging.error(f"Permission denied when accessing the file: {image_path}")
            return "Permission denied."
        except Exception as e:
            logging.error(f"An unexpected error occurred while reading the file: {e}")
            return "Error reading the file."

        try:
            return Image.from_bytes(image_bytes)

        logging.debug(f"Encoded image data: {encoded_image[:100]}...")

        # Retu

        # Set the safety settings to block harmful content
        safety_settings = [
            # ... (safety settings as before)
        ]

        # Create a GenerativeModel object for the Gemini Pro Vision model
        try:
            model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)
        except Exception as e:
            logging.error(f"Error creating the GenerativeModel object: {e}")
            return "Error creating the model."

        # Make the request and stream the responses
        try:
            responses = model.generate_content(
                [image_part, question],
                stream=False,
            )

        except Exception as e:
            logging.error(f"An unexpected error occurred during the request: {e}")
            return "Error during the request."

        # Process the response
        try:
            for response in responses:
                if response.candidates:
                    return response.candidates[0].content.parts[0].text
                else:
                    return "No response candidates found."
        except Exception as e:
            logging.error(f"Error processing the response: {e}")
            return "Error processing the response."

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."


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

available_functions = {
    "ask_gemini_pro_vision": ask_gemini_pro_vision,
}
