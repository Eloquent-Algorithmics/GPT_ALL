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
        logging.basicConfig(
            level=level,
            format=LOGGING_FORMAT,
            filename=LOGGING_FILE
        )
        logging.getLogger('httpcore.http11').setLevel(logging.INFO)
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.WARNING)
        logging.getLogger('httpcore').setLevel(logging.WARNING)
        logging.getLogger('markdown_it.rules_block').setLevel(logging.WARNING)
    else:
        logging.basicConfig(level=level, format=LOGGING_FORMAT)
else:
    logging.disable(logging.CRITICAL)


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
        {
            "role": "system",
            "content": "You are an AI Assistant...",
        },
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
    if (
        response.choices
        and response.choices[0].message
        and response.choices[0].message.content
    ):
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
    user_text: str, memory: list[dict], mem_size: int, model: str
):
    logging.info('Starting conversation with user input line 167: %s', user_text)

    ind = min(mem_size, len(memory))
    if ind == 0:
        memory = [{"role": "system", "content": MAIN_SYSTEM_PROMPT}]
    memory.append({"role": "user", "content": user_text})
    while (
        not check_under_context_limit(
            join_messages(memory),
            128000,
            model
        ) and ind > 1
    ):
        ind -= 1
        memory.pop(0)  # Removes the oldest messages if the limit is exceeded
        logging.debug('Removed oldest message due to context limit')

    response = await base_client.chat.completions.create(
        model=model, messages=memory[-ind:]
    )
    logging.info('Received response from chat completion')

    # Checks if the response has the expected structure and content
    if (
        response.choices
        and response.choices[0].message
        and response.choices[0].message.content is not None
    ):
        tr = response.choices[0].message.content
        memory.append({"role": "assistant", "content": tr})
        logging.info('Added assistant response to memory: %s', tr)
    else:
        # Handles the case where the expected content is not available
        memory.append(
            {
                "role": "assistant",
                "content": "I'm not sure how to respond to that."
            }
        )
        logging.warning('Expected content not available in response')

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
            description = function_info.get(
                "description", "No description available."
            )
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
    **kwargs,
):
    logging.info('Starting conversation with user input line 237: %s', original_user_input)

    memory = await follow_conversation(
        user_text=original_user_input,
        memory=memory,
        mem_size=mem_size,
        model=openai_defaults["model"],
    )
    memory.append({"role": "user", "content": original_user_input})

    while len(json.dumps(memory)) > 128000:
        memory.pop(0)
        logging.debug('Removed oldest message due to context limit')

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
    logging.info('Received response from chat completion')

    response_message = response.choices[0].message
    tool_calls = (
        response_message.tool_calls if hasattr(
            response_message, "tool_calls"
        ) else []
    )

    if response_message.content is not None:
        memory.append(
            {
                "role": "assistant", "content": response_message.content
            }
        )
        logging.info('Added assistant response to memory: %s', response_message.content)

    if tool_calls:
        messages.append(response_message)
        executed_tool_call_ids = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name

            if function_name not in available_functions:
                logging.warning('Function %s is not available', function_name)
                continue

            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            logging.info(
                "Calling function: %s args: %s",
                function_name,
                function_args,
            )
            function_response = await function_to_call(**function_args)
            logging.info(
                "Function %s returned: %s",
                function_name,
                function_response,
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
                "content": f"With the data returned from the tool calls, generate any subsequently required requests and tool calls to process and understand the responses from the tool calls until you have verified you have the correct response to answer the original users request that was: {original_user_input}. And then follow up with any additional requests or tool calls to complete task required to fulfill the original request.",
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
        logging.info('Received second response from chat completion')
        return second_response, memory
    else:
        return response, memory


async def main():
    """
    Main function.
    """
    logging.info('Starting main function')
    os.system("cls" if os.name == "nt" else "clear")

    parser = argparse.ArgumentParser(
        description="GPT_ALL - A GPT-4-turbo based Mixture of Expert tools."
    )
    parser.add_argument(
        "--talk", action="store_true", help="Use TTS for the final response"
    )
    parser.add_argument(
        "--intro", action="store_true", help="Play an intro video at startup"
    )
    args = parser.parse_args()

    use_tts = args.talk
    logging.info('Use TTS: %s', use_tts)

    if args.intro:
        logging.info('Playing intro video')
        play_video("intro_video.mp4")

    console.print(Markdown("# 👋  GPT_ALL 👋"), style="bold blue")

    # Initialize available base functions and tools
    available_functions = {
        "get_current_date_time": get_current_date_time,
        "ask_chat_gpt_4_0314": ask_chat_gpt_4_0314,
        # Add more core functions here
    }
    logging.info('Initialized available functions')

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
                "description": "Ask an older AI LLM that is able to understand more complex concepts and perform complex tasks.",
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
    logging.info('Defined available core tools')

    # Use the load_plugins_and_get_tools function to conditionally add tools
    available_functions, tools = await enable_plugins(available_functions, tools)
    logging.info('Enabled plugins')

    # Initialize the conversation memory
    memory = []
    logging.info('Initialized conversation memory')

    # Main Loop
    while True:
        # Ask the user for input
        user_input = Prompt.ask(
            "\nHow can I be of assistance? ([yellow]/tools[/yellow] or [bold yellow]exit or quit[/bold yellow])",
        )
        logging.info('Received user input: %s', user_input)

        # Check if the user wants to exit the program
        if user_input.lower() == "exit":
            logging.info('User requested to exit the program')
            console.print("\nExiting the program.", style="bold red")
            break

        # Check if the user wants to see the available tools
        elif user_input.lower() == "/tools":
            logging.info('User requested to see the available tools')
            display_help(tools)
            continue

        # Prepare the conversation messages
        messages = [
            {
                "role": "system",
                "content": MAIN_SYSTEM_PROMPT,
            },
            {"role": "user", "content": f"{user_input}"},
        ]
        logging.info('Prepared conversation messages')

        # Start the spinner
        with live_spinner:
            # Start the spinner
            live_spinner.start()
            logging.info('Started spinner')

            # Pass the user input and memory to the run_conversation function
            final_response, memory = await run_conversation(
                messages=messages,
                tools=tools,
                available_functions=available_functions,
                original_user_input=user_input,
                mem_size=10,
                memory=memory,  # Pass the memory variable
            )
            logging.info('Received final response from run_conversation')

            # Stop the spinner
            live_spinner.stop()
            logging.info('Stopped spinner')

        # Print the final response from the model or use TTS
        if final_response:
            final_text = final_response.choices[0].message.content
            logging.info('Final response from model: %s', final_text)
            if use_tts:
                # Use TTS to output the final response
                console.print("\n" + final_text, style="green")
                tts_output(final_text)
            else:
                # Print the final response to the console
                console.print("\n" + final_text, style="green")
        else:
            # Print an error message if the model did not return a response
            logging.warning('Model did not return a response')
            console.print("\nI'm not sure how to help with that.", style="red")

        # Remove tools from the tools list after processing
        tools[:] = [
            tool
            for tool in tools
            if tool.get("function", {}).get("name", "").lower()
            not in user_input.lower()
        ]
        logging.info('Removed used tools from the tools list')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
