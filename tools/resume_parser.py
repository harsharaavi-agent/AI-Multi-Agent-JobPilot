"""Utilities for reading and extracting resume content."""

from __future__ import annotations


class ResumeParser:
    """Basic resume parser."""

    def parse(self, text: str) -> dict:
        """Extract a minimal structure from resume text."""
        words = [part.strip() for part in text.split() if part.strip()]
        return {
            "word_count": len(words),
            "skills": [word.lower() for word in words[:10]],
            "summary": text[:200],
        }
