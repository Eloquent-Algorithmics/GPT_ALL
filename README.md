# KitchenSinkGPT

Welcome to KitchenSinkGPT, an AI-powered assistant designed to help you navigate complex tasks with ease. Built with Python and integrated with OpenAI's GPT-4 model, KitchenSinkGPT offers a rich command-line experience that's both powerful and user-friendly. Designed to utilize new features and functions available with the release of OpenAI API v1 and the 1106 models. The idea is simple, create a way to connect chat gpt to everything, even the kitchen sink (if it has bluetooth) ... and see what we can get it to do. Extend KitchenSinkGPT's capabilities by enabling various plugins or easily build new ones.

## Features

- **AsyncOpenAI Integration**: 
    - Asynchronous parallel function calling to allow the assistant to complete multiple tool calls in a single request.
    - Leverage the power of GPT-4 for complex inquiries using tools and tool calls.

## Available Tools

- **get_current_date_time**:
    - Get the current date and time.
- **ask_chat_gpt_4_0314**:
    - Ask a smarter AI language model that is able to understand more complex concepts and perform complex tasks.
- **send_email**:
    - Send an email message.
- **delete_email**:
    - Delete an email message by ID.
- **get_emails_google**:
    - Retrieve a list of emails from Gmail.
- **get_next_google_calendar_event**:
    - Get the next event from the Google Calendar.
- **search_google**:
    - Search Google and return results.
- **ask_gemini_pro**:
    - Ask Gemini Pro a question and print the response.
- **get_all_news**:
    - Aggregate news articles from NewsAPI.org and The New York Times.
- **get_news_from_newsapi**:
    - Fetch news articles from the NewsAPI.org API.
- **get_news_from_nyt**:
    - Fetch news from The New York Times API.
- **get_vehicle_details**:
    - Retrieve details of a vehicle by VIN.
- **get_system_information**:
    - Get information about the local system.
- **run_system_command**:
    - Run a system command.
- **read_python_script**:
    - Read a Python script.
- **write_python_script**:
    - Write a Python script.
- **amend_python_script**:
    - Amend a Python script.
- **execute_python_script**:
    - Execute a Python script.
- **get_current_weather**:
    - Get the current weather in a location.

- **Plugin System**:
    - easily install new functions/tools to extend the APIs' abilities.
    - Plugins load dynamically if they are enabled via the .env

- **Conversation Memory Management**: 
    - **** >>> NEEDS WORK <<<< ****

- **Conversation Flow**:
    - Managed flow of conversation by appending user input to memory and ensuring responses are within context limits.

- **Dynamic Function Invocation Based on Tool Responses**:
    - Handles dynamic invocation of functions based on tool call responses.
    - Manages conversation state by appending messages from tool calls.
    - Generates follow-up responses considering tool call results.

- **Environment Cleanup**:
    - Cleans up tools list after processing each request.

# ⚠️ Disclamer ⚠️
    - **Please note** some materials may not provide ***the best possible or the most optimal*** recommendations, solutions or source codes. Try to be open minded and take everything as a `step` in the `learning process`. If you encounter something to improve in the materials, **please** write your suggestions to the respected authors.

    - **This version of KitchenSinkGPT is totally experimental, USE IT AT YOUR OWN RISK. Even if a lot of tests have been performed on this version some things can be buggy or some lack of functionality.**
    
    - This version can be driven by the community. If you want to help us improve this version don't hesitate to send a git hub issue or PR.

## Getting Started

### Prerequisites

- Ensure you have conda installed on your system. VScode Dev Container extension and Docker recommended for safety.

### Installation

Clone this repository to your local machine using:

```bash
git clone https://github.com/ExplorerGT92/KitchenSinkGPT.git
```

Navigate into the project directory:

```bash

cd KitchenSinkGPT

.\install.bat

```

## Configuration

To enable specific plugins or features, modify the `.env` file in your project directory according to your needs.


### Usage

Run ksGPT using:

```bash

conda activate ksGPT

python -m app

or

python -m app --talk  # Use --talk to use TTS.

or

python -m app --intro  # Use --intro to play an intro video at startup.
```


## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated. ## Contribution guidelines

**If you want to contribute to KitchenSinkGPT, be sure to review the [contribution guidelines](CONTRIBUTING.md). This project adheres to [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.**

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

[Apache License 2.0](LICENSE)