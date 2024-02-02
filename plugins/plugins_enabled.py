
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
from rich.console import Console
from plugins.plugin_base import PluginBase

console = Console()


async def enable_plugins(available_functions, tools):
    """
    Enable plugins.
    """
    plugins_folder = "plugins"

    for root, dirs, files in os.walk(plugins_folder):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                file_path = os.path.join(root, file)

                spec = importlib.util.spec_from_file_location(
                    file[:-3], file_path
                )
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    continue

                for _, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, PluginBase) and cls is not PluginBase:

                        env_var_name = "ENABLE_%s" % cls.__name__.upper()
                        plugin_enabled = os.getenv(env_var_name, "false").lower() == "true"

                        if plugin_enabled and cls.__name__ not in available_functions:

                            plugin = cls()
                            await plugin.initialize()
                            plugin_tools = plugin.get_tools()
                            available_functions.update(
                                plugin.get_available_functions()
                            )
                            tools.extend(plugin_tools)
                        else:
                            console.print(
                                f"Plugin {cls.__name__} is not enabled. Set {env_var_name} to true to enable it."
                            )

    return available_functions, tools
