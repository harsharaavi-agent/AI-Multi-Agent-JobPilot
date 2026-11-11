"""Tests for matching behavior."""

from agents.matching_agent import MatchingAgent


def test_rank_jobs_returns_sorted_list():
    agent = MatchingAgent()
    jobs = [
        {"title": "Data Analyst"},
        {"title": "Python Engineer"},
    ]
    ranked = agent.rank_jobs(jobs, {"skills": ["python", "fastapi"]})
    assert ranked[0]["job_title"] == "Python Engineer"
