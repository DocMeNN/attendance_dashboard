# src/domain/models/attendance_event.py

"""
Attendance Event Domain Model

Purpose:
    Represents a validated attendance event derived from a message.

Responsibilities:
    - Represent a member attendance event.
    - Validate attendance data.
    - Provide attendance-related business behaviour.
    - Remain technology independent.

Notes:
    - Immutable.
    - Derived from a Message.
    - Timestamp is obtained from the source message.
    - Contains no UI, pandas or infrastructure dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time

from src.domain.enums.attendance_type import AttendanceType

from .message import Message


@dataclass(frozen=True, slots=True)
class AttendanceEvent:
    """
    Immutable attendance event.

    Attributes:
        attendee:
            Name of the attendee.

        attendance_type:
            Type of attendance recorded.

        source_message:
            Message that generated this attendance event.
    """

    attendee: str
    attendance_type: AttendanceType
    source_message: Message

    def __post_init__(self) -> None:
        """Validate attendance event."""

        attendee = self.attendee.strip()

        if not attendee:
            raise ValueError("attendee cannot be empty.")

        if not isinstance(self.attendance_type, AttendanceType):
            raise TypeError("attendance_type must be an AttendanceType.")

        if not isinstance(self.source_message, Message):
            raise TypeError("source_message must be a Message.")

        object.__setattr__(self, "attendee", attendee)

    # ------------------------------------------------------------------
    # Derived Properties
    # ------------------------------------------------------------------

    @property
    def timestamp(self) -> datetime:
        """Return attendance timestamp."""
        return self.source_message.timestamp

    @property
    def event_date(self) -> date:
        """Return attendance date."""
        return self.timestamp.date()

    @property
    def event_time(self) -> time:
        """Return attendance time."""
        return self.timestamp.time()

    @property
    def line_number(self) -> int:
        """Return source line number."""
        return self.source_message.line_number

    @property
    def attendee_name(self) -> str:
        """Return attendee name."""
        return self.attendee

    @property
    def sender(self) -> str:
        """Return sender from the source message."""
        return self.source_message.sender

    @property
    def keyword(self) -> str:
        """Return attendance keyword."""
        return self.attendance_type.value

    # ------------------------------------------------------------------
    # Attendance Classification
    # ------------------------------------------------------------------

    @property
    def is_done(self) -> bool:
        return self.attendance_type is AttendanceType.DONE

    @property
    def is_present(self) -> bool:
        return self.attendance_type is AttendanceType.PRESENT

    @property
    def is_late(self) -> bool:
        return self.attendance_type is AttendanceType.LATE

    @property
    def is_absent(self) -> bool:
        return self.attendance_type is AttendanceType.ABSENT

    @property
    def is_unknown(self) -> bool:
        return self.attendance_type is AttendanceType.UNKNOWN

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def occurred_before(self, other: "AttendanceEvent") -> bool:
        """Return True if this event occurred before another."""
        return self.timestamp < other.timestamp

    def occurred_after(self, other: "AttendanceEvent") -> bool:
        """Return True if this event occurred after another."""
        return self.timestamp > other.timestamp

    def same_attendee(self, other: "AttendanceEvent") -> bool:
        """Return True if both events belong to the same attendee."""
        return self.attendee.casefold() == other.attendee.casefold()

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "attendee": self.attendee,
            "attendance_type": self.attendance_type.value,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "line_number": self.line_number,
        }

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Return readable representation."""

        return (
            f"AttendanceEvent("
            f"attendee='{self.attendee}', "
            f"type='{self.attendance_type.name}', "
            f"time='{self.timestamp}')"
        )
