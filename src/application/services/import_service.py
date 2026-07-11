# src/application/services/import_service.py

"""
Import Application Service

Purpose
-------
Coordinates the complete WhatsApp chat import workflow.

Responsibilities
----------------
- Load a WhatsApp chat export.
- Parse raw chat text.
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
from src.infrastructure.data_engine.parser import parse_chat
from src.infrastructure.data_engine.validator import validate_records


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
            Path to the exported WhatsApp .txt file.

        Returns
        -------
        Session
            Fully constructed Session aggregate.
        """

        raw_text = load_chat(filepath)

        parsed_records = parse_chat(raw_text)

        cleaned_records = clean_records(parsed_records)

        messages = validate_records(cleaned_records)

        if not messages:
            raise ValueError("No valid messages were found in the chat export.")

        session_date = messages[0].timestamp.date()

        return self._dashboard_service.build_session(
            session_date=session_date,
            messages=messages,
        )

    # ------------------------------------------------------------------
    # Service Accessor
    # ------------------------------------------------------------------

    @property
    def dashboard_service(self) -> DashboardService:
        """
        Return the DashboardService used by this service.
        """

        return self._dashboard_service

    # ------------------------------------------------------------------
    # Dunder Methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """
        Return the official representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"dashboard_service="
            f"{self.dashboard_service.__class__.__name__})"
        )

    def __str__(self) -> str:
        """
        Return a human-readable representation.
        """

        return self.__repr__()
