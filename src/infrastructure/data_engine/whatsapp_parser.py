# src/infrastructure/data_engine/whatsapp_parser.py

"""
WhatsApp Export Parser

Purpose
-------
Parses native WhatsApp exported chat files into RawMessageRecord objects.

Unlike parser.py, which parses the project's canonical tab-separated
intermediate format, this module understands the text format produced
directly by WhatsApp.

Supported formats
-----------------

Android user message::

    2/8/26, 11:02 - Jane Doe: Hello

Android system message::

    2/8/26, 09:27 - Messages and calls are end-to-end encrypted.

iPhone user message::

    [08/02/2026, 11:02:15] Jane Doe: Hello

Responsibilities
----------------
- Detect WhatsApp record boundaries.
- Combine multiline messages.
- Parse timestamps.
- Extract sender names.
- Ignore WhatsApp system events.
- Create RawMessageRecord objects.

This module intentionally does NOT:

- Clean messages
- Detect attendance
- Detect activities
- Apply business rules
- Create Domain models
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
import logging
import re
from datetime import datetime

# ============================================================================
# Local Imports
# ============================================================================
from .exceptions import (
    InvalidExportFormatError,
    ParsingError,
)
from .models import RawMessageRecord

# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "parse_whatsapp_chat",
]

# ============================================================================
# Logging
# ============================================================================

logger = logging.getLogger(__name__)

# ============================================================================
# Record Detection Patterns
# ============================================================================

#
# These expressions are intentionally separated from the message parsing
# expressions.
#
# Their only responsibility is determining whether a line begins a new
# WhatsApp record.
#

ANDROID_RECORD_START_PATTERN = re.compile(
    r"""
^
\d{1,2}/\d{1,2}/\d{2,4},
\s+
\d{1,2}:\d{2}
(?:\s?(?:AM|PM|am|pm))?
\s+-\s+
""",
    re.VERBOSE,
)

IPHONE_RECORD_START_PATTERN = re.compile(
    r"""
^\[
\d{1,2}/\d{1,2}/\d{2,4},
\s+
\d{1,2}:\d{2}
(?::\d{2})?
\]
\s+
""",
    re.VERBOSE,
)

# ============================================================================
# User Message Patterns
# ============================================================================

ANDROID_MESSAGE_PATTERN = re.compile(
    r"""
^
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2})
(?:\s?(?P<ampm>AM|PM|am|pm))?
\s+-\s+
(?P<sender>.+?)
:
\s?
(?P<message>.*)
$
""",
    re.VERBOSE | re.DOTALL,
)

IPHONE_MESSAGE_PATTERN = re.compile(
    r"""
^\[
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
\]
\s+
(?P<sender>.+?)
:
\s?
(?P<message>.*)
$
""",
    re.VERBOSE | re.DOTALL,
)
IPHONE_MESSAGE_PATTERN = re.compile(
    r"""
^\[
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
\]
\s+
(?P<sender>.+?)
:
\s?
(?P<message>.*)
$
""",
    re.VERBOSE,
)

# ============================================================================
# System Message Patterns
# ============================================================================

#
# These represent WhatsApp-generated events.
# They are valid export records but should not become RawMessageRecord objects.
#

ANDROID_SYSTEM_PATTERN = re.compile(
    r"""
^
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2})
(?:\s?(?P<ampm>AM|PM|am|pm))?
\s+-\s+
(?P<message>.*)
$
""",
    re.VERBOSE | re.DOTALL,
)

IPHONE_SYSTEM_PATTERN = re.compile(
    r"""
^\[
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
\]
\s+
(?P<message>.*)
$
""",
    re.VERBOSE | re.DOTALL,
)
IPHONE_SYSTEM_PATTERN = re.compile(
    r"""
