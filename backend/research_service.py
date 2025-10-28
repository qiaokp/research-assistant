from typing import List, AsyncGenerator
from models import Message, SearchResult
from search_service import SearchService
from llm_service import LLMService
import asyncio


class DeepResearchService:
    """
    Service for deep research mode.

    Deep research performs multiple search iterations:
    1. Initial search based on user query
    2. Generate follow-up questions from initial results
    3. Perform additional searches for depth
    4. Synthesize all findings into comprehensive answer
    """

    def __init__(self):
        self.search_service = SearchService()
        self.llm_service = LLMService()

    async def conduct_research(
        self,
        query: str,
        messages: List[Message],
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        """
        Conduct deep research on a query.

        Args:
            query: The user's research query
            messages: Conversation history
            temperature: LLM temperature

        Yields:
            Research progress and final synthesis
        """
        yield "\n🔍 **Starting Deep Research Mode**\n\n"

        # Step 1: Initial search
        yield "**Step 1:** Performing initial web search...\n\n"
        initial_results = await self.search_service.search(
            query,
            max_results=5,
            search_depth="advanced"
        )

        if not initial_results:
            yield "⚠️ No search results found. Proceeding with LLM knowledge only.\n\n"
            async for chunk in self._generate_response(messages, None, temperature):
                yield chunk
            return

        yield f"Found {len(initial_results)} sources.\n\n"

        # Step 2: Generate follow-up questions
        yield "**Step 2:** Analyzing results and generating follow-up questions...\n\n"
        follow_up_queries = await self._generate_follow_up_questions(
            query,
            initial_results
        )

        if follow_up_queries:
            yield f"Generated {len(follow_up_queries)} follow-up questions:\n"
            for i, q in enumerate(follow_up_queries, 1):
                yield f"{i}. {q}\n"
            yield "\n"

        # Step 3: Perform follow-up searches
        all_results = initial_results.copy()
        if follow_up_queries:
            yield "**Step 3:** Conducting deeper research...\n\n"
            for i, follow_up_query in enumerate(follow_up_queries[:2], 1):  # Limit to 2 follow-ups
                yield f"Searching: {follow_up_query}\n"
                results = await self.search_service.search(
                    follow_up_query,
                    max_results=3,
                    search_depth="basic"
                )
                all_results.extend(results)
            yield f"\nTotal sources gathered: {len(all_results)}\n\n"

        # Step 4: Synthesize findings
        yield "**Step 4:** Synthesizing findings...\n\n"
        yield "---\n\n"

        # Create enriched context with all search results
        search_context = self.search_service.format_search_results(all_results)

        # Add search context to the conversation
        enriched_messages = messages.copy()
        enriched_messages.append(Message(
            role="system",
            content=f"You have access to the following search results to answer the user's question. Use these sources to provide a comprehensive, well-cited response:\n\n{search_context}"
        ))

        # Generate final response
        async for chunk in self._generate_response(enriched_messages, all_results, temperature):
            yield chunk

    async def _generate_follow_up_questions(
        self,
        original_query: str,
        results: List[SearchResult]
    ) -> List[str]:
        """Generate follow-up questions based on initial search results."""
        if not results:
            return []

        # Create a prompt to generate follow-up questions
        context = "\n".join([f"- {r.title}: {r.content[:200]}" for r in results[:3]])

        prompt_messages = [
            Message(
                role="system",
                content="You are a research assistant. Generate 2-3 focused follow-up questions to deepen research on a topic."
            ),
            Message(
                role="user",
                content=f"Original query: {original_query}\n\nInitial findings:\n{context}\n\nGenerate 2-3 specific follow-up questions to explore this topic more deeply. Return only the questions, one per line."
            )
        ]

        # Collect the response
        response = ""
        async for chunk in self.llm_service.stream_chat(
            prompt_messages,
            temperature=0.7,
            max_tokens=300
        ):
            response += chunk

        # Parse questions from response
        questions = [
            q.strip().lstrip("123456789.-) ")
            for q in response.split("\n")
            if q.strip() and len(q.strip()) > 10
        ]

        return questions[:3]  # Limit to 3 questions

    async def _generate_response(
        self,
        messages: List[Message],
        search_results: List[SearchResult] | None,
        temperature: float,
    ) -> AsyncGenerator[str, None]:
        """Generate the final response using the LLM."""
        async for chunk in self.llm_service.stream_chat(
            messages,
            temperature=temperature,
            max_tokens=3000
        ):
            yield chunk
