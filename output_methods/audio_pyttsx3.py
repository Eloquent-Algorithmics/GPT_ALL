
# !/usr/bin/env python
# coding: utf-8
# Filename: audio_pyttsx3.py
# File Path: output\audio_pyttsx3.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17
# branch: voice_rec_and_tts

"""
This module is responsible for handling audio output.

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
from typing import Union
from io import BytesIO
import pyttsx3
import pygame
from dotenv import load_dotenv
from config import TTS_ENGINE, TTS_VOICE_ID, TTS_RATE, ELEVENLABS_VOICE

# Import ElevenLabs functions
from elevenlabs import generate, play, set_api_key, get_api_key, stream

# Load environment variables from .env file
load_dotenv()

# Set the ElevenLabs API key if it exists in the environment
ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
if ELEVEN_API_KEY:
    set_api_key(ELEVEN_API_KEY)

# Other functions remain unchanged...

def tts_output(text):
    """
    This function outputs the given text as speech.

    Args:
        text (str): The text to output.
    """

    if TTS_ENGINE == "pyttsx3":
        tts_output_pyttsx3(text)
    elif TTS_ENGINE == "elevenlabs" and ELEVEN_API_KEY:
        tts_output_elevenlabs(text)
    else:
        raise ValueError(f"Invalid TTS_ENGINE value or missing ElevenLabs API key: {TTS_ENGINE}")


def tts_output_elevenlabs(text):
    """
    This function outputs the given text as speech using ElevenLabs API.

    Args:
        text (str): The text to output.
    """
    # Generate audio using ElevenLabs API
    audio_bytes = generate(
        text=text,
        voice=ELEVENLABS_VOICE,  # Replace with the desired voice
        model="eleven_multilingual_v2",
        stream=False,  # Set to True if you want to stream the audio
        output_format="mp3_44100_128"
    )

    # Play the generated audio
    play(audio=audio_bytes)


def initialize_audio():
    """
    This function initializes the audio system.
    """
    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.mixer.init()


def play_audio(audio: Union[bytes, BytesIO]):
    """
    This function plays the given audio.

    Args:
        audio (bytes or BytesIO): The audio to play.
    """

    if not isinstance(audio, (bytes, BytesIO)):
        return
    if isinstance(audio, bytes):
        audio = BytesIO(audio)

    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(10)


def tts_output_pyttsx3(text):

    """
    This function outputs the given text as speech using pyttsx3.

    Args:
        text (str): The text to output.
    """

    engine = pyttsx3.init('sapi5')

    voices = engine.getProperty('voices')

    if TTS_VOICE_ID:
        for voice in voices:
            if voice.name == TTS_VOICE_ID:
                engine.setProperty('voice', voice.id)
                break
    else:
        print("TTS_VOICE_ID not set, using default voice")

    engine.setProperty('rate', TTS_RATE)

    engine.say(text)
    engine.runAndWait()
