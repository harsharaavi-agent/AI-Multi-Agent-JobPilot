"""Tests for agent scaffolding."""

from agents.application_agent import ApplicationAgent
from agents.job_search_agent import JobSearchAgent
from agents.matching_agent import MatchingAgent
from agents.resume_agent import ResumeAgent


def test_job_search_agent_returns_results():
    agent = JobSearchAgent()
    jobs = agent.search("python engineer", "Remote")
    assert len(jobs) > 0


def test_matching_agent_scores_job():
    agent = MatchingAgent()
    result = agent.score({"title": "Python Engineer"}, {"skills": ["python", "sql"]})
    assert result["match_score"] >= 0.8


def test_resume_agent_parses_resume():
    agent = ResumeAgent("Python developer with SQL and machine learning experience")
    parsed = agent.parse()
    assert "skills" in parsed
    assert isinstance(parsed["skills"], list)


def test_application_agent_prepares_application():
    agent = ApplicationAgent()
    payload = agent.prepare_application({"title": "Software Engineer"}, {"tailored_summary": "Strong fit"})
    assert payload["status"] == "prepared"
