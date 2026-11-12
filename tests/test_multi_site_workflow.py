"""Tests for multi-site job search and application preparation."""

from agents.multi_site_search_agent import MultiSiteJobSearchAgent
from agents.orchestrator import Orchestrator


def test_multi_site_search_tags_sources_and_deduplicates_urls():
    class Provider:
        def __init__(self, jobs):
            self.jobs = jobs

        def search(self, query, location=None, limit=10):
            return self.jobs[:limit]

    agent = MultiSiteJobSearchAgent(
        {
            "site_one": Provider(
                [{"title": "Engineer", "url": "https://jobs.test/1"}]
            ),
            "site_two": Provider(
                [
                    {"title": "Engineer copy", "url": "https://jobs.test/1"},
                    {"title": "Analyst"},
                ]
            ),
        }
    )

    jobs = agent.search("engineer", max_results_per_site=2)

    assert len(jobs) == 2
    assert jobs[0]["source"] == "site_one"
    assert jobs[1]["source"] == "site_two"


def test_orchestrator_prepares_drafts_without_submitting():
    orchestrator = Orchestrator()

    result = orchestrator.run(
        {"jobs": [{"title": "Python Engineer", "url": "https://jobs.test/1"}]},
        "Python developer with SQL experience",
    )

    assert result["jobs_processed"] == 1
    assert result["applications_submitted"] == 0
    assert result["results"][0]["status"] == "awaiting_user_review"
    assert result["results"][0]["application"]["status"] == "prepared"


def test_search_and_prepare_requires_registered_search_agent():
    orchestrator = Orchestrator()

    try:
        orchestrator.search_and_prepare("engineer", "resume")
    except RuntimeError as exc:
        assert "'job_search'" in str(exc)
    else:
        raise AssertionError("Expected missing search agent to be reported")


def test_search_and_prepare_runs_multi_site_draft_workflow():
    class Provider:
        def search(self, query, location=None, limit=10):
            return [{"title": "Python Engineer", "url": "https://jobs.test/1"}]

    search_agent = MultiSiteJobSearchAgent({"career_site": Provider()})
    orchestrator = Orchestrator({"job_search": search_agent})

    result = orchestrator.search_and_prepare(
        query="Python Engineer",
        resume_text="Python developer with SQL experience",
    )

    assert result["jobs_processed"] == 1
    assert result["results"][0]["job"]["source"] == "career_site"
    assert result["results"][0]["status"] == "awaiting_user_review"
    assert result["applications_submitted"] == 0
