"""Coordinator for multi-agent job application flow."""

from __future__ import annotations

from typing import Any, Dict, List


class Orchestrator:
    """Coordinates the job search and application pipeline."""

    def __init__(self, agents: Dict[str, Any] | None = None):
        self.agents = agents or {}

    def register_agent(self, name: str, agent: Any) -> None:
        self.agents[name] = agent

    def run(self, job_data: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
        """Run the end-to-end pipeline for a set of jobs and resume."""
        jobs = job_data.get("jobs", [])
        results: List[Dict[str, Any]] = []

        for job in jobs:
            result = {
                "job": job,
                "resume_text": resume_text,
                "status": "queued",
            }
            results.append(result)

        return {
            "status": "success",
            "jobs_processed": len(results),
            "results": results,
        }
