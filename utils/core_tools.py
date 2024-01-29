
# !/usr/bin/env python
# coding: utf-8
# Filename: core_tools.py
# Path: utils/core_tools.py

"""

Real Core Tools
===============
This module contains the core system tools that use the local machine only.


Functions
---------
display_help(tools)
    Display the available tools.
get_current_date_time()
    Get the current EST date and time.

"""
import logging
import asyncio
from datetime import datetime
import tzlocal
import pytz
from rich.console import Console

console = Console()


def display_help(tools):
    """
    Display the available enabled tools and or functions.

    Args:
        tools (list): A list of tools.
        # Add more information to the docstring.

    """
    console.print("\n[bold]Available Tools:[/bold]\n", style="bold blue")
    for tool in tools:
        if isinstance(tool, dict) and "function" in tool:
            function_info = tool["function"]
            name = function_info.get("name", "Unnamed")
            description = function_info.get(
                "description", "No description available."
            )
            console.print(f"[bold]{name}[/bold]: {description}")
        else:
            logging.debug("Invalid tool format: %s", tool)
            console.print(f"[red]Invalid tool format: {tool}[/red]")


async def get_current_date_time() -> str:
    """
    Get the current EST date and time.

    Returns:
        str: The current UTC date and time.
    """
    local_timezone = tzlocal.get_localzone()
    now = datetime.now(local_timezone)
    now_est = now.astimezone(pytz.timezone("US/Eastern"))
    return now_est.strftime(
        "The current date and time is %B %d, %Y, %I:%M %p EST."
    )
