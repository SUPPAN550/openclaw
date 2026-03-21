import os
import ssl
import httpx
import urllib3
from typing import Any, Optional

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from langchain_openai import ChatOpenAI

from .base_client import BaseLLMClient
from .validators import validate_model


class MiniMaxClient(BaseLLMClient):
    """Client for MiniMax LLM provider."""

    # MiniMax API configuration
    DEFAULT_BASE_URL = "https://api.minimax.chat/v1"

    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(model, base_url, **kwargs)
        self._group_id = kwargs.get("group_id")

    def get_llm(self) -> Any:
        """Return configured ChatOpenAI instance for MiniMax."""
        llm_kwargs = {
            "model": self.model,
            "base_url": self.base_url or self.DEFAULT_BASE_URL,
        }

        # Get API key from parameter or environment
        api_key = self.kwargs.get("api_key") or os.environ.get("MINIMAX_API_KEY")
        if api_key:
            llm_kwargs["api_key"] = api_key

        # Get group_id from parameter or environment
        group_id = self._group_id or os.environ.get("MINIMAX_GROUP_ID")
        if group_id:
            # MiniMax requires group_id in the headers
            llm_kwargs["default_headers"] = {"MGROUP-ID": group_id}

        # Create HTTP client with proper settings for langgraph compatibility
        # Using HTTPXAdapter with custom settings to avoid connection issues
        http_client = httpx.Client(
            timeout=httpx.Timeout(120.0, connect=10.0),
            # Allow reusing connections but with fresh ones for langgraph
            limits=httpx.Limits(
                max_keepalive_connections=2, 
                max_connections=5,
                keepalive_expiry=5.0
            ),
        )
        llm_kwargs["http_client"] = http_client

        # Pass through other optional parameters
        for key in ("max_retries", "callbacks"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return ChatOpenAI(**llm_kwargs)

    def validate_model(self) -> bool:
        """Validate model for MiniMax."""
        return validate_model("minimax", self.model)
