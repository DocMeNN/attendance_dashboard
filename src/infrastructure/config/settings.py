# infrastructure/config/settings.py

"""
Application Settings

Purpose:
    Defines the immutable runtime configuration for the OYBS Attendance
    Dashboard.

Responsibilities:
    - Centralize application configuration.
    - Compute project paths dynamically.
    - Provide a single immutable settings object.
    - Prevent duplicated configuration throughout the application.

Design Notes:
    - Constants belong in constants.py.
    - Runtime configuration belongs here.
    - This module should be the only source of application settings.

Author:
    OYBS Attendance Dashboard

Created:
    July 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .constants import (
    APPLICATION_NAME,
    APPLICATION_VERSION,
    DATE_FORMAT,
    DATETIME_FORMAT,
    DEFAULT_CHART_HEIGHT,
    DEFAULT_ENCODING,
    DEFAULT_LOG_LEVEL,
    DEFAULT_PAGE_SIZE,
    DEFAULT_TABLE_HEIGHT,
    DISPLAY_DATE_FORMAT,
    DISPLAY_DATETIME_FORMAT,
    TIME_FORMAT,
)


@dataclass(frozen=True, slots=True)
class AppSettings:
    """
    Immutable application configuration.

    This class centralizes runtime configuration and computed
    project paths.

    Attributes:
        application_name:
            Display name of the application.

        application_version:
            Current application version.

        encoding:
            Default file encoding.

        timezone:
            Default application timezone.

        project_root:
            Root directory of the repository.

        src_directory:
            Source code directory.

        data_directory:
            Input data directory.

        output_directory:
            Output directory.

        reports_directory:
            Report output directory.

        exports_directory:
            Export output directory.

        logs_directory:
            Logging directory.
    """

    # -----------------------------------------------------------------
    # Application
    # -----------------------------------------------------------------

    application_name: str = APPLICATION_NAME

    application_version: str = APPLICATION_VERSION

    timezone: str = "Africa/Lagos"

    encoding: str = DEFAULT_ENCODING

    # -----------------------------------------------------------------
    # Date & Time
    # -----------------------------------------------------------------

    date_format: str = DATE_FORMAT

    time_format: str = TIME_FORMAT

    datetime_format: str = DATETIME_FORMAT

    display_date_format: str = DISPLAY_DATE_FORMAT

    display_datetime_format: str = DISPLAY_DATETIME_FORMAT

    # -----------------------------------------------------------------
    # Dashboard
    # -----------------------------------------------------------------

    default_page_size: int = DEFAULT_PAGE_SIZE

    default_chart_height: int = DEFAULT_CHART_HEIGHT

    default_table_height: int = DEFAULT_TABLE_HEIGHT

    # -----------------------------------------------------------------
    # Logging
    # -----------------------------------------------------------------

    log_level: str = DEFAULT_LOG_LEVEL

    # -----------------------------------------------------------------
    # Computed Paths
    # -----------------------------------------------------------------

    @property
    def project_root(self) -> Path:
        """
        Returns the project root directory.

        Example:

            attendance_dashboard/
        """
        return Path(__file__).resolve().parents[3]

    @property
    def src_directory(self) -> Path:
        """Return the src directory."""
        return self.project_root / "src"

    @property
    def infrastructure_directory(self) -> Path:
        """Return infrastructure directory."""
        return self.src_directory / "infrastructure"

    @property
    def domain_directory(self) -> Path:
        """Return domain directory."""
        return self.src_directory / "domain"

    @property
    def application_directory(self) -> Path:
        """Return application directory."""
        return self.src_directory / "application"

    @property
    def presentation_directory(self) -> Path:
        """Return presentation directory."""
        return self.src_directory / "presentation"

    @property
    def data_directory(self) -> Path:
        """Return input data directory."""
        return self.project_root / "data"

    @property
    def output_directory(self) -> Path:
        """Return output directory."""
        return self.project_root / "output"

    @property
    def reports_directory(self) -> Path:
        """Return reports directory."""
        return self.output_directory / "reports"

    @property
    def exports_directory(self) -> Path:
        """Return exports directory."""
        return self.output_directory / "exports"

    @property
    def logs_directory(self) -> Path:
        """Return logs directory."""
        return self.project_root / "logs"

    @property
    def tests_directory(self) -> Path:
        """Return tests directory."""
        return self.project_root / "tests"

    # -----------------------------------------------------------------
    # Utility
    # -----------------------------------------------------------------

    def ensure_directories(self) -> None:
        """
        Create application directories if they do not already exist.
        """

        directories = (
            self.data_directory,
            self.output_directory,
            self.reports_directory,
            self.exports_directory,
            self.logs_directory,
        )

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Singleton Settings Instance
# ---------------------------------------------------------------------

settings = AppSettings()
