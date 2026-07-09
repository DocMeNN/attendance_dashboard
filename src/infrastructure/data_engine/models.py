# src/infrastructure/data_engine/models.py

"""
Infrastructure models for the WhatsApp Data Engine.

This module defines immutable data structures used internally by the
Infrastructure layer while transforming a raw WhatsApp export into
validated Domain objects.

These models are intentionally independent of the Domain layer.

Pipeline
--------
Raw WhatsApp Export
        │
        ▼
RawMessageRecord
        │
        ▼
CleanMessageRecord
        │
        ▼
Domain Models (validator.py)

The classes defined here should never contain business rules.
They exist solely to transport data safely through the parsing pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

__all__ = [
    "RawMessageRecord",
    "CleanMessageRecord",
]


@dataclass(frozen=True, slots=True)
class RawMessageRecord:
    """
    Represents a single message immediately after parsing.

    This object is created by ``parser.py`` after reading the raw
    WhatsApp export. It contains only the information extracted from
    the source file and performs no normalization.

    Attributes
    ----------
    timestamp:
        Date and time extracted from the chat export.

    sender:
        Sender exactly as found in the export.

    message:
        Message exactly as found in the export.

    source_line:
        Original starting line number within the source file.
        Used for diagnostics and error reporting.
    """

    timestamp: datetime
    sender: str
    message: str
    source_line: int


@dataclass(frozen=True, slots=True)
class CleanMessageRecord:
    """
    Represents a normalized infrastructure record.

    This object is produced by ``cleaner.py`` after performing
    infrastructure-level normalization. It contains cleaned text and
    metadata derived from the raw export but deliberately excludes any
    business interpretation.

    Business concepts such as attendance, activities, sessions, or
    analytics are handled later by the Domain layer.

    Attributes
    ----------
    timestamp:
        Normalized timestamp.

    sender:
        Normalized sender name or phone number.

    message:
        Normalized message text.

    source_line:
        Original line number in the source file.

    sender_is_phone_number:
        Indicates whether the sender matches the expected phone number
        pattern.

    is_deleted_message:
        Indicates whether the message is the standard WhatsApp deleted
        message placeholder.

    has_media_omitted:
        Indicates whether the message is the standard WhatsApp
        "<Media omitted>" placeholder.
    """

    timestamp: datetime
    sender: str
    message: str
    source_line: int

    sender_is_phone_number: bool
    is_deleted_message: bool
    has_media_omitted: bool
