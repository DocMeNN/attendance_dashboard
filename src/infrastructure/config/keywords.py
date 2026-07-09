# infrastructure/config/keywords.py

"""
Keywords

Purpose:
    Central repository for all application keywords used during parsing
    and analytics.

Responsibilities:
    - Attendance keywords
    - Activity keywords
    - WhatsApp system keywords
    - Excluded messages

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

# =============================================================================
# ATTENDANCE KEYWORDS
# =============================================================================

DONE = "done"

PRESENT = "present"

ABSENT = "absent"

LATE = "late"

ATTENDANCE_KEYWORDS: frozenset[str] = frozenset(
    {
        DONE,
        PRESENT,
        ABSENT,
        LATE,
    }
)

# =============================================================================
# ACTIVITY KEYWORDS
# =============================================================================

SCRIPTURES_READING = "SCRIPTURES READING"

OPENING_PRAYER = "OPENING PRAYER"

CLOSING_PRAYER = "CLOSING PRAYER"

WORSHIP = "WORSHIP"

ANNOUNCEMENT = "ANNOUNCEMENT"

ACTIVITY_KEYWORDS: frozenset[str] = frozenset(
    {
        SCRIPTURES_READING,
        OPENING_PRAYER,
        CLOSING_PRAYER,
        WORSHIP,
        ANNOUNCEMENT,
    }
)

# =============================================================================
# WHATSAPP SYSTEM MESSAGES
# =============================================================================

THIS_MESSAGE_WAS_DELETED = "This message was deleted"

MEDIA_OMITTED = "<Media omitted>"

IMAGE_OMITTED = "image omitted"

VIDEO_OMITTED = "video omitted"

STICKER_OMITTED = "sticker omitted"

MISSED_VOICE_CALL = "Missed voice call"

MISSED_VIDEO_CALL = "Missed video call"

END_TO_END_ENCRYPTION = "Messages and calls are end-to-end encrypted"

SYSTEM_KEYWORDS: frozenset[str] = frozenset(
    {
        THIS_MESSAGE_WAS_DELETED,
        MEDIA_OMITTED,
        IMAGE_OMITTED,
        VIDEO_OMITTED,
        STICKER_OMITTED,
        MISSED_VOICE_CALL,
        MISSED_VIDEO_CALL,
        END_TO_END_ENCRYPTION,
    }
)

# =============================================================================
# MEMBERSHIP EVENTS
# =============================================================================

JOINED_USING_INVITE = "joined using this group's invite link"

LEFT = "left"

REMOVED = "removed"

ADDED = "added"

CHANGED_SUBJECT = "changed the subject"

CHANGED_GROUP_DESCRIPTION = "changed this group's description"

GROUP_EVENT_KEYWORDS: frozenset[str] = frozenset(
    {
        JOINED_USING_INVITE,
        LEFT,
        REMOVED,
        ADDED,
        CHANGED_SUBJECT,
        CHANGED_GROUP_DESCRIPTION,
    }
)

# =============================================================================
# EXCLUDED MESSAGES
# =============================================================================

EXCLUDED_MESSAGES: frozenset[str] = frozenset(
    {
        THIS_MESSAGE_WAS_DELETED,
        MEDIA_OMITTED,
    }
)

# =============================================================================
# EXPORT LABELS
# =============================================================================

ATTENDANCE_LABEL = "Attendance"

ACTIVITY_LABEL = "Activity"

SUMMARY_LABEL = "Summary"
