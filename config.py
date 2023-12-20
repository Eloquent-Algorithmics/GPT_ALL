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
