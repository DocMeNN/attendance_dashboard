# src/domain/ai/interfaces.py

"""
AI Provider Interface

Purpose:
    Defines the contract for all AI providers used by the application.

Architecture:
    Domain Layer

Dependencies:
    None

Notes:
    The Domain layer must never depend on OpenAI, Gemini, Ollama,
    Streamlit, or any external SDK.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from abc import ABC, abstractmethod

# Local application imports
from .models import AIRequest, AIResponse


class AIProvider(ABC):
    """
    Abstract interface for AI providers.

    Every concrete provider (OpenAI, Gemini, Ollama, etc.)
    must implement this interface.
    """

    @abstractmethod
    def generate(self, request: AIRequest) -> AIResponse:
        """
        Generate an AI response.

        Parameters
        ----------
        request:
            Structured AI request.

        Returns
        -------
        AIResponse
            Structured response from the AI provider.
        """
        raise NotImplementedError
