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


# Logging configuration
LOGGING_ENABLED = os.getenv('LOGGING_ENABLED', 'false').lower() == 'true'
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'WARNING')
LOGGING_FILE = os.getenv('LOGGING_FILE', None)
LOGGING_FORMAT = os.getenv(
    'LOGGING_FORMAT', '%(name)s - %(levelname)s - %(message)s'
)


MAIN_SYSTEM_PROMPT = os.getenv("MAIN_SYSTEM_PROMPT")

# OpenAI main API keys and variables here
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not set")

OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
if OPENAI_ORG_ID is None:
    raise ValueError("OPENAI_ORG_ID not set")

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
if OPENAI_MODEL is None:
    raise ValueError("OPENAI_MODEL not set")

OPENAI_TEMP = float(os.getenv("OPENAI_TEMP", str(0.5)))

OPENAI_TOP_P = float(os.getenv("OPENAI_TOP_P", str(0.5)))

OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", str(1500)))

MAIN_SYSTEM_PROMPT = os.getenv("MAIN_SYSTEM_PROMPT")

TTS_ENGINE = os.getenv("TTS_ENGINE")
if TTS_ENGINE is None:
    raise ValueError("TTS_ENGINE not set")

TTS_VOICE_ID = os.getenv("TTS_VOICE_ID")
if TTS_VOICE_ID is None:
    raise ValueError("TTS_VOICE_ID not set")

TTS_RATE = int(os.getenv("TTS_RATE", str(150)))
