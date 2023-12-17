# AI Assistant Application Documentation

## Overview

This Python script is designed to create an AI assistant that can answer questions and perform complex tasks using available tools and by asking available experts questions. The assistant is designed to assist users by using the tools available to gather data and complete actions required to best complete the users' request.

## Dependencies

The script uses several Python libraries, including:

- `sys`
- `pathlib`
- `os`
- `json`
- `asyncio`
- `datetime`
- `importlib.util`
- `inspect`
- `tzlocal`
- `pytz`
- `dotenv`
- `spacy`
- `openai`
- `rich.console`
- `rich.markdown`
- `rich.prompt`

## Functions

The script contains several functions:

- `get_current_date_time()`: This function returns the current date and time in the Eastern Standard Time (EST) timezone.

- `load_plugins_and_get_tools(available_functions, tools)`: This function dynamically loads plugins from a specified folder and retrieves their tools. The tools are then added to the available functions and tools.

- `display_help(tools)`: This function displays the available tools to the console.

- `run_conversation(messages, tools, available_functions, **kwargs)`: This function runs a conversation with the model. It sends the conversation and available functions to the model, checks if the model wanted to call a function, and if so, calls the function and sends the function's response to the model.

- `main()`: This is the main function of the script. It initializes the available functions and tools, loads plugins and their tools, and runs a loop that asks the user for input, processes the input, and prints the final response from the model.

## Execution

The script is executed by running the `main()` function using `asyncio.run(main())`.

## Usage

The user can interact with the AI assistant by typing in a question or command. The assistant will then use the available tools and functions to provide a response. The user can type `/help` to see the available tools, or `exit` to quit the program.