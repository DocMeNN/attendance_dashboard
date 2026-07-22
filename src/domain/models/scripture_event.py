# src/domain/models/scripture_event.py

"""
Scripture Event Domain Model

Purpose
-------
Represents a detected Scripture Reading activity.

Responsibilities
----------------
- Represent a Scripture Reading activity.
- Preserve the originating source message.
- Provide Scripture Reading-specific domain behaviour.
- Remain technology independent.

Domain Rules
------------
- A ScriptureEvent represents the Scripture Reading activity itself.
- A ScriptureEvent is not a Done acknowledgement.
- A Done acknowledgement is represented by DoneEvent.
- Scripture Reading detection is session-related because the activity
  is part of the detected session timeline.
- The acknowledgement of Scripture Reading remains independent and may
  be counted across any reporting period.

Notes
-----
- Immutable.
- Derived from a Message.
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
from datetime import date, datetime, time

# ============================================================================
# Local Imports
# ============================================================================
from .message import Message

# ============================================================================
# Scripture Event
# ============================================================================


@dataclass(frozen=True, slots=True)
class ScriptureEvent:
    """
    Immutable Scripture Reading activity event.

    Attributes
    ----------
    source_message:
        Message that generated the Scripture Reading event.

    Notes
    -----
    The source message is preserved so the event retains its
    original timestamp, sender, content, and source line.
    """

    source_message: Message

    def __post_init__(self) -> None:
        """Validate the Scripture Reading event."""

        if not isinstance(
            self.source_message,
            Message,
        ):
            raise TypeError(
                "source_message must be a Message.",
            )

    # =========================================================================
    # Source Information
    # =========================================================================

    @property
    def timestamp(self) -> datetime:
        """Return Scripture Reading timestamp."""

        return self.source_message.timestamp

    @property
    def event_date(self) -> date:
        """Return Scripture Reading date."""

        return self.timestamp.date()

    @property
    def event_time(self) -> time:
        """Return Scripture Reading time."""

        return self.timestamp.time()

    @property
    def sender(self) -> str:
        """Return the sender of the source message."""

        return self.source_message.sender

    @property
    def message_text(self) -> str:
        """Return the original message content."""

        return self.source_message.content

    @property
    def line_number(self) -> int:
        """Return the original source line number."""

        return self.source_message.line_number

    # =========================================================================
    # Classification
    # =========================================================================

    @property
    def activity_name(self) -> str:
        """Return the domain activity name."""

        return "Scripture Reading"

    @property
    def is_scripture_reading(self) -> bool:
        """Return True because this is a Scripture Reading event."""

        return True

    # =========================================================================
    # Comparison
    # =========================================================================

    def occurred_before(
        self,
        other: "ScriptureEvent",
    ) -> bool:
        """Return True if this event occurred before another."""

        return self.timestamp < other.timestamp

    def occurred_after(
        self,
        other: "ScriptureEvent",
    ) -> bool:
        """Return True if this event occurred after another."""

        return self.timestamp > other.timestamp

    def occurred_on_same_date(
        self,
        other: "ScriptureEvent",
    ) -> bool:
        """Return True if both events occurred on the same date."""

        return self.event_date == other.event_date

    # =========================================================================
    # Serialization
    # =========================================================================

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "activity_name": self.activity_name,
            "timestamp": self.timestamp,
            "event_date": self.event_date,
            "sender": self.sender,
            "message": self.message_text,
            "line_number": self.line_number,
        }

    # =========================================================================
    # Dunder Methods
    # =========================================================================

    def __str__(self) -> str:
        """Return readable representation."""

        return (
            "ScriptureEvent("
            f"date='{self.event_date}', "
            f"time='{self.event_time}', "
            f"sender='{self.sender}')"
        )
