# src/domain/analytics/attendance.py

"""
Domain Attendance Analytics

Purpose
-------
Provides pure business logic for attendance-related calculations.

Responsibilities
----------------
- Filter attendance events.
- Calculate attendance statistics.
- Count attendance classifications.
- Remain technology independent.

Rules
-----
- No pandas.
- No Streamlit.
- No file I/O.
- No database access.
- No infrastructure dependencies.

Notes
-----
- Operates only on immutable Domain models.
- Does not construct AttendanceSummary objects.
- AttendanceSummary is derived from a Session model.
"""

from __future__ import annotations

# Standard library imports
from collections import Counter
from typing import Iterable

# Third-party imports
# None
# Local imports
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.member import Member


def get_present_events(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendance events marked as present.
    """
    return tuple(event for event in attendance_events if event.is_present)


def get_late_events(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendance events marked as late.
    """
    return tuple(event for event in attendance_events if event.is_late)


def get_absent_events(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendance events marked as absent.
    """
    return tuple(event for event in attendance_events if event.is_absent)


def get_attendees(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[str, ...]:
    """
    Return unique attendee names preserving
    chronological order.
    """
    seen: set[str] = set()
    attendees: list[str] = []

    for event in attendance_events:
        if event.is_absent:
            continue

        key = event.attendee.casefold()

        if key not in seen:
            seen.add(key)
            attendees.append(event.attendee)

    return tuple(attendees)


def calculate_attendance_rate(
    attendance_events: Iterable[AttendanceEvent],
    expected_attendees: int,
) -> float:
    """
    Calculate attendance percentage.

    Parameters
    ----------
    attendance_events:
        Attendance events.

    expected_attendees:
        Total expected attendees.

    Returns
    -------
    float
        Attendance percentage.
    """
    if expected_attendees <= 0:
        return 0.0

    present = len(get_attendees(attendance_events))

    return round(
        (present / expected_attendees) * 100,
        2,
    )


def calculate_member_attendance_rate(
    member: Member,
    attendance_events: Iterable[AttendanceEvent],
) -> float:
    """
    Calculate attendance rate for a member.

    The current domain model represents attendance
    using attendee names, so comparison is performed
    using normalized names.
    """
    member_events = tuple(
        event
        for event in attendance_events
        if event.attendee.casefold() == member.normalized_name
    )

    if not member_events:
        return 0.0

    attended = sum(event.is_present or event.is_late for event in member_events)

    return round(
        (attended / len(member_events)) * 100,
        2,
    )


def count_attendance_types(
    attendance_events: Iterable[AttendanceEvent],
) -> Counter[AttendanceType]:
    """
    Count attendance events by AttendanceType.
    """
    return Counter(event.attendance_type for event in attendance_events)
