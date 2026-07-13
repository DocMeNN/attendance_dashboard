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
Android example::

    2/8/26, 11:02 - Jane Doe: Hello

iPhone example::

    [08/02/2026, 11:02:15] Jane Doe: Hello

Responsibilities
----------------
- Detect WhatsApp message boundaries.
- Combine multiline messages.
- Parse timestamps.
- Extract sender names.
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
# Regular Expressions
# ============================================================================

ANDROID_PATTERN = re.compile(
    r"""
^
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2})
(?:\s?(?P<ampm>AM|PM|am|pm))?
\s+-\s+
(?P<sender>.*?)
:
\s?
(?P<message>.*)
$
""",
    re.VERBOSE,
)

IPHONE_PATTERN = re.compile(
    r"""
^\[
(?P<date>\d{1,2}/\d{1,2}/\d{2,4}),
\s+
(?P<time>\d{1,2}:\d{2}(?::\d{2})?)
\]
\s+
(?P<sender>.*?)
:
\s?
(?P<message>.*)
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

    logical_messages = _build_logical_messages(
        raw_text,
    )

    if not logical_messages:
        raise InvalidExportFormatError("No WhatsApp messages were detected.")

    records: list[RawMessageRecord] = []

    for line_number, message in logical_messages:

        record = _parse_message(
            message=message,
            line_number=line_number,
        )

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
    Merge multiline WhatsApp messages into
    single logical records.
    """

    messages: list[tuple[int, str]] = []

    current: list[str] = []
    current_line = 1

    for line_number, line in enumerate(
        raw_text.splitlines(),
        start=1,
    ):

        if _starts_new_message(line):

            if current:
                messages.append(
                    (
                        current_line,
                        "\n".join(current),
                    )
                )

            current = [line]
            current_line = line_number

        else:

            if current:
                current.append(line)

    if current:
        messages.append(
            (
                current_line,
                "\n".join(current),
            )
        )

    return messages


def _starts_new_message(
    line: str,
) -> bool:
    """
    Return True if the line begins a new
    WhatsApp message.
    """

    return bool(ANDROID_PATTERN.match(line) or IPHONE_PATTERN.match(line))


# ============================================================================
# Record Parser
# ============================================================================


def _parse_message(
    *,
    message: str,
    line_number: int,
) -> RawMessageRecord:
    """
    Parse a logical WhatsApp message.
    """

    match = ANDROID_PATTERN.match(message)

    if match is not None:
        return _build_record(
            match=match,
            line_number=line_number,
        )

    match = IPHONE_PATTERN.match(message)

    if match is not None:
        return _build_record(
            match=match,
            line_number=line_number,
        )

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
    """
    Parse WhatsApp timestamps.

    Supports:

    - 2/8/26, 11:02
    - 2/8/2026, 11:02
    - 2/8/26, 11:02 PM
    - 08/02/2026, 11:02:15
    """

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
        ("Unable to parse timestamp " f"'{timestamp}' " f"on line {line_number}.")
    )


# ============================================================================
# Module Initialization
# ============================================================================

logger.info("WhatsApp parser initialized successfully.")
