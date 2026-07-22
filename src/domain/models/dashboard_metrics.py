"""
Dashboard Metrics Domain Model

Purpose
-------
Represents the complete set of metrics required by
the presentation layer.

Responsibilities
----------------
- Transport dashboard metrics.
- Represent participation-based attendance.
- Represent activity statistics.
- Represent Done acknowledgement statistics.
- Remain immutable.
- Remain technology independent.

Domain Rules
------------
- Attendance is based on participation within a session.
- Present count represents unique participants.
- Done acknowledgements are independent acknowledgement events.
- Activity count represents total activity events.
- Unique activity count represents distinct activity types.
- Activity breakdown represents value counts by activity type.

Notes
-----
- Immutable.
- DTO-style transport object.
- Contains no UI, pandas or infrastructure dependencies.

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass, field
from datetime import date

# ============================================================================
# Dashboard Metrics
# ============================================================================


@dataclass(frozen=True, slots=True)
class DashboardMetrics:
    """
    Immutable dashboard metrics.

    This object is the single source of metric data
    for the presentation layer.
    """

    session_date: date

    expected_attendees: int

    present_count: int

    absent_count: int

    attendance_percentage: float

    # ------------------------------------------------------------------
    # Activity Metrics
    # ------------------------------------------------------------------

    activity_count: int = 0

    unique_activity_count: int = 0

    activity_breakdown: dict[str, int] = field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Done Metrics
    # ------------------------------------------------------------------

    done_count: int = 0

    # ------------------------------------------------------------------
    # Session Metrics
    # ------------------------------------------------------------------

    first_attendee: str | None = None

    session_duration: str = "00:00:00"

    # ------------------------------------------------------------------
    # General Metrics
    # ------------------------------------------------------------------

    total_messages: int = 0

    total_attendance_events: int = 0

    total_activity_events: int = 0

    # ------------------------------------------------------------------
    # Longitudinal / Presentation Metrics
    # ------------------------------------------------------------------

    leaderboard: tuple[str, ...] = field(
        default_factory=tuple,
    )

    attendance_trend: tuple[float, ...] = field(
        default_factory=tuple,
    )

    summary_cards: dict[str, str | int | float] = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:
        """Validate dashboard metrics."""

        if self.expected_attendees < 0:
            raise ValueError(
                "expected_attendees cannot be negative.",
            )

        if self.present_count < 0:
            raise ValueError(
                "present_count cannot be negative.",
            )

        if self.absent_count < 0:
            raise ValueError(
                "absent_count cannot be negative.",
            )

        if not 0 <= self.attendance_percentage <= 100:
            raise ValueError(
                "attendance_percentage must be between 0 and 100.",
            )

        if self.activity_count < 0:
            raise ValueError(
                "activity_count cannot be negative.",
            )

        if self.unique_activity_count < 0:
            raise ValueError(
                "unique_activity_count cannot be negative.",
            )

        if self.done_count < 0:
            raise ValueError(
                "done_count cannot be negative.",
            )

        if self.total_messages < 0:
            raise ValueError(
                "total_messages cannot be negative.",
            )

        if self.total_attendance_events < 0:
            raise ValueError(
                "total_attendance_events cannot be negative.",
            )

        if self.total_activity_events < 0:
            raise ValueError(
                "total_activity_events cannot be negative.",
            )

        if any(count < 0 for count in self.activity_breakdown.values()):
            raise ValueError(
                "activity_breakdown counts cannot be negative.",
            )

    # =========================================================================
    # Attendance
    # =========================================================================

    @property
    def has_attendance(self) -> bool:
        """Return True if participation exists."""

        return self.present_count > 0

    @property
    def has_absentees(self) -> bool:
        """Return True if expected members did not participate."""

        return self.absent_count > 0

    # =========================================================================
    # Activities
    # =========================================================================

    @property
    def has_activities(self) -> bool:
        """Return True if activity events exist."""

        return self.activity_count > 0

    @property
    def has_multiple_activity_types(self) -> bool:
        """Return True if multiple activity types exist."""

        return self.unique_activity_count > 1

    # =========================================================================
    # Done Acknowledgements
    # =========================================================================

    @property
    def has_done(self) -> bool:
        """Return True if Done acknowledgements exist."""

        return self.done_count > 0

    # =========================================================================
    # State
    # =========================================================================

    @property
    def is_empty(self) -> bool:
        """Return True if the dashboard contains no meaningful data."""

        return (
            self.total_messages == 0
            and self.present_count == 0
            and self.activity_count == 0
            and self.done_count == 0
        )

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "session_date": self.session_date,
            "expected_attendees": self.expected_attendees,
            "present_count": self.present_count,
            "absent_count": self.absent_count,
            "attendance_percentage": self.attendance_percentage,
            "activity_count": self.activity_count,
            "unique_activity_count": self.unique_activity_count,
            "activity_breakdown": self.activity_breakdown,
            "done_count": self.done_count,
            "first_attendee": self.first_attendee,
            "session_duration": self.session_duration,
            "total_messages": self.total_messages,
            "total_attendance_events": self.total_attendance_events,
            "total_activity_events": self.total_activity_events,
            "leaderboard": self.leaderboard,
            "attendance_trend": self.attendance_trend,
            "summary_cards": self.summary_cards,
        }

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __str__(self) -> str:
        """Return readable representation."""

        return (
            "DashboardMetrics("
            f"attendance={self.attendance_percentage:.2f}%, "
            f"present={self.present_count}, "
            f"activities={self.activity_count}, "
            f"unique_activities={self.unique_activity_count}, "
            f"done={self.done_count})"
        )
