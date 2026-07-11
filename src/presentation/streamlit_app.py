# src/presentation/streamlit_app.py

"""
Attendance Dashboard Application

Purpose
-------
Application entry point for the OYBS WhatsApp Attendance Dashboard.

Responsibilities
----------------
- Configure the Streamlit application.
- Initialize the Presentation Context.
- Render the application header.
- Route navigation to the selected page.
- Handle unexpected application-level exceptions.

Architectural Rules
-------------------
This module intentionally remains thin.

It must:
- Configure the Presentation layer.
- Delegate navigation.
- Delegate page rendering.

It must not:
- Perform business logic.
- Access Infrastructure directly.
- Perform analytics.
- Parse data.
- Build Session aggregates.

Dependency Flow
---------------
Presentation
    ↓
Application
    ↓
Domain
    ↑
Infrastructure

Author
------
OYBS Attendance Dashboard

Created
-------
July 2026
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
import traceback

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import context, navigation, theme

# ============================================================================
# Application Entry Point
# ============================================================================


def main() -> None:
    """
    Launch the Streamlit application.

    Responsibilities
    ----------------
    1. Configure Streamlit.
    2. Initialize presentation context.
    3. Render application header.
    4. Determine selected page.
    5. Delegate rendering.
    """

    theme.configure_page()

    context.initialize()

    theme.render_application_header()

    page_renderer = navigation.get_selected_page()

    page_renderer()


# ============================================================================
# Direct Execution Support
# ============================================================================


def run() -> None:
    """
    Execute the application with error handling.

    Used when this module is launched directly.
    """

    try:
        main()

    except Exception:
        st.error(
            "An unexpected application error occurred.",
        )

        with st.expander(
            "Technical Details",
        ):
            st.code(
                traceback.format_exc(),
            )


# ============================================================================
# Bootstrap
# ============================================================================

if __name__ == "__main__":
    run()
