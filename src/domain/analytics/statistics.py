# filepath: src/domain/analytics/statistics.py

"""
Domain Statistics Analytics.

Purpose
-------
Provides aggregate statistics across multiple attendance summaries.

Rules
-----
- No pandas
- No Streamlit
- No database access
- No file I/O
- Pure domain logic only.
"""

from __future__ import annotations

from typing import Iterable

from src.domain.models.attendance_summary import AttendanceSummary


def average_attendance(
    summaries: Iterable[AttendanceSummary],
) -> float:
    """
    Return the average attendance percentage across sessions.
    """
    summaries = tuple(summaries)

    if not summaries:
        return 0.0

    return round(
        sum(summary.attendance_percentage for summary in summaries) / len(summaries),
        2,
    )


def highest_attendance(
    summaries: Iterable[AttendanceSummary],
) -> AttendanceSummary | None:
    """
    Return the session with the highest attendance percentage.
    """
    summaries = tuple(summaries)

    if not summaries:
        return None

    return max(
        summaries,
        key=lambda summary: summary.attendance_percentage,
    )


def lowest_attendance(
    summaries: Iterable[AttendanceSummary],
) -> AttendanceSummary | None:
    """
    Return the session with the lowest attendance percentage.
    """
    summaries = tuple(summaries)

    if not summaries:
        return None

    return min(
        summaries,
        key=lambda summary: summary.attendance_percentage,
    )


def total_expected_attendees(
    summaries: Iterable[AttendanceSummary],
) -> int:
    """
    Return the total expected attendees across sessions.
    """
    return sum(summary.expected_attendees for summary in summaries)


def total_present(
    summaries: Iterable[AttendanceSummary],
) -> int:
    """
    Return the total number of attendees present.
    """
    return sum(summary.present_count for summary in summaries)


def total_absent(
    summaries: Iterable[AttendanceSummary],
) -> int:
    """
    Return the total number of absentees.
    """
    return sum(summary.absent_count for summary in summaries)


def total_activities(
    summaries: Iterable[AttendanceSummary],
) -> int:
    """
    Return the total recorded activities.
    """
    return sum(summary.activity_event_count for summary in summaries)


def total_attendance_events(
    summaries: Iterable[AttendanceSummary],
) -> int:
    """
    Return the total attendance events.
    """
    return sum(summary.attendance_event_count for summary in summaries)


def sessions_with_quorum(
    summaries: Iterable[AttendanceSummary],
) -> tuple[AttendanceSummary, ...]:
    """
    Return all sessions that achieved quorum.
    """
    return tuple(summary for summary in summaries if summary.has_quorum)


def full_attendance_sessions(
    summaries: Iterable[AttendanceSummary],
) -> tuple[AttendanceSummary, ...]:
    """
    Return all sessions with full attendance.
    """
    return tuple(summary for summary in summaries if summary.is_full_attendance)
