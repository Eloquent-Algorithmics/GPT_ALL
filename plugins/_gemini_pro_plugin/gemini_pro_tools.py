
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
model = genai.GenerativeModel(model_name="gemini-pro",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)


def ask_gemini_pro_synchronous(plugin_instance, question):
    """
    Ask Gemini Pro a question and get a response.
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
            "description": "This function allows you to ask the Gemini Pro LLM a question synchronously and get a response synchronously.",
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
            "description": "This function allows you to ask the Gemini Pro LLM a question asynchronously and get a response asynchronously.",
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
