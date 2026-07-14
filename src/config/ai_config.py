# src/config/ai_config.py

"""
AI Configuration

Purpose:
    Centralizes configuration settings for the AI subsystem.

Architecture:
    Configuration Layer

Dependencies:
    Standard Library Only

Notes:
    This module does not create AI clients or connect to providers.
    It simply exposes configuration values for the application.

Author: Me
"""

from __future__ import annotations

# Standard library imports
import os
from dataclasses import dataclass
from enum import StrEnum


class AIProvider(StrEnum):
    """
    Supported AI providers.
    """

    OPENAI = "openai"
    GEMINI = "gemini"
    OLLAMA = "ollama"


@dataclass(slots=True, frozen=True)
class AIConfig:
    """
    AI configuration settings.
    """

    provider: AIProvider
    model: str
    api_key: str | None
    base_url: str | None
    temperature: float
    max_tokens: int
    timeout: int


def load_ai_config() -> AIConfig:
    """
    Load AI configuration from environment variables.

    Returns
    -------
    AIConfig
        Application AI configuration.
    """

    provider = AIProvider(os.getenv("AI_PROVIDER", AIProvider.OLLAMA.value).lower())

    default_models = {
        AIProvider.OPENAI: "gpt-5.5",
        AIProvider.GEMINI: "gemini-flash-latest",
        AIProvider.OLLAMA: "llama3.2:3b",
    }

    model = os.getenv(
        "AI_MODEL",
        default_models[provider],
    )

    return AIConfig(
        provider=provider,
        model=model,
        api_key=os.getenv("AI_API_KEY"),
        base_url=os.getenv("AI_BASE_URL"),
        temperature=float(os.getenv("AI_TEMPERATURE", "0.3")),
        max_tokens=int(os.getenv("AI_MAX_TOKENS", "1024")),
        timeout=int(os.getenv("AI_TIMEOUT", "60")),
    )
