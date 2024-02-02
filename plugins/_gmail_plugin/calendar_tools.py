
# !/usr/bin/env python
# coding: utf-8
# Filename: calendar_tools.py
# Path: plugins/_gmail_plugin/calendar_tools.py

"""
This module contains the Gmail Calendar functions and tools.
"""

import datetime
from googleapiclient.errors import HttpError


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
            return "No upcoming events found."
        else:
            event = events[0]
            start = event["start"].get("dateTime", event["start"].get("date"))
            return f"Next event: {event['summary']} at {start}"
    except HttpError:
        return "An error occurred while retrieving events."


async def add_event(calendar_service, event_details):
    """Add an event to the user's calendar."""
    try:
        event = calendar_service.events().insert(calendarId='primary', body=event_details).execute()
        return f"Event created: {event.get('htmlLink')}"
    except HttpError as error:
        return f"An error occurred: {error}"


async def update_event(calendar_service, event_id, updated_event_details):
    """Update an existing event by ID."""
    try:
        updated_event = calendar_service.events().update(calendarId='primary', eventId=event_id, body=updated_event_details).execute()
        return f"Event updated: {updated_event.get('htmlLink')}"
    except HttpError as error:
        return f"An error occurred: {error}"


async def delete_event(calendar_service, event_id):
    """Delete an event by its ID."""
    try:
        calendar_service.events().delete(calendarId='primary', eventId=event_id).execute()
        return "Event deleted successfully."
    except HttpError as error:
        return f"An error occurred: {error}"


async def list_events(calendar_service, max_results=10):
    """List the next 10 events on the user's calendar."""
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    try:
        events_result = calendar_service.events().list(calendarId='primary', timeMin=now,
                                                       maxResults=max_results, singleEvents=True,
                                                       orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except HttpError as error:
        return f"An error occurred: {error}"


async def get_event(calendar_service, event_id):
    """Get a specific event by ID."""
    try:
        event = calendar_service.events().get(calendarId='primary', eventId=event_id).execute()
        return event
    except HttpError as error:
        return f"An error occurred: {error}"


async def clear_calendar(calendar_service):
    """Clears all events from the primary calendar."""
    try:
        calendar_service.calendars().clear(calendarId='primary').execute()
        return "Primary calendar cleared."
    except HttpError as error:
        return f"An error occurred: {error}"


async def list_calendars(calendar_service):
    """List all calendars for the user."""
    try:
        calendar_list = calendar_service.calendarList().list().execute()
        return calendar_list.get('items', [])
    except HttpError as error:
        return f"An error occurred: {error}"


async def create_calendar(calendar_service, calendar_details):
    """Create a new calendar."""
    try:
        calendar = calendar_service.calendars().insert(body=calendar_details).execute()
        return f"Calendar created: {calendar.get('summary')}"
    except HttpError as error:
        return f"An error occurred: {error}"


async def update_calendar(calendar_service, calendar_id, updated_calendar_details):
    """Update an existing calendar by ID."""
    try:
        updated_calendar = calendar_service.calendars().update(calendarId=calendar_id, body=updated_calendar_details).execute()
        return f"Calendar updated: {updated_calendar.get('summary')}"
    except HttpError as error:
        return f"An error occurred: {error}"


async def delete_calendar(calendar_service, calendar_id):
    """Delete a calendar by its ID."""
    try:
        calendar_service.calendars().delete(calendarId=calendar_id).execute()
        return "Calendar deleted successfully."
    except HttpError as error:
        return f"An error occurred: {error}"


calendar_tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_next_calendar_event",
            "description": "Fetch the next event from the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_event",
            "description": "Add a new event to the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_details": {
                        "type": "object",
                        "description": "A dictionary containing event details following Google's event format."
                    },
                },
                "required": ["event_details"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_event",
            "description": "Update an existing event in the user's Google Calendar by event ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to update."
                    },
                    "updated_event_details": {
                        "type": "object",
                        "description": "A dictionary containing updated event details."
                    },
                },
                "required": ["event_id", "updated_event_details"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_event",
            "description": "Delete an event from the user's Google Calendar by event ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to delete."
                    },
                },
                "required": ["event_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_events",
            "description": "List the upcoming events from the user's Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of events to return."
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_event",
            "description": "Retrieve a specific event from the user's Google Calendar by event ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The ID of the event to retrieve."
                    },
                },
                "required": ["event_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clear_calendar",
            "description": "Clears all events from the user's primary Google Calendar.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
     {
        "type": "function",
        "function": {
            "name": "list_calendars",
            "description": "List all calendars for the user.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_calendar",
            "description": "Create a new calendar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_details": {
                        "type": "object",
                        "description": "A dictionary containing calendar details following Google's calendar format."
                    },
                },
                "required": ["calendar_details"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_calendar",
            "description": "Update an existing calendar by ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "The ID of the calendar to update."
                    },
                    "updated_calendar_details": {
                        "type": "object",
                        "description": "A dictionary containing updated calendar details."
                    },
                },
                "required": ["calendar_id", "updated_calendar_details"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_calendar",
            "description": "Delete a calendar by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "calendar_id": {
                        "type": "string",
                        "description": "The ID of the calendar to delete."
                    },
                },
                "required": ["calendar_id"],
            },
        },
    },
]

available_functions = {
    "get_next_calendar_event": get_next_calendar_event,
    "add_event": add_event,
    "update_event": update_event,
    "delete_event": delete_event,
    "list_events": list_events,
    "get_event": get_event,
    "clear_calendar": clear_calendar,
    "list_calendars": list_calendars,
    "create_calendar": create_calendar,
    "update_calendar": update_calendar,
    "delete_calendar": delete_calendar,
}
