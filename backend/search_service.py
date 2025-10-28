import httpx
from typing import List, Optional
from models import SearchResult
from config import settings


class SearchService:
    """Service for web search using Tavily API."""

    def __init__(self):
        self.api_key = settings.tavily_api_key
        self.base_url = "https://api.tavily.com"

    async def search(
        self,
        query: str,
        max_results: int = 5,
        search_depth: str = "basic"
    ) -> List[SearchResult]:
        """
        Perform a web search using Tavily API.

        Args:
            query: Search query string
            max_results: Maximum number of results to return
            search_depth: "basic" or "advanced" for depth of search

        Returns:
            List of SearchResult objects
        """
        if not self.api_key:
            return []

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "max_results": max_results,
                        "search_depth": search_depth,
                        "include_answer": False,
                        "include_raw_content": False,
                    }
                )
                response.raise_for_status()
                data = response.json()

                results = []
                for item in data.get("results", []):
                    results.append(SearchResult(
                        title=item.get("title", ""),
                        url=item.get("url", ""),
                        content=item.get("content", ""),
                        score=item.get("score", 0.0)
                    ))

                return results

        except Exception as e:
            print(f"Search error: {e}")
            return []

    def format_search_results(self, results: List[SearchResult]) -> str:
        """Format search results into a readable string for the LLM."""
        if not results:
            return "No search results found."

        formatted = "## Search Results\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"### [{i}] {result.title}\n"
            formatted += f"**URL:** {result.url}\n"
            formatted += f"**Content:** {result.content}\n\n"

        return formatted
