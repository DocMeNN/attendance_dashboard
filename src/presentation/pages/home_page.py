# src/presentation/pages/home_page.py

"""
Home Page

Purpose
-------
Provides the landing workspace for the OYBS Attendance Dashboard.

Responsibilities
----------------
- Upload WhatsApp chat exports.
- Configure expected attendees.
- Delegate chat importing to ImportService.
- Store the resulting Session through Presentation Context.
- Display current session status.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No analytics calculations.
- No direct parsing.
- No Infrastructure access.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
import tempfile
from pathlib import Path

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import context
from src.presentation.components.common import (
    filters,
    sidebar,
)

# ============================================================================
# Constants
# ============================================================================

APPLICATION_NAME = "OYBS WhatsApp Attendance Dashboard"

# ============================================================================
# Helpers
# ============================================================================


def _render_sidebar() -> None:
    """
    Render the application sidebar.
    """

    sidebar.render_title("Application")

    sidebar.render_info(
        APPLICATION_NAME,
    )

    sidebar.render_divider()

    sidebar.render_section("Status")

    if context.has_session():
        sidebar.render_success("Session Loaded")
    else:
        sidebar.render_warning("No Session Loaded")

    sidebar.render_divider()

    sidebar.render_text(
        f"Expected Attendees: {context.expected_attendees()}",
    )


def _render_configuration() -> None:
    """
    Render application configuration controls.
    """

    st.subheader("Configuration")

    expected_attendees = filters.render_number_input(
        label="Expected Attendees",
        value=context.expected_attendees(),
        minimum=0,
        maximum=1000,
    )

    context.set_expected_attendees(
        expected_attendees,
    )


def _render_upload() -> None:
    """
    Render the WhatsApp chat upload workflow.
    """

    st.subheader("Upload WhatsApp Chat")

    uploaded_file = st.file_uploader(
        "Select a WhatsApp exported chat (.txt)",
        type=["txt"],
    )

    if uploaded_file is None:
        return

    if not st.button(
        "Build Session",
        type="primary",
        use_container_width=True,
    ):
        return

    with st.spinner("Building session..."):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt",
        ) as temp_file:
            temp_file.write(
                uploaded_file.getvalue(),
            )
            temp_path = Path(
                temp_file.name,
            )

        try:
            session = context.import_service().import_chat(
                temp_path,
            )

            context.set_session(
                session,
            )

            st.success(
                "Session successfully loaded.",
            )

            st.rerun()

        except Exception as exc:
            st.error(
                str(exc),
            )

        finally:
            temp_path.unlink(
                missing_ok=True,
            )


def _render_session_status() -> None:
    """
    Render the current Session status.
    """

    st.subheader("Current Session")

    if not context.has_session():
        st.info(
            "No session loaded.",
        )
        return

    session = context.current_session()

    if session is None:
        return

    left_column, right_column = st.columns(2)

    with left_column:
        st.metric(
            "Session Date",
            str(session.session_date),
        )

        st.metric(
            "Attendees",
            session.attendee_count,
        )

    with right_column:
        st.metric(
            "Done Events",
            session.done_count,
        )

        st.metric(
            "Activity Events",
            session.activity_count,
        )


# ============================================================================
# Public API
# ============================================================================


def render() -> None:
    """
    Render the Home page.
    """

    context.initialize()

    _render_sidebar()

    st.title("🏠 Home")

    st.write(
        """
Welcome to the **OYBS WhatsApp Attendance Dashboard**.

Upload a WhatsApp chat export to begin analysing attendance,
activity and engagement.
"""
    )

    st.divider()

    _render_configuration()

    st.divider()

    _render_upload()

    st.divider()

    _render_session_status()
