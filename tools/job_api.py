"""Client wrapper for job APIs."""

from __future__ import annotations

from typing import Any, Dict, List


class JobAPIClient:
    """Small abstraction for querying job listings."""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or "https://example.com/jobs"

    def search(self, query: str, location: str | None = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Return mock search results."""
        return [
            {
                "title": query,
                "location": location or "Remote",
                "source": self.base_url,
                "match_score": 0.9,
            }
        ][:limit]
