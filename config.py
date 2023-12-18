"""
This module loads environment variables from the .env file.
"""
import os
from dotenv import load_dotenv
from rich.live import Live
from rich.spinner import Spinner

# Load the .env file

load_dotenv()

# Define the live_spinner
live_spinner = Live(Spinner("aesthetic", " "), auto_refresh=True)


# Enable/disable tools
ENABLE_OPENAI_TOOLS = os.getenv(
    "ENABLE_OPENAI_TOOLS",
    "false"
).lower() == "true"

ENABLE_GOOGLE_SEARCH_TOOLS = os.getenv(
    "ENABLE_GOOGLE_SEARCH_TOOLS",
    "false"
).lower() == "true"

ENABLE_ASK_GPT_4_0314 = os.getenv(
    "ENABLE_ASK_GPT_4_0314",
    "false"
).lower() == "true"


# Add your API keys and variables here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not set")

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
if OPENAI_MODEL is None:
    raise ValueError("OPENAI_MODEL not set")

# Convert temperature and top_p to float
OPENAI_TEMP = float(os.getenv("OPENAI_TEMP", str(0.5)))

OPENAI_TOP_P = float(os.getenv("OPENAI_TOP_P", str(0.5)))

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY not set")

GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")
if GOOGLE_API_KEY is None or GOOGLE_CSE_ID is None:
    raise ValueError("GOOGLE_API_KEY and GOOGLE_CSE_ID not set")

TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")
TTS_VOICE_ID = os.getenv("TTS_VOICE_ID")
TTS_RATE = os.getenv("TTS_RATE")
