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
- Provide chronological attendance analytics.
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

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from typing import Iterable

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.member import Member

# ============================================================================
# Attendance Event Filters
# ============================================================================


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


# ============================================================================
# Attendees
# ============================================================================


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

        if key in seen:
            continue

        seen.add(key)
        attendees.append(event.attendee)

    return tuple(attendees)


def get_unique_attendees(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[str, ...]:
    """
    Return unique attendees.

    Alias for get_attendees() to provide a clearer
    analytics-oriented API.
    """

    return get_attendees(
        attendance_events,
    )


def count_unique_attendees(
    attendance_events: Iterable[AttendanceEvent],
) -> int:
    """
    Return the number of unique attendees.
    """

    return len(
        get_attendees(
            attendance_events,
        )
    )


# ============================================================================
# Chronological Analytics
# ============================================================================


def get_attendance_timeline(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendance events ordered
    chronologically.

    Events are sorted using the original
    WhatsApp message timestamp.
    """

    return tuple(
        sorted(
            attendance_events,
            key=lambda event: event.timestamp,
        )
    )


def get_first_arrivals(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendees ordered from
    earliest arrival to latest arrival.

    Duplicate attendee records are removed,
    preserving the first occurrence only.
    """

    timeline = get_attendance_timeline(
        attendance_events,
    )

    seen: set[str] = set()

    arrivals: list[AttendanceEvent] = []

    for event in timeline:

        if event.is_absent:
            continue

        key = event.attendee.casefold()

        if key in seen:
            continue

        seen.add(key)
        arrivals.append(event)

    return tuple(arrivals)


# ============================================================================
# Reverse Chronological Analytics
# ============================================================================


def get_latest_arrivals(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendees ordered from
    latest arrival to earliest arrival.

    Duplicate attendee records are removed,
    preserving the latest occurrence only.
    """

    timeline = reversed(
        get_attendance_timeline(
            attendance_events,
        )
    )

    seen: set[str] = set()

    arrivals: list[AttendanceEvent] = []

    for event in timeline:

        if event.is_absent:
            continue

        key = event.attendee.casefold()

        if key in seen:
            continue

        seen.add(key)
        arrivals.append(event)

    return tuple(arrivals)


def count_attendance_events(
    attendance_events: Iterable[AttendanceEvent],
) -> int:
    """
    Return the total number of attendance events.
    """

    return sum(1 for _ in attendance_events)


# ============================================================================
# Attendance Statistics
# ============================================================================


def calculate_attendance_rate(
    attendance_events: Iterable[AttendanceEvent],
    expected_attendees: int,
) -> float:
    """
    Calculate attendance percentage.
    """

    if expected_attendees <= 0:
        return 0.0

    present = count_unique_attendees(
        attendance_events,
    )

    return round(
        (present / expected_attendees) * 100,
        2,
    )


def calculate_member_attendance_rate(
    member: Member,
    attendance_events: Iterable[AttendanceEvent],
) -> float:
    """
    Calculate attendance percentage
    for a single member.
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


# ============================================================================
# Attendance Classification
# ============================================================================


def count_attendance_types(
    attendance_events: Iterable[AttendanceEvent],
) -> Counter[AttendanceType]:
    """
    Count attendance events grouped by
    AttendanceType.
    """

    return Counter(event.attendance_type for event in attendance_events)
