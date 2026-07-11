# src/application/services/ai_service.py

"""
AI Service

Purpose:
    Coordinates AI interactions for the application.

Architecture:
    Application Layer

Dependencies:
    Domain layer
    Configuration layer
    Infrastructure factory

Notes:
    This service is provider-agnostic. It renders prompts,
    builds AI requests, and delegates generation to the
    configured AI provider.

Author: Me
"""

from __future__ import annotations

# Local application imports
from src.config.ai_config import AIConfig
from src.domain.ai.interfaces import AIProvider
from src.domain.ai.models import AIRequest, AIResponse
from src.domain.ai.prompts import PromptTemplate, render_prompt
from src.infrastructure.ai.provider_factory import AIProviderFactory


class AIService:
    """
    Coordinates AI operations for the application.
    """

    def __init__(
        self,
        config: AIConfig,
        provider: AIProvider | None = None,
    ) -> None:
        """
        Initialize the AI service.

        Parameters
        ----------
        config:
            AI configuration.

        provider:
            Optional provider implementation.
            Primarily used for dependency injection during testing.
        """

        self._config = config
        self._provider = provider or AIProviderFactory.create(config)

    def generate(
        self,
        template: PromptTemplate,
        **prompt_data: object,
    ) -> AIResponse:
        """
        Generate AI output using a prompt template.

        Parameters
        ----------
        template:
            Prompt template identifier.

        **prompt_data:
            Values used to render the prompt template.

        Returns
        -------
        AIResponse
            Structured AI response.
        """

        prompt = render_prompt(
            template,
            **prompt_data,
        )

        request = AIRequest(
            prompt=prompt,
            temperature=self._config.temperature,
            max_tokens=self._config.max_tokens,
        )

        return self._provider.generate(request)
