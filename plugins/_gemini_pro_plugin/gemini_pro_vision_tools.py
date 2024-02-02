
# !/usr/bin/env python
# coding: utf-8
# Filename: gemini_pro_tools.py
# Path: plugins/_gemini_pro_plugin/gemini_pro_vision_tools.py

"""
This module defines the Gemini Pro Vision Tools.
"""

import os 
import google.generativeai as genai
from vertexai.preview.generative_models import Image

SOURCE_FOLDER = "uploads"


async def ask_gemini_pro_vision(self, question, specific_file_name) -> Image:
    """
    Ask Gemini Pro Vision a question about a specific image file.

    Args:
        question: The question to ask.
        specific_file_name: The name of the image file.
    """
    try:

        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 1024,
        }

        try:
            image_path = os.path.join(SOURCE_FOLDER, specific_file_name)

            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()

        except FileNotFoundError:

            return "File not found."

        except PermissionError:

            return "Permission denied."

        except TypeError:

            return "Error reading the file."

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

        try:
            model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)

        except TypeError:

            return "Error creating the model."

        except ValueError:

            return "Error creating the model."

        try:
            responses = model.generate_content(
                [image_bytes, question],
                stream=False,
            )
        except FileNotFoundError:

            return "File not found."

        except PermissionError:

            return "Permission denied."

        except TypeError:

            return "Error reading the file."

        except ValueError:

            return "Error creating the model."

        try:
            for response in responses:
                if response.candidates:
                    return response.candidates[0].content.parts[0].text
                else:
                    return "No response candidates found."

        except FileNotFoundError:

            return "File not found."
        except PermissionError:

            return "Permission denied."
        except TypeError:

            return "Error reading the file."
        except ValueError:

            return "Error creating the model."

    except FileNotFoundError:
        return "File not found."
    except PermissionError:
        return "Permission denied."
    except TypeError:

        return "Error reading the file."
    except ValueError:
        return "Error creating the model."


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
                        "description": "The question to ask Gemini Pro Vision",
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
