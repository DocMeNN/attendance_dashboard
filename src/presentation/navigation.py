# src/presentation/navigation.py

"""
Presentation Navigation

Purpose
-------
Provides centralized navigation for the Streamlit application.

Responsibilities
----------------
- Render sidebar navigation.
- Register available pages.
- Return the selected page renderer.

Architectural Rules
-------------------
- Presentation only.
- No business logic.
- No Domain access.
- No Infrastructure access.
"""

from __future__ import annotations

# ============================================================================
# Standard Library Imports
# ============================================================================
from collections.abc import Callable

# ============================================================================
# Third-Party Imports
# ============================================================================
import streamlit as st

# ============================================================================
# Local Imports
# ============================================================================
from src.presentation import theme
from src.presentation.pages import (
    activity_page,
    attendance_page,
    dashboard_page,
    reports_page,
    settings_page,
)

# ============================================================================
# Type Alias
# ============================================================================

PageRenderer = Callable[[], None]

# ============================================================================
# Page Registry
# ============================================================================

PAGE_REGISTRY: dict[str, PageRenderer] = {
    theme.DASHBOARD_PAGE: dashboard_page.render,
    theme.ATTENDANCE_PAGE: attendance_page.render,
    theme.ACTIVITY_PAGE: activity_page.render,
    theme.REPORTS_PAGE: reports_page.render,
    theme.SETTINGS_PAGE: settings_page.render,
}

# ============================================================================
# Navigation
# ============================================================================


def get_selected_page() -> PageRenderer:
    """
    Return the renderer for the selected page.
    """

    st.sidebar.title("Navigation")

    selected = st.sidebar.radio(
        "Go to",
        theme.NAVIGATION_PAGES,
    )

    return PAGE_REGISTRY[selected]
