
# !/usr/bin/env python
# coding: utf-8
# Filename: by_voice.py
# File Path: _input\by_voice.py
# Last modified by: ExplorerGT92
# Last modified on: 2023/12/17
# branch: voice_rec_and_tts

"""
This module is responsible for handling voice commands using speech recognition
and spacy.
"""

import spacy
import speech_recognition as sr


from output.audio_pyttsx3 import tts_output


nlp = spacy.load("en_core_web_md")


def get_similarity_score(text1, text2):
    """
    Compute the similarity score between two texts using spacy nlp pipeline.

    Args:
        text1 (str): The first text to compare.
        text2 (str): The second text to compare.

    Returns:
        float: The similarity score between the two texts.
    """
    logging.debug("Computing similarity score between '%s' and '%s'", text1, text2)
    doc1 = nlp(text1)
    doc2 = nlp(text2)
    score = doc1.similarity(doc2)
    logging.debug("Similarity score: %s", score)
    return score


def recognize_command(text, commands):
    """
    Recognizes a command from the given text.

    Args:
        text (str): The input text to recognize the command from.
        commands (list): A list of available commands.

    Returns:
        str: The recognized command if found, otherwise None.
    """
    if text is None:
        return None

    max_similarity = 0
    best_match = None

    for command in commands:
        similarity = get_similarity_score(text.lower(), command)

        if similarity > max_similarity:
            max_similarity = similarity
            best_match = command

    if max_similarity > 0.7:  # You can adjust this threshold
        logging.debug("Recognized command: %s", best_match)
        return best_match
    else:
        return None


def get_user_input():
    """
    Prompts the user to choose between typing or speaking a command.

    Returns:
        str: The user's command.
    """
    # print("Please enter a command or type 'speak' to use voice recognition:")
    user_input = input()
    logging.debug("User input: %s", user_input)
    if user_input.lower() == "speak":
        return recognize_speech()
    else:
        return user_input


def recognize_speech():
    """
    Recognizes speech using the default microphone as the audio source.

    Returns:
        str: The recognized text if successful, otherwise None.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=30, phrase_time_limit=30)
        except sr.WaitTimeoutError:
            print("Timeout: No speech detected")
            return None
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as request_error:
        print(f"Could not request results; {request_error}")
        return None
