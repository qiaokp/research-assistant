import httpx
from typing import List, AsyncGenerator, Optional
from models import Message
from config import settings


class LLMService:
    """Service for interacting with open-source LLMs."""

    def __init__(self):
        self.provider = settings.llm_provider

    async def stream_chat(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat completions from the LLM.

        Args:
            messages: List of conversation messages
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Yields:
            String chunks of the response
        """
        if self.provider == "ollama":
            async for chunk in self._stream_ollama(messages, temperature, max_tokens):
                yield chunk
        elif self.provider == "openrouter":
            async for chunk in self._stream_openrouter(messages, temperature, max_tokens):
                yield chunk
        else:
            yield f"Error: Unknown provider '{self.provider}'"

    async def _stream_ollama(
        self,
        messages: List[Message],
        temperature: float,
        max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        """Stream from Ollama."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Convert messages to Ollama format
                ollama_messages = [
                    {"role": msg.role, "content": msg.content}
                    for msg in messages
                ]

                async with client.stream(
                    "POST",
                    f"{settings.ollama_base_url}/api/chat",
                    json={
                        "model": settings.ollama_model,
                        "messages": ollama_messages,
                        "stream": True,
                        "options": {
                            "temperature": temperature,
                            "num_predict": max_tokens,
                        }
                    }
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line:
                            import json
                            data = json.loads(line)
                            if "message" in data:
                                content = data["message"].get("content", "")
                                if content:
                                    yield content

        except Exception as e:
            yield f"Error connecting to Ollama: {str(e)}\n\n"
            yield "Make sure Ollama is running (ollama serve) and the model is pulled.\n"
            yield f"Try: ollama pull {settings.ollama_model}"

    async def _stream_openrouter(
        self,
        messages: List[Message],
        temperature: float,
        max_tokens: int,
    ) -> AsyncGenerator[str, None]:
        """Stream from OpenRouter."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                headers = {
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                }

                openrouter_messages = [
                    {"role": msg.role, "content": msg.content}
                    for msg in messages
                ]

                async with client.stream(
                    "POST",
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": settings.openrouter_model,
                        "messages": openrouter_messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens,
                        "stream": True,
                    }
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            if data_str == "[DONE]":
                                break

                            import json
                            try:
                                data = json.loads(data_str)
                                if "choices" in data:
                                    delta = data["choices"][0].get("delta", {})
                                    content = delta.get("content", "")
                                    if content:
                                        yield content
                            except json.JSONDecodeError:
                                continue

        except Exception as e:
            yield f"Error connecting to OpenRouter: {str(e)}\n\n"
            yield "Make sure your OPENROUTER_API_KEY is set correctly."
