# src/infrastructure/ai/clients/__init__.py

"""
AI SDK Clients

Purpose:
    Exposes SDK client wrappers used by AI providers.

Architecture:
    Infrastructure Layer

Author: Me
"""

from .gemini_client import GeminiClient
from .ollama_client import OllamaClient
from .openai_client import OpenAIClient

__all__ = [
    "GeminiClient",
    "OllamaClient",
    "OpenAIClient",
]
