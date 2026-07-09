# src/domain/models/dashboard_metrics.py

"""
Dashboard Metrics Domain Model

Purpose:
    Represents the complete set of metrics required by the
    presentation layer.

Responsibilities:
    - Transport dashboard metrics.
    - Remain immutable.
    - Remain technology independent.

Notes:
    - DTO (Data Transfer Object).
    - Contains no business logic.
    - Contains no UI, pandas or infrastructure dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True, slots=True)
class DashboardMetrics:
    """
    Immutable dashboard metrics.

    This object is the single source of data for the
    presentation layer.
    """

    session_date: date

    expected_attendees: int

    present_count: int

    absent_count: int

    attendance_percentage: float

    activity_count: int

    first_attendee: str | None = None

    session_duration: str = "00:00:00"

    total_messages: int = 0

    total_attendance_events: int = 0

    total_activity_events: int = 0

    leaderboard: tuple[str, ...] = field(default_factory=tuple)

    attendance_trend: tuple[float, ...] = field(default_factory=tuple)

    activity_breakdown: dict[str, int] = field(default_factory=dict)

    summary_cards: dict[str, str | int | float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate dashboard metrics."""

        if self.expected_attendees < 0:
            raise ValueError("expected_attendees cannot be negative.")

        if self.present_count < 0:
            raise ValueError("present_count cannot be negative.")

        if self.absent_count < 0:
            raise ValueError("absent_count cannot be negative.")

        if not 0 <= self.attendance_percentage <= 100:
            raise ValueError("attendance_percentage must be between 0 and 100.")

    @property
    def has_attendance(self) -> bool:
        """Return True if attendance exists."""
        return self.present_count > 0

    @property
    def has_activities(self) -> bool:
        """Return True if activities exist."""
        return self.activity_count > 0

    @property
    def is_empty(self) -> bool:
        """Return True if dashboard has no data."""
        return (
            self.total_messages == 0
            and self.present_count == 0
            and self.activity_count == 0
        )

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "session_date": self.session_date,
            "expected_attendees": self.expected_attendees,
            "present_count": self.present_count,
            "absent_count": self.absent_count,
            "attendance_percentage": self.attendance_percentage,
            "activity_count": self.activity_count,
            "first_attendee": self.first_attendee,
            "session_duration": self.session_duration,
            "total_messages": self.total_messages,
            "total_attendance_events": self.total_attendance_events,
            "total_activity_events": self.total_activity_events,
            "leaderboard": self.leaderboard,
            "attendance_trend": self.attendance_trend,
            "activity_breakdown": self.activity_breakdown,
            "summary_cards": self.summary_cards,
        }

    def __str__(self) -> str:
        """Return readable representation."""
        return (
            f"DashboardMetrics("
            f"attendance={self.attendance_percentage:.2f}%, "
            f"present={self.present_count}, "
            f"activities={self.activity_count})"
        )
