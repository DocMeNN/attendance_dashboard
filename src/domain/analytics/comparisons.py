# src/domain/analytics/comparisons.py

"""
Domain Comparison Analytics.

Purpose
-------
Provides business logic for comparing attendance summaries across
multiple sessions.

Responsibilities
----------------
- Compare attendance between sessions.
- Identify attendance improvements and declines.
- Find best and worst performing sessions.
- Support trend reporting for higher application layers.

Notes
-----
- Pure domain logic.
- No pandas.
- No Streamlit.
- No database access.
- No file I/O.
"""

from __future__ import annotations

# Standard library imports
from typing import Iterable

# Third-party imports
# None
# Local imports
from src.domain.models.attendance_summary import AttendanceSummary


def compare_attendance(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> float:
    """
    Return the percentage-point difference in attendance.

    Positive values indicate an increase.
    Negative values indicate a decrease.
    """
    return round(
        second.attendance_percentage - first.attendance_percentage,
        2,
    )


def attendance_improved(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> bool:
    """
    Return True if attendance improved.
    """
    return second.attendance_percentage > first.attendance_percentage


def attendance_declined(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> bool:
    """
    Return True if attendance declined.
    """
    return second.attendance_percentage < first.attendance_percentage


def attendance_unchanged(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> bool:
    """
    Return True if attendance remained unchanged.
    """
    return second.attendance_percentage == first.attendance_percentage


def best_session(
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


def worst_session(
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


def compare_expected_attendance(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> int:
    """
    Return the difference in expected attendees.
    """
    return second.expected_attendees - first.expected_attendees


def compare_present_count(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> int:
    """
    Return the difference in members present.
    """
    return second.present_count - first.present_count


def compare_absent_count(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> int:
    """
    Return the difference in absentees.
    """
    return second.absent_count - first.absent_count
