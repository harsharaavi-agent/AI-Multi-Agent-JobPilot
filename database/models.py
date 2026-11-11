"""Database models for candidate profiles and job applications."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class CandidateProfile:
    """Represents the candidate's professional profile."""

    name: str
    email: str
    skills: List[str] = field(default_factory=list)
    experience_years: int = 0
    bio: str = ""


@dataclass
class JobApplication:
    """Represents a job application record."""

    job_id: str
    company: str
    role: str
    status: str = "draft"
    metadata: Dict[str, Any] = field(default_factory=dict)
