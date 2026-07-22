# src/domain/enums/activity_type.py
# MeRulz 001: Complete file replacement only. Do not patch partial sections.

"""
Activity Type Enumeration

Purpose
-------
Defines the canonical activity types recognized by the
Online Bible Study community analytics platform.

Domain Context
--------------
This platform analyzes participation in an online Bible Study
community. It is not a church service analytics system.

Canonical Activity Types
------------------------
- Scripture Reading
- Insight
- Discussion
- Announcement
- Done
- Prayer Session

Session Boundary Markers
------------------------
Opening Prayer and Closing Prayer are not independent activity
types.

They are session boundary markers used to identify a Prayer Session:

    Opening Prayer -> Prayer Session begins
    Closing Prayer -> Prayer Session ends

The domain may therefore detect prayer sessions using these
markers without representing them as separate ActivityType values.

Rules
-----
- No WORSHIP activity.
- No generic MESSAGE activity.
- No OFFERING activity.
- DONE represents a Scripture Reading acknowledgement.
- PRAYER_SESSION represents a prayer meeting/session.
"""

from __future__ import annotations

from enum import Enum


class ActivityType(str, Enum):
    """
    Canonical activity types in the Online Bible Study community.
    """

    SCRIPTURE_READING = "Scripture Reading"

    INSIGHT = "Insight"

    DISCUSSION = "Discussion"

    ANNOUNCEMENT = "Announcement"

    DONE = "Done"

    PRAYER_SESSION = "Prayer Session"

    def __str__(self) -> str:
        """Return the human-readable activity name."""

        return self.value
