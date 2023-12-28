
# !/usr/bin/env python
# coding: utf-8
# Filename: google_search_tools.py
# Path: plugins/_google_search_plugin/google_search_tools.py

"""
Tools for interacting with Google Search API.
"""

import os
import logging
import asyncio
from typing import List
import aiohttp

TOOL_API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")

# Configure a separate logger for the Google Search plugin
google_search_logger = logging.getLogger('GoogleSearchPlugin')
google_search_logger.setLevel(logging.INFO)

# Create a log directory if it doesn't exist
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up the file handler to write logs to a file in the plugin's log directory
log_file_path = os.path.join(log_directory, 'google_search.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(
    logging.Formatter('%(name)s - %(levelname)s - %(message)s')
)
google_search_logger.addHandler(file_handler)


async def search_google(
    query: str,
    cr=None,
    dateRestrict=None,
    exactTerms=None,
    excludeTerms=None,
    fileType=None,
    filter=None,
    gl=None,
    lowRange=None,
    highRange=None,
    hl=None,
    hq=None,
    imgColorType=None,
    imgDominantColor=None,
    imgSize=None,
    imgType=None,
    linkSite=None,
    lr=None,
    num=None,
    orTerms=None,
    relatedSite=None,
    rights=None,
    safe=None,
    searchType=None,
    siteSearch=None,
    siteSearchFilter=None,
    sort=None,
    start=None,
) -> List:
    """
    Search Google and return results.

    Parameters:
    - query (str): The search query.
    - cr (str, optional): Country restrictions for the search.
    - dateRestrict (str, optional): Restricts results to URLs based on date.
    - exactTerms (str, optional): Phrase that all documents in the search results must contain.
    - excludeTerms (str, optional): Word or phrase that should not appear in any documents in the search results.
    - fileType (str, optional): Restricts results to files of a specified extension.
    - filter (str, optional): Controls turning on or off the duplicate content filter.
    - gl (str, optional): Geolocation of end user.
    - lowRange (str, optional): Starting value for a search range.
    - highRange (str, optional): Ending value for a search range.
    - hl (str, optional): Sets the user interface language.
    - hq (str, optional): Appends the specified query terms to the query.
    - imgColorType (str, optional): Returns black and white, grayscale, or color images.
    - imgDominantColor (str, optional): Returns images of a specific dominant color.
    - imgSize (str, optional): Returns images of a specified size.
    - imgType (str, optional): Returns images of a type.
    - linkSite (str, optional): Specifies that all search results should contain a link to a particular URL.
    - lr (str, optional): Restricts the search to documents written in a particular language.
    - num (int, optional): Number of search results to return.
    - orTerms (str, optional): Provides additional search terms to check for in a document.
    - relatedSite (str, optional): Specifies that all search results should be pages that are related to the specified URL.
    - rights (str, optional): Filters based on licensing.
    - safe (str, optional): Search safety level.
    - searchType (str, optional): Specifies the search type: image or web.
    - siteSearch (str, optional): Specifies all search results should be pages from a given site.
    - siteSearchFilter (str, optional): Controls whether to include or exclude results from the site named in the siteSearch parameter.
    - sort (str, optional): The sort expression to apply to the result.
    - start (int, optional): The index of the first result to return.

    Returns:
    List: A list of search results.
    """
    # Initialize the params dictionary with all parameters

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": TOOL_API_KEY,
        "cx": CSE_ID,
        "q": query,
        "cr": cr,
        "dateRestrict": dateRestrict,
        "exactTerms": exactTerms,
        "excludeTerms": excludeTerms,
        "fileType": fileType,
        "filter": filter,
        "gl": gl,
        "lowRange": lowRange,
        "highRange": highRange,
        "hl": hl,
        "hq": hq,
        "imgColorType": imgColorType,
        "imgDominantColor": imgDominantColor,
        "imgSize": imgSize,
        "imgType": imgType,
        "linkSite": linkSite,
        "lr": lr,
        "num": num,
        "orTerms": orTerms,
        "relatedSite": relatedSite,
        "rights": rights,
        "safe": safe,
        "searchType": searchType,
        "siteSearch": siteSearch,
        "siteSearchFilter": siteSearchFilter,
        "sort": sort,
        "start": start,
    }
    if searchType == "image":
        params["searchType"] = searchType
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}

    google_search_logger.info(
        "Making request to Google CSE API with params: %s",
        params
    )

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params, timeout=5) as res:
                data = await res.json()
                google_search_logger.info(
                    "Received response from Google CSE API: %s",
                    data
                )
                results = []
                if data.get("items"):
                    for item in data["items"]:
                        results.append(
                            {
                                "title": item["title"],
                                "description": item["snippet"],
                                "link": item["link"],
                            }
                        )
                # Log the results before returning using the plugin-specific logger
                google_search_logger.info("Search results: %s", results)
                return results
        except asyncio.TimeoutError:
            google_search_logger.error(
                "Request to Google CSE API timed out."
            )
            return []