^\[
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
\]
\s+
(?P<message>.+)
$
""",
    re.VERBOSE,
)

# ============================================================================
# Public API
# ============================================================================


def parse_whatsapp_chat(
    raw_text: str,
) -> list[RawMessageRecord]:
    """
    Parse a native WhatsApp export.

    Parameters
    ----------
    raw_text:
        Raw WhatsApp export.

    Returns
    -------
    list[RawMessageRecord]
    """

    logger.info("Parsing WhatsApp export.")

    logical_messages = _build_logical_messages(raw_text)

    if not logical_messages:
        raise InvalidExportFormatError("No WhatsApp messages were detected.")

    records: list[RawMessageRecord] = []

    for line_number, message in logical_messages:

        record = _parse_message(
            message=message,
            line_number=line_number,
        )

        if record is None:
            continue

        records.append(record)

    logger.info(
        "Parsed %d WhatsApp messages.",
        len(records),
    )

    return records


# ============================================================================
# Message Builder
# ============================================================================


def _build_logical_messages(
    raw_text: str,
) -> list[tuple[int, str]]:
    """
    Build logical WhatsApp records.

    WhatsApp exports may contain:

    - User messages
    - System events
    - Multi-line messages
    - Blank lines within messages

    A new logical record always begins with a timestamp.
    Every subsequent line belongs to that record until the
    next timestamp is encountered.
    """

    logical_messages: list[tuple[int, str]] = []

    current_lines: list[str] = []
    current_line_number: int | None = None

    for line_number, line in enumerate(
        raw_text.splitlines(),
        start=1,
    ):

        if _starts_new_message(line):

            if current_lines:

                logical_messages.append(
                    (
                        current_line_number or line_number,
                        "\n".join(current_lines),
                    )
                )

            current_lines = [line]
            current_line_number = line_number

            continue

        #
        # Ignore anything that appears before the first
        # WhatsApp record.
        #
        if not current_lines:
            continue

        #
        # Preserve blank lines.
        #
        current_lines.append(line)

    if current_lines:

        logical_messages.append(
            (
                current_line_number or 1,
                "\n".join(current_lines),
            )
        )

    logger.debug(
        "Built %d logical WhatsApp records.",
        len(logical_messages),
    )

    return logical_messages


def _starts_new_message(
    line: str,
) -> bool:
    """
    Determine whether a line begins a new WhatsApp record.

    This function only detects the beginning of a record.
    It does not determine whether the record is a user
    message or a WhatsApp system event.
    """

    return (
        ANDROID_RECORD_START_PATTERN.match(line) is not None
        or IPHONE_RECORD_START_PATTERN.match(line) is not None
    )


# ============================================================================
# Record Parser
# ============================================================================


def _parse_message(
    *,
    message: str,
    line_number: int,
) -> RawMessageRecord | None:
    """
    Parse a logical WhatsApp record.

    Returns
    -------
    RawMessageRecord
        When the record is a user message.

    None
        When the record is a valid WhatsApp system event.
    """

    #
    # Android user message
    #

    match = ANDROID_MESSAGE_PATTERN.match(message)

    if match is not None:

        return _build_record(
            match=match,
            line_number=line_number,
        )

    #
    # iPhone user message
    #

    match = IPHONE_MESSAGE_PATTERN.match(message)

    if match is not None:

        return _build_record(
            match=match,
            line_number=line_number,
        )

    #
    # Android system event
    #

    if ANDROID_SYSTEM_PATTERN.match(message):

        logger.debug(
            "Ignoring Android system event on line %d.",
            line_number,
        )

        return None

    #
    # iPhone system event
    #

    if IPHONE_SYSTEM_PATTERN.match(message):

        logger.debug(
            "Ignoring iPhone system event on line %d.",
            line_number,
        )

        return None

    raise InvalidExportFormatError(
        ("Unsupported WhatsApp export format " f"at line {line_number}.")
    )


# ============================================================================
# Record Builder
# ============================================================================


def _build_record(
    *,
    match: re.Match[str],
    line_number: int,
) -> RawMessageRecord:
    """
    Build a RawMessageRecord from a regex match.
    """

    timestamp = _parse_timestamp(
        date_text=match.group("date"),
        time_text=match.group("time"),
        ampm=match.groupdict().get("ampm"),
        line_number=line_number,
    )

    sender = match.group("sender").strip()

    message = match.group("message")

    return RawMessageRecord(
        timestamp=timestamp,
        sender=sender,
        message=message,
        source_line=line_number,
    )


# ============================================================================
# Timestamp Parsing
# ============================================================================


def _parse_timestamp(
    *,
    date_text: str,
    time_text: str,
    ampm: str | None,
    line_number: int,
) -> datetime:

    timestamp = f"{date_text} " f"{time_text}" f"{' ' + ampm if ampm else ''}"

    formats = (
        "%m/%d/%y %H:%M",
        "%m/%d/%Y %H:%M",
        "%m/%d/%y %I:%M %p",
        "%m/%d/%Y %I:%M %p",
        "%d/%m/%y %H:%M",
        "%d/%m/%Y %H:%M",
        "%d/%m/%y %I:%M %p",
        "%d/%m/%Y %I:%M %p",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%y %H:%M:%S",
    )

    for fmt in formats:

        try:
            return datetime.strptime(
                timestamp,
                fmt,
            )

        except ValueError:
            continue

    raise ParsingError(
        (f"Unable to parse timestamp '{timestamp}' " f"on line {line_number}.")
    )


# ============================================================================
# Module Initialization
# ============================================================================

logger.info("WhatsApp parser initialized successfully.")
