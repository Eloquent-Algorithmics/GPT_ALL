
# !/usr/bin/env python
# coding: utf-8
# Filename: core_tools.py
# Path: utils/core_tools.py

"""
Core tools.

This file contains the core tools for the AI Assistant.
"""

from openai import OpenAI, AsyncOpenAI
from rich.console import Console
from config import (
    live_spinner,
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

    with live_spinner:
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

    with live_spinner:
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

    with live_spinner:
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
