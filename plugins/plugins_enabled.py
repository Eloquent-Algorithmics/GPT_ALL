
# !/usr/bin/env python
# coding: utf-8
# Filename: plugin_enabled.py
# Path: plugins/plugin_enabled.py

"""
Enable plugins.
"""

import os
import importlib.util
import inspect
import logging
from rich.console import Console
from plugins.plugin_base import PluginBase

console = Console()

# Configure a separate logger for the Google Drive functions and tools
enable_plugins_logger = logging.getLogger('Enable_Plugins')
enable_plugins_logger.setLevel(logging.INFO)

# Create a log directory if it doesn't exist
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up the file handler to write logs to a file in the plugin's log directory
log_file_path = os.path.join(log_directory, 'enable_plugins.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(
    logging.Formatter('%(levelname)s - %(message)s')
)
enable_plugins_logger.addHandler(file_handler)


# Defines the enable plugins function
async def enable_plugins(available_functions, tools):
    """
    Enable plugins.
    """
    plugins_folder = "plugins"
    enable_plugins_logger.info("Starting to enable plugins...")

    # Recursively walk through the plugins directory
    for root, dirs, files in os.walk(plugins_folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                file_path = os.path.join(root, file)
                enable_plugins_logger.info("Found plugin file: %s", file_path)

                # Import the module dynamically
                spec = importlib.util.spec_from_file_location(
                    file[:-3], file_path
                )
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    enable_plugins_logger.info("Successfully imported module: %s", file)
                except Exception as e:
                    enable_plugins_logger.error("Failed to import module %s: %s", file, e)
                    continue

                # Find the plugin class
                for _, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, PluginBase) and cls is not PluginBase:
                        enable_plugins_logger.info("Found plugin class: %s", cls.__name__)

                        # Generate the environment variable name based on the class name
                        env_var_name = "ENABLE_%s" % cls.__name__.upper()
                        plugin_enabled = os.getenv(env_var_name, "false").lower() == "true"
                        enable_plugins_logger.info(
                            "Environment variable %s is set to %s",
                            env_var_name,
                            plugin_enabled
                        )

                        if plugin_enabled and cls.__name__ not in available_functions:
                            enable_plugins_logger.info("Enabling plugin: %s", cls.__name__)

                            # Instantiate the plugin
                            plugin = cls()
                            # Initialize the plugin
                            await plugin.initialize()
                            # Get the tools from the plugin
                            plugin_tools = plugin.get_tools()
                            # Add the plugin's functions and tools
                            available_functions.update(
                                plugin.get_available_functions()
                            )
                            tools.extend(plugin_tools)
                            enable_plugins_logger.info(
                                "Enabled plugin: %s with tools: %s",
                                cls.__name__,
                                plugin_tools
                            )
                        else:
                            enable_plugins_logger.info("Plugin %s is not enabled or already added.", cls.__name__)

    enable_plugins_logger.info("Available functions: %s", available_functions)
    enable_plugins_logger.info("Tools: %s", tools)
    return available_functions, tools
