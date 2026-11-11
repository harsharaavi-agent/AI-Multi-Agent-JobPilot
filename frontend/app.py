"""Frontend entry point for the job pilot."""

from __future__ import annotations


def render_dashboard() -> str:
    """Return a simple dashboard summary."""
    return "AI Multi-Agent JobPilot Dashboard"


if __name__ == "__main__":
    print(render_dashboard())
