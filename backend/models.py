from pydantic import BaseModel
from typing import Optional, List, Literal


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    style: str = "default"
    deep_research: bool = False
    max_tokens: Optional[int] = 2000
    temperature: Optional[float] = 0.7


class StyleConfig(BaseModel):
    name: str
    display_name: str
    system_prompt: str
    description: str


class SearchResult(BaseModel):
    title: str
    url: str
    content: str
    score: float
