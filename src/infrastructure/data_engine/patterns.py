# src/infrastructure/data_engine/patterns.py

"""
Compiled regular expression patterns for the Infrastructure Data Engine.

This module centralizes every regular expression used by the data engine.
Patterns are compiled once at import time and shared across all modules.

Guiding Principles
------------------
- Compile once, use everywhere.
- Avoid inline regular expressions.
- Keep patterns focused on infrastructure concerns.
- Never implement business rules with regular expressions.

Current export format
---------------------
The parser consumes a canonical tab-separated export in the form::

    YYYY-MM-DD HH:MM:SS<TAB>Sender<TAB>Message

Example::

    2026-02-09 06:54:00    Jane Doe    Done
"""

from __future__ import annotations

import re

__all__ = [
    "TAB_DELIMITER_PATTERN",
    "WHITESPACE_PATTERN",
    "MULTIPLE_NEWLINES_PATTERN",
    "PHONE_NUMBER_PATTERN",
    "MEDIA_OMITTED_PATTERN",
    "DELETED_MESSAGE_PATTERN",
]

# ---------------------------------------------------------------------
# Generic whitespace
# ---------------------------------------------------------------------

WHITESPACE_PATTERN = re.compile(r"\s+")

MULTIPLE_NEWLINES_PATTERN = re.compile(r"\n{2,}")

# ---------------------------------------------------------------------
# Canonical export format
# ---------------------------------------------------------------------

TAB_DELIMITER_PATTERN = re.compile(r"\t")

# ---------------------------------------------------------------------
# Phone numbers
#
# Examples
# --------
# +2348061234567
# +1XXXXXXXXXX
# ---------------------------------------------------------------------

PHONE_NUMBER_PATTERN = re.compile(r"^\+\d{7,15}$")

# ---------------------------------------------------------------------
# WhatsApp placeholders
# ---------------------------------------------------------------------

MEDIA_OMITTED_PATTERN = re.compile(
    r"^<Media omitted>$",
    re.IGNORECASE,
)

DELETED_MESSAGE_PATTERN = re.compile(
    r"^This message was deleted$",
    re.IGNORECASE,
)
