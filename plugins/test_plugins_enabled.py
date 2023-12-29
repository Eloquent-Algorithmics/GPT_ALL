import unittest
from unittest.mock import MagicMock, patch
from plugins.plugins_enabled import enable_plugins

class TestEnablePlugins(unittest.TestCase):
    @patch("os.walk")
    @patch("importlib.util.spec_from_file_location")
    @patch("importlib.util.module_from_spec")
    @patch("inspect.getmembers")
    @patch("os.getenv")
    async def test_enable_plugins(self, mock_getenv, mock_getmembers, mock_module_from_spec, mock_spec_from_file_location, mock_walk):
        # Mock the necessary dependencies
        mock_getenv.return_value = "true"
        mock_getmembers.return_value = [("PluginClass", MagicMock())]
        mock_module_from_spec.return_value = MagicMock()
        mock_spec_from_file_location.return_value = MagicMock()
        mock_walk.return_value = [("/path/to/plugins", [], ["plugin.py"])]

        # Define the expected results
        expected_available_functions = {"PluginClass": MagicMock()}
        expected_tools = [MagicMock()]

        # Call the function under test
        available_functions, tools = await enable_plugins({}, [])

        # Assert the results
        self.assertEqual(available_functions, expected_available_functions)
        self.assertEqual(tools, expected_tools)

if __name__ == "__main__":
    unittest.main()