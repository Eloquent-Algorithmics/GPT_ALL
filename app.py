
# !/usr/bin/env python
# coding: utf-8
# Filename: app.py
# Run command: python -m app

"""
This is the main part of the script
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import json
import asyncio
import argparse
import threading
from moviepy.editor import VideoFileClip
from openai import AsyncOpenAI
import pytz
import tzlocal
import tiktoken
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from output_methods.audio_pyttsx3 import tts_output
from plugins.plugins_enabled import enable_plugins
from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_TEMP,
    OPENAI_TOP_P,
    MAIN_SYSTEM_PROMPT,
    LOGGING_ENABLED,
    LOGGING_LEVEL,
    LOGGING_FILE,
    LOGGING_FORMAT,
    live_spinner,
)

sys.path.append(str(Path(__file__).parent))

# Define the rich console
console = Console()

# Define the OpenAI API clients
openai_model = OPENAI_MODEL
base_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
gpt4_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Define the default OpenAI parameters
openai_defaults = {
    "model": OPENAI_MODEL,
    "temperature": OPENAI_TEMP,
    "top_p": OPENAI_TOP_P,
    "max_tokens": 1500,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

# Configure logging based on the settings from .env
if LOGGING_ENABLED:
    # Set the logging level based on the LOGGING_LEVEL string
    level = getattr(logging, LOGGING_LEVEL.upper(), logging.WARNING)
    # Configure logging with or without a log file
    if LOGGING_FILE:
        logging.basicConfig(level=level, format=LOGGING_FORMAT, filename=LOGGING_FILE)
    else:
        logging.basicConfig(level=level, format=LOGGING_FORMAT)
else:
    logging.disable(logging.CRITICAL)


def play_video(video_path):
    """
    This function plays a intro video in a separate thread.

    Args:
        video_path (str): The path to the video file.
    """
    def video_player(path):
        clip = VideoFileClip(path)
        clip.preview()
        clip.close()

    # Create a thread to play the video
    video_thread = threading.Thread(target=video_player, args=(video_path,))
    video_thread.start()


async def get_current_date_time() -> str:
    """
    Get the current UTC date and time.

    Returns:
        str: The current UTC date and time.
    """
    local_timezone = tzlocal.get_localzone()
    now = datetime.now(local_timezone)
    now_est = now.astimezone(pytz.timezone("US/Eastern"))
    return now_est.strftime(
        "The current date and time is %B %d, %Y, %I:%M %p EST."
    )


async def ask_chat_gpt_4_0314(**kwargs) -> str:
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
        {"role": "system", "content": "You are an AI Assistant...", },
        {"role": "user", "content": question},
        {"role": "assistant", "content": text},
    ]

    with live_spinner:
        response = await gpt4_client.chat.completions.create(
            model="gpt-4-0314",
            messages=messages,
            temperature=0,
            max_tokens=1500,
            top_p=0.3,
            frequency_penalty=0,
            presence_penalty=0,
        )

    # Check if the response has the expected structure and content
    if (response.choices and
            response.choices[0].message and
            response.choices[0].message.content):
        return response.choices[0].message.content
    else:
        # Handle the case where the expected content is not available
        return "An error occurred or no content was returned."


def join_messages(memory: list[dict]):
    """
    This function joins messages for conversation memory.
    """
    text = ""
    for m in memory:
        content = m.get("content")
        if content is not None:
            text += content + "\n"
    return text


def check_under_context_limit(text: str, limit: int, model: str):
    """
    This function checks if the context is under the token limit.
    """
    enc = tiktoken.encoding_for_model(model)
    numtokens = len(enc.encode(text))
    return numtokens <= limit


async def follow_conversation(
        user_text: str,
        memory: list[dict],
        mem_size: int,
        model: str
):
    """
    This function follows the conversation.
    """
    ind = min(mem_size, len(memory))
    if ind == 0:
        memory = [{"role": "system", "content": MAIN_SYSTEM_PROMPT}]
    memory.append({"role": "user", "content": user_text})
    while not check_under_context_limit(
        join_messages(memory),
        128000,
        model
    ) and ind > 1:
        ind -= 1
        memory.pop(0)  # Remove the oldest messages if the limit is exceeded
    response = await base_client.chat.completions.create(
        model=model,
        messages=memory[-ind:]
    )
    # Check if the response has the expected structure and content
    if (response.choices and
            response.choices[0].message and
            response.choices[0].message.content is not None):
        tr = response.choices[0].message.content
        memory.append(
            {
                "role": "assistant",
                "content": tr
            }
        )
    else:
        # Handle the case where the expected content is not available
        memory.append(
            {
                "role": "assistant",
                "content": "I'm not sure how to respond to that."
            }
        )

    return memory


def display_help(tools):
    """
    Display the available tools.
    """
    console.print("\n[bold]Available Tools:[/bold]\n", style="bold blue")
    for tool in tools:
        if isinstance(tool, dict) and "function" in tool:
            function_info = tool["function"]
            name = function_info.get("name", "Unnamed")
            description = function_info.get("description", "No description available.")
            console.print(f"[bold]{name}[/bold]: {description}")
        else:
            console.print(f"Invalid tool format: {tool}")


async def run_conversation(
    messages,
    tools,
    available_functions,
    original_user_input,
    memory,
    mem_size,
    **kwargs
):
    """
    Run the conversation.
    """
    memory = await follow_conversation(
        user_text=original_user_input,
        memory=memory,
        mem_size=mem_size,
        model=openai_defaults["model"]
    )
    memory.append({"role": "user", "content": original_user_input})

    while len(json.dumps(memory)) > 128000:
        memory.pop(0)

    response = await base_client.chat.completions.create(
        model=openai_defaults["model"],
        messages=memory[-mem_size:],
        tools=tools,
        tool_choice="auto",
        temperature=openai_defaults["temperature"],
        top_p=openai_defaults["top_p"],
        max_tokens=openai_defaults["max_tokens"],
        frequency_penalty=openai_defaults["frequency_penalty"],
        presence_penalty=openai_defaults["presence_penalty"],
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls if hasattr(
        response_message,
        'tool_calls'
    ) else []

    if response_message.content is not None:
        memory.append(
            {
                "role": "assistant",
                "content": response_message.content
            }
        )

    if tool_calls:
        messages.append(response_message)
        executed_tool_call_ids = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name

            if function_name not in available_functions:
                console.print(
                    f"Function {function_name} is not available.",
                    style="red"
                )
                continue

            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            logging.info(
                "Calling function: %s args: %s",
                function_name,
                function_args,
                extra={"style": "purple"},
            )
            function_response = await function_to_call(**function_args)
            logging.info(
                "Function %s returned: %s\n",
                function_name,
                function_response,
                extra={"style": "orange"},
            )

            if function_response is None:
                function_response = "No response received from the function."
            elif not isinstance(function_response, str):
                function_response = json.dumps(function_response)

            function_response_message = {
                "role": "tool",
                "name": function_name,
                "content": function_response,
                "tool_call_id": tool_call.id,
            }

            messages.append(function_response_message)
            executed_tool_call_ids.append(tool_call.id)

        # Ensure the next message prompts the assistant to use tool responses
        messages.append(
            {
                "role": "user",
                "content": f"With the data returned from the tool calls, generate the second response to the original request that was: {original_user_input}, that makes use of the tool responses.",
            }
        )

        # Create next completion ensuring to pass the updated messages array
        second_response = await base_client.chat.completions.create(
            model=openai_defaults["model"],
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=openai_defaults["temperature"],
            top_p=openai_defaults["top_p"],
            max_tokens=openai_defaults["max_tokens"],
            frequency_penalty=openai_defaults["frequency_penalty"],
            presence_penalty=openai_defaults["presence_penalty"],
        )
        return second_response, memory
    else:
        return response, memory


async def main():
    """
    Main function.
    """
    os.system("cls" if os.name == "nt" else "clear")

    parser = argparse.ArgumentParser(
        description='KitchenSinkGPT - A GPT-4-turbo based Mixture of Experts AI Assistant'
    )
    parser.add_argument(
        '--talk', action='store_true', help='Use TTS for the final response'
    )
    parser.add_argument(
        '--intro', action='store_true', help='Play an intro video at startup'
    )
    args = parser.parse_args()

    use_tts = args.talk

    if args.intro:
        play_video('intro_video.mp4')

    console.print(
        Markdown(
            "# 👋  KitchenSinkGPT 👋"
        ),
        style="bold blue"
    )

    # Initialize available base functions and tools
    available_functions = {
        "get_current_date_time": get_current_date_time,
        "ask_chat_gpt_4_0314": ask_chat_gpt_4_0314,
        # Add more core functions here
    }

    # Define the available core tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_date_time",
                "description": "Get the current date and time.",
            },
        },
        {
            "type": "function",
            "function": {
                "name": "ask_chat_gpt_4_0314",
                "description": "Ask a smarter AI LLM that is able to understand more complex concepts and perform complex tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "temperature": {
                            "type": "integer",
                            "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                        },
                        "question": {
                            "type": "string",
                            "description": "What's requested to be done with the text.",
                        },
                        "text": {
                            "type": "string",
                            "description": "The text to be analyzed",
                        },
                    },
                    "required": ["question", "text"],
                },
            },
        },
    ]

    # Use the load_plugins_and_get_tools function to conditionally add tools
    available_functions, tools = await enable_plugins(
        available_functions,
        tools
    )

    # Initialize the conversation memory
    memory = []

    # Main Loop
    while True:

        # Ask the user for input
        user_input = Prompt.ask(
            "\nHow can I be of assistance? ([yellow]/tools[/yellow] or [bold yellow]exit or quit[/bold yellow])",
        )

        # Check if the user wants to exit the program
        if user_input.lower() == "exit":
            console.print("\nExiting the program.", style="bold red")
            break

        # Check if the user wants to see the available tools
        elif user_input.lower() == "/tools":
            display_help(tools)
            continue

        # Prepare the conversation messages
        messages = [
            {
                "role": "system",
                "content": MAIN_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"{user_input}"
            },
        ]

        # Start the spinner
        with live_spinner:

            # Start the spinner
            live_spinner.start()

            # Pass the user input and memory to the run_conversation function
            final_response, memory = await run_conversation(
                messages=messages,
                tools=tools,
                available_functions=available_functions,
                original_user_input=user_input,
                mem_size=10,
                memory=memory,  # Pass the memory variable
            )

            # Stop the spinner
            live_spinner.stop()

        # Print the final response from the model or use TTS
        if final_response:
            final_text = final_response.choices[0].message.content
            if use_tts:
                # Use TTS to output the final response
                console.print("\n" + final_text, style="green")
                tts_output(final_text)
            else:
                # Print the final response to the console
                console.print("\n" + final_text, style="green")
        else:
            # Print an error message if the model did not return a response
            console.print(
                "\nI'm not sure how to help with that.",
                style="red"
            )

        # Remove tools from the tools list after processing
        tools[:] = [
            tool for tool in tools
            if not tool.get("function", {}).get("name", "").lower()
            in user_input.lower()
        ]


if __name__ == "__main__":
    asyncio.run(
        main()
    )
