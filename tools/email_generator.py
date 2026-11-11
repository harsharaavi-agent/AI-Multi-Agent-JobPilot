"""Generates simple email drafts for application follow-ups."""

from __future__ import annotations


class EmailGenerator:
    """Generate follow-up or outreach emails."""

    def generate_follow_up(self, recipient: str, subject: str, body: str) -> str:
        """Return a basic email draft."""
        return (
            f"Subject: {subject}\n\n"
            f"Dear {recipient},\n\n{body}\n\n"
            "Best regards,\n"
            "AI JobPilot"
        )
