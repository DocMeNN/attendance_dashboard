# src/application/builders/session_builder.py

"""
Session Builder

Purpose
-------
Builds immutable Session aggregates from validated Message objects.

Responsibilities
----------------
- Validate input messages.
- Determine the active meeting session.
- Construct AttendanceEvent objects.
- Construct DoneEvent objects.
- Construct ActivityEvent objects.
- Assemble immutable Session aggregates.

Rules
-----
- No pandas.
- No Streamlit.
- No analytics.
- No reporting.
- No infrastructure parsing.
- No file I/O.
- Technology independent.

Notes
-----
- Operates exclusively on Domain models.
- Acts as an orchestration layer.
- Business rules remain inside the Domain layer.

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
from collections.abc import Iterable
from datetime import date

# ============================================================================
# Local Imports
# ============================================================================
from src.domain.constants.keywords import (
    DONE_KEYWORDS,
    SESSION_START_KEYWORDS,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.message import Message
from src.domain.models.session import Session
from src.domain.policies.activity_policy import (
    classify_activity,
    is_supported_activity,
)


class SessionBuilder:
    """
    Build immutable Session aggregates from validated messages.

    Workflow
    --------

        Messages
            │
            ▼
      Validate & Sort
            │
            ▼
     Detect Session Start
            │
            ▼
      Session Messages
            │
       ┌────┼────────┐
       ▼    ▼        ▼
    Attendance Done Activities
       │    │        │
       └────┴────────┘
            │
            ▼
         Session
    """

    # ------------------------------------------------------------------
    # Public Builder
    # ------------------------------------------------------------------

    def build(
        self,
        session_date: date,
        messages: Iterable[Message],
    ) -> Session:
        """
        Build a Session aggregate.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        attendance_events = self._build_attendance_events(
            session_messages,
        )

        done_events = self._build_done_events(
            session_messages,
        )

        activity_events = self._build_activity_events(
            session_messages,
        )

        return Session(
            session_date=session_date,
            attendance_events=attendance_events,
            done_events=done_events,
            activity_events=activity_events,
        )

    # ------------------------------------------------------------------
    # Attendance Construction
    # ------------------------------------------------------------------

    def _build_attendance_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[AttendanceEvent, ...]:
        """
        Build AttendanceEvent objects.

        Every valid participant message represents participation.
        """

        attendance_events: list[AttendanceEvent] = []

        for message in messages:
            attendance_events.append(
                self._attendance_event(
                    message,
                )
            )

        return tuple(
            attendance_events,
        )

    # ------------------------------------------------------------------
    # Done Construction
    # ------------------------------------------------------------------

    def _build_done_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[DoneEvent, ...]:
        """
        Build DoneEvent objects.

        Multiple Done messages are preserved.
        """

        done_events: list[DoneEvent] = []

        for message in messages:

            if not self._is_done_message(
                message,
            ):
                continue

            done_events.append(
                self._done_event(
                    message,
                )
            )

        return tuple(
            done_events,
        )

    # ------------------------------------------------------------------
    # Activity Construction
    # ------------------------------------------------------------------

    def _build_activity_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[ActivityEvent, ...]:
        """
        Build ActivityEvent objects from session messages.

        Every supported message is classified according to
        the domain Activity Policy.
        """

        activity_events: list[ActivityEvent] = []

        prayer_session_active = False

        for message in messages:

            if not is_supported_activity(
                message.content,
                prayer_session_active=prayer_session_active,
            ):
                continue

            activity_type = self._activity_type(
                message,
                prayer_session_active=prayer_session_active,
            )

            if activity_type is None:
                continue

            activity_events.append(
                self._activity_event(
                    message,
                    activity_type,
                )
            )

            if self._is_prayer_session_opening(
                message,
            ):
                prayer_session_active = True

            elif self._is_prayer_session_closing(
                message,
            ):
                prayer_session_active = False

        return tuple(
            activity_events,
        )

    # ------------------------------------------------------------------
    # Activity Classification
    # ------------------------------------------------------------------

    def _activity_type(
        self,
        message: Message,
        *,
        prayer_session_active: bool = False,
    ) -> ActivityType | None:
        """
        Determine the ActivityType represented by a message.

        The domain Activity Policy is the authoritative source
        for activity classification.
        """

        activity_name = classify_activity(
            message.content,
            prayer_session_active=prayer_session_active,
        )

        activity_mapping: dict[str, ActivityType] = {
            "Scripture Reading": ActivityType.SCRIPTURE_READING,
            "Insight": ActivityType.INSIGHT,
            "Discussion": ActivityType.DISCUSSION,
            "Announcement": ActivityType.ANNOUNCEMENT,
            "Done": ActivityType.DONE,
            "Prayer Session": ActivityType.PRAYER_SESSION,
        }

        return activity_mapping.get(
            activity_name,
        )

    # ------------------------------------------------------------------
    # Prayer Session Boundaries
    # ------------------------------------------------------------------

    def _is_prayer_session_opening(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message opens a prayer session.
        """

        normalized = message.content.strip().casefold()

        return normalized.startswith(
            "opening prayer",
        ) or normalized.startswith(
            "prayer session opens",
        )

    def _is_prayer_session_closing(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message closes a prayer session.
        """

        normalized = message.content.strip().casefold()

        return (
            normalized.startswith(
                "closing prayer",
            )
            or normalized.startswith(
                "closing prayers",
            )
            or normalized.startswith(
                "prayer session closes",
            )
        )

    # ------------------------------------------------------------------
    # Keyword Helpers
    # ------------------------------------------------------------------

    def _is_done_message(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message is a Done acknowledgement.
        """

        return message.is_single_word and message.lowercase_content in DONE_KEYWORDS

    def _is_session_start(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message marks the beginning
        of a study session.
        """

        return any(
            message.contains(
                keyword,
            )
            for keyword in SESSION_START_KEYWORDS
        )

    # ------------------------------------------------------------------
    # Validation Helpers
    # ------------------------------------------------------------------

    def _validate_messages(
        self,
        messages: Iterable[Message],
    ) -> tuple[Message, ...]:
        """
        Validate and chronologically sort supplied messages.
        """

        validated = tuple(
            messages,
        )

        for message in validated:

            if not isinstance(
                message,
                Message,
            ):
                raise TypeError(
                    "messages must contain only Message instances.",
                )

        return tuple(
            sorted(
                validated,
                key=lambda message: message.timestamp,
            )
        )

    # ------------------------------------------------------------------
    # Session Extraction
    # ------------------------------------------------------------------

    def _session_messages(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[Message, ...]:
        """
        Extract messages belonging to the study session.

        Messages before the first configured session-start
        marker are ignored.
        """

        session_started = False
        session_messages: list[Message] = []

        for message in messages:

            if not session_started:

                if self._is_session_start(
                    message,
                ):
                    session_started = True

                continue

            session_messages.append(
                message,
            )

        return tuple(
            session_messages,
        )

    # ------------------------------------------------------------------
    # Event Factories
    # ------------------------------------------------------------------

    def _attendance_event(
        self,
        message: Message,
    ) -> AttendanceEvent:
        """
        Create an AttendanceEvent from a Message.
        """

        return AttendanceEvent(
            attendee=message.sender,
            source_message=message,
        )

    def _done_event(
        self,
        message: Message,
    ) -> DoneEvent:
        """
        Create a DoneEvent from a Message.
        """

        return DoneEvent(
            attendee=message.sender,
            source_message=message,
        )

    def _activity_event(
        self,
        message: Message,
        activity_type: ActivityType,
    ) -> ActivityEvent:
        """
        Create an ActivityEvent from a Message.
        """

        return ActivityEvent(
            activity_type=activity_type,
            source_message=message,
        )

    # ------------------------------------------------------------------
    # Public Builder Utilities
    # ------------------------------------------------------------------

    def build_attendance_events(
        self,
        messages: Iterable[Message],
    ) -> tuple[AttendanceEvent, ...]:
        """
        Build attendance events only.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        return self._build_attendance_events(
            session_messages,
        )

    def build_done_events(
        self,
        messages: Iterable[Message],
    ) -> tuple[DoneEvent, ...]:
        """
        Build Done events only.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        return self._build_done_events(
            session_messages,
        )

    def build_activity_events(
        self,
        messages: Iterable[Message],
    ) -> tuple[ActivityEvent, ...]:
        """
        Build activity events only.
        """

        ordered_messages = self._validate_messages(
            messages,
        )

        session_messages = self._session_messages(
            ordered_messages,
        )

        return self._build_activity_events(
            session_messages,
        )

    # ------------------------------------------------------------------
    # Builder Metadata
    # ------------------------------------------------------------------

    @property
    def name(self) -> str:
        """
        Return the builder name.
        """

        return self.__class__.__name__

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
