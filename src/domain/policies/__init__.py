# src/domain/policies/__init__.py

"""
Domain Policies Package

Purpose
-------
Provides centralized business rules for the OYBS domain.

Responsibilities
----------------
- Expose domain policy functions.
- Centralize policy-level business rules.
- Keep business rules independent of application,
  infrastructure, presentation, and external frameworks.

Policies
--------
Activity Policy:
    Determines how messages become domain activities.

Attendance Policy:
    Determines how participation is classified as attendance.

Notes
-----
- Domain layer only.
- No UI dependencies.
- No pandas dependencies.
- No infrastructure dependencies.
- No parsing logic.
"""

from .activity_policy import (
    ACTIVITY_ANNOUNCEMENT,
    ACTIVITY_DISCUSSION,
    ACTIVITY_DONE,
    ACTIVITY_INSIGHT,
    ACTIVITY_PRAYER_SESSION,
    ACTIVITY_SCRIPTURE_READING,
    classify_activity,
    is_announcement_activity,
    is_done_activity,
    is_insight_activity,
    is_prayer_session_closing,
    is_prayer_session_opening,
    is_scripture_reading_activity,
    is_session_boundary_activity,
    is_supported_activity,
    normalize_message,
    starts_with_keyword,
    supported_activity_names,
)
from .attendance_policy import (
    attendance_from_activity,
    attendance_from_done,
    attendance_from_message,
    attendance_summary,
    classify_attendance,
    count_participants,
    count_present_participants,
    is_participating_sender,
    is_participation_message,
    is_present,
    participating_senders,
    unique_attendance_events,
)

__all__ = [
    "ACTIVITY_ANNOUNCEMENT",
    "ACTIVITY_DISCUSSION",
    "ACTIVITY_DONE",
    "ACTIVITY_INSIGHT",
    "ACTIVITY_PRAYER_SESSION",
    "ACTIVITY_SCRIPTURE_READING",
    "attendance_from_activity",
    "attendance_from_done",
    "attendance_from_message",
    "attendance_summary",
    "classify_activity",
    "classify_attendance",
    "count_participants",
    "count_present_participants",
    "is_announcement_activity",
    "is_done_activity",
    "is_insight_activity",
    "is_participating_sender",
    "is_participation_message",
    "is_prayer_session_closing",
    "is_prayer_session_opening",
    "is_present",
    "is_scripture_reading_activity",
    "is_session_boundary_activity",
    "is_supported_activity",
    "normalize_message",
    "participating_senders",
    "starts_with_keyword",
    "supported_activity_names",
    "unique_attendance_events",
]
