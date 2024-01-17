
# !/usr/bin/env python
# coding: utf-8
# Filename: app.py
# Run command: python -m app

"""
This is the main operations of the script
"""

import argparse
import asyncio
import inspect
import json
import logging
import os
import sys
from pathlib import Path

import httpx
import tiktoken
from openai import AsyncOpenAI
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from config import (
    LOGGING_ENABLED,
    LOGGING_FILE,
    LOGGING_FORMAT,
    LOGGING_LEVEL,
    MAIN_SYSTEM_PROMPT,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_TEMP,
    OPENAI_TOP_P,
    OPENAI_MAX_TOKENS,
    live_spinner,
)
from utils.openai_model_tools import (
    ask_chat_gpt_4_0314_synchronous,
    ask_chat_gpt_4_0314_asynchronous,
    ask_chat_gpt_4_0613_synchronous,
    ask_chat_gpt_4_0613_asynchronous,
    ask_gpt_4_vision,
)
from utils.openai_dalle_tools import generate_an_image_with_dalle3
from utils.core_tools import get_current_date_time, display_help
from output_methods.audio_pyttsx3 import tts_output
from plugins.plugins_enabled import enable_plugins

sys.path.append(str(Path(__file__).parent))

# Define the rich console
console = Console()

# Define the main OpenAI client
openai_model = OPENAI_MODEL

# Define the main OpenAI client
main_client = AsyncOpenAI(
    api_key=OPENAI_API_KEY,
    http_client=httpx.AsyncClient(
        limits=httpx.Limits(
            max_connections=1000,
            max_keepalive_connections=100,
        )
    )
)

