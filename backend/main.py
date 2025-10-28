from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator
import json

from models import ChatRequest, Message
from config import settings
from styles import get_style, get_all_styles
from llm_service import LLMService
from search_service import SearchService
from research_service import DeepResearchService

app = FastAPI(title="Research Assistant API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
llm_service = LLMService()
search_service = SearchService()
research_service = DeepResearchService()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "provider": settings.llm_provider,
        "model": settings.ollama_model if settings.llm_provider == "ollama" else settings.openrouter_model
    }


@app.get("/styles")
async def list_styles():
    """Get all available conversation styles."""
    styles = get_all_styles()
    return {
        "styles": [
            {
                "name": style.name,
                "display_name": style.display_name,
                "description": style.description
            }
            for style in styles.values()
        ]
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint with support for different styles and deep research mode.

    Request body:
        - messages: List of conversation messages
        - style: Conversation style (default, concise, explanatory, etc.)
        - deep_research: Enable deep research mode (default: false)
        - temperature: LLM temperature (default: 0.7)
        - max_tokens: Maximum tokens to generate (default: 2000)

    Returns:
        Server-Sent Events stream of response chunks
    """
    try:
        # Get the selected style
        style_config = get_style(request.style)

        # Prepare messages with system prompt
        messages = [
            Message(role="system", content=style_config.system_prompt),
            *request.messages
        ]

        async def generate() -> AsyncGenerator[str, None]:
            """Generate SSE stream."""
            try:
                if request.deep_research and len(request.messages) > 0:
                    # Deep research mode
                    user_query = request.messages[-1].content
                    async for chunk in research_service.conduct_research(
                        user_query,
                        messages,
                        request.temperature or 0.7
                    ):
                        yield f"data: {json.dumps({'content': chunk})}\n\n"
                else:
                    # Standard chat mode - optionally with web search
                    # Check if we should perform a web search (if query seems to need current info)
                    should_search = request.deep_research or _should_use_search(request.messages[-1].content if request.messages else "")

                    if should_search and settings.tavily_api_key:
                        # Perform a quick search
                        user_query = request.messages[-1].content
                        search_results = await search_service.search(user_query, max_results=3)

                        if search_results:
                            search_context = search_service.format_search_results(search_results)
                            messages.append(Message(
                                role="system",
                                content=f"Relevant search results:\n\n{search_context}"
                            ))

                    # Stream the LLM response
                    async for chunk in llm_service.stream_chat(
                        messages,
                        request.temperature or 0.7,
                        request.max_tokens or 2000
                    ):
                        yield f"data: {json.dumps({'content': chunk})}\n\n"

                yield f"data: {json.dumps({'done': True})}\n\n"

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                yield f"data: {json.dumps({'error': error_msg})}\n\n"

        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _should_use_search(query: str) -> bool:
    """Determine if a query should trigger web search."""
    # Keywords that suggest need for current information
    search_keywords = [
        "latest", "current", "recent", "today", "now", "2024", "2025",
        "news", "update", "what is", "who is", "when did"
    ]
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in search_keywords)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
