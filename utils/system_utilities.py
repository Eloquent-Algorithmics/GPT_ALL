
# !/usr/bin/env python
# coding: utf-8
# Filename: system_utilities.py
# Path: utils/system_utilities.py

"""
This module defines system utilities.
"""

import os
import sys
import logging
from config import LOGGING_ENABLED, LOGGING_LEVEL, LOGGING_FORMAT, LOGGING_FILE


async def clear_log_files(log_file_paths):
    log_files_deleted = []
    """
    Clear all .log files in the project folders.

    Args:
        enabled_plugins (list): A list of enabled plugin names.
    """

    # Disable logging
    logging.disable(logging.CRITICAL)

    # Close handlers for enabled plugins' loggers
    for plugin_name in enabled_plugins:
        plugin_logger = logging.getLogger(plugin_name)
        handlers = plugin_logger.handlers[:]
        for handler in handlers:
            handler.close()
            plugin_logger.removeHandler(handler)

    # Close all other logging handlers that may have opened the log files
    handlers = logging.root.handlers[:]
    for handler in handlers:
        handler.close()
        logging.root.removeHandler(handler)

    # Start from the current directory or adjust the path as necessary
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.log'):
                log_file_path = os.path.join(root, file)
                # Only attempt to delete log files for enabled plugins
                if any(plugin_name in log_file_path for plugin_name in enabled_plugins):
                    try:
                        os.remove(log_file_path)
                        log_files_deleted.append(log_file_path)
                    except Exception as e:
                        # If logging is needed here, it should be minimal and to stderr
                        print(f"Error deleting log file {log_file_path}: {e}", file=sys.stderr)

    # Re-enable logging
    logging.disable(logging.NOTSET)

    # Reconfigure logging based on the settings from .env
    if LOGGING_ENABLED:
        # Set the logging level based on the LOGGING_LEVEL string
        level = getattr(logging, LOGGING_LEVEL.upper(), logging.WARNING)
        # Configure logging with or without a log file
        if LOGGING_FILE:
            logging.basicConfig(
                level=level,
                format=LOGGING_FORMAT,
                filename=LOGGING_FILE,
                filemode='w'  # Overwrite the log file if it exists
            )
        else:
            logging.basicConfig(level=level, format=LOGGING_FORMAT)

        # Set a higher logging level for a package to prevent DEBUG logs
        logging.getLogger('markdown_it').setLevel(logging.ERROR)
        logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
        logging.getLogger('httpcore').setLevel(logging.ERROR)
    else:
        logging.disable(logging.CRITICAL)

    return f"Cleared the following log files: {', '.join(log_files_deleted)}" if log_files_deleted else "No log files found to clear."
