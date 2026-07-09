# src/domain/models/activity_event.py

"""
Activity Event Domain Model

Purpose:
    Represents a validated meeting activity derived from a message.

Responsibilities:
    - Represent a meeting activity.
    - Validate activity data.
    - Provide activity-related business behaviour.
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

from src.domain.enums.activity_type import ActivityType

from .message import Message


@dataclass(frozen=True, slots=True)
class ActivityEvent:
    """
    Immutable activity event.

    Attributes:
        activity_type:
            Type of activity.

        source_message:
            Message that generated this activity event.
    """

    activity_type: ActivityType
    source_message: Message

    def __post_init__(self) -> None:
        """Validate the activity event."""

        if not isinstance(self.activity_type, ActivityType):
            raise TypeError("activity_type must be an ActivityType.")

        if not isinstance(self.source_message, Message):
            raise TypeError("source_message must be a Message.")

    # ------------------------------------------------------------------
    # Derived Properties
    # ------------------------------------------------------------------

    @property
    def timestamp(self) -> datetime:
        """Return activity timestamp."""
        return self.source_message.timestamp

    @property
    def event_date(self) -> date:
        """Return activity date."""
        return self.timestamp.date()

    @property
    def event_time(self) -> time:
        """Return activity time."""
        return self.timestamp.time()

    @property
    def sender(self) -> str:
        """Return sender."""
        return self.source_message.sender

    @property
    def line_number(self) -> int:
        """Return original source line number."""
        return self.source_message.line_number

    @property
    def activity_name(self) -> str:
        """Return formatted activity name."""
        return self.activity_type.name.replace("_", " ").title()

    # ------------------------------------------------------------------
    # Activity Classification
    # ------------------------------------------------------------------

    @property
    def is_opening_prayer(self) -> bool:
        return self.activity_type is ActivityType.OPENING_PRAYER

    @property
    def is_scripture_reading(self) -> bool:
        return self.activity_type is ActivityType.SCRIPTURE_READING

    @property
    def is_worship(self) -> bool:
        return self.activity_type is ActivityType.WORSHIP

    @property
    def is_announcement(self) -> bool:
        return self.activity_type is ActivityType.ANNOUNCEMENT

    @property
    def is_message(self) -> bool:
        return self.activity_type is ActivityType.MESSAGE

    @property
    def is_offering(self) -> bool:
        return self.activity_type is ActivityType.OFFERING

    @property
    def is_closing_prayer(self) -> bool:
        return self.activity_type is ActivityType.CLOSING_PRAYER

    @property
    def is_other(self) -> bool:
        return self.activity_type is ActivityType.OTHER

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def occurred_before(self, other: "ActivityEvent") -> bool:
        """Return True if this event occurred before another."""
        return self.timestamp < other.timestamp

    def occurred_after(self, other: "ActivityEvent") -> bool:
        """Return True if this event occurred after another."""
        return self.timestamp > other.timestamp

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Return dictionary representation."""

        return {
            "activity_type": self.activity_type.value,
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
            f"ActivityEvent("
            f"type='{self.activity_type.name}', "
            f"time='{self.timestamp}')"
        )
