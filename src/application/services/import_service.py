# src/application/services/import_service.py

"""
Import Application Service

Purpose
-------
Coordinates the complete WhatsApp chat import workflow.

Responsibilities
----------------
- Load a WhatsApp chat export.
- Detect the export format.
- Delegate parsing to the appropriate parser.
- Clean parsed records.
- Validate cleaned records.
- Build a Session aggregate.
- Return a ready-to-use Session.

Architectural Rules
-------------------
- Orchestrates application workflow only.
- Contains no business logic.
- Contains no UI code.
- Contains no analytics.

Dependency Flow
---------------
Presentation
    ↓
ImportService
    ↓
Infrastructure Data Engine
    ↓
Domain Models
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from pathlib import Path

# ============================================================================
# Local Imports
# ============================================================================
from src.application.services.dashboard_service import DashboardService
from src.domain.models.session import Session
from src.infrastructure.data_engine.cleaner import clean_records
from src.infrastructure.data_engine.loader import load_chat
from src.infrastructure.data_engine.models import RawMessageRecord
from src.infrastructure.data_engine.parser import parse_chat
from src.infrastructure.data_engine.validator import validate_records
from src.infrastructure.data_engine.whatsapp_parser import (
    parse_whatsapp_chat,
)

# ============================================================================
# Import Service
# ============================================================================


class ImportService:
    """
    Application service responsible for importing WhatsApp chat exports.
    """

    def __init__(
        self,
        dashboard_service: DashboardService | None = None,
    ) -> None:
        """
        Initialize the ImportService.
        """

        self._dashboard_service = (
            dashboard_service if dashboard_service is not None else DashboardService()
        )

    # ------------------------------------------------------------------
    # Import Workflow
    # ------------------------------------------------------------------

    def import_chat(
        self,
        filepath: str | Path,
    ) -> Session:
        """
        Import a WhatsApp chat export and build a Session.

        Parameters
        ----------
        filepath
            Path to the exported chat file.

        Returns
        -------
        Session
            Fully constructed Session aggregate.
        """

        raw_text = load_chat(
            filepath,
        )

        parsed_records = self._parse_records(
            raw_text,
        )

        cleaned_records = clean_records(
            parsed_records,
        )

        messages = validate_records(
            cleaned_records,
        )

        if not messages:
            raise ValueError("No valid messages were found in the chat export.")

        session_date = messages[0].timestamp.date()

        return self._dashboard_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Parser Selection
    # ------------------------------------------------------------------

    def _parse_records(
        self,
        raw_text: str,
    ) -> list[RawMessageRecord]:
        """
        Parse the chat using the appropriate parser.

        Native WhatsApp exports are parsed by
        ``whatsapp_parser.py``.

        Canonical tab-separated exports are parsed by
        ``parser.py``.
        """

        if self._is_whatsapp_export(
            raw_text,
        ):
            return parse_whatsapp_chat(
                raw_text,
            )

        return parse_chat(
            raw_text,
        )

    def _is_whatsapp_export(
        self,
        raw_text: str,
    ) -> bool:
        """
        Return True when the text appears to be a
        native WhatsApp export.
        """

        for line in raw_text.splitlines():

            line = line.strip()

            if not line:
                continue

            return " - " in line and ":" in line and "\t" not in line

        return False

    # ------------------------------------------------------------------
    # Service Accessor
    # ------------------------------------------------------------------

    @property
    def dashboard_service(
        self,
    ) -> DashboardService:
        """
        Return the DashboardService used by this service.
        """

        return self._dashboard_service

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(
        self,
    ) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"dashboard_service="
            f"{self.dashboard_service.__class__.__name__})"
        )

    def __str__(
        self,
    ) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
