# infrastructure/config/regex.py

"""
Regex Configuration

Purpose:
    Central repository for all compiled regular expressions used
    throughout the Attendance Dashboard application.

Responsibilities:
    - WhatsApp message parsing
    - Date extraction
    - Time extraction
    - Attendance detection
    - System message detection
    - Media message detection
    - Phone number extraction

Notes:
    This module exposes ONLY compiled regular expressions.
    Raw regex strings should never be imported elsewhere.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

import re
from re import Pattern

###############################################################################
# DATE / TIME
###############################################################################

# Example:
# 12/06/2025, 08:34 - John Doe: done

DATE_PATTERN: Pattern[str] = re.compile(r"\d{1,2}/\d{1,2}/\d{2,4}")

TIME_PATTERN: Pattern[str] = re.compile(r"\d{1,2}:\d{2}")

DATETIME_PATTERN: Pattern[str] = re.compile(
    r"""
    ^
    (?P<date>\d{1,2}/\d{1,2}/\d{2,4})
    ,
    \s*
    (?P<time>\d{1,2}:\d{2})
    """,
    re.VERBOSE,
)

###############################################################################
# WHATSAPP MESSAGE PARSER
###############################################################################

# Captures:
#
# date
# time
# sender
# message
#
# Example:
#
# 12/05/2025, 20:14 - John Doe: done

WHATSAPP_MESSAGE_PATTERN: Pattern[str] = re.compile(
    r"""
    ^
    (?P<date>\d{1,2}/\d{1,2}/\d{2,4})
    ,
    \s*
    (?P<time>\d{1,2}:\d{2})
    \s*-\s*
    (?P<sender>.*?)
    :
    \s*
    (?P<message>.*)
    $
    """,
    re.VERBOSE,
)

###############################################################################
# ATTENDANCE
###############################################################################

DONE_PATTERN: Pattern[str] = re.compile(
    r"^\s*done[.!?]*\s*$",
    re.IGNORECASE,
)

PRESENT_PATTERN: Pattern[str] = re.compile(
    r"^\s*present[.!?]*\s*$",
    re.IGNORECASE,
)

ABSENT_PATTERN: Pattern[str] = re.compile(
    r"^\s*absent[.!?]*\s*$",
    re.IGNORECASE,
)

LATE_PATTERN: Pattern[str] = re.compile(
    r"^\s*late[.!?]*\s*$",
    re.IGNORECASE,
)

###############################################################################
# ACTIVITY
###############################################################################

SCRIPTURE_READING_PATTERN: Pattern[str] = re.compile(
    r"scriptures?\s+reading",
    re.IGNORECASE,
)

OPENING_PRAYER_PATTERN: Pattern[str] = re.compile(
    r"opening\s+prayer",
    re.IGNORECASE,
)

CLOSING_PRAYER_PATTERN: Pattern[str] = re.compile(
    r"closing\s+prayer",
    re.IGNORECASE,
)

###############################################################################
# MEDIA
###############################################################################

MEDIA_PATTERN: Pattern[str] = re.compile(
    r"<media omitted>",
    re.IGNORECASE,
)

IMAGE_PATTERN: Pattern[str] = re.compile(
    r"image omitted",
    re.IGNORECASE,
)

VIDEO_PATTERN: Pattern[str] = re.compile(
    r"video omitted",
    re.IGNORECASE,
)

STICKER_PATTERN: Pattern[str] = re.compile(
    r"sticker omitted",
    re.IGNORECASE,
)

###############################################################################
# SYSTEM MESSAGES
###############################################################################

SYSTEM_MESSAGE_PATTERN: Pattern[str] = re.compile(
    r"""
    (
        joined\ using\ this\ group's\ invite\ link
        |
        left
        |
        removed
        |
        added
        |
        changed\ the\ subject
        |
        changed\ this\ group's\ description
        |
        created\ group
        |
        changed\ the\ group\ icon
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

###############################################################################
# DELETED MESSAGE
###############################################################################

DELETED_MESSAGE_PATTERN: Pattern[str] = re.compile(
    r"this message was deleted",
    re.IGNORECASE,
)

###############################################################################
# END-TO-END ENCRYPTION NOTICE
###############################################################################

ENCRYPTION_NOTICE_PATTERN: Pattern[str] = re.compile(
    r"end-to-end encrypted",
    re.IGNORECASE,
)

###############################################################################
# PHONE NUMBERS
###############################################################################

PHONE_NUMBER_PATTERN: Pattern[str] = re.compile(r"\+?\d[\d\s()-]{7,20}")

###############################################################################
# URLS
###############################################################################

URL_PATTERN: Pattern[str] = re.compile(
    r"https?://\S+",
    re.IGNORECASE,
)

###############################################################################
# EMAIL
###############################################################################

EMAIL_PATTERN: Pattern[str] = re.compile(
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
)

###############################################################################
# WHITESPACE
###############################################################################

MULTIPLE_WHITESPACE_PATTERN: Pattern[str] = re.compile(r"\s+")

LEADING_TRAILING_WHITESPACE_PATTERN: Pattern[str] = re.compile(r"^\s+|\s+$")

###############################################################################
# EMPTY MESSAGE
###############################################################################

EMPTY_MESSAGE_PATTERN: Pattern[str] = re.compile(r"^\s*$")

###############################################################################
# NUMERIC
###############################################################################

INTEGER_PATTERN: Pattern[str] = re.compile(r"^\d+$")

###############################################################################
# PUNCTUATION
###############################################################################

ENDING_PUNCTUATION_PATTERN: Pattern[str] = re.compile(r"[.!?]+$")
