# src/domain/enums/base_enum.py

"""
Base Enumeration

Purpose:
    Provides common functionality for all domain enumerations.

Responsibilities:
    - Convert strings to enum members.
    - Check membership.
    - Return enum values.
    - Return enum names.
    - Return choices for UI layers.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from enum import StrEnum
from typing import Self


class BaseEnum(StrEnum):
    """Base class for all domain enumerations."""

    @classmethod
    def from_string(cls, value: str) -> Self:
        """
        Convert a string to an enum member.

        Args:
            value:
                String representation.

        Returns:
            Matching enum member.

        Raises:
            ValueError:
                If no matching member exists.
        """
        normalized = value.strip().lower()

        for member in cls:
            if member.value == normalized:
                return member

        raise ValueError(f"{value!r} is not a valid {cls.__name__}.")

    @classmethod
    def has_value(cls, value: str) -> bool:
        """
        Return True if the value exists.
        """
        normalized = value.strip().lower()

        return any(member.value == normalized for member in cls)

    @classmethod
    def values(cls) -> list[str]:
        """
        Return all enum values.
        """
        return [member.value for member in cls]

    @classmethod
    def names(cls) -> list[str]:
        """
        Return all enum names.
        """
        return [member.name for member in cls]

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        """
        Return choices suitable for UI layers.

        Example:
            [
                ("done", "DONE"),
                ("late", "LATE")
            ]
        """
        return [(member.value, member.name.replace("_", " ").title()) for member in cls]

    @classmethod
    def default(cls) -> Self:
        """
        Return the first enum member.

        Override in subclasses if necessary.
        """
        return next(iter(cls))

    def __str__(self) -> str:
        """Return enum value."""
        return self.value
