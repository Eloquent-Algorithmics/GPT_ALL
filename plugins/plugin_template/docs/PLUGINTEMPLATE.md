
# Plugin Template Documentation

## Overview

This document provides a template for creating a new plugin that fits into the provided plugin framework. The template includes a base plugin class and a tools module for interacting with an external API.

## Plugin Structure

- `my_plugin.py`: The main plugin file that defines the plugin class.
- `my_tools.py`: A module containing tools and functions for interacting with an external API.

## Plugin Class

The `MyPlugin` class inherits from `PluginBase` and defines the plugin. It includes methods for initialization and loading tools.

### Methods

- `initialize()`: An asynchronous method that initializes the plugin.
- `load_plugin_tools()`: Loads tools and functions from the `my_tools` module.

## Tools Module

The `my_tools` module contains functions to interact with an external API and defines a list of tools and available functions.

### Functions

- `get_data_from_my_api()`: An asynchronous function that fetches data from the external API.

### Tool List

- `my_tool_list`: A list of tools that includes the function name, description, and parameters.

### Available Functions

- `available_functions`: A dictionary mapping function names to their corresponding functions.

## Environment Variables

- `MY_API_URL`: The URL of the external API.
- `MY_API_KEY`: The API key for the external API.

## Usage

To use this template, replace `MyPlugin` and `my_tools` with the specific details of your plugin and API. Define the parameters and processing logic within the `get_data_from_my_api` function as per your API's requirements.