
# !/usr/bin/env python
# coding: utf-8
# Filename: config.py
# Path: /config.py

"""
This module loads environment variables from the .env file.

The .env file is not included in the repository for security reasons.
"""

import os
from dotenv import load_dotenv
from rich.live import Live
from rich.spinner import Spinner

# Load the .env file
load_dotenv()

# Define the live_spinner
live_spinner = Live(Spinner("pong", " "), auto_refresh=True)

# Main app system prompt.
MAIN_SYSTEM_PROMPT = os.getenv("MAIN_SYSTEM_PROMPT")

# Main app OpenAI API key.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not set")

# Main app OpenAI organization ID.
OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
if OPENAI_ORG_ID is None:
    raise ValueError("OPENAI_ORG_ID not set")

# Main app OpenAI model ID.
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
if OPENAI_MODEL is None:
    raise ValueError("OPENAI_MODEL not set")

# Main app OpenAI Temperature.
OPENAI_TEMP = float(os.getenv("OPENAI_TEMP", str(0.5)))

# Main app OpenAI Top P.
OPENAI_TOP_P = float(os.getenv("OPENAI_TOP_P", str(0.5)))

# Main app OpenAI MAX Response token limit.
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", str(1500)))

# Configures the main app to use the local system TTS engine.
TTS_ENGINE = os.getenv("TTS_ENGINE")
if TTS_ENGINE is None:
    raise ValueError("TTS_ENGINE not set")

# Configures the main app to use the local system TTS voice ID.
TTS_VOICE_ID = os.getenv("TTS_VOICE_ID")
if TTS_VOICE_ID is None:
    raise ValueError("TTS_VOICE_ID not set")

# Configures the main app to use the local system TTS rate.
TTS_RATE = int(os.getenv("TTS_RATE", str(150)))

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE = os.getenv("ELEVENLABS_VOICE", "Rachel")
