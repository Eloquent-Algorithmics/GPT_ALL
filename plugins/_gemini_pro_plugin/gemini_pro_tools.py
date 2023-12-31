
# !/usr/bin/env python
# coding: utf-8
# Filename: gemini_pro_tools.py
# Path: plugins/_gemini_pro_plugin/gemini_pro_tools.py

"""
This module defines the Gemini Pro Tools.
"""

import google.generativeai as genai

generation_config = {
    "temperature": 0.5,
    "top_p": 0.5,
    "top_k": 32,
    "max_output_tokens": 1024,
}

# Set the safety settings to block harmful content
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

# Create object for the Gemini Pro model
model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)


def ask_gemini_pro_synchronous(plugin_instance, question):
    """
    Ask Gemini Pro a question and get a response.

    This function is synchronous, meaning that it will block the
    main thread until the response is received.

    Args:
        plugin_instance (GeminiProPlugin): The Gemini Pro plugin instance.
        question (str): The question to ask Gemini Pro.

    Returns:
        str: The response from Gemini Pro.
    """
    # Create a conversation object
    convo = model.start_chat(history=[])

    # Ask the question and get the response
    convo.send_message(question)

    response_text = convo.last.text

    return response_text


async def ask_gemini_pro_asynchronous(plugin_instance, question):
    """
    Ask Gemini Pro a question and get a response.

    This function is asynchronous, meaning that it will not block the
    main thread while waiting for the response.

    """
    # Create a conversation object
    convo = model.start_chat(history=[])

    # Ask the question and get the response
    convo.send_message(question)

    response_text = convo.last.text

    return response_text


gemini_pro_tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_gemini_pro_synchronous",
            "description": "This function allows you to send a request to the Gemini Pro LLM (which can be used for natural language tasks, multi-turn text and code chat, code generation) synchronously and get a response you can you use later in your workflow.",
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
    {
        "type": "function",
        "function": {
            "name": "ask_gemini_pro_asynchronous",
            "description": "This function allows you to send a request to the Gemini Pro LLM (which can be used for natural language tasks, multi-turn text and code chat, code generation) asynchronously and get a response you can you use later in your workflow.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "The question to ask the Gemini Pro LLM.",
                    },
                },
                "required": ["question"],
            },
        },
    },
]

available_functions = {
    "ask_gemini_pro_synchronous": ask_gemini_pro_synchronous,
    "ask_gemini_pro_asynchronous": ask_gemini_pro_asynchronous,
}
