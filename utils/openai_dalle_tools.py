
# !/usr/bin/env python
# coding: utf-8
# Filename: openai_dalle_tools.py
# Path: utils/openai_dalle_tools.py

"""
This file contains the OpenAi Dall-e tools for the AI Assistant.
"""

from openai import OpenAI, AsyncOpenAI
from config import (
    OPENAI_API_KEY,
    OPENAI_ORG_ID
)

api_key = OPENAI_API_KEY
openai_org_id = OPENAI_ORG_ID

# Create an OpenAI client instance using keyword arguments
client = OpenAI(api_key=api_key, organization=openai_org_id, timeout=60)

# Create an AsyncOpenAI client instance using keyword arguments
client_async = AsyncOpenAI(api_key=api_key, organization=openai_org_id, timeout=60)


async def generate_an_image_with_dalle3(**kwargs) -> str:
    """
    Generate an image with DALL-E 3.
    """
    prompt = kwargs.get("prompt", "")
    n = kwargs.get("n", 1)
    size = kwargs.get("size", "1024x1024")
    quality = kwargs.get("quality", "hd")
    style = kwargs.get("style", "natural")
    response_format = kwargs.get("response_format", "url")

    response = await client_async.images.generate(
        model="dall-e-3",  # The model identifier
        prompt=prompt,  # Prompt required for image generation 4000 characters max
        n=n,  # Must be between 1 and 10
        size=size,  # 1024x1024, 1792x1024, or 1024x1792 dall-e-3 model
        quality=quality,  # hd or standard
        style=style,  # natural or vivid
        response_format=response_format,  # b64_json or url
    )
    await client_async.close()
    return response.data[0].url
