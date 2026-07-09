# src/domain/models/session.py

"""
Session Domain Model

Purpose:
    Represents a complete meeting session.

Responsibilities:
    - Aggregate attendance events.
    - Aggregate activity events.
    - Provide session-level business behaviour.
    - Remain technology independent.

Notes:
    - Immutable.
    - Aggregate Root of the Domain.
    - Contains no UI, pandas or infrastructure dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta

from .activity_event import ActivityEvent
from .attendance_event import AttendanceEvent


@dataclass(frozen=True, slots=True)
class Session:
    """
    Immutable meeting session.
    """

    session_date: date
    attendance_events: tuple[AttendanceEvent, ...] = field(default_factory=tuple)
    activity_events: tuple[ActivityEvent, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        """Validate session."""

        if not isinstance(self.session_date, date):
            raise TypeError("session_date must be a date.")

        attendance = tuple(
            sorted(
                self.attendance_events,
                key=lambda event: event.timestamp,
            )
        )

        activity = tuple(
            sorted(
                self.activity_events,
                key=lambda event: event.timestamp,
            )
        )

        object.__setattr__(self, "attendance_events", attendance)
        object.__setattr__(self, "activity_events", activity)

    # ------------------------------------------------------------------
    # Counts
    # ------------------------------------------------------------------

    @property
    def attendance_count(self) -> int:
        """Return attendance event count."""
        return len(self.attendance_events)

    @property
    def activity_count(self) -> int:
        """Return activity event count."""
        return len(self.activity_events)

    @property
    def total_events(self) -> int:
        """Return total events."""
        return self.attendance_count + self.activity_count

    # ------------------------------------------------------------------
    # Attendance
    # ------------------------------------------------------------------

    @property
    def attendees(self) -> tuple[str, ...]:
        """Return attendees in chronological order."""
        return tuple(event.attendee for event in self.attendance_events)

    @property
    def unique_attendees(self) -> tuple[str, ...]:
        """Return unique attendees preserving order."""

        seen: set[str] = set()
        members: list[str] = []

        for event in self.attendance_events:
            key = event.attendee.casefold()

            if key not in seen:
                seen.add(key)
                members.append(event.attendee)

        return tuple(members)

    @property
    def attendee_count(self) -> int:
        """Return unique attendee count."""
        return len(self.unique_attendees)

    @property
    def first_attendance(self) -> AttendanceEvent | None:
        """Return first attendance event."""
        return self.attendance_events[0] if self.attendance_events else None

    @property
    def last_attendance(self) -> AttendanceEvent | None:
        """Return last attendance event."""
        return self.attendance_events[-1] if self.attendance_events else None

    @property
    def first_attendee(self) -> str | None:
        """Return first attendee."""
        event = self.first_attendance
        return event.attendee if event else None

    # ------------------------------------------------------------------
    # Activities
    # ------------------------------------------------------------------

    @property
    def first_activity(self) -> ActivityEvent | None:
        """Return first activity."""
        return self.activity_events[0] if self.activity_events else None

    @property
    def last_activity(self) -> ActivityEvent | None:
        """Return last activity."""
        return self.activity_events[-1] if self.activity_events else None

    # ------------------------------------------------------------------
    # Timeline
    # ------------------------------------------------------------------

    @property
    def start_time(self) -> datetime | None:
        """Return first recorded event."""

        events = [*self.attendance_events] + [*self.activity_events]

        if not events:
            return None

        return min(event.timestamp for event in events)

    @property
    def end_time(self) -> datetime | None:
        """Return last recorded event."""

        events = [*self.attendance_events] + [*self.activity_events]

        if not events:
            return None

        return max(event.timestamp for event in events)

    @property
    def duration(self) -> timedelta:
        """Return session duration."""

        if self.start_time is None or self.end_time is None:
            return timedelta(0)

        return self.end_time - self.start_time

    @property
    def has_attendance(self) -> bool:
        """Return True if attendance exists."""
        return bool(self.attendance_events)

    @property
    def has_activities(self) -> bool:
        """Return True if activities exist."""
        return bool(self.activity_events)

    @property
    def is_empty(self) -> bool:
        """Return True if session has no events."""
        return self.total_events == 0

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def attendee_exists(self, attendee: str) -> bool:
        """Return True if attendee exists."""
        return attendee.casefold() in {
            member.casefold() for member in self.unique_attendees
        }

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "session_date": self.session_date,
            "attendance_count": self.attendance_count,
            "activity_count": self.activity_count,
            "attendee_count": self.attendee_count,
            "duration": str(self.duration),
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Return total number of events."""
        return self.total_events

    def __bool__(self) -> bool:
        """Return True if session contains events."""
        return not self.is_empty

    def __str__(self) -> str:
        """Return readable representation."""
        return (
            f"Session("
            f"date={self.session_date}, "
            f"attendees={self.attendee_count}, "
            f"activities={self.activity_count})"
        )
