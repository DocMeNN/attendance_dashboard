# src/domain/models/attendance_summary.py

"""
Attendance Summary Domain Model

Purpose:
    Represents the final attendance summary for a meeting session.

Responsibilities:
    - Provide summary statistics.
    - Provide attendance metrics.
    - Expose business-friendly summary information.
    - Remain technology independent.

Notes:
    - Immutable.
    - Built from a Session.
    - Contains no UI, pandas or infrastructure dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from .session import Session


@dataclass(frozen=True, slots=True)
class AttendanceSummary:
    """
    Immutable attendance summary.

    Attributes:
        session:
            Session from which the summary is derived.

        expected_attendees:
            Expected number of attendees.
    """

    session: Session
    expected_attendees: int

    def __post_init__(self) -> None:
        """Validate the summary."""

        if not isinstance(self.session, Session):
            raise TypeError("session must be a Session.")

        if self.expected_attendees < 0:
            raise ValueError("expected_attendees cannot be negative.")

    # ------------------------------------------------------------------
    # Session Information
    # ------------------------------------------------------------------

    @property
    def session_date(self) -> date:
        """Return session date."""
        return self.session.session_date

    @property
    def start_time(self) -> datetime | None:
        """Return meeting start time."""
        return self.session.start_time

    @property
    def end_time(self) -> datetime | None:
        """Return meeting end time."""
        return self.session.end_time

    @property
    def duration(self) -> timedelta:
        """Return meeting duration."""
        return self.session.duration

    # ------------------------------------------------------------------
    # Attendance Statistics
    # ------------------------------------------------------------------

    @property
    def attendees(self) -> tuple[str, ...]:
        """Return attendees."""
        return self.session.unique_attendees

    @property
    def present_count(self) -> int:
        """Return number of attendees present."""
        return self.session.attendee_count

    @property
    def absent_count(self) -> int:
        """Return number of absentees."""

        return max(
            self.expected_attendees - self.present_count,
            0,
        )

    @property
    def attendance_percentage(self) -> float:
        """Return attendance percentage."""

        if self.expected_attendees == 0:
            return 0.0

        return round(
            (self.present_count / self.expected_attendees) * 100,
            2,
        )

    @property
    def absentee_percentage(self) -> float:
        """Return absentee percentage."""

        if self.expected_attendees == 0:
            return 0.0

        return round(
            (self.absent_count / self.expected_attendees) * 100,
            2,
        )

    # ------------------------------------------------------------------
    # Session Statistics
    # ------------------------------------------------------------------

    @property
    def first_attendee(self) -> str | None:
        """Return first attendee."""
        return self.session.first_attendee

    @property
    def attendance_events(self):
        """Return attendance events."""
        return self.session.attendance_events

    @property
    def activity_events(self):
        """Return activity events."""
        return self.session.activity_events

    @property
    def attendance_event_count(self) -> int:
        """Return attendance event count."""
        return self.session.attendance_count

    @property
    def activity_event_count(self) -> int:
        """Return activity event count."""
        return self.session.activity_count

    @property
    def total_event_count(self) -> int:
        """Return total event count."""
        return self.session.total_events

    @property
    def has_quorum(self) -> bool:
        """
        Return True if attendance is at least 50%.
        """

        if self.expected_attendees == 0:
            return False

        return self.present_count >= (self.expected_attendees / 2)

    @property
    def is_full_attendance(self) -> bool:
        """Return True if everyone attended."""

        return (
            self.expected_attendees > 0
            and self.present_count == self.expected_attendees
        )

    @property
    def is_empty(self) -> bool:
        """Return True if no attendance exists."""
        return self.present_count == 0

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "session_date": self.session_date,
            "expected_attendees": self.expected_attendees,
            "present_count": self.present_count,
            "absent_count": self.absent_count,
            "attendance_percentage": self.attendance_percentage,
            "absentee_percentage": self.absentee_percentage,
            "first_attendee": self.first_attendee,
            "duration": str(self.duration),
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Return number of attendees present."""
        return self.present_count

    def __bool__(self) -> bool:
        """Return True if attendance exists."""
        return self.present_count > 0

    def __str__(self) -> str:
        """Return readable representation."""

        return (
            f"AttendanceSummary("
            f"date={self.session_date}, "
            f"present={self.present_count}, "
            f"expected={self.expected_attendees}, "
            f"attendance={self.attendance_percentage:.2f}%)"
        )
