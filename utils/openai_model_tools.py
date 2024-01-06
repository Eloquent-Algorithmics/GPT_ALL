
# !/usr/bin/env python
# coding: utf-8
# Filename: openai_model_tools.py
# Path: utils/openai_model_tools.py

"""
Core tools.

This file contains the core tools for the AI Assistant.
"""
import requests
import base64
import mimetypes
from openai import OpenAI, AsyncOpenAI
from rich.console import Console
from pathlib import Path
from plugins._gmail_plugin.drive_tools import (
    available_functions,
)
from 
from config import (
    OPENAI_API_KEY,
    OPENAI_ORG_ID,
)
console = Console()

api_key = OPENAI_API_KEY
openai_org_id = OPENAI_ORG_ID

# Create an OpenAI client instance using keyword arguments
gpt4_client = OpenAI(api_key=api_key, organization=openai_org_id, timeout=10)

# Create an AsyncOpenAI client instance using keyword arguments
gpt4_client_async = AsyncOpenAI(api_key=api_key, organization=openai_org_id, timeout=10)


def ask_chat_gpt_4_0314_synchronous(**kwargs) -> str:
    """
    Ask ChatGPT a question and return the response.

    Args:
        kwargs (dict): The keyword arguments to pass to the function.
    Returns:
        str: The response from ChatGPT.
    """

    question = kwargs.get("question", "")
    text = kwargs.get("text", "")

    messages = [
        {
            "role": "system",
            "content": "You are a specialized AI language model designed to act as an expert tool within a larger conversational system. Your role is to provide detailed and expert-level responses to queries directed to you by the controller AI. You should focus on delivering precise information and insights based on your specialized knowledge and capabilities. Your responses should be concise, relevant, and strictly within the scope of the expertise you represent. You are not responsible for maintaining the overall conversation with the end user, but rather for supporting the controller AI by processing and responding to specific requests for information or analysis. Adhere to the constraints provided by the controller, such as token limits and context relevance, and ensure that your contributions are well-reasoned and can be seamlessly integrated into the broader conversation managed by the controller AI.",
        },
        {"role": "user", "content": question},
        {"role": "assistant", "content": text},
    ]

    response = gpt4_client.chat.completions.create(
        model="gpt-4-0314",
        messages=messages,
        temperature=0,
        max_tokens=2048,
        top_p=0.3,
        frequency_penalty=0,
        presence_penalty=0,
    )

    if (
        response.choices
        and response.choices[0].message
        and response.choices[0].message.content
    ):
        return response.choices[0].message.content
    else:
        return "An error occurred or no content was returned."


async def ask_chat_gpt_4_0314_asynchronous(**kwargs) -> str:
    """
    Ask ChatGPT a question and return the response.

    Args:
        kwargs (dict): The keyword arguments to pass to the function.
    Returns:
        str: The response from ChatGPT.
    """

    question = kwargs.get("question", "")
    text = kwargs.get("text", "")

    messages = [
        {
            "role": "system",
            "content": "You are a specialized AI language model designed to act as an expert tool within a larger conversational system. Your role is to provide detailed and expert-level responses to queries directed to you by the controller AI. You should focus on delivering precise information and insights based on your specialized knowledge and capabilities. Your responses should be concise, relevant, and strictly within the scope of the expertise you represent. You are not responsible for maintaining the overall conversation with the end user, but rather for supporting the controller AI by processing and responding to specific requests for information or analysis. Adhere to the constraints provided by the controller, such as token limits and context relevance, and ensure that your contributions are well-reasoned and can be seamlessly integrated into the broader conversation managed by the controller AI.",
        },
        {"role": "user", "content": question},
        {"role": "assistant", "content": text},
    ]

    response = await gpt4_client_async.chat.completions.create(
        model="gpt-4-0314",
        messages=messages,
        temperature=0.2,
        max_tokens=2048,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
    )

    if (
        response.choices
        and response.choices[0].message
        and response.choices[0].message.content
    ):
        return response.choices[0].message.content
    else:
        return "An error occurred or no content was returned."


