
# !/usr/bin/env python
# coding: utf-8
# Filename: calendar_tools.py
# Path: plugins/_gmail_plugin/calendar_tools.py

"""
This module contains the Gmail Calendar functions and tools.
"""

import datetime
import logging
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(
    filename='calendar_tools.log',
    level=logging.INFO,
    format='%(levelname)s:%(message)s'
)


async def get_next_calendar_event(calendar_service):
    """
    This function gets the next event from the users Google Calendar.
    """
    now = datetime.datetime.utcnow().isoformat() + "Z"
    try:
        events_result = (
            calendar_service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=1,
                singleEvents=True,
                orderBy="startTime"
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            logging.info("No upcoming events found.")
            return "No upcoming events found."
        else:
            event = events[0]
            start = event["start"].get("dateTime", event["start"].get("date"))
            logging.info("Next event: %s at %s", event['summary'], start)
            return f"Next event: {event['summary']} at {start}"
    except HttpError as error:
        logging.error("An error occurred: %s", error)
        return "An error occurred while retrieving events."


calendar_tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_next_calendar_event",
            "description": "Fetch next event from the users Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

available_functions = {
    "get_next_calendar_event": get_next_calendar_event,
}
