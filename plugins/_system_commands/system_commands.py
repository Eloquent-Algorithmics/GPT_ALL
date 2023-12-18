# Filename: system_commands_plugin.py
# Path: plugins\system_commands_plugin.py

"""
This file contains the System Commands plugin.
"""

import platform
import subprocess
import json
from plugins.plugin_base import PluginBase


class SystemCommandsPlugin(PluginBase):
    """
    This class defines the System Commands plugin.
    """

    async def initialize(self):
        # Initialization code if needed
        pass

    async def get_system_information(self):
        """
        Gets system information.
        """
        # Get system architecture
        arch = platform.architecture()[0]

        # Get system distribution (works on Linux only)
        if platform.system() == "Linux":
            distro_info = " ".join(platform.linux_distribution())
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

    async def run_system_command(self, command):
        """
        Runs a system command and returns the output.
        """
        try:
            result = subprocess.run(
                command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
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

    def get_tools(self):
        system_tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_system_information",
                    "description": "Get information about the system.",
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "run_system_command",
                    "description": "Run a system command.",
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
        ]

        self.tools.extend(system_tools)

        available_functions = {
            "get_system_information": self.get_system_information,
            "run_system_command": self.run_system_command,
        }

        return available_functions, self.tools