def ask_chat_gpt_4_0613_synchronous(**kwargs) -> str:
    """
    Ask ChatGPT a question and return the response.

    Args:
        kwargs (dict): The keyword arguments to pass to the function.
    Returns:
        str: The response from ChatGPT.
    """

    question = kwargs.get("question", "")
    text = kwargs.get("text", "")

    messages = [
        {
            "role": "system",
            "content": "You are a specialized AI language model designed to act as an expert tool within a larger conversational system. Your role is to provide detailed and expert-level responses to queries directed to you by the controller AI. You should focus on delivering precise information and insights based on your specialized knowledge and capabilities. Your responses should be concise, relevant, and strictly within the scope of the expertise you represent. You are not responsible for maintaining the overall conversation with the end user, but rather for supporting the controller AI by processing and responding to specific requests for information or analysis. Adhere to the constraints provided by the controller, such as token limits and context relevance, and ensure that your contributions are well-reasoned and can be seamlessly integrated into the broader conversation managed by the controller AI.",
        },
        {"role": "user", "content": question},
        {"role": "assistant", "content": text},
    ]

    response = gpt4_client.chat.completions.create(
        model="gpt-4-613",
        messages=messages,
        temperature=0.2,
        max_tokens=2048,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Check if the response has the expected structure and content
    if (
        response.choices
        and response.choices[0].message
        and response.choices[0].message.content
    ):
        return response.choices[0].message.content
    else:
        # Handle the case where the expected content is not available
        return "An error occurred or no content was returned."


async def ask_chat_gpt_4_0613_asynchronous(**kwargs) -> str:
    """
    Ask ChatGPT a question and return the response.

    Args:
        kwargs (dict): The keyword arguments to pass to the function.
    Returns:
        str: The response from ChatGPT.
    """

    question = kwargs.get("question", "")
    text = kwargs.get("text", "")

    messages = [
        {
            "role": "system",
            "content": "You are a specialized AI language model designed to act as an expert tool within a larger conversational system. Your role is to provide detailed and expert-level responses to queries directed to you by the controller AI. You should focus on delivering precise information and insights based on your specialized knowledge and capabilities. Your responses should be concise, relevant, and strictly within the scope of the expertise you represent. You are not responsible for maintaining the overall conversation with the end user, but rather for supporting the controller AI by processing and responding to specific requests for information or analysis. Adhere to the constraints provided by the controller, such as token limits and context relevance, and ensure that your contributions are well-reasoned and can be seamlessly integrated into the broader conversation managed by the controller AI.",
        },
        {"role": "user", "content": question},
        {"role": "assistant", "content": text},
    ]

    response = await gpt4_client_async.chat.completions.create(
        model="gpt-4-0613",
        messages=messages,
        temperature=0.2,
        max_tokens=2048,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
    )

    if (
        response.choices
        and response.choices[0].message
        and response.choices[0].message.content
    ):
        return response.choices[0].message.content
    else:
        return "An error occurred or no content was returned."


# Function to encode the image
def encode_image(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise ValueError("Could not determine the MIME type of the image.")
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

# Function to send the image to the vision model
async def ask_gpt_4_vision(image_name, drive_service=None):
    # Check if the image exists in the local uploads folder
    local_image_path = Path("uploads") / image_name
    if local_image_path.is_file():
        base64_image = encode_image(local_image_path)
    else:
        # If not found locally, search in Google Drive (if drive_service is provided)
        if drive_service:
            files_info = await available_functions["list_files"](drive_service, "MyDrive/GPT_ALL/uploads")
            file_id = next((f['id'] for f in files_info if f['name'] == image_name), None)
            if file_id:
                # Download the file from Google Drive
                local_image_path = await available_functions["download_file"](drive_service, file_id, "uploads/")
                base64_image = encode_image(local_image_path)
            else:
                return "Image not found in local uploads folder or Google Drive."
        else:
            return "Image not found in local uploads folder."

    # Send the request to the vision model
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "question"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": base64_image
                        }
                    }
                ]
            }
        ],
        "max_tokens": 600
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()
