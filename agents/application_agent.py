"""Application automation agent."""

from __future__ import annotations

from typing import Any, Dict


class ApplicationAgent:
    """Handles application preparation and submission information."""

    def prepare_application(self, job: Dict[str, Any], tailored_resume: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare the payload for an application to a job."""
        return {
            "job_title": job.get("title", "Unknown"),
            "status": "prepared",
            "resume_summary": tailored_resume.get("tailored_summary", ""),
            "cover_letter": "Generated cover letter drafted for this role.",
        }
