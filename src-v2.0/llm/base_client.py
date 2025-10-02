from abc import ABC, abstractmethod

from ..utils.config import ModelParameters
from .llm_basics import LLMMessage, LLMResponse
import os, sys

class BaseLLMClient(ABC):
    """Base class for LLM clients."""

    def __init__(self, model_parameters: ModelParameters):
        self.api_key: str = model_parameters.api_key
        self.base_url: str | None = model_parameters.base_url
        self.api_version: str | None = model_parameters.api_version

    @abstractmethod
    def set_chat_history(self, messages: list[LLMMessage]) -> None:
        """Set the chat history."""
        pass

    @abstractmethod
    def chat(
        self,
        messages: list[LLMMessage],
        model_parameters: ModelParameters,
        reuse_history: bool = True,
        temperature: float | None = None,
    ) -> LLMResponse:
        """Send chat messages to the LLM."""
        pass