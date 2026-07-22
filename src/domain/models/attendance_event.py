# src/domain/models/attendance_event.py

"""
Attendance Event Domain Model

Purpose
-------
Represents one participation event within a session.

Domain Rule
-----------
Attendance is participation.

Any recognized participation in a session produces
a PRESENT AttendanceEvent.

There are no LATE, ABSENT, or UNKNOWN attendance
classifications in this domain model.

Responsibilities
----------------
- Represent a participant's participation event.
- Validate attendance data.
- Preserve the originating source message.
- Provide attendance-related business behaviour.
- Remain technology independent.

Notes
-----
- Immutable.
- Derived from a Message.
- Timestamp is obtained from the source message.
- Contains no UI, pandas or infrastructure dependencies.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass
from datetime import date, datetime, time

# ============================================================================
# Local Imports
# ============================================================================
from .message import Message

# ============================================================================
# Attendance Event
# ============================================================================


@dataclass(frozen=True, slots=True)
class AttendanceEvent:
    """
    Immutable participation event.

    An AttendanceEvent represents one recognized instance
    of participation by an attendee within a session.

    Attendance is intentionally simple:

        Participation
            ↓
          PRESENT

    The event does not represent absence, lateness, or
    an unknown attendance state.
    """

    attendee: str
    source_message: Message

    def __post_init__(self) -> None:
        """
        Validate the attendance event.
        """

        attendee = self.attendee.strip()

        if not attendee:
            raise ValueError(
                "attendee cannot be empty.",
            )

        if not isinstance(
            self.source_message,
            Message,
        ):
            raise TypeError(
                "source_message must be a Message.",
            )

        object.__setattr__(
            self,
            "attendee",
            attendee,
        )

    # =========================================================================
    # Derived Properties
    # =========================================================================

    @property
    def timestamp(self) -> datetime:
        """
        Return the participation timestamp.
        """

        return self.source_message.timestamp

    @property
    def event_date(self) -> date:
        """
        Return the participation date.
        """

        return self.timestamp.date()

    @property
    def event_time(self) -> time:
        """
        Return the participation time.
        """

        return self.timestamp.time()

    @property
    def line_number(self) -> int:
        """
        Return the original source line number.
        """

        return self.source_message.line_number

    @property
    def attendee_name(self) -> str:
        """
        Return the attendee name.
        """

        return self.attendee

    @property
    def sender(self) -> str:
        """
        Return the sender from the source message.
        """

        return self.source_message.sender

    # =========================================================================
    # Attendance Classification
    # =========================================================================

    @property
    def is_present(self) -> bool:
        """
        Return True because this event represents participation.
        """

        return True

    @property
    def is_absent(self) -> bool:
        """
        Return False because absence is not represented by an
        AttendanceEvent in the OYBS domain.
        """

        return False

    @property
    def is_late(self) -> bool:
        """
        Return False because lateness is not represented by an
        AttendanceEvent in the OYBS domain.
        """

        return False

    # =========================================================================
    # Comparison
    # =========================================================================

    def occurred_before(
        self,
        other: "AttendanceEvent",
    ) -> bool:
        """
        Return True if this event occurred before another.
        """

        return self.timestamp < other.timestamp

    def occurred_after(
        self,
        other: "AttendanceEvent",
    ) -> bool:
        """
        Return True if this event occurred after another.
        """

        return self.timestamp > other.timestamp

    def same_attendee(
        self,
        other: "AttendanceEvent",
    ) -> bool:
        """
        Return True if both events belong to the same attendee.
        """

        return self.attendee.casefold() == other.attendee.casefold()

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, object]:
        """
        Return dictionary representation.
        """

        return {
            "attendee": self.attendee,
            "timestamp": self.timestamp,
            "sender": self.sender,
            "line_number": self.line_number,
        }

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __str__(self) -> str:
        """
        Return readable representation.
        """

        return (
            "AttendanceEvent("
            f"attendee='{self.attendee}', "
            f"type='PRESENT', "
            f"time='{self.timestamp}')"
        )
