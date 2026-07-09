# src/infrastructure/data_engine/cleaner.py

"""
Normalize parsed WhatsApp records.

This module performs infrastructure-level normalization on
``RawMessageRecord`` instances and produces immutable
``CleanMessageRecord`` instances.

Responsibilities
----------------
- Normalize sender names.
- Normalize message text.
- Normalize whitespace.
- Detect phone numbers.
- Detect WhatsApp placeholder messages.

This module intentionally performs NO business logic.

Business concepts such as attendance, activities, sessions,
or analytics belong to the Domain layer.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable

from .models import (
    CleanMessageRecord,
    RawMessageRecord,
)
from .patterns import (
    DELETED_MESSAGE_PATTERN,
    MEDIA_OMITTED_PATTERN,
    PHONE_NUMBER_PATTERN,
    WHITESPACE_PATTERN,
)

__all__ = [
    "clean_records",
]

logger = logging.getLogger(__name__)


def clean_records(
    records: Iterable[RawMessageRecord],
) -> list[CleanMessageRecord]:
    """
    Normalize parsed message records.

    Parameters
    ----------
    records
        Parsed infrastructure records.

    Returns
    -------
    list[CleanMessageRecord]
        Normalized infrastructure records.
    """
    records = list(records)

    logger.info(
        "Cleaning %d parsed records.",
        len(records),
    )

    cleaned = [_clean_record(record) for record in records]

    logger.info(
        "Successfully cleaned %d records.",
        len(cleaned),
    )

    return cleaned


def _clean_record(
    record: RawMessageRecord,
) -> CleanMessageRecord:
    """
    Normalize a single parsed record.

    This function performs infrastructure-level normalization
    without applying any business rules.
    """
    sender = _normalize_sender(
        record.sender,
    )

    message = _normalize_message(
        record.message,
    )

    return CleanMessageRecord(
        timestamp=record.timestamp,
        sender=sender,
        message=message,
        source_line=record.source_line,
        sender_is_phone_number=_is_phone_number(
            sender,
        ),
        is_deleted_message=_is_deleted_message(
            message,
        ),
        has_media_omitted=_has_media_placeholder(
            message,
        ),
    )


def _normalize_sender(
    sender: str,
) -> str:
    """
    Normalize sender whitespace.

    Consecutive whitespace characters are collapsed into a
    single space and leading/trailing whitespace is removed.

    Parameters
    ----------
    sender
        Raw sender name or phone number.

    Returns
    -------
    str
        Normalized sender.
    """
    return WHITESPACE_PATTERN.sub(
        " ",
        sender,
    ).strip()


def _normalize_message(
    message: str,
) -> str:
    """
    Normalize message text while preserving paragraph structure.

    Normalization performed
    -----------------------
    - Strip leading and trailing whitespace.
    - Collapse consecutive whitespace within each line.
    - Remove leading and trailing whitespace from each line.
    - Remove empty lines.
    - Preserve the original line ordering.

    Parameters
    ----------
    message
        Raw message text.

    Returns
    -------
    str
        Normalized message text.
    """
    normalized_lines: list[str] = []

    for line in message.splitlines():
        cleaned_line = WHITESPACE_PATTERN.sub(
            " ",
            line,
        ).strip()

        if cleaned_line:
            normalized_lines.append(cleaned_line)

    return "\n".join(normalized_lines)


def _is_phone_number(
    sender: str,
) -> bool:
    """
    Determine whether the sender is represented as a phone number.

    Parameters
    ----------
    sender
        Normalized sender string.

    Returns
    -------
    bool
        True if the sender matches the expected international phone
        number format; otherwise False.
    """
    return PHONE_NUMBER_PATTERN.fullmatch(sender) is not None


def _is_deleted_message(
    message: str,
) -> bool:
    """
    Determine whether the message is the standard WhatsApp
    deleted-message placeholder.

    Parameters
    ----------
    message
        Normalized message text.

    Returns
    -------
    bool
        True if the message is the WhatsApp deleted-message
        placeholder; otherwise False.
    """
    return DELETED_MESSAGE_PATTERN.fullmatch(message) is not None


def _has_media_placeholder(
    message: str,
) -> bool:
    """
    Determine whether the message is the standard WhatsApp
    media placeholder.

    Parameters
    ----------
    message
        Normalized message text.

    Returns
    -------
    bool
        True if the message is the WhatsApp media placeholder;
        otherwise False.
    """
    return MEDIA_OMITTED_PATTERN.fullmatch(message) is not None
