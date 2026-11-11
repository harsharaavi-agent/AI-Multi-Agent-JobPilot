"""Agent that evaluates how well a resume matches a job."""

from __future__ import annotations

from typing import Any, Dict, List


class MatchingAgent:
    """Calculates job-to-candidate fit."""

    def __init__(self, prompt_template: str | None = None):
        self.prompt_template = prompt_template or "Match candidate to role."

    def score(self, job: Dict[str, Any], resume_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Return a compatibility score and notes for a specific job."""
        match_score = 0.85
        skills = resume_summary.get("skills", [])
        job_title = str(job.get("title", "")).lower()

        if any(skill in job_title for skill in skills[:5]):
            match_score = 0.92

        return {
            "job_title": job.get("title", "Unknown"),
            "match_score": round(match_score, 2),
            "summary": f"Strong alignment with {job_title or 'the role'}.",
        }

    def rank_jobs(self, jobs: List[Dict[str, Any]], resume_summary: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rank a list of jobs by match score."""
        ranked = []
        for job in jobs:
            ranked.append(self.score(job, resume_summary))
        ranked.sort(key=lambda item: item["match_score"], reverse=True)
        return ranked
