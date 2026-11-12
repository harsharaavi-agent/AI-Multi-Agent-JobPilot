"""Coordinator for multi-agent job application flow."""

from __future__ import annotations

from typing import Any, Dict, List

from agents.application_agent import ApplicationAgent
from agents.matching_agent import MatchingAgent
from agents.resume_agent import ResumeAgent
from agents.resume_tailoring_agent import ResumeTailoringAgent
from agents.review_agent import ReviewAgent


class Orchestrator:
    """Coordinates the job search and application pipeline."""

    def __init__(self, agents: Dict[str, Any] | None = None):
        self.agents = dict(agents) if agents is not None else {}

    def register_agent(self, name: str, agent: Any) -> None:
        self.agents[name] = agent

    def run(self, job_data: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
        """Score jobs and prepare application drafts for candidate review."""
        jobs = job_data.get("jobs", [])
        resume_agent = self.agents.get("resume", ResumeAgent())
        matching_agent = self.agents.get("matching", MatchingAgent())
        review_agent = self.agents.get("review", ReviewAgent())
        tailoring_agent = self.agents.get(
            "resume_tailoring", ResumeTailoringAgent()
        )
        application_agent = self.agents.get("application", ApplicationAgent())
        resume_summary = resume_agent.parse(resume_text)
        results: List[Dict[str, Any]] = []

        for job in jobs:
            match = matching_agent.score(job, resume_summary)
            review = review_agent.review(job, match)
            result: Dict[str, Any] = {
                "job": job,
                "match": match,
                "review": review,
                "status": (
                    "awaiting_user_review"
                    if review["approved"]
                    else "not_recommended"
                ),
                "application": None,
            }

            if review["approved"]:
                tailored_resume = tailoring_agent.tailor(resume_text, job)
                result["application"] = application_agent.prepare_application(
                    job, tailored_resume
                )

            results.append(result)

        return {
            "status": "success",
            "jobs_processed": len(results),
            "applications_submitted": 0,
            "results": results,
        }

    def search_and_prepare(
        self,
        query: str,
        resume_text: str,
        location: str | None = None,
        max_results_per_site: int = 10,
    ) -> Dict[str, Any]:
        """Search configured career sites and prepare drafts for review."""
        search_agent = self.agents.get("job_search")
        if search_agent is None:
            raise RuntimeError(
                "No multi-site job search agent registered as 'job_search'."
            )

        jobs = search_agent.search(
            query=query,
            location=location,
            max_results_per_site=max_results_per_site,
        )
        return self.run({"jobs": jobs}, resume_text)
