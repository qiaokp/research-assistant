from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: Literal["ollama", "openrouter"] = "ollama"

    # Ollama settings
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"

    # OpenRouter settings
    openrouter_api_key: str = ""
    openrouter_model: str = "mistralai/mistral-7b-instruct"

    # Tavily settings
    tavily_api_key: str = ""

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
