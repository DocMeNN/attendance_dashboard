# src/domain/models/message.py

"""
Message Domain Model

Purpose:
    Defines the immutable Message value object used throughout the
    OYBS Attendance Dashboard domain.

Responsibilities:
    - Represent a single communication message.
    - Validate message data.
    - Provide rich domain behaviour.
    - Remain technology independent.

Notes:
    - This model is intentionally generic.
    - It contains no WhatsApp-specific logic.
    - It contains no pandas, Streamlit, database, or UI dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Final


@dataclass(frozen=True, slots=True)
class Message:
    """
    Immutable domain representation of a communication message.

    Args:
        timestamp:
            Date and time the message was created.

        sender:
            Name or identifier of the sender.

        content:
            Message body.

        line_number:
            Original line number within the imported source.

    Raises:
        ValueError:
            If any supplied value is invalid.
    """

    timestamp: datetime
    sender: str
    content: str
    line_number: int

    _MAX_LINE_NUMBER: Final[int] = 10_000_000

    def __post_init__(self) -> None:
        """Validate the message."""

        if not isinstance(self.timestamp, datetime):
            raise ValueError("timestamp must be a datetime instance.")

        if not isinstance(self.sender, str):
            raise ValueError("sender must be a string.")

        sender = self.sender.strip()

        if not sender:
            raise ValueError("sender cannot be empty.")

        if not isinstance(self.content, str):
            raise ValueError("content must be a string.")

        if self.line_number < 1:
            raise ValueError("line_number must be greater than zero.")

        if self.line_number > self._MAX_LINE_NUMBER:
            raise ValueError("line_number exceeds allowed range.")

        object.__setattr__(self, "sender", sender)
        object.__setattr__(self, "content", self.content.strip())

    # ------------------------------------------------------------------
    # Date & Time
    # ------------------------------------------------------------------

    @property
    def message_date(self) -> date:
        """Return the message date."""
        return self.timestamp.date()

    @property
    def message_time(self) -> time:
        """Return the message time."""
        return self.timestamp.time()

    # ------------------------------------------------------------------
    # Content
    # ------------------------------------------------------------------

    @property
    def normalized_content(self) -> str:
        """
        Return normalized content.

        Multiple spaces are collapsed and leading/trailing
        whitespace removed.
        """
        return " ".join(self.content.split())

    @property
    def lowercase_content(self) -> str:
        """Return lowercase content."""
        return self.normalized_content.lower()

    @property
    def stripped_content(self) -> str:
        """Return stripped content."""
        return self.content.strip()

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def character_count(self) -> int:
        """Return character count."""
        return len(self.content)

    @property
    def word_count(self) -> int:
        """Return number of words."""
        if self.is_blank:
            return 0

        return len(self.normalized_content.split())

    @property
    def is_blank(self) -> bool:
        """Return True if content is blank."""
        return not self.content.strip()

    @property
    def is_single_word(self) -> bool:
        """Return True if message contains one word."""
        return self.word_count == 1

    @property
    def is_multi_word(self) -> bool:
        """Return True if message contains multiple words."""
        return self.word_count > 1

    # ------------------------------------------------------------------
    # Content Inspection
    # ------------------------------------------------------------------

    @property
    def has_numbers(self) -> bool:
        """Return True if message contains digits."""
        return any(character.isdigit() for character in self.content)

    @property
    def has_letters(self) -> bool:
        """Return True if message contains alphabetic characters."""
        return any(character.isalpha() for character in self.content)

    @property
    def has_uppercase(self) -> bool:
        """Return True if uppercase characters exist."""
        return any(character.isupper() for character in self.content)

    @property
    def has_lowercase(self) -> bool:
        """Return True if lowercase characters exist."""
        return any(character.islower() for character in self.content)

    @property
    def is_uppercase(self) -> bool:
        """
        Return True if all alphabetic characters are uppercase.
        """
        letters = [c for c in self.content if c.isalpha()]

        return bool(letters) and all(c.isupper() for c in letters)

    @property
    def is_lowercase(self) -> bool:
        """
        Return True if all alphabetic characters are lowercase.
        """
        letters = [c for c in self.content if c.isalpha()]

        return bool(letters) and all(c.islower() for c in letters)

    @property
    def starts_with_alpha(self) -> bool:
        """Return True if first non-space character is alphabetic."""
        text = self.stripped_content

        return bool(text) and text[0].isalpha()

    @property
    def ends_with_punctuation(self) -> bool:
        """Return True if message ends with punctuation."""
        text = self.stripped_content

        if not text:
            return False

        return text[-1] in ".!?:;,"

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def contains(self, text: str, *, case_sensitive: bool = False) -> bool:
        """
        Check whether the message contains text.

        Args:
            text:
                Text to search for.

            case_sensitive:
                Perform a case-sensitive search.

        Returns:
            True if found.
        """
        if case_sensitive:
            return text in self.content

        return text.lower() in self.lowercase_content

    def starts_with(self, text: str, *, case_sensitive: bool = False) -> bool:
        """
        Check whether the message starts with text.
        """
        if case_sensitive:
            return self.stripped_content.startswith(text)

        return self.lowercase_content.startswith(text.lower())

    def ends_with(self, text: str, *, case_sensitive: bool = False) -> bool:
        """
        Check whether the message ends with text.
        """
        if case_sensitive:
            return self.stripped_content.endswith(text)

        return self.lowercase_content.endswith(text.lower())

    def to_dict(self) -> dict[str, object]:
        """
        Return a dictionary representation.

        Useful for serialization and testing.
        """
        return {
            "timestamp": self.timestamp,
            "sender": self.sender,
            "content": self.content,
            "line_number": self.line_number,
        }

    def __str__(self) -> str:
        """Return a human-readable representation."""
        preview = self.normalized_content

        if len(preview) > 50:
            preview = f"{preview[:47]}..."

        return (
            f"Message("
            f"sender='{self.sender}', "
            f"timestamp='{self.timestamp.isoformat(sep=' ')}', "
            f"content='{preview}')"
        )

    def __len__(self) -> int:
        """Return character count."""
        return self.character_count
