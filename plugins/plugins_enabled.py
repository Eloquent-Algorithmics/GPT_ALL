"""
Enable plugins.
"""

import os
import importlib.util
import inspect
from plugins.plugin_base import PluginBase


async def enable_plugins(available_functions, tools):
    plugins_folder = "plugins"

    # Iterate through the files in the plugins folder
    for file in os.listdir(plugins_folder):
        if file.endswith(".py") and not file.startswith("_"):
            # Import the module dynamically
            spec = importlib.util.spec_from_file_location(file[:-3], os.path.join(plugins_folder, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Find the plugin class
            for _, cls in inspect.getmembers(module, inspect.isclass):
                if issubclass(cls, PluginBase) and cls is not PluginBase:
                    # Check if the plugin is enabled
                    env_var_name = f"ENABLE_{cls.__name__.upper()}"
                    if os.getenv(env_var_name, "false").lower() == "true":
                        # Instantiate the plugin
                        plugin = cls()
                        # Initialize the plugin
                        await plugin.initialize()
                        # Get the tools from the plugin
                        plugin_tools = plugin.get_tools()
                        # Add the plugin's functions and tools
                        available_functions.update(plugin_tools)
                        tools.extend(plugin_tools.values())

    return available_functions, tools
