"""Resume analysis agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ResumeAgent:
    """Parses and summarizes candidate resume details."""

    resume_text: str = ""
    skills: List[str] = field(default_factory=list)
    experience: Dict[str, str] = field(default_factory=dict)

    def parse(self, resume_text: str | None = None) -> Dict[str, object]:
        text = resume_text or self.resume_text
        if not text:
            return {"skills": [], "experience": {}, "summary": ""}

        tokens = [part.strip() for part in text.split() if part.strip()]
        skills = sorted({token.lower() for token in tokens if len(token) > 4})[:20]

        return {
            "skills": skills,
            "experience": {"years": "3+", "source": "parsed_resume"},
            "summary": text[:200],
        }
