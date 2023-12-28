
# !/usr/bin/env python
# coding: utf-8
# Filename: test_google_search_tools.py
# Path: plugins/_google_search_plugin/test_google_search_tools.py

import asyncio
import unittest
from unittest.mock import MagicMock
from google_search_tools import search_google

class TestGoogleSearchPlugin(unittest.TestCase):
    def test_search_google(self):
        """ search_google() should return the search results. """
        query = "test query"
        expected_results = [
            {
                "title": "Test Title",
                "description": "Test Description",
                "link": "https://www.example.com"
            }
        ]
        # Mock the aiohttp.ClientSession and its get method
        mock_session = MagicMock()
        mock_get = MagicMock()
        mock_get.return_value.__aenter__.return_value = mock_get
        mock_get.json.return_value = {
            "items": [
                {
                    "title": "Test Title",
                    "snippet": "Test Description",
                    "link": "https://www.example.com"
                }
            ]
        }
        mock_session.get = mock_get

        # Patch the aiohttp.ClientSession to return the mock session
        with unittest.mock.patch("aiohttp.ClientSession", return_value=mock_session):
            # Run the coroutine using asyncio.run() and store the results
            results = asyncio.run(search_google(query))

        self.assertEqual(results, expected_results)

if __name__ == "__main__":
    unittest.main()
