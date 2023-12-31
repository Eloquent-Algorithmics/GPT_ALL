
# !/usr/bin/env python
# coding: utf-8
# Filename: system_commands_tools.py
# Path: plugins/_system_commands/system_commands_tools.py

"""
This file contains the System Commands function definitions and tools.
"""

import sys
import platform
import subprocess
import json


async def get_system_information():
    """
    Gets system information.
    """
    # Get system architecture
    is_64bits = sys.maxsize > 2**32
    arch = "64bit" if is_64bits else "32bit"

    # Get system distribution (works on Linux only)
    if platform.system() == "Linux":
        try:
            distro_info = " ".join(platform.freedesktop_os_release().values())
        except (OSError, AttributeError):
            distro_info = None
    else:
        distro_info = None

    # Get Windows version (works on Windows only)
    if platform.system() == "Windows":
        win_ver = platform.win32_ver()
        win_version = f"{win_ver[0]} {win_ver[1]} {win_ver[3]}"
    else:
        win_version = None

    # Get macOS version (works on macOS only)
    if platform.system() == "Darwin":
        mac_ver = platform.mac_ver()
        mac_version = f"{mac_ver[0]} {mac_ver[2]}"
    else:
        mac_version = None

    # Build the system information dictionary
    system_info = {
        "architecture": arch,
        "distribution": distro_info,
        "windows_version": win_version,
        "mac_version": mac_version,
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
    }

    return json.dumps(system_info)


async def run_system_command(command):
    """
    Runs a system command and returns the output.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return json.dumps({
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        })
    except subprocess.CalledProcessError as e:
        return json.dumps({
            "error": "Command execution failed",
            "details": str(e),
            "returncode": e.returncode
        })


async def read_python_script(file_path):
    """
    Reads the content of a Python script.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return json.dumps({
            "content": content
        })
    except PermissionError as e:
        return json.dumps({
            "error": "Failed to write the Python script",
            "details": str(e)
        })
    except FileNotFoundError as e:
        return json.dumps({
            "error": "File not found",
            "details": str(e)
        })
    except IsADirectoryError as e:
        return json.dumps({
            "error": "The path is a directory",
            "details": str(e)
        })
    except OSError as e:
        return json.dumps({
            "error": "OS error",
            "details": str(e)
        })


async def write_python_script(file_path, content):
    """
    Writes content to a Python script.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return json.dumps({
            "message": "Python script written successfully"
        })
    except PermissionError as e:
        return json.dumps({
            "error": "Failed to write the Python script",
            "details": str(e)
        })
    except FileNotFoundError as e:
        return json.dumps({
            "error": "File not found",
            "details": str(e)
        })
    except IsADirectoryError as e:
        return json.dumps({
            "error": "The path is a directory",
            "details": str(e)
        })
    except OSError as e:
        return json.dumps({
            "error": "OS error",
            "details": str(e)
        })


async def amend_python_script(file_path, content):
    """
    Amends a Python script by appending content to it.
    """
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)
        return json.dumps({
            "message": "Python script amended successfully"
        })
    except IOError as e:
        return json.dumps({
            "error": "Failed to amend the Python script",
            "details": str(e)
        })


async def execute_python_script(file_path):
    """
    Executes a Python script and returns the output.
    """
    try:
        result = subprocess.run(
            ['python', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return json.dumps({
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        })
    except subprocess.CalledProcessError as e:
        return json.dumps({
            "error": "Python script execution failed",
            "details": str(e),
            "returncode": e.returncode
        })


system_commands_tool_list = [
    {
        "type": "function",
        "function": {
            "name": "get_system_information",
            "description": "This function allows you to gather information about the local machine.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_system_command",
            "description": "This function allows you to run a system command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to run.",
                    },
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_python_script",
            "description": "This function allows you to read a Python script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "path to the Python script.",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_python_script",
            "description": "This function allows you to write a Python script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "path to the Python script.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the script.",
                    },
                },
                "required": ["file_path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "amend_python_script",
            "description": "This function allows you to amend a Python script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "path to the Python script.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to append to the script.",
                    },
                },
                "required": ["file_path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_python_script",
            "description": "This function allows you to execute a Python script.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "path to the Python script.",
                    },
                },
                "required": ["file_path"],
            },
        },
    },
]

available_functions = {
    "get_system_information": get_system_information,
    "run_system_command": run_system_command,
    "read_python_script": read_python_script,
    "write_python_script": write_python_script,
    "amend_python_script": amend_python_script,
    "execute_python_script": execute_python_script,
}
