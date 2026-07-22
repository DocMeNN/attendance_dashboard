# src/domain/analytics/comparisons.py

"""
Domain Comparison Analytics

Purpose
-------
Provides pure business logic for comparing attendance participation
and session metrics across multiple sessions.

Domain Rules
------------
- Attendance is participation of any kind within a session.
- A participant is Present when they participate.
- There is no Late classification.
- There is no Absent classification at session participation level.
- Attendance comparisons therefore focus on participation.

Responsibilities
----------------
- Compare attendance participation between sessions.
- Identify participation improvements and declines.
- Compare expected attendee counts.
- Compare present participant counts.
- Find best and worst performing sessions.
- Support trend analysis for higher application layers.

Rules
-----
- No pandas.
- No Streamlit.
- No database access.
- No file I/O.
- No infrastructure dependencies.
- No presentation logic.

Notes
-----
- Pure domain logic.
- Operates on immutable domain models.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Iterable

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.models.attendance_summary import AttendanceSummary

# ============================================================================
# Attendance Comparison
# ============================================================================


def compare_attendance(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> float:
    """
    Return the percentage-point difference in participation.

    Positive values indicate improvement.
    Negative values indicate decline.
    Zero indicates no change.
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
    Return True if participation improved.
    """

    return second.attendance_percentage > first.attendance_percentage


def attendance_declined(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> bool:
    """
    Return True if participation declined.
    """

    return second.attendance_percentage < first.attendance_percentage


def attendance_unchanged(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> bool:
    """
    Return True if participation remained unchanged.
    """

    return second.attendance_percentage == first.attendance_percentage


# ============================================================================
# Session Performance
# ============================================================================


def best_session(
    summaries: Iterable[AttendanceSummary],
) -> AttendanceSummary | None:
    """
    Return the session with the highest participation percentage.
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
    Return the session with the lowest participation percentage.
    """

    summaries = tuple(summaries)

    if not summaries:
        return None

    return min(
        summaries,
        key=lambda summary: summary.attendance_percentage,
    )


# ============================================================================
# Expected Attendee Comparison
# ============================================================================


def compare_expected_attendance(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> int:
    """
    Return the difference in expected attendee counts.

    Positive values indicate an increase.
    Negative values indicate a decrease.
    """

    return second.expected_attendees - first.expected_attendees


# ============================================================================
# Participation Comparison
# ============================================================================


def compare_present_count(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> int:
    """
    Return the difference in unique participants.

    Positive values indicate more participants
    in the second session.
    """

    return second.present_count - first.present_count


# ============================================================================
# Composite Comparison
# ============================================================================


def compare_sessions(
    first: AttendanceSummary,
    second: AttendanceSummary,
) -> dict[str, object]:
    """
    Return a complete comparison between two sessions.
    """

    percentage_difference = compare_attendance(
        first,
        second,
    )

    return {
        "first_session_date": first.session_date,
        "second_session_date": second.session_date,
        "attendance_difference": percentage_difference,
        "attendance_improved": percentage_difference > 0,
        "attendance_declined": percentage_difference < 0,
        "attendance_unchanged": percentage_difference == 0,
        "expected_attendees_difference": compare_expected_attendance(
            first,
            second,
        ),
        "present_count_difference": compare_present_count(
            first,
            second,
        ),
    }
