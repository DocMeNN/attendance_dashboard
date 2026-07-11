# src/infrastructure/ai/providers/base_provider.py

"""
Base AI Provider

Purpose:
    Provides shared functionality for all AI provider
    implementations.

Architecture:
    Infrastructure Layer

Dependencies:
    Configuration Layer
    Domain Layer

Notes:
    Concrete providers inherit from this class and implement
    the `generate()` method defined by the AIProvider interface.

Author: Me
"""

from __future__ import annotations

# Standard library imports
from abc import ABC
from typing import Any

# Local application imports
from src.config.ai_config import AIConfig
from src.domain.ai.exceptions import AIResponseError
from src.domain.ai.interfaces import AIProvider


class BaseAIProvider(AIProvider, ABC):
    """
    Base class for concrete AI providers.
    """

    def __init__(self, config: AIConfig) -> None:
        """
        Initialize the provider.

        Parameters
        ----------
        config:
            Application AI configuration.
        """
        self._config = config

    @property
    def config(self) -> AIConfig:
        """
        Return the complete AI configuration.
        """
        return self._config

    @property
    def model(self) -> str:
        """
        Configured model name.
        """
        return self._config.model

    @property
    def timeout(self) -> int:
        """
        Configured request timeout.
        """
        return self._config.timeout

    @property
    def temperature(self) -> float:
        """
        Default generation temperature.
        """
        return self._config.temperature

    @property
    def max_tokens(self) -> int:
        """
        Default maximum output tokens.
        """
        return self._config.max_tokens

    @property
    def api_key(self) -> str | None:
        """
        Configured API key.
        """
        return self._config.api_key

    @property
    def base_url(self) -> str | None:
        """
        Configured base URL.
        """
        return self._config.base_url

    @staticmethod
    def require_text(content: str | None) -> str:
        """
        Validate that a provider returned text.

        Parameters
        ----------
        content:
            Text returned by the provider.

        Returns
        -------
        str
            Validated text.

        Raises
        ------
        AIResponseError
            If the response is empty.
        """
        if content is None:
            raise AIResponseError("AI provider returned no content.")

        text = content.strip()

        if not text:
            raise AIResponseError("AI provider returned an empty response.")

        return text

    @staticmethod
    def safe_int(value: Any) -> int:
        """
        Safely convert a value to an integer.

        Returns zero if conversion fails.
        """
        try:
            return int(value)
        except TypeError, ValueError:
            return 0
