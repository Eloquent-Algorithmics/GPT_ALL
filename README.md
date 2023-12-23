# KitchenSinkGPT
<p align="center">
  <img src="ksGPT.png" alt="hero_image">
</p>
Welcome to KitchenSinkGPT: a cutting-edge AI assistant empowered by the capabilities of large language models (LLMs). This versatile assistant is adept at harvesting and interpreting real-time data from a plethora of sources, all while seamlessly meshing with the extensive functionalities of Python 3.12. At its heart lies OpenAI's GPT-4-1106 model, skillfully selecting functions and tools from a suite of specialized "experts" to optimize token efficiency.

KitchenSinkGPT boasts a dynamic command-line interface, embodying both power and flexibility. Engineered to harness the most recent advancements, tools, and expanded context windows available in the latest OpenAI API updates. The goal is clear and ambitious: to integrate chat GPT with an array of applications and devices, extending even to the kitchen sink (when Bluetooth-equipped), unlocking unprecedented possibilities. KitchenSinkGPT's capabilities are further amplified by a range of built-in plugins, and you're encouraged to craft your own to broaden its diverse array of functionalities.


<br>
<details>
<summary>Currently Included Tools</summary>

- **get_current_date_time**:
    - Get the current date and time.
- **ask_chat_gpt_4_0314**:
    - Send a request the 0314 (or any) model with a custom system prompt and tool set.
- **send_email**:
    - Send an email message using Gmail.
- **delete_email**:
    - Delete an email message by ID from Gmail.
- **get_emails_google**:
    - Retrieve a list of emails from Gmail.
- **get_next_google_calendar_event**:
    - Get the next event from the Google Calendar.
- **search_google**:
    - Search Google and return results.
- **ask_gemini_pro**:
    - Ask Gemini Pro for help.
- **get_all_news**:
    - Aggregate news articles from NewsAPI.org and The New York Times based on a query.
- **get_news_from_newsapi**:
    - Fetch news articles from the NewsAPI.org API based on a query.
- **get_news_from_nyt**:
    - Fetch news articles from The New York Times API based on a query.
- **get_vehicle_details**:
    - Retrieve details of a vehicle by VIN from the NHTSA vPic API.
- **get_system_information**:
    - Get information about the local machine.
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

</details>

## Features

- **AsyncOpenAI Integration**: 
    - Asynchronous parallel function calling to allow the assistant to complete multiple tool calls in a single request.
    - Leverage the power of GPT-4 for complex inquiries using tools and tool calls.

- **Conversation Memory Management**: 
    - **** >>> NEEDS WORK <<<< ****

- **Conversation Flow**:
    - Managed flow of conversation by appending user input to memory and ensuring responses are within context limits.

- **Dynamic Function Invocation Based on Tool Responses**:
    - Handles dynamic invocation of functions based on tool call responses.
    - Manages conversation state by appending messages from tool calls.
    - Generates follow-up responses considering tool call results.

- **Environment Cleanup**:
    - Cleans up tools list after processing each request to help manage token usage.

- **Modular Plugin System**:
    - easily install new functions/tools to extend KitchenSinkGPTs' abilities.
    - Plugins load dynamically if enabled via the .env

## Getting Started

### Prerequisites

- Ensure you have conda installed on your system.

- VScode Dev Container extension and Docker <br>is recommended for safety with system commands enabled.

### Installation

Clone this repository to your local machine using:

```bash
git clone https://github.com/Eloquent-Algorithmics/KitchenSinkGPT.git
```

Navigate into the project directory:

```bash

cd KitchenSinkGPT

.\install.bat

```

## Configuration

To enable specific plugins or features, modify the `.env` file in your project directory according to your needs.

**OpenAI API key is required** all others optional.


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

# ⚠️ Disclamer ⚠️
**Please note** some materials may not provide ***the best possible or the most optimal*** recommendations, solutions or source codes. Try to be open minded and take everything as a `step` in the `learning process`. If you encounter something to improve in the materials, **please** write your suggestions to the respected authors.

**This version of KitchenSinkGPT is totally experimental, USE IT AT YOUR OWN RISK. Even if a lot of tests have been performed on this version some things can be buggy or some lack of functionality.**

This version can be driven by the community. If you want to help improve this version don't hesitate to submit a github issue or PR.

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
