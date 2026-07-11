# src/presentation/__init__.py

"""
Presentation Layer

Purpose
-------
Provides the user interface layer for the Attendance Dashboard
application.

The Presentation layer is responsible for:

- Rendering Streamlit pages
- Managing navigation
- Applying UI themes
- Displaying analytics and reports
- Handling user interactions

Architectural Rules
-------------------
- Must depend only on the Application layer.
- Must never access Infrastructure directly.
- Must never contain business rules.
- Must never modify Domain objects.

Dependency Direction
--------------------
Presentation
    ↓
Application
    ↓
Domain
    ↑
Infrastructure
"""

from __future__ import annotations
