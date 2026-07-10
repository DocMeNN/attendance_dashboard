# src/application/builders/session_builder.py

"""
Session Builder

Purpose:
    Builds immutable Session aggregates from validated Message objects.

Responsibilities:
    - Validate input messages.
    - Determine the active meeting session.
    - Construct AttendanceEvent objects.
    - Construct DoneEvent objects.
    - Construct ActivityEvent objects.
    - Assemble immutable Session aggregates.

Rules:
    - No pandas.
    - No Streamlit.
    - No analytics.
    - No reporting.
    - No infrastructure parsing.
    - No file I/O.
    - Technology independent.

Notes:
    - Operates exclusively on Domain models.
    - Acts as an orchestration layer.
    - Business rules remain inside the Domain layer.

Author:
    OYBS Attendance Dashboard

Created:
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
    ACTIVITY_KEYWORDS,
    DONE_KEYWORDS,
    SESSION_START_KEYWORDS,
)
from src.domain.enums.activity_type import ActivityType
from src.domain.enums.attendance_type import AttendanceType
from src.domain.models.activity_event import ActivityEvent
from src.domain.models.attendance_event import AttendanceEvent
from src.domain.models.done_event import DoneEvent
from src.domain.models.message import Message
from src.domain.models.session import Session


class SessionBuilder:
    """
       Builds immutable Session aggregates from validated messages.

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
        ┌──────┼────────┐
        ▼      ▼        ▼
    Attendance Done  Activities
        │      │        │
        └──────┴────────┘
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

        Parameters
        ----------
        session_date:
            Date of the meeting session.

        messages:
            Validated domain messages.

        Returns
        -------
        Session
            Immutable Session aggregate.
        """

        ordered_messages = self._validate_messages(messages)

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

        Business Rules
        --------------
        - Every interaction counts as attendance.
        - Every Done message also counts as attendance.
        """

        attendance_events: list[AttendanceEvent] = []

        for message in messages:
            attendance_events.append(self._attendance_event(message))

        return tuple(attendance_events)

    # ------------------------------------------------------------------
    # Done Construction
    # ------------------------------------------------------------------

    def _build_done_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[DoneEvent, ...]:
        """
        Build DoneEvent objects.

        Duplicate removal is intentionally deferred to
        the Domain analytics layer.
        """

        done_events: list[DoneEvent] = []

        for message in messages:

            if not self._is_done_message(message):
                continue

            done_events.append(self._done_event(message))

        return tuple(done_events)

    # ------------------------------------------------------------------
    # Activity Construction
    # ------------------------------------------------------------------

    def _build_activity_events(
        self,
        messages: tuple[Message, ...],
    ) -> tuple[ActivityEvent, ...]:
        """
        Build ActivityEvent objects from session messages.

        Messages that do not represent configured meeting
        activities are ignored.
        """

        activity_events: list[ActivityEvent] = []

        for message in messages:

            activity_type = self._activity_type(message)

            if activity_type is None:
                continue

            activity_events.append(
                self._activity_event(
                    message,
                    activity_type,
                )
            )

        return tuple(activity_events)

    # ------------------------------------------------------------------
    # Activity Classification
    # ------------------------------------------------------------------

    def _activity_type(
        self,
        message: Message,
    ) -> ActivityType | None:
        """
        Determine the ActivityType represented by a message.

        Returns
        -------
        ActivityType | None
            Matching activity type or None if the message
            is not recognised as a meeting activity.
        """

        if self._matches_keywords(
            message,
            ACTIVITY_KEYWORDS["opening_prayer"],
        ):
            return ActivityType.OPENING_PRAYER

        if self._matches_keywords(
            message,
            ACTIVITY_KEYWORDS["scripture_reading"],
        ):
            return ActivityType.SCRIPTURE_READING

        if self._matches_keywords(
            message,
            ACTIVITY_KEYWORDS["worship"],
        ):
            return ActivityType.WORSHIP

        if self._matches_keywords(
            message,
            ACTIVITY_KEYWORDS["announcement"],
        ):
            return ActivityType.ANNOUNCEMENT

        if self._matches_keywords(
            message,
            ACTIVITY_KEYWORDS["message"],
        ):
            return ActivityType.MESSAGE

        if self._matches_keywords(
            message,
            ACTIVITY_KEYWORDS["offering"],
        ):
            return ActivityType.OFFERING

        if self._matches_keywords(
            message,
            ACTIVITY_KEYWORDS["closing_prayer"],
        ):
            return ActivityType.CLOSING_PRAYER

        return None

    # ------------------------------------------------------------------
    # Keyword Helpers
    # ------------------------------------------------------------------

    def _matches_keywords(
        self,
        message: Message,
        keywords: frozenset[str],
    ) -> bool:
        """
        Return True if the supplied message contains at
        least one configured keyword.
        """

        return any(message.contains(keyword) for keyword in keywords)

    def _is_done_message(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message is a standalone
        attendance acknowledgement.

        Examples
        --------
        Done
        done
        DONE
        """

        return message.is_single_word and message.lowercase_content in DONE_KEYWORDS

    def _is_session_start(
        self,
        message: Message,
    ) -> bool:
        """
        Return True if the message marks the beginning
        of a meeting session.

        Session start detection is entirely driven by
        SESSION_START_KEYWORDS.
        """

        return self._matches_keywords(
            message,
            SESSION_START_KEYWORDS,
        )

    # ------------------------------------------------------------------
    # Validation Helpers
    # ------------------------------------------------------------------

    def _validate_messages(
        self,
        messages: Iterable[Message],
    ) -> tuple[Message, ...]:
        """
        Validate, normalize and sort the supplied messages.

        Parameters
        ----------
        messages:
            Iterable of domain Message objects.

        Returns
        -------
        tuple[Message, ...]
            Chronologically ordered messages.

        Raises
        ------
        TypeError
            If any object is not a Message.
        """

        validated = tuple(messages)

        for message in validated:

            if not isinstance(message, Message):
                raise TypeError("messages must contain only Message instances.")

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
        Extract the messages belonging to a meeting session.

        Business Rule
        -------------
        The session begins immediately after the first
        configured Scripture Reading message.

        Messages before the session start marker are ignored.
        """

        session_started = False
        session_messages: list[Message] = []

        for message in messages:

            if not session_started:

                if self._is_session_start(message):
                    session_started = True

                continue

            session_messages.append(message)

        return tuple(session_messages)

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
            attendance_type=AttendanceType.PRESENT,
            source_message=message,
        )

    def _done_event(
        self,
        message: Message,
    ) -> DoneEvent:
        """
        Create a DoneEvent from a Message.

        Multiple Done messages are preserved.

        Duplicate elimination is intentionally deferred to the
        Domain analytics layer where the business rule is:

            same attendee + same timestamp
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

        Primarily intended for unit testing and diagnostics.
        """

        ordered_messages = self._validate_messages(messages)

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

        Primarily intended for unit testing and diagnostics.
        """

        ordered_messages = self._validate_messages(messages)

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

        Primarily intended for unit testing and diagnostics.
        """

        ordered_messages = self._validate_messages(messages)

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