search_google_tools = [
    {
        "type": "function",
        "function": {
            "name": "search_google",
            "description": "Search Google and return results.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query to perform the search on.",
                    },
                    "cr": {
                        "type": "string",
                        "description": "Restricts search results to documents originating in a particular country. You may use Boolean operators in the cr parameter's value.",
                    },
                    "dateRestrict": {
                        "type": "string",
                        "description": "Restricts results to URLs based on date.",
                    },
                    "exactTerms": {
                        "type": "string",
                        "description": "Identifies a phrase that all documents in the search results must contain.",
                    },
                    "excludeTerms": {
                        "type": "string",
                        "description": "Identifies a word or phrase that should not appear in any documents in the search results.",
                    },
                    "fileType": {
                        "type": "string",
                        "description": "Restricts results to files of a specified extension.",
                    },
                    "filter": {
                        "type": "string",
                        "description": "Controls turning on or off the duplicate content filter.",
                    },
                    "gl": {
                        "type": "string",
                        "description": "Geolocation of end user. The gl parameter value is a two-letter country code.",
                    },
                    "lowRange": {
                        "type": "string",
                        "description": "Specifies the starting value for a search range.",
                    },
                    "highRange": {
                        "type": "string",
                        "description": "Specifies the ending value for a search range.",
                    },
                    "hl": {
                        "type": "string",
                        "description": "Sets the user interface language.",
                    },
                    "hq": {
                        "type": "string",
                        "description": "Appends the specified query terms to the query.",
                    },
                    "imgColorType": {
                        "type": "string",
                        "enum": ["mono", "gray", "color"],
                        "description": "Returns black and white, grayscale, or color images.",
                    },
                    "imgDominantColor": {
                        "type": "string",
                        "enum": ["yellow", "green", "teal", "blue", "purple", "pink", "white", "gray", "black", "brown"],
                        "description": "Returns images of a specific dominant color.",
                    },
                    "imgSize": {
                        "type": "string",
                        "enum": ["icon", "small", "medium", "large", "xlarge", "xxlarge", "huge"],
                        "description": "Returns images of a specified size.",
                    },
                    "imgType": {
                        "type": "string",
                        "enum": ["clipart", "face", "lineart", "news", "photo"],
                        "description": "Returns images of a type.",
                    },
                    "linkSite": {
                        "type": "string",
                        "description": "Specifies that all search results should contain a link to a particular URL.",
                    },
                    "lr": {
                        "type": "string",
                        "description": "Restricts the search to documents written in a particular language.",
                    },
                    "num": {
                        "type": "integer",
                        "description": "Number of search results to return.",
                    },
                    "orTerms": {
                        "type": "string",
                        "description": "Provides additional search terms to check for in a document.",
                    },
                    "relatedSite": {
                        "type": "string",
                        "description": "Specifies that all search results should be pages that are related to the specified URL.",
                    },
                    "rights": {
                        "type": "string",
                        "description": "Filters based on licensing.",
                    },
                    "safe": {
                        "type": "string",
                        "enum": ["active", "off"],
                        "description": "Search safety level.",
                    },
                    "searchType": {
                        "type": "string",
                        "enum": ["image", "web"],
                        "description": "Specifies the search type: image or web.",
                    },
                    "siteSearch": {
                        "type": "string",
                        "description": "Specifies all search results should be pages from a given site.",
                    },
                    "siteSearchFilter": {
                        "type": "string",
                        "enum": ["e", "i"],
                        "description": "Controls whether to include or exclude results from the site named in the siteSearch parameter.",
                    },
                    "sort": {
                        "type": "string",
                        "description": "The sort expression to apply to the result.",
                    },
                    "start": {
                        "type": "integer",
                        "description": "The index of the first result to return.",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

available_functions = {
    "search_google": search_google,
}
