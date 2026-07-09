# src/domain/analytics/attendance.py

"""
Domain Attendance Analytics.

This module contains pure business logic for calculating attendance
statistics and summaries.

Rules
-----
- No pandas
- No Streamlit
- No file I/O
- No database access
- No logging

All functions operate on immutable Domain models.
"""

from __future__ import annotations

from collections import Counter
from typing import Iterable

from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.attendance_summary import AttendanceSummary
from src.domain.models.member import Member


def get_attendees(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return every attendance event where the member attended.

    Parameters
    ----------
    attendance_events:
        Collection of attendance events.

    Returns
    -------
    tuple[AttendanceEvent, ...]
        Attendance events marked as PRESENT or LATE.
    """
    return tuple(
        event
        for event in attendance_events
        if event.attendance_type in (AttendanceType.PRESENT, AttendanceType.LATE)
    )


def get_absentees(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendance events marked absent.
    """
    return tuple(
        event
        for event in attendance_events
        if event.attendance_type == AttendanceType.ABSENT
    )


def get_late_members(
    attendance_events: Iterable[AttendanceEvent],
) -> tuple[AttendanceEvent, ...]:
    """
    Return attendance events marked late.
    """
    return tuple(
        event
        for event in attendance_events
        if event.attendance_type == AttendanceType.LATE
    )


def calculate_attendance_rate(
    attendance_events: Iterable[AttendanceEvent],
) -> float:
    """
    Calculate attendance percentage for a session.

    Attendance Rate =
        (Present + Late) / Total × 100

    Returns
    -------
    float
        Attendance percentage.
    """
    events = tuple(attendance_events)

    if not events:
        return 0.0

    attendees = len(get_attendees(events))

    return (attendees / len(events)) * 100.0


def calculate_member_attendance_rate(
    member: Member,
    attendance_events: Iterable[AttendanceEvent],
) -> float:
    """
    Calculate one member's attendance percentage.
    """
    member_events = tuple(
        event for event in attendance_events if event.member_id == member.id
    )

    if not member_events:
        return 0.0

    attended = sum(
        event.attendance_type in (AttendanceType.PRESENT, AttendanceType.LATE)
        for event in member_events
    )

    return (attended / len(member_events)) * 100.0


def summarize_attendance(
    attendance_events: Iterable[AttendanceEvent],
) -> AttendanceSummary:
    """
    Build an AttendanceSummary from attendance events.
    """
    events = tuple(attendance_events)

    counts = Counter(event.attendance_type for event in events)

    total = len(events)

    return AttendanceSummary(
        total_members=total,
        present=counts.get(AttendanceType.PRESENT, 0),
        late=counts.get(AttendanceType.LATE, 0),
        absent=counts.get(AttendanceType.ABSENT, 0),
        attendance_rate=calculate_attendance_rate(events),
    )
