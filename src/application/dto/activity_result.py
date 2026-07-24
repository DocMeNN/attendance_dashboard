# src/application/dto/activity_result.py

"""
Activity Application Result DTO

Purpose
-------
Represents activity-related results returned by the Application Layer.

Architecture
------------
Application Layer - Data Transfer Object

Responsibilities
----------------
- Carry activity results between Application and Presentation layers.
- Provide a stable, typed application-level result structure.
- Prevent raw dictionaries from becoming the public application contract.

Rules
-----
- No business logic.
- No pandas.
- No Streamlit.
- No infrastructure dependencies.
- No AI dependencies.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.enums.activity_type import ActivityType

if TYPE_CHECKING:
    from src.domain.models.activity_event import ActivityEvent


# ============================================================================
# Activity Result
# ============================================================================


@dataclass(frozen=True, slots=True)
class ActivityResult:
    """
    Immutable application-level activity result.

    Represents activity information produced by
    application services.
    """

    activity_count: int
    activity_types: dict[ActivityType, int]
    activity_events: tuple[ActivityEvent, ...]
    first_activity: ActivityEvent | None
    last_activity: ActivityEvent | None

    @property
    def has_activities(self) -> bool:
        """
        Return True when activity events exist.
        """

        return self.activity_count > 0

    @property
    def is_empty(self) -> bool:
        """
        Return True when no activity events exist.
        """

        return self.activity_count == 0

    @property
    def first_activity_time(self) -> datetime | None:
        """
        Return the timestamp of the first activity event.
        """

        if self.first_activity is None:
            return None

        return self.first_activity.timestamp

    @property
    def last_activity_time(self) -> datetime | None:
        """
        Return the timestamp of the last activity event.
        """

        if self.last_activity is None:
            return None

        return self.last_activity.timestamp

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"activity_count={self.activity_count}, "
            f"activity_types={self.activity_types!r})"
        )

    def __str__(self) -> str:
        """
        Return a readable representation.
        """

        return self.__repr__()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "ActivityResult",
]
