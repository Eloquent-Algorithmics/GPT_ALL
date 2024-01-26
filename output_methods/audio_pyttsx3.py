
# !/usr/bin/env python
# coding: utf-8
# Filename: audio_pyttsx3.py
# File Path: output/audio_pyttsx3.py

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
import websockets
import base64
import asyncio

# Import ElevenLabs functions
from elevenlabs import generate, play, set_api_key, get_api_key, stream

# Load environment variables from .env file
load_dotenv()

# Set the ElevenLabs API key if it exists in the environment
ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
if ELEVEN_API_KEY:
    set_api_key(ELEVEN_API_KEY)
TTS_ENGINE = os.getenv('TTS_ENGINE')


def tts_output(text):
    """
    This function outputs the given text as speech.

    Args:
        text (str): The text to output.
    """
    if TTS_ENGINE == "pyttsx3":
        tts_output_pyttsx3(text)
    elif TTS_ENGINE == "elevenlabs" and ELEVEN_API_KEY:
        # Since tts_output_elevenlabs is an async function, we need to run it with asyncio.run
        asyncio.run(tts_output_elevenlabs(text))
    else:
        raise ValueError(f"Invalid TTS_ENGINE value or missing ElevenLabs API key: {TTS_ENGINE}")


async def stream_elevenlabs(audio_stream):
    """Stream audio data using pygame player."""
    initialize_audio()
    async for chunk in audio_stream:
        if chunk:
            play_audio(chunk)


async def text_to_speech_input_streaming(voice_id, text_iterator):
    """Send text to ElevenLabs API and stream the returned audio."""
    uri = f"wss://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream-input?model_id=eleven_monolingual_v1"

    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "text": " ",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8},
            "xi_api_key": ELEVEN_API_KEY,
        }))

        async def listen():
            """Listen to the websocket for audio data and stream it."""
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    if data.get("audio"):
                        yield base64.b64decode(data["audio"])
                    elif data.get('isFinal'):
                        break
                except websockets.exceptions.ConnectionClosed as e:
                    print(f"Connection closed with error: {e}")
                    break
                except websockets.exceptions.ConnectionClosedOK:
                    print("Connection closed without error.")
                    break

        listen_task = asyncio.create_task(stream_elevenlabs(listen()))

        async for text in text_iterator:
            await websocket.send(json.dumps({"text": text, "try_trigger_generation": True}))

        await websocket.send(json.dumps({"text": ""}))

        await listen_task


def tts_output_elevenlabs(text):
    """
    This function outputs the given text as speech using ElevenLabs API with streaming.

    Args:
        text (str): The text to output.
    """
    async def text_iterator():
        yield text

    asyncio.run(text_to_speech_input_streaming(ELEVENLABS_VOICE, text_iterator()))


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
