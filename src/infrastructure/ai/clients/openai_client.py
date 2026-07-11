# src/infrastructure/ai/clients/openai_client.py

"""
OpenAI SDK Client

Purpose:
    Encapsulates all communication with the OpenAI SDK.

Architecture:
    Infrastructure Layer

Author: Me
"""

from __future__ import annotations

from typing import Any

from openai import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

from src.config.ai_config import AIConfig
from src.domain.ai.exceptions import (
    AIAuthenticationError,
    AIConnectionError,
    AIProviderError,
    AIRateLimitError,
)


class OpenAIClient:
    """
    Thin wrapper around the OpenAI SDK.
    """

    def __init__(self, config: AIConfig) -> None:
        self._client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
        )

    def generate(
        self,
        *,
        model: str,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
    ) -> Any:
        """
        Execute a completion request.

        Returns
        -------
        Raw OpenAI SDK response.
        """

        try:
            return self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        except AuthenticationError as exc:
            raise AIAuthenticationError("OpenAI authentication failed.") from exc

        except RateLimitError as exc:
            raise AIRateLimitError("OpenAI rate limit exceeded.") from exc

        except APIConnectionError as exc:
            raise AIConnectionError("Unable to connect to OpenAI.") from exc

        except APIStatusError as exc:
            raise AIProviderError(f"OpenAI returned HTTP {exc.status_code}.") from exc
