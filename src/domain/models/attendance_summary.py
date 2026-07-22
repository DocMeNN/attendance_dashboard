"""
Attendance Summary Domain Model

Purpose
-------
Represents the final attendance and participation summary
for a meeting session.

Responsibilities
----------------
- Provide session participation statistics.
- Provide attendance metrics.
- Expose activity metrics.
- Expose Done acknowledgement metrics.
- Remain technology independent.

Domain Rules
------------
- Attendance means participation of any kind within a session.
- A participant is considered present if they participate in the session.
- Presence is based on unique participants.
- Done acknowledgements are separate from session attendance.
- A Done acknowledgement may exist independently of a session.
- Activity metrics are session-scoped.
- Activity counts preserve event totals and value counts by activity type.

Notes
-----
- Immutable.
- Built from a Session.
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
from dataclasses import dataclass
from datetime import date, datetime, timedelta

# ============================================================================
# Local Imports
# ============================================================================
from .session import Session

# ============================================================================
# Attendance Summary
# ============================================================================


@dataclass(frozen=True, slots=True)
class AttendanceSummary:
    """
    Immutable attendance and participation summary.

    Attributes
    ----------
    session:
        Session from which the summary is derived.

    expected_attendees:
        Expected number of members in the attendance population.

    Notes
    -----
    The summary intentionally treats session participation as attendance.

    Therefore, any participant who generates a qualifying participation
    event within the session is considered present.
    """

    session: Session
    expected_attendees: int

    def __post_init__(self) -> None:
        """Validate the summary."""

        if not isinstance(self.session, Session):
            raise TypeError("session must be a Session.")

        if self.expected_attendees < 0:
            raise ValueError(
                "expected_attendees cannot be negative.",
            )

    # =========================================================================
    # Session Information
    # =========================================================================

    @property
    def session_date(self) -> date:
        """Return session date."""

        return self.session.session_date

    @property
    def start_time(self) -> datetime | None:
        """Return session start time."""

        return self.session.start_time

    @property
    def end_time(self) -> datetime | None:
        """Return session end time."""

        return self.session.end_time

    @property
    def duration(self) -> timedelta:
        """Return session duration."""

        return self.session.duration

    # =========================================================================
    # Participation / Attendance
    # =========================================================================

    @property
    def attendees(self) -> tuple[str, ...]:
        """
        Return unique participants in the session.

        Participation of any kind within the session
        qualifies the participant as present.
        """

        return self.session.unique_attendees

    @property
    def present_count(self) -> int:
        """
        Return number of unique participants.

        Attendance is participation of any kind
        within the session.
        """

        return self.session.attendee_count

    @property
    def absent_count(self) -> int:
        """
        Return number of expected members who did not participate.

        This is a population-based calculation and does not represent
        an explicit ABSENT event from the WhatsApp export.
        """

        return max(
            self.expected_attendees - self.present_count,
            0,
        )

    @property
    def attendance_percentage(self) -> float:
        """Return participation-based attendance percentage."""

        if self.expected_attendees == 0:
            return 0.0

        return round(
            (self.present_count / self.expected_attendees) * 100,
            2,
        )

    @property
    def absentee_percentage(self) -> float:
        """Return percentage of expected members who did not participate."""

        if self.expected_attendees == 0:
            return 0.0

        return round(
            (self.absent_count / self.expected_attendees) * 100,
            2,
        )

    # =========================================================================
    # Attendance Event Statistics
    # =========================================================================

    @property
    def attendance_events(self):
        """
        Return all attendance participation events.

        This represents event-level participation and may contain
        multiple events for the same participant.
        """

        return self.session.attendance_events

    @property
    def attendance_event_count(self) -> int:
        """Return total participation event count."""

        return self.session.attendance_count

    @property
    def first_attendee(self) -> str | None:
        """Return the first participant in the session."""

        return self.session.first_attendee

    # =========================================================================
    # Done Acknowledgement Statistics
    # =========================================================================

    @property
    def done_events(self):
        """
        Return Done acknowledgement events associated with the session.

        Done events are separate from attendance participation.
        """

        return self.session.done_events

    @property
    def done_count(self) -> int:
        """
        Return number of Done acknowledgements in the session.

        Each Done acknowledgement is counted independently.
        """

        return self.session.done_count

    @property
    def first_done(self):
        """Return the first Done acknowledgement in the session."""

        return self.session.first_done

    @property
    def last_done(self):
        """Return the last Done acknowledgement in the session."""

        return self.session.last_done

    # =========================================================================
    # Activity Statistics
    # =========================================================================

    @property
    def activity_events(self):
        """Return all activity events in the session."""

        return self.session.activity_events

    @property
    def activity_event_count(self) -> int:
        """Return total activity event count."""

        return self.session.activity_count

    @property
    def unique_activity_count(self) -> int:
        """
        Return number of unique activity types in the session.
        """

        return len(self.activity_value_counts)

    @property
    def activity_value_counts(self) -> dict[str, int]:
        """
        Return value counts for activity types.

        Example
        -------
        {
            "SCRIPTURE_READING": 1,
            "OPENING_PRAYER": 1,
            "MESSAGE": 2,
        }
        """

        counts: dict[str, int] = {}

        for event in self.activity_events:
            key = event.activity_type.value

            counts[key] = counts.get(key, 0) + 1

        return counts

    # =========================================================================
    # Session Statistics
    # =========================================================================

    @property
    def total_event_count(self) -> int:
        """Return total number of session events."""

        return self.session.total_events

    @property
    def has_quorum(self) -> bool:
        """
        Return True if participation reaches at least 50%
        of the expected population.
        """

        if self.expected_attendees == 0:
            return False

        return self.present_count >= (self.expected_attendees / 2)

    @property
    def is_full_attendance(self) -> bool:
        """Return True if all expected members participated."""

        return (
            self.expected_attendees > 0
            and self.present_count >= self.expected_attendees
        )

    @property
    def is_empty(self) -> bool:
        """Return True if no participation exists."""

        return self.present_count == 0

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
            "absentee_percentage": self.absentee_percentage,
            "first_attendee": self.first_attendee,
            "attendance_event_count": self.attendance_event_count,
            "done_count": self.done_count,
            "activity_event_count": self.activity_event_count,
            "unique_activity_count": self.unique_activity_count,
            "activity_value_counts": self.activity_value_counts,
            "duration": str(self.duration),
        }

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __len__(self) -> int:
        """Return number of unique participants."""

        return self.present_count

    def __bool__(self) -> bool:
        """Return True if participation exists."""

        return self.present_count > 0

    def __str__(self) -> str:
        """Return readable representation."""

        return (
            "AttendanceSummary("
            f"date={self.session_date}, "
            f"present={self.present_count}, "
            f"expected={self.expected_attendees}, "
            f"attendance={self.attendance_percentage:.2f}%, "
            f"activities={self.unique_activity_count}, "
            f"done={self.done_count})"
        )
