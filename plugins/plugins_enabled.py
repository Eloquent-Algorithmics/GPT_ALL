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
from plugins.plugin_base import PluginBase

# Configure logging to output to the console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
                logging.info(f"Found plugin file: {file_path}")
                # Import the module dynamically
                spec = importlib.util.spec_from_file_location(
                    file[:-3], file_path
                )
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    logging.error(f"Failed to import module {file}: {e}")
                    continue

                # Find the plugin class
                for _, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, PluginBase) and cls is not PluginBase:
                        logging.info(f"Found plugin class: {cls.__name__}")
                        # Check if the plugin is enabled
                        env_var_name = f"ENABLE_{cls.__name__.upper()}"
                        plugin_enabled = os.getenv(env_var_name, "false").lower() == "true"
                        logging.info(f"Environment variable {env_var_name} is set to {plugin_enabled}")
                        if plugin_enabled:
                            logging.info(f"Enabling plugin: {cls.__name__}")
                            # Instantiate the plugin
                            plugin = cls()
                            # Initialize the plugin
                            await plugin.initialize()
                            # Get the tools from the plugin
                            plugin_tools = plugin.get_tools()
                            # Add the plugin's functions and tools
                            available_functions.update(plugin_tools)
                            tools.extend(plugin_tools.values())
                        else:
                            logging.info(f"Plugin {cls.__name__} is not enabled.")

    logging.info("Finished enabling plugins.")
    return available_functions, tools
