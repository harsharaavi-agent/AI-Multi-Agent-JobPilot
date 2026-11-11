"""Job search agent responsible for fetching and filtering jobs."""

from __future__ import annotations

from typing import Any, Dict, List


class JobSearchAgent:
    """Collects and prioritizes relevant jobs from supported sources."""

    def __init__(self, client: Any | None = None):
        self.client = client

    def search(self, query: str, location: str | None = None, max_results: int = 10) -> List[Dict[str, Any]]:
        """Return a list of jobs matching the query."""
        if self.client is not None:
            return self.client.search(query=query, location=location, limit=max_results)

        return [
            {
                "title": query,
                "location": location or "Remote",
                "source": "mock",
                "match_score": 0.9,
            }
        ][:max_results]

class JobSearchAgent:

    def __init__(self):
        self.name = "Job Search Agent"

    def search_jobs(self, jobs, target_role):

        matched_jobs = []

        for job in jobs:

            title = job.get("title", "").lower()

            if target_role.lower() in title:
                matched_jobs.append(job)

        return matched_jobs


if __name__ == "__main__":

    jobs = [
        {
            "title": "AI Engineer",
            "company": "Google"
        },
        {
            "title": "Software Engineer",
            "company": "Amazon"
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Microsoft"
        }
    ]

    agent = JobSearchAgent()

    results = agent.search_jobs(
        jobs,
        "AI Engineer"
    )

    print(results)
