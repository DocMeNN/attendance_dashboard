# src/infrastructure/ai/clients/gemini_client.py

"""
Gemini SDK Client

Purpose:
    Encapsulates all communication with the Google Gemini SDK.

Architecture:
    Infrastructure Layer

Dependencies:
    google-genai

Notes:
    This client is a thin wrapper around the Gemini SDK.
    It does not know about AIRequest, AIResponse,
    PromptTemplate, or any domain concepts.

Author: Me
"""

from __future__ import annotations

# Third-party imports
from google import genai
from google.genai import types

# Local application imports
from src.config.ai_config import AIConfig
from src.domain.ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIProviderError,
    AIRateLimitError,
)


class GeminiClient:
    """
    Thin wrapper around the Google Gemini SDK.
    """

    def __init__(self, config: AIConfig) -> None:
        """
        Initialize the Gemini client.
        """
        self._client = genai.Client(
            api_key=config.api_key,
        )

    def generate(
        self,
        *,
        model: str,
        prompt: str,
        system_prompt: str | None,
        temperature: float,
        max_tokens: int,
    ):
        """
        Generate text using Gemini.

        Returns
        -------
        GenerateContentResponse
            Raw SDK response.
        """

        try:
            return self._client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )

        except Exception as exc:
            #
            # Replace these mappings with official Gemini SDK
            # exception classes when they become available.
            #
            error_name = exc.__class__.__name__

            if "Authentication" in error_name:
                raise AIAuthenticationError(str(exc)) from exc

            if "RateLimit" in error_name:
                raise AIRateLimitError(str(exc)) from exc

            if "Connection" in error_name:
                raise AIConnectionError(str(exc)) from exc

            raise AIProviderError(str(exc)) from exc
