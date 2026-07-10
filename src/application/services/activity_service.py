# src/application/services/activity_service.py

"""
Activity Application Service

Purpose:
    Provides application-level activity use cases by orchestrating
    the SessionBuilder and Domain activity analytics.

Responsibilities:
    - Build Session aggregates.
    - Coordinate activity analytics.
    - Expose activity-related application services.
    - Remain free of business logic.

Rules:
    - No pandas.
    - No Streamlit.
    - No plotting.
    - No reporting.
    - No infrastructure parsing.
    - No business rules.

Notes:
    - Business rules remain inside the Domain layer.
    - This service coordinates Domain components only.
    - Technology independent.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections import Counter
from collections.abc import Iterable
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from src.application.builders.session_builder import SessionBuilder
from src.domain.analytics.activity import (
    count_activity_types,
    first_activity_event,
    get_activity_events,
    last_activity_event,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.message import Message
from src.domain.models.session import Session


class ActivityService:
    """
    Application service for activity workflows.

    The service coordinates Session construction and
    delegates business calculations to the Domain layer.
    """

    def __init__(
        self,
        session_builder: SessionBuilder | None = None,
    ) -> None:
        """
        Initialize the service.
        """

        self._session_builder = (
            session_builder if session_builder is not None else SessionBuilder()
        )

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------

    def build_session(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build an immutable Session aggregate.
        """

        return self._session_builder.build(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Activity
    # ------------------------------------------------------------------

    def activity_events(
        self,
        session: Session,
    ) -> tuple[ActivityEvent, ...]:
        """
        Return all activity events.
        """

        return get_activity_events(
            session.activity_events,
        )

    def activity_count(
        self,
        session: Session,
    ) -> int:
        """
        Return the number of activity events.
        """

        return len(self.activity_events(session))

    def activity_counts(
        self,
        session: Session,
    ) -> Counter[ActivityType]:
        """
        Count activity events by ActivityType.
        """

        return count_activity_types(
            session.activity_events,
        )

    def first_activity(
        self,
        session: Session,
    ) -> ActivityEvent | None:
        """
        Return the first recorded activity.
        """

        return first_activity_event(
            session.activity_events,
        )

    def last_activity(
        self,
        session: Session,
    ) -> ActivityEvent | None:
        """
        Return the last recorded activity.
        """

        return last_activity_event(
            session.activity_events,
        )

    # ------------------------------------------------------------------
    # Activity Lookup
    # ------------------------------------------------------------------

    def activity_events_by_type(
        self,
        session: Session,
        activity_type: ActivityType,
    ) -> tuple[ActivityEvent, ...]:
        """
        Return all activity events of the specified type.
        """

        return tuple(
            event
            for event in session.activity_events
            if event.activity_type is activity_type
        )

    def has_activity(
        self,
        session: Session,
        activity_type: ActivityType,
    ) -> bool:
        """
        Return True if the specified activity exists.
        """

        return bool(
            self.activity_events_by_type(
                session,
                activity_type,
            )
        )

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def has_activities(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if the session contains activities.
        """

        return session.has_activities

    def is_empty(
        self,
        session: Session,
    ) -> bool:
        """
        Return True if the session contains no events.
        """

        return session.is_empty

    # ------------------------------------------------------------------
    # Builder
    # ------------------------------------------------------------------

    @property
    def builder(self) -> SessionBuilder:
        """
        Return the SessionBuilder used by this service.
        """

        return self._session_builder

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return f"{self.__class__.__name__}" f"(builder={self.builder.name})"

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
