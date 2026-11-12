"""AI-powered job application agents."""

from __future__ import annotations

from importlib import import_module
from typing import Any

_AGENT_MODULES = {
    "ApplicationAgent": "application_agent",
    "JobSearchAgent": "job_search_agent",
    "MultiSiteJobSearchAgent": "multi_site_search_agent",
    "MatchingAgent": "matching_agent",
    "Orchestrator": "orchestrator",
    "ResumeAgent": "resume_agent",
    "ResumeTailoringAgent": "resume_tailoring_agent",
    "ReviewAgent": "review_agent",
}

__all__ = list(_AGENT_MODULES)


def __getattr__(name: str) -> Any:
    """Load an agent only when it is requested."""
    module_name = _AGENT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    module = import_module(f".{module_name}", __name__)
    agent = getattr(module, name)
    globals()[name] = agent
    return agent
