
# !/usr/bin/env python
# coding: utf-8
# Filename: test_plugin_base.py
# Path: plugins/tests/test_plugin_base.py

"""
Test the PluginBase class.
"""

import unittest
from unittest.mock import MagicMock
from plugin_base import PluginBase


class TestPluginBase(unittest.TestCase):
    """
    Test the PluginBase class.

    """
    def test_initialize(self):
        """ initialize() should raise NotImplementedError. """
        plugin = PluginBase()
        with self.assertRaises(NotImplementedError):
            plugin.initialize()

    def test_load_plugin_tools(self):
        """ load_plugin_tools() should raise NotImplementedError. """
        plugin = PluginBase()
        with self.assertRaises(NotImplementedError):
            plugin.load_plugin_tools()

    def test_get_tools(self):
        """ get_tools() should return the tools list. """
        plugin = PluginBase()
        plugin.tools = [MagicMock()]
        self.assertEqual(plugin.get_tools(), [MagicMock()])

    def test_get_available_functions(self):
        """ get_available_functions() should return the available functions """
        plugin = PluginBase()
        plugin.available_functions = {
            "function1": MagicMock(),
            "function2": MagicMock()
        }
        self.assertEqual(plugin.get_available_functions(), {
            "function1": MagicMock(),
            "function2": MagicMock()
            }
        )


if __name__ == "__main__":
    unittest.main()