# Define the parameters for the OpenAI main client.
openai_defaults = {
    "model": OPENAI_MODEL,
    "temperature": OPENAI_TEMP,
    "top_p": OPENAI_TOP_P,
    "max_tokens": OPENAI_MAX_TOKENS,
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
        # Set the logging level for specific libraries
        logging.getLogger(
            'httpcore.http11').setLevel(logging.INFO)
        logging.getLogger(
            'googleapiclient.discovery_cache').setLevel(logging.WARNING)
        logging.getLogger(
            'httpcore').setLevel(logging.WARNING)
        logging.getLogger(
            'markdown_it.rules_block').setLevel(logging.WARNING)
        logging.getLogger(
            'comtypes').setLevel(logging.WARNING)
    else:
        logging.basicConfig(level=level, format=LOGGING_FORMAT)
else:
    logging.disable(logging.CRITICAL)


def join_messages(memory: list[dict]):
    """
    This function joins messages for conversation memory.

    Args:
        memory: The conversation memory.

    Returns:
        The joined messages.
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

    Args:
        text: The text to check.
        limit: The token limit.
        model: The model to use.

    Returns:
        Whether the context is under the token limit.
    """
    enc = tiktoken.encoding_for_model(model)
    numtokens = len(enc.encode(text))
    return numtokens <= limit


async def follow_conversation(
    user_text: str, memory: list[dict], mem_size: int, model: str
):
    """
    This function follows the conversation.

    Args:
        user_text: The user text.
        memory: The conversation memory.
        mem_size: The memory size.
        model: The model to use.

    Returns:
        The conversation memory.
    """
    logging.info(
        'Starting conversation with user input from line 159: %s',
        user_text
    )

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
        logging.debug('Line 172 Removed oldest message due to context limit')

    response = await main_client.chat.completions.create(
        model=model, messages=memory[-ind:]
    )
    logging.info('Line 177 Received response from chat completion')

    # Checks if the response has the expected structure and content
    if (
        response.choices
        and response.choices[0].message
        and response.choices[0].message.content is not None
    ):
        tr = response.choices[0].message.content
        memory.append({"role": "assistant", "content": tr})
        logging.info('Line 187 Added assistant response to memory: %s', tr)
    else:
        # Handles the case where the expected content is not available
        memory.append(
            {
                "role": "assistant",
                "content": "I'm not sure how to respond to that."
            }
        )
        logging.warning('Line 196 Expected content not available in response')

    return memory


async def run_conversation(
    messages,
    tools,
    available_functions,
    original_user_input,
    memory,
    mem_size,
    **kwargs,
):
    """
    This function runs the conversation.

    Args:
        messages: The messages.
        tools: The tools.
        available_functions: The available functions.
        original_user_input: The original user input.
        memory: The conversation memory.
        mem_size: The memory size.
        **kwargs: The keyword arguments.

    Returns:
        The final response from the model.
    """
    logging.info(
        'Starting conversation with user input line 225: %s',
        original_user_input
    )

    memory = await follow_conversation(
        user_text=original_user_input,
        memory=memory,
        mem_size=mem_size,
        model=openai_defaults["model"],
    )
    memory.append({"role": "user", "content": original_user_input})

    while len(json.dumps(memory)) > 128000:
        memory.pop(0)
        logging.debug('Line 240 removed oldest message due to context limit')

    response = await main_client.chat.completions.create(
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
    logging.info('Line 253 received response from chat completion')

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
        logging.info(
            'Line 268 added assistant response to memory: %s',
            response_message.content
        )

    if tool_calls:
        messages.append(response_message)
        executed_tool_call_ids = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name

            if function_name not in available_functions:
                logging.warning(
                    'Line 281 function %s is not available',
                    function_name
                )
                continue

            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            logging.info(
                "Line 290 calling function: %s args: %s",
                function_name,
                function_args,
            )
            # Inside your run_conversation function
            if inspect.iscoroutinefunction(function_to_call):
                function_response = await function_to_call(**function_args)
            else:
                function_response = function_to_call(**function_args)
            logging.info(
                "Line 300 function %s returned: %s",
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
                "content": (
                    f"Using any data received from the tool calls, dynamically structure the workflow to "
                    f"process and integrate the information. Continue to perform necessary operations, "
                    f"including additional requests and tool calls, to ensure the accuracy and completeness "
                    f"of the response. Your goal is to provide a well-reasoned and verified answer to the "
                    f"original user request, which was: '{original_user_input}'. Adapt the workflow as needed "
                    f"to address all aspects of the user's request and deliver a comprehensive solution."
                ),
            }
        )

        # Create next completion ensuring to pass the updated messages array
        second_response = await main_client.chat.completions.create(
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
        logging.info('Line 350 received second response from chat completion')
        return second_response, memory
    else:
        return response, memory


async def main():
    """
    This is the main function of the script.

    Returns:
        The final response from the LLM to the user.

    """
    os.system("cls" if os.name == "nt" else "clear")

    parser = argparse.ArgumentParser(
        description="GPT_ALL - A GPT-4-turbo based Mixture of Expert tools."
    )
    parser.add_argument(
        "--talk", action="store_true", help="Use TTS for the final response"
    )
    args = parser.parse_args()

    use_tts = args.talk

    console.print(Markdown("# 👋  GPT_ALL 👋"), style="bold blue")

    # Initialize available base functions and tools
    available_functions = {
        "get_current_date_time": get_current_date_time,
        "ask_chat_gpt_4_0314_synchronous": ask_chat_gpt_4_0314_synchronous,
        "ask_chat_gpt_4_0314_asynchronous": ask_chat_gpt_4_0314_asynchronous,
        "ask_chat_gpt_4_0613_synchronous": ask_chat_gpt_4_0613_synchronous,
        "ask_chat_gpt_4_0613_asynchronous": ask_chat_gpt_4_0613_asynchronous,
        "generate_an_image_with_dalle3": generate_an_image_with_dalle3,
        "ask_gpt_4_vision": ask_gpt_4_vision,
    }

    # Define core tools here
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_date_time",
                "description": "Get the current date and time from the local machine.",
            },
        },
        {
            "type": "function",
            "function": {
                "name": "ask_chat_gpt_4_0314_synchronous",
                "description": "This function allows you to ask a larger AI LLM for assistance synchronously, like asking a more experienced colleague for assistance. This LLMs maximum token output limit is 2048 and this model's maximum context length is 8192 tokens",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "temperature": {
                            "type": "integer",
                            "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                        },
                        "question": {
                            "type": "string",
                            "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
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
        {
            "type": "function",
            "function": {
                "name": "ask_chat_gpt_4_0314_asynchronous",
                "description": "This function allows you to ask a larger AI LLM for assistance asynchronously, like asking a more experienced colleague for assistance. This LLMs maximum token output limit is 2048 and this model's maximum context length is 8192 tokens",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "temperature": {
                            "type": "integer",
                            "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                        },
                        "question": {
                            "type": "string",
                            "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
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
        {
            "type": "function",
            "function": {
                "name": "ask_chat_gpt_4_0613_synchronous",
                "description": "This function allows you to ask a larger AI LLM for assistance synchronously, like asking a more experienced colleague for assistance. This LLMs maximum token output limit is 2048 and this model's maximum context length is 8192 tokens",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "temperature": {
                            "type": "integer",
                            "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                        },
                        "question": {
                            "type": "string",
                            "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
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
        {
            "type": "function",
            "function": {
                "name": "ask_chat_gpt_4_0613_asynchronous",
                "description": "This function allows you to ask a larger AI LLM for assistance asynchronously, like asking a more experienced colleague for assistance. This LLMs maximum token output limit is 2048 and this model's maximum context length is 8192 tokens",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "temperature": {
                            "type": "integer",
                            "description": "The temperature associated with request: 0 for factual, 2 for creative.",
                        },
                        "question": {
                            "type": "string",
                            "description": "What are you, the ai assistant, requesting to be done with the text you are providing?",
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
        {
            "type": "function",
            "function": {
                "name": "ask_gpt_4_vision",
                "description": "Ask GPT-4 Vision a question about a specific image file located in the 'uploads' folder.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "image_name": {
                            "type": "string",
                            "description": "The name of the image file in the 'uploads' folder.",
                        },
                    },
                    "required": ["image_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "generate_an_image_with_dalle3",
                "description": "Generate an image with DALL-E 3.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The prompt to use for image generation.",
                        },
                        "n": {
                            "type": "integer",
                            "description": "The number of images to generate.",
                        },
                        "size": {
                            "type": "string",
                            "description": "The image size to generate.",
                        },
                        "quality": {
                            "type": "string",
                            "description": "The image quality to generate.",
                        },
                        "style": {
                            "type": "string",
                            "description": "The image style to generate. natural or vivid",
                        },
                        "response_format": {
                            "type": "string",
                            "description": "The response format to use for image generation b64_json or url.",
                        },
                    },
                    "required": ["prompt"],
                },
            },
        },
    ]

    # Use the load_plugins_and_get_tools function to conditionally add tools
    available_functions, tools = await enable_plugins(
        available_functions,
        tools
    )
    logging.info('Enabled plugins line 560')

    # Initialize the conversation memory
    memory = []

    # Main Loop
    while True:
        # Ask the user for input
        user_input = Prompt.ask(
            "\nHow can I be of assistance? ([yellow]/tools[/yellow] or [bold yellow]quit[/bold yellow])",
        )
        logging.info('Line 555 received user input: %s', user_input)

        # Check if the user wants to exit the program
        if user_input.lower() == "quit":
            logging.info('User requested to quit the program')
            console.print("\nQuitting the program.", style="bold red")
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
                "content": f"{MAIN_SYSTEM_PROMPT}",
            },
            {
                "role": "assistant",
                "content": "Understood. As we continue, feel free to direct any requests or tasks you'd like assistance with. Whether it's querying information, managing schedules, processing data, or utilizing any of the tools and functionalities I have available, I'm here to help. Just let me know what you need, and I'll do my best to assist you effectively and efficiently.",
            },
            {"role": "user", "content": f"{user_input}"},
        ]
        logging.info('Line 581 prepared conversation messages')

        with live_spinner:

            live_spinner.start()

            # Pass the user input and memory to the run_conversation function
            final_response, memory = await run_conversation(
                messages=messages,
                tools=tools,
                available_functions=available_functions,
                original_user_input=user_input,
                mem_size=200,
                memory=memory,
            )
            # Stop the spinner
            live_spinner.stop()

        # Print the final response from the model or use TTS
        if final_response:
            response_message = final_response.choices[0].message
            if response_message.content is not None:
                final_text = response_message.content
                if use_tts:
                    # Use TTS to output the final response
                    console.print("\n" + final_text, style="green")
                    tts_output(final_text)
                else:
                    # Print the final response to the console
                    console.print("\n" + final_text, style="green")
            else:
                # Print an error message if the model did not return a response
                logging.warning('Model did not return a response line 610')
                console.print("\nI'm not sure how to help with that.", style="red")
        else:
            # Print an error message if the model did not return a response
            logging.warning('Model did not return a response line 614')
            console.print("\nI'm not sure how to help with that.", style="red")

        # Remove tools from the tools list after processing
        tools[:] = [tool for tool in tools if not tool.get("function", {}).get("name", "").lower() in user_input.lower()]
        logging.info('Removed used tools from the tools list line 622')


# Run the main function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
