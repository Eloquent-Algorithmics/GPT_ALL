
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


# Defines the enable plugins function
async def enable_plugins(available_functions, tools):
    """
    Enable plugins.
    """
    plugins_folder = "plugins"
    logging.info("Starting to enable plugins...")

    # Recursively walk through the plugins directory
    for root, dirs, files in os.walk(plugins_folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                file_path = os.path.join(root, file)
                logging.info("Found plugin file: %s", file_path)

                # Import the module dynamically
                spec = importlib.util.spec_from_file_location(
                    file[:-3], file_path
                )
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    logging.info("Successfully imported module: %s", file)
                except Exception as e:
                    logging.error("Failed to import module %s: %s", file, e)
                    continue

                # Find the plugin class
                for _, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, PluginBase) and cls is not PluginBase:
                        logging.info("Found plugin class: %s", cls.__name__)

                        # Check if the plugin is enabled
                        env_var_name = "ENABLE_%s" % cls.__name__.upper()
                        plugin_enabled = os.getenv(env_var_name, "false").lower() == "true"  # Define plugin_enabled here
                        logging.info("Environment variable %s is set to %s", env_var_name, plugin_enabled)

                        if plugin_enabled:
                            logging.info("Enabling plugin: %s", cls.__name__)

                            # Instantiate the plugin
                            plugin = cls()
                            # Initialize the plugin
                            await plugin.initialize()
                            # Get the tools from the plugin
                            plugin_tools = plugin.get_tools()
                            # Add the plugin's functions and tools
                            available_functions.update(plugin.get_available_functions())
                            tools.extend(plugin_tools)
                            logging.info("Enabled plugin: %s with tools: %s", cls.__name__, plugin_tools)
                        else:
                            logging.info("Plugin %s is not enabled.", cls.__name__)

    logging.info("Available functions: %s", available_functions)
    logging.info("Tools: %s", tools)
    return available_functions, tools
