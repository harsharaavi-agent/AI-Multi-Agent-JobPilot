"""Review agent for validating application quality."""

from __future__ import annotations

from typing import Any, Dict


class ReviewAgent:
    """Checks candidate fit quality and final review notes."""

    def review(self, job: Dict[str, Any], match_result: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate final fit before sending application."""
        score = match_result.get("match_score", 0)
        return {
            "job_title": job.get("title", "Unknown"),
            "approved": score >= 0.8,
            "notes": "Proceed with application when the score is above the threshold.",
            "score": score,
        }
