# infrastructure/config/constants.py

"""
Constants

Purpose:
    Central location for immutable application-wide constants.

Responsibilities:
    - Date and time formats
    - File extensions
    - Default values
    - Attendance statuses
    - Report names
    - Export settings

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from pathlib import Path

# =============================================================================
# APPLICATION
# =============================================================================

APPLICATION_NAME: str = "OYBS Attendance Dashboard"
APPLICATION_VERSION: str = "1.0.0"

# =============================================================================
# ENCODING
# =============================================================================

DEFAULT_ENCODING: str = "utf-8"

# =============================================================================
# FILE EXTENSIONS
# =============================================================================

WHATSAPP_EXPORT_EXTENSION: str = ".txt"

EXCEL_EXTENSION: str = ".xlsx"

CSV_EXTENSION: str = ".csv"

PDF_EXTENSION: str = ".pdf"

SUPPORTED_INPUT_EXTENSIONS: tuple[str, ...] = (WHATSAPP_EXPORT_EXTENSION,)

# =============================================================================
# DIRECTORY NAMES
# =============================================================================

DATA_DIRECTORY = Path("data")

OUTPUT_DIRECTORY = Path("output")

LOG_DIRECTORY = Path("logs")

REPORT_DIRECTORY = OUTPUT_DIRECTORY / "reports"

EXPORT_DIRECTORY = OUTPUT_DIRECTORY / "exports"

# =============================================================================
# DATE & TIME
# =============================================================================

DATE_FORMAT = "%d/%m/%Y"

TIME_FORMAT = "%H:%M"

DATETIME_FORMAT = "%d/%m/%Y, %H:%M"

DISPLAY_DATE_FORMAT = "%d %b %Y"

DISPLAY_DATETIME_FORMAT = "%d %b %Y %H:%M"

# =============================================================================
# ATTENDANCE STATUS
# =============================================================================

STATUS_PRESENT = "Present"

STATUS_ABSENT = "Absent"

STATUS_LATE = "Late"

STATUS_UNKNOWN = "Unknown"

VALID_ATTENDANCE_STATUS = (
    STATUS_PRESENT,
    STATUS_ABSENT,
    STATUS_LATE,
)

# =============================================================================
# REPORTS
# =============================================================================

ATTENDANCE_REPORT_NAME = "Attendance Report"

ACTIVITY_REPORT_NAME = "Activity Report"

SUMMARY_REPORT_NAME = "Summary Report"

# =============================================================================
# SHEETS
# =============================================================================

ATTENDANCE_SHEET = "Attendance"

ACTIVITY_SHEET = "Activities"

SUMMARY_SHEET = "Summary"

# =============================================================================
# EXPORTS
# =============================================================================

DEFAULT_EXCEL_ENGINE = "openpyxl"

DEFAULT_PDF_FILENAME = "attendance_report.pdf"

DEFAULT_EXCEL_FILENAME = "attendance_report.xlsx"

DEFAULT_CSV_FILENAME = "attendance_report.csv"

# =============================================================================
# LOGGING
# =============================================================================

DEFAULT_LOG_LEVEL = "INFO"

DEFAULT_LOG_FILE = "attendance_dashboard.log"

# =============================================================================
# VALIDATION
# =============================================================================

MINIMUM_MESSAGE_LENGTH = 1

MAXIMUM_MESSAGE_LENGTH = 10000

# =============================================================================
# DASHBOARD
# =============================================================================

DEFAULT_PAGE_SIZE = 25

DEFAULT_CHART_HEIGHT = 450

DEFAULT_TABLE_HEIGHT = 500
