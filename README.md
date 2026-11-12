# AI Multi-Agent JobPilot

A lightweight multi-agent job application assistant built with Python.

## Structure

- `agents/` contains the orchestration and job/resume matching logic.
- `backend/` includes the FastAPI API entry point.
- `database/` holds model and mock persistence layers.
- `tools/` contains utilities like job retrieval, resume parsing, and email generation.
- `prompts/` stores prompt templates for matching and resume tailoring.
- `tests/` includes the basic pytest suite.

## Getting started

1. Create a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run tests: `pytest`
4. Start the API: `uvicorn backend.main:app --reload`

## Notes

This project is scaffolded for extension with real job search providers, resume parsing libraries, and LLM-powered matching logic.

## Multi-site job workflow

`MultiSiteJobSearchAgent` fans a search out to configured provider adapters.
Each adapter must expose `search(query, location=None, limit=10)` and return a
list of job dictionaries. Configure adapters using the official API, feed, or
integration offered by each career site; this repository does not include
site-specific credentials or integrations.

Register the search agent with the orchestrator and run the draft workflow:

```python
from agents.multi_site_search_agent import MultiSiteJobSearchAgent
from agents.orchestrator import Orchestrator

search_agent = MultiSiteJobSearchAgent(
    {"career_site_a": site_a_adapter, "career_site_b": site_b_adapter}
)
pilot = Orchestrator({"job_search": search_agent})
result = pilot.search_and_prepare(
    query="Python engineer",
    location="Remote",
    resume_text="Paste your resume text here",
)
```

The workflow searches each configured provider (up to `max_results_per_site`
listings per provider), scores and reviews jobs, and prepares drafts for
recommended roles. It does not submit applications: review every draft and
confirm each application yourself. Provider failures are reported rather than
silently treated as empty search results.

## Free API deployment and testing

The included [`render.yaml`](./render.yaml) deploys the FastAPI service on
Render's Free web-service plan. It uses a small deployment-specific dependency
file so deployment does not install the unrelated packages in `requirements.txt`.

1. Push this repository to GitHub.
2. In Render, choose **New → Blueprint**, connect the repository, and apply the
   `render.yaml` configuration. When prompted, set `JOBPILOT_API_KEY` to a
   strong random value. Do not commit the key or your resume.
3. After the deploy completes, open `https://<your-service>.onrender.com/docs`.
   The free service can sleep when idle, so the first request may take about a
   minute to wake it.
4. Test `GET /health`, then use `POST /applications/prepare` with this JSON
   body and an `X-API-Key` header containing your configured key:

   ```json
   {
     "resume_text": "Python developer with SQL experience",
     "jobs": [
       {
         "title": "Python Engineer",
         "company": "Example Co.",
         "url": "https://example.com/jobs/123",
         "description": "Build Python APIs and data services."
       }
     ]
   }
   ```

   A successful response includes `jobs_processed`, a match and review per job,
   an application draft, and `applications_submitted: 0`. The endpoint accepts
   job records supplied by the caller; live career-site search requires
   separately configured provider adapters. Render's Free filesystem is
   ephemeral, and this API does not persist requests or application records.

To run the same API locally:

```powershell
pip install -r requirements-deploy.txt
$env:JOBPILOT_API_KEY = "set-a-local-test-key"
uvicorn backend.main:app --reload
```
