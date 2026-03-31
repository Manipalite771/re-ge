"""Anthropic Bedrock client wrapper for Claude Opus 4.6."""

import json
from typing import Optional

import anthropic

from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    ANTHROPIC_MODEL,
    MAX_TOKENS,
)


_client: Optional[anthropic.AnthropicBedrock] = None


def get_client() -> anthropic.AnthropicBedrock:
    """Get or create the Bedrock client (singleton)."""
    global _client
    if _client is None:
        _client = anthropic.AnthropicBedrock(
            aws_access_key=AWS_ACCESS_KEY_ID,
            aws_secret_key=AWS_SECRET_ACCESS_KEY,
            aws_region=AWS_REGION,
        )
    return _client


def call_llm(
    user_prompt: str,
    system_prompt: str = "",
    temperature: float = 0.3,
    max_tokens: int = MAX_TOKENS,
    response_format: str = "text",
) -> str:
    """Make a single LLM call and return the text response.

    Args:
        user_prompt: The user message content.
        system_prompt: Optional system message.
        temperature: Sampling temperature.
        max_tokens: Max tokens in response.
        response_format: "text" or "json" — if json, instructs the model to respond in JSON.
    """
    client = get_client()

    if response_format == "json" and "JSON" not in user_prompt:
        user_prompt += "\n\nRespond with valid JSON only. No markdown fences."

    messages = [{"role": "user", "content": user_prompt}]

    kwargs = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages,
    }
    if system_prompt:
        kwargs["system"] = system_prompt

    response = client.messages.create(**kwargs)

    text = response.content[0].text

    if response_format == "json":
        # Strip markdown fences if model added them
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
        text = text.strip()

    return text


def call_llm_json(
    user_prompt: str,
    system_prompt: str = "",
    temperature: float = 0.0,
    max_tokens: int = MAX_TOKENS,
) -> dict:
    """Make an LLM call and parse the response as JSON."""
    text = call_llm(
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format="json",
    )
    return json.loads(text)
