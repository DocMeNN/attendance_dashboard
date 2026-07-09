# src/infrastructure/data_engine/exceptions.py

"""
Custom exceptions for the Infrastructure Data Engine.

This module defines the exception hierarchy used by the data ingestion
pipeline. These exceptions represent infrastructure-level failures only
and must never be used to signal business rule violations.

Exception Hierarchy
-------------------
DataEngineError
├── FileLoadError
├── InvalidExportFormatError
├── MalformedRecordError
└── ParsingError

The Application layer may catch these exceptions to provide user-friendly
feedback without exposing implementation details.
"""

from __future__ import annotations

__all__ = [
    "DataEngineError",
    "FileLoadError",
    "InvalidExportFormatError",
    "MalformedRecordError",
    "ParsingError",
]


class DataEngineError(Exception):
    """
    Base exception for all Infrastructure Data Engine errors.

    All custom exceptions raised by the data engine should inherit from
    this class, allowing callers to catch a single exception type when
    appropriate.
    """


class FileLoadError(DataEngineError):
    """
    Raised when a chat export cannot be loaded.

    Examples
    --------
    - File does not exist.
    - File cannot be opened.
    - Unsupported encoding.
    - Insufficient permissions.
    """


class InvalidExportFormatError(DataEngineError):
    """
    Raised when the input file is not a supported chat export format.

    Examples
    --------
    - Incorrect file structure.
    - Missing required columns.
    - Invalid delimiter.
    - Corrupted export.
    """


class MalformedRecordError(DataEngineError):
    """
    Raised when an individual message record is malformed.

    Examples
    --------
    - Missing timestamp.
    - Missing sender.
    - Missing message.
    - Invalid field count.
    """


class ParsingError(DataEngineError):
    """
    Raised when a record cannot be parsed successfully.

    Examples
    --------
    - Invalid timestamp format.
    - Unexpected parser state.
    - Failed field extraction.
    """
